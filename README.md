# 🚀 Bellum Astrum

Bellum Astrum is a learning project focused on backend development with FastAPI, PostgreSQL database (Neon), and spaceship battle logic. The project is now organized to facilitate expansion with a modern frontend.

---

## 🎯 Project Goals

- 🧩 **Backend Learning:** Practice with FastAPI, SQLAlchemy, and Pydantic.
- 🔗 **RESTful API:** Endpoints for game resources.
- 🤖 **AI-Ready Base:** Structure ready for intelligent agents and frontend integration.

---

## ✨ Features

### 🎮 Core Game Systems
- 🕹️ CRUD for users and ships
- ⚔️ Advanced battle system with rank-based bonuses and NPC mechanics
- 🛒 Ship market (buy/sell)
- 🛠️ Shipyard system with repair and cooldown
- 💼 **Work System**: Soft recovery mechanism for players who lose all ships/money
- 🌱 Data seeding endpoints
- 📡 Modular and extensible REST API

### 🎯 Progression & Economy
- 🎯 **Progression System**: Experience, levels, and military ranks (Recruit to Fleet Admiral)
- ⭐ **Rank Bonuses**: Multiplicative stat bonuses based on user rank
- 💰 **Work System**: Rank-based jobs with progressive income (700-40,000 credits)
- ⏰ **Cooldown System**: Shorter work intervals for higher ranks (2h to 30min)
- 🤖 **Smart NPC System**: Balanced AI opponents with special battle mechanics
- 📈 **Dynamic XP Gains**: Experience scales based on opponent difficulty

### 🖥️ Frontend & UI
- 🖥️ Modern web interface (React + Vite + Tailwind)
- 🔐 JWT-based authentication system
- 🌍 Multi-language support (Portuguese/English)
- 🎮 Complete game interface with sidebar navigation
- 📊 User dashboard with statistics and ELO ranking

### 🔧 Technical Infrastructure
- 🗄️ **Centralized Database Module**: Organized database management with lifecycle controls
- 📝 **Comprehensive Logging**: System audit trails and monitoring
- 🔧 **Database Scripts**: Command-line tools for database management
- 🔄 Automated GitHub release workflow (changelog-based)
- 🧪 Full end-to-end automated tests (18 tests covering all systems)
- 📝 Standardized Copilot instructions

---

## 🛠️ Tech Stack

- **Backend:** Python 3.12+, FastAPI, SQLAlchemy, Pydantic
- **Database:** PostgreSQL (Neon, etc.) — `DATABASE_URL` required
- **Authentication:** JWT with bcrypt password hashing
- **Testing:** Pytest, FastAPI TestClient
- **Frontend:** React 19, Vite, TypeScript, Tailwind CSS v3
- **API Client:** Axios with automatic token injection
- **Internationalization:** Custom translation system (PT-BR/EN-US)
- **Structure:** Backend in `backend/app/`, Frontend in `frontend/`, Database in `database/`

---

## 🏗️ Database Architecture

The project features a centralized database module with clean imports and lifecycle management, now using PostgreSQL (Neon) as the only supported backend:

### Database Structure
```
database/
├── __init__.py           # Clean exports for easy imports
├── config.py             # Database configuration and engine setup
├── session.py            # Session management and dependency injection
├── models.py             # SQLAlchemy models (User, Ship, OwnedShips, etc.)
├── base_data.py          # Initial data for seeding
├── lifecycle.py          # Database initialization and health checks
├── setup.py              # Main command-line setup script
└── scripts/              # Quick utility scripts
    ├── init_db.py        # Quick initialization
    ├── seed_db.py        # Quick seeding
    └── reset_db.py       # Quick reset
```

### Database Models
- **User**: Game user accounts with ELO ranking, experience, levels, ranks, and statistics
- **Ship**: Ship templates with base characteristics (30 ships in 6 tiers)
- **OwnedShips**: Individual ships owned by users with current stats
- **BattleHistory**: Records of battles with detailed logs
- **SystemLogs**: Comprehensive audit logging for security and debugging
- **ShipyardLog**: Tracks last shipyard usage per user/ship
- **RankBonus**: Stores rank-based stat bonuses for progression system

### Database Management

You can manage the database using the provided command-line scripts. These commands allow you to initialize, seed, reset, clear, and check the health of your PostgreSQL database.

