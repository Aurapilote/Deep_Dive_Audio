import os
import json
import base64
import time
from datetime import datetime
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import google.generativeai as genai
from duckduckgo_search import DDGS
from elevenlabs import ElevenLabs, VoiceSettings
from pydub import AudioSegment
from prompts import get_extraction_prompt, get_radio_script_prompt

# --- CONFIGURATION ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not GOOGLE_API_KEY or not ELEVENLABS_API_KEY:
    raise ValueError("❌ Clés API manquantes dans .env")

# ID de la voix (Yann - dynamique & pro)
VOICE_ID = "nr2EGJNe96rzn9FRlTId"

# Jingles (place tes fichiers dans le même dossier)
INTRO_JINGLE = "jingles/intro.mp3"  # 6 secondes
OUTRO_JINGLE = "jingles/outro.mp3"  # 6 secondes

# Initialisation des clients
genai.configure(api_key=GOOGLE_API_KEY)
eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# --- 1. GMAIL (Ingestion) ---
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

def get_all_avolta_emails():
    print("📧 Connexion à Gmail...")
    service = get_gmail_service()
    query = 'from:news@avolta.io newer_than:7d'
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    full_text_content = ""
    print(f"   -> {len(messages)} emails trouvés.")

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        if 'parts' in msg['payload']:
            parts = [p for p in msg['payload']['parts'] if p['mimeType'] == 'text/html']
            data = parts[0]['body']['data'] if parts else msg['payload']['body']['data']
        else:
            data = msg['payload']['body']['data']
        
        decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')
        soup = BeautifulSoup(decoded_data, "html.parser")
        full_text_content += f"\n--- EMAIL DU {msg['internalDate']} ---\n" + soup.get_text(separator='\n')

    return full_text_content

# --- 2. GEMINI (Extraction & Rédaction) ---
def extract_fundings_with_gemini(text_content):
    print("🧠 Analyse et tri des levées avec Gemini Flash...")
    model = genai.GenerativeModel('gemini-2.5-flash-lite', generation_config={"response_mime_type": "application/json"})
    
    try:
        response = model.generate_content(get_extraction_prompt(text_content))
        return json.loads(response.text)
    except Exception as e:
        print(f"Erreur extraction : {e}")
        return {"startups": []}

def write_radio_script_gemini(enriched_data, duration: str = "5 minutes"):
    print(f"✍️  Rédaction du script radio ({duration}) avec Gemini Flash...")
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    context_str = json.dumps(enriched_data, indent=2, ensure_ascii=False)
    response = model.generate_content(get_radio_script_prompt(context_str, duration))
    return response.text

# --- 3. RECHERCHE (Enrichissement) ---
def enrich_startup_info(startup_list):
    print("🕵️‍♂️  Enrichissement des données via DuckDuckGo...")
    enriched_data = []
    with DDGS() as ddgs:
        for startup in startup_list.get('startups', []):
            name = startup['name']
            print(f"   -> Recherche : {name}")
            time.sleep(1)
            try:
                results = list(ddgs.text(f"what does {name} startup do?", max_results=1))
                summary = results[0]['body'] if results else "Tech company"
            except Exception as e:
                print(f"   ⚠️  Erreur recherche {name}: {e}")
                summary = "Tech company"
            enriched_data.append({**startup, "what_they_do": summary})
    return enriched_data

# --- 4. ELEVENLABS (Génération Audio) ---
def generate_audio_elevenlabs(text):
    print("🎙️  Génération de l'audio avec ElevenLabs...")
    
    try:
        # Conversion du texte en audio avec réglages "Natural Vibe"
        audio_generator = eleven_client.text_to_speech.convert(
            voice_id=VOICE_ID,
            model_id="eleven_multilingual_v2", 
            text=text,
            voice_settings=VoiceSettings(
                speed=1.13,
                stability=0.83,       # Plus bas = plus d'expressivité/variation (0.3-0.5)
                similarity_boost=0.80, # Garde la clarté de la voix
                style=0.95,            # Exagère un peu le style (bon pour radio)
                use_speaker_boost=True
            )
        )
        
        # Sauvegarde du fichier voix (temp)
        temp_voice = f"temp_voice_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
        with open(temp_voice, "wb") as f:
            for chunk in audio_generator:
                f.write(chunk)
        
        # Chargement de l'audio généré
        voice_audio = AudioSegment.from_mp3(temp_voice)
        
        # Ajout intro/outro si les fichiers existent
        final_audio = voice_audio
        
        if os.path.exists(INTRO_JINGLE):
            intro = AudioSegment.from_mp3(INTRO_JINGLE)
            final_audio = intro + final_audio
            print("   ♫ Intro jingle ajouté")
        
        if os.path.exists(OUTRO_JINGLE):
            outro = AudioSegment.from_mp3(OUTRO_JINGLE)
            final_audio = final_audio + outro
            print("   ♫ Outro jingle ajouté")
        
        # Export final
        filename = f"radio_avolta_{datetime.now().strftime('%Y%m%d')}.mp3"
        final_audio.export(filename, format="mp3")
        
        # Nettoyage fichier temp
        os.remove(temp_voice)
                
        print(f"\n✅ SUCCESS ! Ton briefing radio est prêt : {filename}")
        
    except Exception as e:
        print(f"❌ Erreur ElevenLabs : {e}")

# --- MAIN ---
if __name__ == '__main__':
    print("🚀 Lancement du pipeline Deep Dive\n")
    
    # 1. Récupération des emails
    raw_text = get_all_avolta_emails()
    
    if len(raw_text) > 100:
        # 2. Extraction des levées
        data = extract_fundings_with_gemini(raw_text)
        
        if data.get('startups'):
            # 3. Enrichissement
            final_data = enrich_startup_info(data)
            
            # 4. Écriture du script radio
            script = write_radio_script_gemini(final_data)
            print("\n--- SCRIPT TEXTE ---\n", script, "\n")
            
            # 5. Génération audio
            generate_audio_elevenlabs(script)
        else:
            print("❌ Pas de levées trouvées cette semaine.")
    else:
        print("❌ Pas assez de contenu email.")