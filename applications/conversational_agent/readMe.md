# Agent Conversationnel

## Structure de l'Application
```
conversational_agent/
├── agent.py          # Implémentation de l'agent conversationnel
├── cli.py           # Interface en ligne de commande
├── web_app.py       # Interface web avec FastAPI
├── static/          # Fichiers statiques pour l'interface web
│   └── index.html   # Interface utilisateur web
├── prompts.py       # Définition des prompts prédéfinis
├── requirements.txt # Dépendances du projet
└── .env            # Configuration des variables d'environnement
```

## Installation et Configuration

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

2. Configurer le fichier `.env` :
```
OPENAI_API_KEY=votre_clé_api_openai
```

## Utilisation

### Interface Web (Recommandée)
1. Démarrer le serveur :
```bash
python web_app.py
```
2. Ouvrir un navigateur et accéder à `http://localhost:8000`

### Interface CLI
```bash
python cli.py [options]
```

Options disponibles :
- `--session <nom_session>` : Identifiant de session (défaut: default_user)
- `--prompt-type <type>` : Type de prompt prédéfini (teacher, french, coder, writer)
- `--system-prompt <prompt>` : Prompt système personnalisé
- `--db-path <chemin>` : Chemin vers le fichier de base de données

Exemple :
```bash
python cli.py --session user1 --prompt-type teacher
```

## Fonctionnalités Principales

### Interface Web
- Gestion de sessions multiples
- Visualisation et modification du prompt système
- Historique des conversations
- Sélection de prompts prédéfinis
- Interface responsive et intuitive
- Messages système avec retours visuels

### Composants Clés
1. **Agent Conversationnel** (`agent.py`)
   - Gestion du modèle de langage (OpenAI)
   - Gestion de la mémoire des conversations
   - Traitement des prompts système
   - Gestion des sessions utilisateurs

2. **Interface Web** (`web_app.py` + `static/index.html`)
   - API REST avec FastAPI
   - Interface utilisateur moderne avec Tailwind CSS
   - Gestion asynchrone des requêtes
   - Modales pour les fonctionnalités avancées

3. **Interface CLI** (`cli.py`)
   - Commandes interactives
   - Support des arguments en ligne de commande
   - Gestion des sessions
   - Commandes d'administration

### Gestion de la Mémoire
- Stockage persistant des conversations
- Historique par session
- Gestion des prompts système personnalisés
- Support de multiples utilisateurs simultanés

## Commandes CLI Disponibles
- `quit` : Quitter l'application
- `history` : Afficher l'historique de la conversation
- `prompt` : Afficher le prompt système actuel
- `set_prompt` : Définir un nouveau prompt système
- `use_prompt <type>` : Utiliser un prompt prédéfini
- `list_prompts` : Afficher les prompts prédéfinis disponibles
- `reset` : Réinitialiser la conversation
- `list_sessions` : Lister toutes les sessions disponibles
- `switch_session <session_id>` : Changer de session
- `help` : Afficher le message d'aide

## Notes de Développement
- L'application utilise FastAPI pour l'API REST
- L'interface web utilise Tailwind CSS pour le style
- Les sessions sont persistantes grâce à SQLite
- Support complet des caractères UTF-8 (accents français)
- Gestion des erreurs et messages de confirmation
