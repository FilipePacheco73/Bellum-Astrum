# 🚀 Bellum Astrum

Bellum Astrum is a learning project focused on backend development with FastAPI, PostgreSQL database (Neon), and spaceship battle logic. The project is now organized to facilitate expansion with a modern frontend.

---

## 🎯 Project Goals

- 🧩 **Backend Learning:** Practice with FastAPI, SQLAlchemy, and Pydantic.
- 🔗 **RESTful API:** Endpoints for game resources.
- 🤖 **AI-Ready Base:** Structure ready for intelligent agents and frontend integration.

---

## ✨ Features

- 🕹️ CRUD for users and ships
- ⚔️ Battle system with ship activation
- 🛒 Ship market (buy/sell)
- 🛠️ Shipyard system with repair and cooldown
- 🌱 Data seeding endpoints
- 📡 Modular and extensible REST API
- 🖥️ Modern web interface (React + Vite + Tailwind)
- 🔐 JWT-based authentication system
- 🌍 Multi-language support (Portuguese/English)
- 🎮 Complete game interface with sidebar navigation
- 📊 User dashboard with statistics and ELO ranking
- 🗄️ **Centralized Database Module**: Organized database management with lifecycle controls
- 📝 **Comprehensive Logging**: System audit trails and monitoring
- 🔧 **Database Scripts**: Command-line tools for database management
- 🔄 Automated GitHub release workflow (changelog-based)
- 🧪 Full end-to-end automated tests (buy, activate, battle, repair, sell)
- 📝 Standardized Copilot instructions

---

## 🛠️ Tech Stack

- **Backend:** Python 3.12+, FastAPI, SQLAlchemy, Pydantic
- **Database:** PostgreSQL (Neon, Render, etc.) — `DATABASE_URL` required
- **Authentication:** JWT with bcrypt password hashing
- **Testing:** Pytest, FastAPI TestClient
- **Frontend:** React 19, Vite, TypeScript, Tailwind CSS v3
- **API Client:** Axios with automatic token injection
- **Internationalization:** Custom translation system (PT-BR/EN-US)
- **Structure:** Backend in `backend/app/`, Frontend in `frontend/`, Database in `database/`

---

## 🏗️ Database Architecture

The project features a centralized database module with clean imports and lifecycle management, now using PostgreSQL (Neon/Render) as the only supported backend:

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
- **User**: Game user accounts with ELO ranking and statistics
- **Ship**: Ship templates with base characteristics
- **OwnedShips**: Individual ships owned by users with current stats
- **BattleHistory**: Records of battles with detailed logs
- **SystemLogs**: Comprehensive audit logging for security and debugging
- **ShipyardLog**: Tracks last shipyard usage per user/ship

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
- PostgreSQL database (Neon, Render, etc.)
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

# Set your PostgreSQL connection string (Neon, Render, etc.)
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
├── backend/
│   └── app/
│       ├── main.py            # FastAPI entry point with lifespan management
│       ├── crud/              # CRUD operations (users, ships, battles, market, logs)
│       ├── routes/            # API routes/endpoints
│       ├── schemas/           # Pydantic schemas (modularized)
│       ├── test/              # Automated tests (pytest)
│       ├── utils/             # Utility functions (auth, logging, etc.)
│       └── __init__.py
│
├── database/                  # Centralized database module
│   ├── __init__.py            # Clean exports and imports
│   ├── base_data.py           # Initial seed data with environment variables
│   ├── config.py              # Database configuration and engine
│   ├── lifecycle.py           # Database initialization and health checks
│   ├── models.py              # SQLAlchemy models (User, Ship, etc.)
│   ├── session.py             # Session management and dependency injection
│   ├── setup.py               # Main command-line setup script
│   └── scripts/               # Quick utility scripts
│       ├── init_db.py         # Quick database initialization
│       ├── reset_db.py        # Quick database reset
│       └── seed_db.py         # Quick database seeding
│
├── frontend/
│   ├── public/                # Static assets (logos, images, flags)
│   ├── src/                   # React source code
│   │   ├── assets/            # Static assets for React
│   │   ├── components/        # Reusable React components
│   │   ├── config/            # API client configuration
│   │   ├── contexts/          # React context providers
│   │   ├── locales/           # Localization and translations
│   │   ├── pages/             # Main pages/routes
│   │   ├── App.tsx            # Main App component
│   │   ├── main.tsx           # React entry point
│   │   ├── index.css          # Global styles
│   │   └── vite-env.d.ts      # TypeScript definitions
│   ├── package.json           # Frontend dependencies
│   ├── tailwind.config.ts     # Tailwind CSS configuration
│   ├── tsconfig.json          # TypeScript configuration
│   └── vite.config.ts         # Vite configuration
│
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Main Python dependencies
├── README.md                  # Project documentation
└── CHANGELOG.md               # Version history and changes
```

---

## 🗺️ Project Flowchart

```mermaid
flowchart LR
    User["👤 User"]
    Frontend["🌐 Frontend (React/Vite)"]
    API["🚀 FastAPI API"]
    DB["🗄️ PostgreSQL (Neon/Render)"]

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
- DB: PostgreSQL database (Neon/Render)

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
- `GET /api/v1/ships/` – List all ships
- `GET /api/v1/ships/{ship_id}` – Get specific ship details


### Market System
- `POST /api/v1/market/buy/{ship_id}` – Authenticated user buys a ship
- `POST /api/v1/market/sell/{owned_ship_number}` – Authenticated user sells a ship

### Shipyard
- `POST /api/v1/shipyard/repair` – Repair a ship (authenticated, with cooldown)
---

## 🚀 Release Automation

Releases are now created automatically on every push to `main`, using the latest changelog entry as the release notes.

---

## 🤖 Copilot Instructions

Custom Copilot instructions for this project are available in `.github/instructions/copilot-instructions.md`.

### Battle System
- `POST /api/v1/battle/activate-ship/` – Activate a ship for battle
- `POST /api/v1/battle/battle` – Battle between two users

### Logs
- `POST /api/v1/logs/` – Create a new log entry
- `GET /api/v1/logs/` – List all logs
- `GET /api/v1/logs/{log_id}` – Get log by ID
- `DELETE /api/v1/logs/{log_id}` – Delete log by ID

---

## 🏆 Next Steps

- [ ] User profile and settings page
- [ ] Responsive/mobile-friendly frontend
- [ ] Real-time multiplayer features
- [ ] Enhanced battle system with animations
- [ ] Ship customization and upgrades
- [ ] Leaderboards and tournaments
- [ ] API documentation improvements (OpenAPI, examples)
- [ ] Enhanced error handling and user feedback
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
JWT Authentication & Security         :done,    des10, 2025-06-26, 2d
Complete Game Interface & Dashboard   :done,    des11, 2025-06-26, 3d
Comprehensive Logging System          :done,    des12, 2025-07-01, 1d
Centralized Database Module           :done,    des13, 2025-07-02, 1d
Logs endpoints & modular schemas      :done,    des14, 2025-07-09, 1d
Migration to PostgreSQL/Neon/Render   :done,    des15, 2025-07-09, 1d
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