```bash
# Initialize database with sample data
python database/setup.py init --seed

# Add sample data to existing database  
python database/setup.py seed

# Reset database (drop + recreate)
python database/setup.py reset --seed

# Clear all data (keep structure)
python database/setup.py clear

# Check database health
python database/setup.py health
```

> **Note:**
> - Make sure your `DATABASE_URL` environment variable is set to your PostgreSQL connection string before running these commands.

### Clean Imports
```python
# Simple imports for common use cases
from database import get_db, User, Ship, OwnedShips
from database import initialize_database, check_database_health

# All database functionality accessible through clean interface
```

---

## 🏁 Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL database (Neon,, etc.)
- (Recommended) Virtual environment: `python -m venv venv`

### Quick Start

```bash
# Clone the repository
git clone https://github.com/FilipePacheco73/Bellum-Astrum.git
cd Bellum-Astrum

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set your PostgreSQL connection string (Neon,, etc.)
# Example (Windows):
$env:DATABASE_URL="postgresql://user:password@host:port/dbname"
# Example (Linux/macOS):
export DATABASE_URL="postgresql://user:password@host:port/dbname"

# Initialize database with sample data
python database/setup.py init --seed

# Start the API server
uvicorn backend.app.main:app --reload
```

The API will be available at: [http://localhost:8000](http://localhost:8000)  
Interactive docs at: [http://localhost:8000/docs](http://localhost:8000/docs)  
Health check at: [http://localhost:8000/health](http://localhost:8000/health)

### Frontend Setup (Optional)

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: [http://localhost:5173](http://localhost:5173)

---

## 🗂️ Project Structure

```
/Bellum-Astrum
│
├── .github/                            # GitHub configuration and automation
│   ├── instructions/                   # Development guidelines and instructions
│   │   └── copilot-instructions.md     # Custom Copilot instructions for this project
│   └── workflows/                      # GitHub Actions CI/CD workflows
│       └── release.yml                 # Automated release workflow based on changelog
│
├── backend/
│   └── app/
│       ├── main.py                     # FastAPI entry point with lifespan management
│       ├── crud/                       # CRUD operations (users, ships, battles, market, logs)
│       ├── routes/                     # API routes/endpoints
│       ├── schemas/                    # Pydantic schemas (modularized)
│       ├── test/                       # Automated tests (pytest)
│       ├── utils/                      # Utility functions (auth, logging, etc.)
│       └── __init__.py
│
├── database/                           # Centralized database module
│   ├── __init__.py                     # Clean exports and imports
│   ├── base_data.py                    # Initial seed data with environment variables
│   ├── config.py                       # Database configuration and engine
│   ├── lifecycle.py                    # Database initialization and health checks
│   ├── models.py                       # SQLAlchemy models (User, Ship, etc.)
│   ├── session.py                      # Session management and dependency injection
│   ├── setup.py                        # Main command-line setup script
│   └── scripts/                        # Quick utility scripts
│       ├── init_db.py                  # Quick database initialization
│       ├── reset_db.py                 # Quick database reset
│       └── seed_db.py                  # Quick database seeding
│
├── frontend/
│   ├── public/                         # Static assets (logos, images, flags)
│   ├── src/                            # React source code
│   │   ├── assets/                     # Static assets for React
│   │   ├── components/                 # Reusable React components
│   │   ├── config/                     # API client configuration
│   │   ├── contexts/                   # React context providers
│   │   ├── locales/                    # Localization and translations
│   │   ├── pages/                      # Main pages/routes
│   │   ├── App.tsx                     # Main App component
│   │   ├── main.tsx                    # React entry point
│   │   ├── index.css                   # Global styles
│   │   └── vite-env.d.ts               # TypeScript definitions
│   ├── package.json                    # Frontend dependencies
│   ├── tailwind.config.ts              # Tailwind CSS configuration
│   ├── tsconfig.json                   # TypeScript configuration
│   └── vite.config.ts                  # Vite configuration
│
├── .gitignore                          # Git ignore rules
├── LICENSE                             # MIT License
├── requirements.txt                    # Main Python dependencies
├── README.md                           # Project documentation
└── CHANGELOG.md                        # Version history and changes
```

---

## 🗺️ Project Flowchart

```mermaid
flowchart LR
    User["👤 User"]
    Frontend["🌐 Frontend (React/Vite)"]
    API["🚀 FastAPI API"]
    DB["🗄️ PostgreSQL (Neon)"]

    User -->|"Interacts"| Frontend
    Frontend -->|"HTTP Requests (REST, JWT)"| API
    API -->|"ORM (SQLAlchemy)"| DB
    DB -->|"Data"| API
    API -->|"JSON Response"| Frontend
    Frontend -->|"UI Update"| User
```

**Legend:**
- User: Game player (web interface)
- Frontend: React app (Vite, Tailwind)
- API: FastAPI backend (auth, business logic, REST endpoints)
- DB: PostgreSQL database (Neon)

- All authentication, business logic, and data persistence flow through this pipeline.
- Logging, health checks, and admin tools interact directly with the API and database, but are not shown to the end user.

---

## 🧩 Main Endpoints

### Authentication
- `POST /api/v1/users/register` – Register new user with email and password
- `POST /api/v1/users/login` – Login user and receive JWT token

### Users
- `GET /api/v1/users/` – List all users
- `GET /api/v1/users/{user_id}` – Get specific user details

### Ships
- `GET /api/v1/ships/` – List all ship templates
- `GET /api/v1/ships/{ship_id}` – Get specific ship template details

### Market System
- `POST /api/v1/market/buy/{ship_id}` – Authenticated user buys a ship
- `POST /api/v1/market/sell/{owned_ship_number}` – Authenticated user sells a ship

### Shipyard
- `POST /api/v1/shipyard/repair` – Repair a ship (authenticated, with cooldown)

### Battle System
- `POST /api/v1/battle/activate-ship/` – Activate a ship for battle
- `POST /api/v1/battle/deactivate-ship/` – Deactivate a ship from battle
- `POST /api/v1/battle/battle` – Battle between two users with rank bonuses and progression
- `GET /api/v1/battle/ship-limits/` – Get user's ship activation limits based on rank

### Work System (Recovery)
- `POST /api/v1/work/perform` – Perform work to earn credits (rank-based income)
- `GET /api/v1/work/status` – Check work availability and cooldown status
- `GET /api/v1/work/history` – View work history and total earnings
- `GET /api/v1/work/types` – Get available work types for current rank

### Logs
- `POST /api/v1/logs/` – Create a new log entry
- `GET /api/v1/logs/` – List all logs with pagination and filtering
- `GET /api/v1/logs/{log_id}` – Get log by ID
- `DELETE /api/v1/logs/{log_id}` – Delete log by ID

---

## 💼 Work System (Recovery Mechanism)

The work system provides a "soft reset" mechanism for players who have lost all their ships and money, ensuring no player gets permanently stuck.

### 🎯 How It Works
- **No Requirements**: Can work even with 0 credits and no ships
- **Rank-Based Jobs**: Each rank has a specific work type (maintenance, patrol, trading, etc.)
- **Progressive Income**: Higher ranks earn more credits per work session
- **Cooldown System**: Must wait between work sessions (shorter for higher ranks)
- **Quick Recovery**: Designed so RECRUIT players can buy a basic ship in 2-3 work sessions

### 💰 Income by Rank
| Rank | Work Type | Base Income | Cooldown | Time to Ship* |
|------|-----------|-------------|----------|---------------|
| RECRUIT | Maintenance | 700 | 2h | ~4h |
| ENSIGN | Patrol | 1,400 | 1.75h | ~3.5h |
| LIEUTENANT | Trading | 2,500 | 1.5h | ~1h |
| ... | ... | ... | ... | ... |
| FLEET_ADMIRAL | Strategy | 40,000 | 0.5h | ~1h |

*Time to buy cheapest ship (1,500 credits)

### 🔄 Recovery Process
1. Player loses all ships/money in battles
2. Use `/work/perform` to earn credits (no requirements)
3. Wait for cooldown to complete
4. Repeat until enough credits for a ship
5. Buy ship from market and return to normal gameplay

---

## 🎯 Progression System

Bellum Astrum features a comprehensive progression system that enhances gameplay through experience, levels, and military ranks.

### Experience & Levels
- **Exponential Growth**: XP requirements increase exponentially (base 100, factor 1.5)
- **Dynamic XP Gains**: Earn more XP fighting higher-level opponents, less for lower-level
- **Battle Participation**: Both winners and losers gain experience from battles
- **Level-Up Rewards**: Automatic progression checks after each battle

### Military Ranks
The game features 11 military ranks based on Fibonacci-like level requirements:

| Rank | Level Required | Stat Bonus |
|------|----------------|------------|
| Recruit | 1 | 0% |
| Ensign | 3 | 5% |
| Lieutenant | 5 | 10% |
| Lieutenant Commander | 8 | 15% |
| Commander | 13 | 20% |
| Captain | 21 | 25% |
| Commodore | 35 | 30% |
| Rear Admiral | 55 | 35% |
| Vice Admiral | 89 | 40% |
| Admiral | 144 | 50% |
| Fleet Admiral | 233 | 60% |

### Rank Bonuses
Rank bonuses apply multiplicatively to all ship stats during battles:
- **Attack**: Increased damage output
- **Shield**: Enhanced defensive capabilities
- **HP**: Additional health points
- **Evasion**: Improved dodge chance
- **Fire Rate**: Faster attack speed
- **Value**: Higher ship worth

### NPC System
11 NPCs distributed across different ranks provide balanced opposition:
- **Balanced Economy**: NPCs don't gain or lose currency
- **Ship Restoration**: NPC ships auto-repair after battles
- **ELO Protection**: Only human players gain/lose ELO against NPCs
- **Progressive Challenge**: NPCs scale from Recruit to Fleet Admiral

---

## 🚀 Release Automation

Releases are now created automatically on every push to `main`, using the latest changelog entry as the release notes.

---

## 🤖 Copilot Instructions

Custom Copilot instructions for this project are available in `.github/instructions/copilot-instructions.md`.

## 🏆 Next Steps

- [ ] User profile and settings page
- [ ] Responsive/mobile-friendly frontend
- [ ] Real-time multiplayer features
- [ ] Enhanced battle system with animations
- [ ] Ship customization and upgrades beyond rank bonuses
- [ ] Guild/Alliance system for team battles
- [ ] Leaderboards and tournaments with rank-based brackets
- [ ] Mission/Campaign system with story progression
- [ ] Advanced NPC AI behaviors and personalities
- [ ] Ship crafting and blueprint system
- [ ] API documentation improvements (OpenAPI, examples)
- [ ] Enhanced error handling and user feedback
- [ ] CI/CD pipeline (tests, lint, deploy)
- [ ] Docker support (dev/prod)
- [ ] Admin dashboard for managing users/ships/NPCs
- [ ] Unit and integration tests for frontend
- [ ] Interface for AI agents

---

## 📊 Timeline (Commit History)

```mermaid
gantt
dateFormat  YYYY-MM-DD
axisFormat  %d/%m
section Project Timeline
Initial commit & repo structure        :done,    des1, 2025-06-03, 2d
Database schema & API refactor         :done,    des2, 2025-06-05, 2d
Market system & seeding endpoints      :done,    des3, 2025-06-07, 3d
Battle system & statistics             :done,    des4, 2025-06-10, 2d
Battle routes & ship activation        :done,    des5, 2025-06-11, 4d
Requirements & project structure       :done,    des6, 2025-06-15, 3d
CHANGELOG & frontend foundation        :done,    des7, 2025-06-18, 6d
Frontend components & navbar           :done,    des8, 2025-06-24, 2d
JWT Authentication & Security          :done,    des9, 2025-06-26, 2d
User dashboard & game interface        :done,    des10, 2025-06-28, 2d
Enhanced logging & error handling      :done,    des11, 2025-07-01, 1d
Centralized database module            :done,    des12, 2025-07-02, 1d
README updates & flowchart             :done,    des13, 2025-07-03, 6d
CRUD refactor & logging system         :done,    des14, 2025-07-09, 1d
PostgreSQL migration & health checks   :done,    des15, 2025-07-09, 1d
Shipyard system & GitHub automation    :done,    des16, 2025-07-12, 1d
Work system & NPC progression          :done,    des17, 2025-07-12, 1d
Multi-ship battles & formation system  :active,  des18, 2025-07-13, 1d
```

---

## 🤝 Contributing

Contributions are welcome! Open issues or submit pull requests to collaborate.

## 📜 License

MIT License

## 👤 Author

[FilipePacheco73](https://github.com/FilipePacheco73)

---

*This project is a playground for exploring backend, APIs, and artificial intelligence in a fun, competitive setting!*