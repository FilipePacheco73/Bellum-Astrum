# 🚀 Space BattleShip

Space BattleShip is a learning project focused on backend development with FastAPI, SQLite database, and game logic integration for spaceship battles. The goal is to provide a robust API for managing users, ships, battles, and the market, serving as a foundation for future AI integrations and possible frontends.

---

## 🎯 Project Goals

- 🧩 **Backend Learning:** Practice with FastAPI, SQLAlchemy, and Pydantic.
- 🔗 **RESTful API:** Endpoints for managing game resources.
- 🤖 **AI-Ready Base:** Structure ready for future integration of intelligent agents.

---

## ✨ Features

- 🕹️ CRUD for users and ships
- ⚔️ Battle system between users
- 🛒 Ship market (buy/sell)
- 🌱 Data seeding endpoints
- 📡 Modular and extensible REST API

---

## 🛠️ Tech Stack

- **Backend:** Python 3.12+, FastAPI, SQLAlchemy, Pydantic
- **Database:** SQLite
- **Testing:** Pytest, FastAPI TestClient

---

## 🏁 Getting Started

### Prerequisites

- Python 3.12+
- (Recommended) Virtual environment: `python -m venv venv`

### Installation

```bash
# Clone the repository
git clone https://github.com/FilipePacheco73/Space-BattleShip.git
cd Space-BattleShip
# Create and activate a virtual environment (optional)
python -m venv venv
# On Windows:
venv\Scripts\activate
# Install dependencies
pip install -r requirements.txt
```

### Running the API

```bash
uvicorn app.main:app --reload
```

Access the interactive documentation at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🗂️ Project Structure

```
/Space-BattleShip
│
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── schemas.py           # Pydantic schemas
│   ├── crud/                # CRUD operations
│   ├── database/            # Database config and models
│   ├── routes/              # API routes/endpoints
│   └── test/                # Automated tests
├── requirements.txt         # Python dependencies
└── README.md
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
- [ ] AI agent interface
- [ ] Authentication and multiplayer

---

## 📈 Project History

- Initial backend and database structure
- Implementation of main endpoints (users, ships, battles, market)
- Automated tests with pytest
- Next steps: API refinement, AI integration, authentication

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
```

- Each bar represents a key phase or feature, based on actual commit dates and messages.
- For full commit details, see the [GitHub commit history](https://github.com/FilipePacheco73/Space-BattleShip/commits/main).

---

## 🤝 Contributing

Contributions are welcome! Open issues or submit pull requests to collaborate.

## 📜 License

MIT License

## 👤 Author

[FilipePacheco73](https://github.com/FilipePacheco73)

---

*This project is a playground for exploring backend, APIs, and artificial intelligence in a fun, competitive setting!*
