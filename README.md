PROJET : AVOLTA DEEP DIVE RADIO
=====================================================

DESCRIPTION
-----------
De la Newsletter au Podcast VC en un clic.

Ce projet automatise la veille technologique hebdomadaire. Il récupère les newsletters de levées de fonds (Avolta), analyse les deals, enrichit les données avec une recherche de marché, et génère un briefing radio audio prêt à être diffusé.


FONCTIONNALITES
---------------
* Ingestion Automatique : Connexion sécurisée à l'API Gmail pour récupérer les newsletters "news@avolta.io" des 7 derniers jours.
* Extraction Intelligente : Utilisation de Google Gemini 1.5 Flash pour nettoyer le HTML et extraire les données structurées (Startups, Montants).
* Enrichissement VC : Agent autonome qui utilise DuckDuckGo pour analyser le Business Model et les concurrents de chaque startup.
* Rédaction "On Air" : Google Gemini 1.5 Pro rédige un script radio dynamique avec un ton "Venture Capitalist" (analogies, analyse de marché).
* Audio High-End : Génération vocale via ElevenLabs (Multilingual v2) pour un rendu parfait du mélange Français/Anglais Tech.


STACK TECHNIQUE
---------------
* Langage : Python 3.9+
* APIs :
  - Gmail API (Lecture des mails)
  - Google Gemini API (Intelligence & Parsing)
  - ElevenLabs API (Text-to-Speech)
* Bibliothèques principales : google-generativeai, elevenlabs, duckduckgo-search, beautifulsoup4


INSTALLATION
------------

1. Cloner le projet (si vous utilisez git) :
   git clone https://github.com/votre-pseudo/avolta-deep-dive.git

2. Installer les dépendances :
   Ouvrez votre terminal et lancez la commande suivante :
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client beautifulsoup4 google-generativeai duckduckgo-search elevenlabs python-dotenv

3. Configuration des Clés API :
   Créez un fichier nommé ".env" à la racine du projet et ajoutez vos clés dedans :
   
   GOOGLE_API_KEY="votre_clé_gemini_ici"
   ELEVENLABS_API_KEY="votre_clé_elevenlabs_ici"

4. Configuration Gmail (OAuth) :
   - Allez sur la Google Cloud Console (https://console.cloud.google.com/).
   - Activez l'API "Gmail".
   - Créez des identifiants OAuth 2.0. IMPORTANT : Choisissez le type "Application de Bureau" (Desktop App).
   - Téléchargez le fichier JSON, renommez-le "credentials.json" et placez-le dans le dossier du projet.


UTILISATION
-----------
Pour lancer la matinale, exécutez simplement le script principal :

> python vibe_radio.py

Le processus :
1. Une fenêtre s'ouvre pour l'autorisation Gmail (uniquement la première fois).
2. Le script scanne les mails et trouve les levées de fonds.
3. Il effectue l'enquête sur les startups.
4. Il génère le script et l'audio.
5. Le fichier MP3 est lu automatiquement à la fin.
