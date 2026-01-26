# SpotR - Spotify Mood Recognition

**Your music, Your Mood, Unveiled**

SpotR est une application web full-stack qui analyse vos habitudes d'écoute Spotify pour déterminer votre humeur musicale et fournir des informations personnalisées.

## Fonctionnalités

- **Authentification Spotify** - Connexion sécurisée via OAuth 2.0
- **Affichage du profil** - Visualisez vos informations Spotify
- **Top Tracks** - Découvrez vos morceaux les plus écoutés avec pochettes d'album
- **Playlists** - Parcourez vos playlists avec liens directs vers Spotify
- **Analyse d'humeur** - Détection d'humeur en temps réel basée sur votre historique d'écoute
- **Timeline d'humeur** - Visualisez l'évolution de votre humeur avec des graphiques interactifs
- **Analyse Jour/Nuit** - Comparez vos habitudes d'écoute entre le jour et la nuit

## Technologies

### Frontend
| Technologie | Version | Utilisation |
|-------------|---------|-------------|
| React | 19.2.0 | Framework UI |
| Vite | 7.2.4 | Outil de build |
| React Router | 7.10.1 | Routage client |
| Axios | 1.13.2 | Client HTTP |
| Recharts | 3.5.1 | Visualisation de données |

### Backend
| Technologie | Utilisation |
|-------------|-------------|
| Flask | Framework Web |
| SQLAlchemy | ORM |
| SQLite | Base de données |
| python-dotenv | Variables d'environnement |
| requests | Client HTTP pour l'API Spotify |

## Structure du Projet

```
SpotR/
├── README.md
│
├── spotR_interface/                # Frontend (React + Vite)
│   ├── public/
│   │   ├── assets/
│   │   │   └── images/             # Logo et images
│   │   └── vite.svg
│   ├── src/
│   │   ├── components/
│   │   │   ├── Footer.jsx          # Pied de page avec liens sociaux
│   │   │   ├── MoodGraph.jsx       # Graphique d'évolution d'humeur
│   │   │   ├── Playlist.jsx        # Affichage des playlists
│   │   │   ├── ProfileUser.jsx     # Profil utilisateur
│   │   │   ├── ProtectedRoute.jsx  # Protection des routes
│   │   │   ├── Recommendations.jsx # Recommandations (préparé)
│   │   │   └── TopTracks.jsx       # Top morceaux
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx       # Page principale
│   │   │   └── Home.jsx            # Page d'accueil
│   │   ├── services/
│   │   │   ├── auth_api.js         # API authentification
│   │   │   └── spotify_api.js      # API Spotify
│   │   ├── App.jsx                 # Composant principal + routes
│   │   ├── App.css                 # Styles principaux
│   │   ├── index.css               # Styles globaux
│   │   └── main.jsx                # Point d'entrée React
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── eslint.config.js
│
└── spotR_server/                   # Backend (Flask)
    ├── database/
    │   └── spotr.db                # Base de données SQLite
    ├── models/
    │   ├── __init__.py
    │   ├── user.py                 # Modèle utilisateur
    │   └── tokens.py               # Modèle tokens OAuth
    ├── routes/
    │   ├── analysis_route.py       # Routes d'analyse d'humeur
    │   ├── auth_route.py           # Routes authentification Spotify
    │   ├── client_auth.py          # Route /api/me
    │   └── client_route.py         # Routes données Spotify
    ├── services/
    │   ├── mood_analysis.py        # Algorithme d'analyse d'humeur
    │   ├── spotify_auth.py         # Gestion OAuth Spotify
    │   └── spotify_client.py       # Client API Spotify
    ├── tests/
    │   ├── conftest.py             # Configuration pytest
    │   ├── test_analysis.py        # Tests analyse d'humeur
    │   ├── test_auth.py            # Tests authentification
    │   └── test_spotify_api.py     # Tests API Spotify
    ├── utils/
    │   └── auth.py                 # Utilitaire require_login
    ├── app.py                      # Application Flask
    ├── config.py                   # Configuration
    ├── extensions.py               # Extensions (SQLAlchemy)
    └── requirements.txt            # Dépendances Python
```

## Installation

### Prérequis

- Python 3.10+
- Node.js 18+
- Compte Développeur Spotify

### 1. Cloner le dépôt

```bash
git clone https://github.com/AlexisIvan2000/SpotR.git
cd SpotR
```

### 2. Configuration du Backend

```bash
cd spotR_server

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows :
.\venv\Scripts\activate
# macOS/Linux :
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Configuration du Frontend

```bash
cd spotR_interface

# Installer les dépendances
npm install
```

### 4. Variables d'Environnement

Créez un fichier `.env` dans `spotR_server/` :

```env
SPOTR_SECRET_KEY=votre_cle_secrete
SPOTIFY_CLIENT_ID=votre_client_id_spotify
SPOTIFY_CLIENT_SECRET=votre_client_secret_spotify
SPOTIFY_REDIRECT_URI=http://127.0.0.1:5000/auth/spotify/callback
```

#### Obtenir les Identifiants Spotify

1. Allez sur [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Créez une nouvelle application
3. Ajoutez `http://127.0.0.1:5000/auth/spotify/callback` aux URIs de redirection
4. Copiez le Client ID et Client Secret dans votre fichier `.env`

## Lancer l'Application

### Démarrer le Serveur Backend

```bash
cd spotR_server
.\venv\Scripts\activate  # Windows
python app.py
```

Serveur disponible sur : `http://127.0.0.1:5000`

### Démarrer le Serveur Frontend

```bash
cd spotR_interface
npm run dev
```

Application disponible sur : `http://127.0.0.1:5173`

## Endpoints API

### Authentification

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/auth/spotify/login` | Initier l'OAuth Spotify |
| GET | `/auth/spotify/callback` | Callback OAuth |
| POST | `/auth/spotify/logout` | Déconnexion |
| GET | `/api/me` | Infos utilisateur connecté |

### Données Spotify

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/profile` | Profil Spotify |
| GET | `/api/top-tracks` | Top tracks de l'utilisateur |
| GET | `/api/recent-tracks` | Morceaux récemment écoutés |
| GET | `/api/playlists` | Playlists de l'utilisateur |
| GET | `/api/audio-features?ids=` | Caractéristiques audio des morceaux |

### Analyse

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/analysis/mood` | Analyse d'humeur des morceaux récents |

## Algorithme d'Analyse d'Humeur

L'analyse d'humeur est basée sur :

| Facteur | Impact |
|---------|--------|
| **Popularité du morceau** | >70: +2, >50: +1, sinon: -1 |
| **Contenu explicite** | +1 si explicite |
| **Heure d'écoute** | Nuit (22h-6h): -1, Jour (10h-18h): +1 |

**Labels d'humeur :**
- **Energetic** - Score >= 2
- **Chill** - Score < 2

## Tests

Lancer la suite de tests :

```bash
cd spotR_server
.\venv\Scripts\activate
pytest -v
```

**50 tests** couvrant :
- Routes d'authentification
- Routes API Spotify
- Fonctions d'analyse d'humeur
- Routes protégées

## Auteur

**Alexis Moungang**

- GitHub : [@AlexisIvan2000](https://github.com/AlexisIvan2000)
- LinkedIn : [Alexis Moungang](https://www.linkedin.com/in/alexis-moungang-396104371)

---

Fait avec React, Flask et l'API Spotify
