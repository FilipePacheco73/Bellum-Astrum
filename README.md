# 🚀 Bellum Astrum

Bellum Astrum (formerly Space BattleShip) is a learning project focused on backend development with FastAPI, SQLite database, and spaceship battle logic. The project is now organized to facilitate expansion with a modern frontend.

---

## 🎯 Project Goals

- 🧩 **Backend Learning:** Practice with FastAPI, SQLAlchemy, and Pydantic.
- 🔗 **RESTful API:** Endpoints for game resources.
- 🤖 **AI-Ready Base:** Structure ready for intelligent agents and frontend integration.

---

## ✨ Features

- 🕹️ CRUD for users and ships
- ⚔️ Battle system
- 🛒 Ship market (buy/sell)
- 🌱 Data seeding endpoints
- 📡 Modular and extensible REST API
- 🖥️ Modern web interface (React + Vite + Tailwind)

---

## 🛠️ Tech Stack

- **Backend:** Python 3.12+, FastAPI, SQLAlchemy, Pydantic
- **Database:** SQLite
- **Testing:** Pytest, FastAPI TestClient
- **Frontend:** React, Vite, TypeScript, Tailwind CSS
- **Structure:** Backend in `backend/app/`, Frontend in `frontend/`

---

## 🏁 Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- (Recommended) Virtual environment: `python -m venv venv`

### Backend Installation

```bash
# Clone the repository
git clone https://github.com/FilipePacheco73/Bellum-Astrum.git
cd Bellum-Astrum
# Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# Install backend dependencies
pip install -r requirements.txt
```

### Running the Backend API

```bash
uvicorn backend.app.main:app --reload
```

Access the interactive documentation at: [http://localhost:8000/docs](http://localhost:8000/docs)

### Frontend Installation

```bash
cd frontend
npm install
```

### Running the Frontend

```bash
npm run dev
```

Access the web interface at: [http://localhost:5173](http://localhost:5173)

---

## 🗂️ Project Structure

```
/Bellum-Astrum
│
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entry point
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── crud/             # CRUD operations
│   │   ├── database/         # Database config and models
│   │   ├── routes/           # API routes/endpoints
│   │   └── test/             # Automated tests
│   └── requirements.txt      # Python dependencies
│
├── frontend/
│   ├── src/                  # React source code
│   │   ├── components/       # Reusable React components (Navbar, SpaceBackground, etc.)
│   │   ├── pages/            # Main pages/routes (Home, Register, Market, etc.)
│   │   ├── contexts/         # React context providers (LanguageContext, etc.)
│   │   ├── locales/          # Localization and translations
│   │   ├── assets/           # Static assets (images, icons)
│   │   ├── App.tsx           # Main App component
│   │   ├── main.tsx          # React entry point
│   │   └── ...               # Other configs and styles
│   ├── public/               # Static assets
│   ├── package.json          # Frontend dependencies
│   └── ...                   # Vite, Tailwind, config files
│
├── README.md
└── CHANGELOG.md
```

---

## 🗺️ Project Flowchart

```mermaid
flowchart LR
    User((User))
    Frontend(Frontend: React/Vite/Tailwind)
    Backend(Backend: FastAPI)
    DB[(SQLite Database)]

    User -- HTTP/Browser --> Frontend
    Frontend -- REST API --> Backend
    Backend -- ORM/SQL --> DB
    Backend -- JSON Response --> Frontend
    Frontend -- UI/UX --> User
```

---

## 🗺️ Data Model Flowchart

```mermaid
erDiagram
    USER ||--o{ OWNED_SHIP : owns
    USER ||--o{ BATTLE_HISTORY : participates_in
    SHIP ||--o{ OWNED_SHIP : is_type
    OWNED_SHIP ||--o{ BATTLE_HISTORY : used_in
    USER {
        int user_id
        string nickname
        int elo
    }
    SHIP {
        int ship_id
        string ship_name
        float attack
        float shield
        float evasion
        float fire_rate
        float hp
        int value
    }
    OWNED_SHIP {
        int owned_ship_number
        int user_id
        int ship_id
        bool is_active
    }
    BATTLE_HISTORY {
        int battle_id
        int user1_id
        int user2_id
        int winner_id
        int user1_ship_number
        int user2_ship_number
        datetime timestamp
    }
```

---

## 🧩 Main Endpoints

- `POST /api/v1/seed/users` – Seed the database with initial users
- `POST /api/v1/seed/ships` – Seed the database with initial ships
- `GET /api/v1/users/` – List all users
- `GET /api/v1/ships/` – List all ships
- `POST /api/v1/market/buy/{user_id}/{ship_id}` – User buys a ship
- `POST /api/v1/market/sell/{user_id}/{owned_ship_number}` – User sells a ship
- `POST /api/v1/battle/battle` – Battle between two users

See the Swagger documentation for payload and response details.

---

## 🏆 Roadmap

- [x] CRUD for users and ships
- [x] Data seeding endpoints
- [x] Battle system
- [x] Ship market (buy/sell)
- [x] Backend reorganization to `backend/app/`
- [x] Start modern frontend (React, Vite or Next.js)
- [x] Internationalization (i18n) for frontend
- [ ] Authentication and multiplayer
- [ ] User profile and settings page
- [ ] Responsive/mobile-friendly frontend
- [ ] Error handling and user feedback improvements
- [ ] API documentation improvements (OpenAPI, examples)
- [ ] CI/CD pipeline (tests, lint, deploy)
- [ ] Docker support (dev/prod)
- [ ] Admin dashboard for managing users/ships
- [ ] Unit and integration tests for frontend
- [ ] Interface for AI agents

---

## 📊 Timeline (Commit History)

```mermaid
gantt
dateFormat  YYYY-MM-DD
axisFormat  %d/%m
section Project Timeline
Initial commit & repo structure        :done,    des1, 2025-06-04, 1d
Database schema & seeding             :done,    des2, 2025-06-04, 3d
API endpoints for users/ships         :done,    des3, 2025-06-05, 2d
Market & seeding endpoints            :done,    des4, 2025-06-07, 3d
Battle system & statistics            :done,    des5, 2025-06-10, 2d
Refactor & .gitignore improvements    :done,    des6, 2025-06-10, 1d
Battle/activation routes & tests      :done,    des7, 2025-06-11, 4d
Requirements & merges                 :done,    des8, 2025-06-15, 1d
Register page & .gitignore update     :done,    des9, 2025-06-24, 1d

section Releases
v0.1.0 :milestone, m1, 2025-06-10, 0d
v0.1.1 :milestone, m2, 2025-06-15, 0d
v0.1.2 :milestone, m3, 2025-06-18, 0d
v0.2.0 :milestone, m4, 2025-06-18, 0d
v0.2.1 :milestone, m5, 2025-06-24, 0d
```

- Each bar represents a key phase or feature, based on actual commit dates and messages.
- For full commit details, see the [GitHub commit history](https://github.com/FilipePacheco73/Bellum-Astrum/commits/main).

---

## 🤝 Contributing

Contributions are welcome! Open issues or submit pull requests to collaborate.

## 📜 License

MIT License

## 👤 Author

[FilipePacheco73](https://github.com/FilipePacheco73)

---

*This project is a playground for exploring backend, APIs, and artificial intelligence in a fun, competitive setting!*