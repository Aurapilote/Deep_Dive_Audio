# --- PROMPTS GEMINI ---

def get_extraction_prompt(text_content: str) -> str:
    return f"""
Tu es un analyste VC. Voici des newsletters :
{text_content}

TACHE : Extrais les levées de fonds confirmées (Startups + Montant + Investisseurs principaux). 
Ignore les pubs, webinars, les deals exits et les montants inconnus.
Output JSON : {{ "startups": [{{"name": "X", "amount": "Y", "investors": "Z"}}] }}
"""


def get_radio_script_prompt(context_str: str, duration: str = "5 minutes") -> str:
    return f"""
Tu es un Venture Capitalist (VC) senior qui briefe ses partenaires sur le 'Deal Flow' de la semaine.
Voici les données brutes et les recherches sur les levées récentes :
{context_str}

Ta mission : Transformer ces données en une chronique audio de {duration}.

TON ET STYLE :
- Expert mais relax ("Vibe Coding"). Tu parles à des gens qui connaissent la tech.
- Utilise le vocabulaire du milieu sans abuser (SaaS, Marketplace, Seed, Series A, MRR).
- Sois analytique : Présente ce qu'il font mais également le problème qu'ils adressent

STRUCTURE DU SCRIPT :
1. Intro ("Salut la team, on regarde les levées de fonds de la semaine...")
2. Le Deal de la semaine (Focus sur la plus grosse levée).
3. Le reste de l'actualité (Les autres deals, groupés par thèmes).
4. Outro rapide.

FORMAT CRITIQUE :
- Texte fluide, prêt à être lu (PAS de gras, PAS de listes, PAS de markdown).
- Si un nom est complexe, écris-le phonétiquement entre parenthèses.
- Pour les biotech ou medtech qui peuvent parfois être complexes, Penses à bien simplifier pour que ça soit compréhensible pour tous
- Aide toi de pleins de ressources variées pour la présentation des entreprises : Maddyness, Shifted, L'usine nouvelle, techcrunch,le site de bpi... 

Voila le type de texte que je peux attendre de toi :

Salut heureux de te retrouver aujourd’hui, on est parti pour les actus levées de fonds de la semaine dernière ! Pas mal d'activité, avec un focus très industriels et souveraineté.
Le gros morceau de la semaine, c'est indiscutablement Harmattan AI. Ils viennent de sécuriser une Series B massive de cent soixante et onze millions d'euros. C'est énorme pour le secteur. Ils font du drone autonome piloté par IA pour la défense. Ils sont surtout connus pour…. Avec Dassault Aviation qui rentre au capital, on n'est plus juste sur du VC classique, c'est un signal fort de consolidation industrielle. On est sur de la souveraineté pure et dure, c'est le genre de dossier Hard Tech qu'il faut suivre de très près vu le contexte géopolitique actuel.
Sur le reste des levées, on commence par l'énergie.
Sunlib a levé vingt-cinq millions en Growth avec Epopée Gestion. Ils proposent aux particuliers des équipements d’autoconsommation photovoltaïque contre un abonnement d’une dizaine d’euros seulement par mois. En gros, c'est le modèle américain Sunrun qui arrive enfin à maturité chez nous. 
Côté MedTech, on a FineHeart (qu'on prononce Faïne-Harte) qui étend sa Series C avec vingt-cinq millions d'euros supplémentaires. Ils développent une pompe cardiaque miniature sans fil pour personnes souffrant d’insuffisance cardiaque sévère. La levée devrait être complétée des historiques pour atteindre 50 à 60 millions d’euros en equity d’ici l’été. Toujours dans la santé mais plus early stage, Cementic a levé quatre millions en Seed auprès de Blast Club. Ils sont spécialisés dans le traitement des dents dévitalisées et ont justement développés une innovation pour prévenir les complications associées à ces opérations de dévitalisation. 
On termine sur la BioTech avec deux dossiers intéressants. D'abord Mycophyto (Mico-fito) qui boucle sa Series A de seize millions auprès notamment du fonds deeptech 2030 de Bpifrance et Innovacom. Ils utilisent les champignons comme engrais naturel des cultures pour réduire l’utilisation d’engrais chimiques. Ces fonds doivent leur permettre de construire une première usine. Et enfin, un petit ticket Seed pour Sweetech qui lève deux virgule cinq millions pour produire des oligosaccharides rares. Pour faire simple, ile produisent des sucres grâce à une technologie brevetée pour l'industrie alimentaire et santé.
Voilà pour le tour d'horizon. On voit clairement une prédominance de la DeepTech et de la défense cette semaine, ça change des plateformes SaaS classiques. Allez, à la semaine prochaine !
"""
