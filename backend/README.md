# 🚀 Bellum Astrum - Backend Documentation

The backend is built with FastAPI, providing a robust RESTful API for the spaceship battle game. This document covers setup, architecture, and API endpoints.

---

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python 3.12+)
- **ORM**: SQLAlchemy with Pydantic models
- **Authentication**: JWT with bcrypt password hashing
- **Database**: PostgreSQL (via centralized database module)
- **Testing**: Pytest with FastAPI TestClient
- **Validation**: Pydantic schemas for request/response models

---

## 🏗️ Project Structure

```
backend/
├── .env                    # Environment variables (JWT secrets, etc.)
├── __init__.py            # Package initialization
└── app/                   # Main application package
    ├── main.py            # FastAPI app entry point with lifespan management
    ├── dependencies.py    # Dependency injection (database sessions, auth)
    ├── crud/              # CRUD operations by feature
    │   ├── battle_crud.py # Battle logic and calculations
    │   ├── market_crud.py # Ship buying/selling logic
    │   ├── user_crud.py   # User management operations
    │   ├── work_crud.py   # Work system logic
    │   └── ...            # Other CRUD modules
    ├── routes/            # API endpoint definitions
    │   ├── auth.py        # Authentication endpoints
    │   ├── battle.py      # Battle system endpoints
    │   ├── market.py      # Market system endpoints
    │   ├── ships.py       # Ship management endpoints
    │   ├── users.py       # User management endpoints
    │   ├── work.py        # Work system endpoints
    │   └── ...            # Other route modules
    ├── schemas/           # Pydantic models (organized by feature)
    │   ├── battle_schemas.py
    │   ├── user_schemas.py
    │   ├── ship_schemas.py
    │   └── ...
    ├── utils/             # Utility functions
    │   ├── auth.py        # JWT token handling
    │   ├── logging.py     # Logging utilities
    │   └── ...
    └── test/              # Automated tests
        ├── test_auth.py
        ├── test_battle.py
        ├── test_routes.py
        └── ...
```

---

## ⚙️ Setup & Installation

### 1. Environment Setup

```bash
# Navigate to project root
cd Bellum-Astrum

# Create and activate virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

Create `backend/.env` with the following configuration:

```env
# Environment (local, dev, prod)
ENVIRONMENT=local

# JWT Configuration - Different keys for each environment
JWT_SECRET_KEY_LOCAL=your-local-jwt-secret-key-here
JWT_SECRET_KEY_DEV=your-dev-jwt-secret-key-here-change-this-in-production
JWT_SECRET_KEY_PROD=your-production-jwt-secret-key-here-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_HOURS_LOCAL=24
JWT_ACCESS_TOKEN_EXPIRE_HOURS_DEV=24
JWT_ACCESS_TOKEN_EXPIRE_HOURS_PROD=24
```

**⚠️ Security**: Always use strong, unique JWT secret keys for each environment.

### 3. Database Setup

The backend uses the centralized database module. Ensure the database is set up first:

```bash
# See database/README.md for detailed setup instructions
python database/setup.py init
python database/setup.py seed
```

### 4. Start the Backend Server

```bash
# Navigate to backend directory
cd backend

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **Base URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Health Check**: http://localhost:8000/health

---

## 🔗 API Endpoints

### System Endpoints
- `GET /` - Root endpoint with welcome message and version info
- `GET /version` - Detailed version and project information
- `GET /health` - System health check with database status

### Authentication & Users
- `POST /api/v1/users/register` - Register a new user with validation
- `POST /api/v1/users/login` - User login with JWT token
- `GET /api/v1/users/` - List all users (filtered for PvP/NPC modes)
- `GET /api/v1/users/{user_id}` - Get specific user details with stats
- `PUT /api/v1/users/{user_id}/formation` - Update user battle formation

### Ships Management
- `GET /api/v1/ships/` - List all ship templates with complete stats
- `GET /api/v1/ships/{ship_id}` - Get specific ship template details
- `GET /api/v1/ships/user/{user_id}/ships` - Get user's owned ships with current/base stats
- `GET /api/v1/ships/owned/{ship_number}` - Get specific owned ship details

### Battle System
- `POST /api/v1/battle/activate-ship/` - Activate ship for battle formation
- `POST /api/v1/battle/deactivate-ship/` - Deactivate ship from battle
- `POST /api/v1/battle/battle` - Execute battle with rank bonuses and XP gains
- `GET /api/v1/battle/ship-limits/` - Get ship activation limits by rank

### Market System
- `POST /api/v1/market/buy/{ship_id}` - Purchase ship with credit validation
- `POST /api/v1/market/sell/{owned_ship_number}` - Sell owned ship

### Shipyard System
- `POST /api/v1/shipyard/repair` - Repair ship with 60-second cooldown
- `GET /api/v1/shipyard/status` - Check repair cooldowns for all ships

### Work System
- `POST /api/v1/work/perform` - Perform rank-based work for credits
- `GET /api/v1/work/status` - Check work cooldown and availability
- `GET /api/v1/work/history` - View work history with statistics
- `GET /api/v1/work/types` - Get available work types for user's rank

### System Logs
- `POST /api/v1/logs/` - Create system log entry
- `GET /api/v1/logs/` - List logs with filtering and pagination
- `GET /api/v1/logs/{log_id}` - Get specific log entry
- `DELETE /api/v1/logs/{log_id}` - Delete log entry (admin)

---

## 🎮 Game Systems

### Battle System
The battle system is the core of the game, featuring:
- **Complex Combat**: Damage calculations with attack, shield, evasion, and fire rate
- **Rank Bonuses**: Multiplicative stat bonuses based on user military rank (0% to 60%)
- **Multi-ship Battles**: Support for fleets with ship activation limits by rank
- **Experience System**: Dynamic XP gains based on opponent difficulty and level difference
- **NPC Integration**: Special handling for AI opponents with balanced mechanics

### Progression System
- **Military Ranks**: 11 ranks from Recruit to Fleet Admiral with Fibonacci-like level requirements
- **Experience**: Exponential XP growth with battle participation rewards
- **Stat Bonuses**: Rank-based multipliers affecting all ship statistics during battles

### Work System (Recovery Mechanism)
- **Soft Reset**: Prevents players from getting permanently stuck without ships/credits
- **Rank-Based Jobs**: Different work types and income levels based on military rank
- **Smart Cooldowns**: Balanced intervals from 2 minutes (Recruit) to 12 minutes (Fleet Admiral)
- **Progressive Income**: 700 credits (Recruit) to 17,500 credits (Fleet Admiral) per work session

### Economic Systems
- **Market**: Dynamic ship trading with credit validation
- **Shipyard**: Ship repair system with cooldown management
- **Currency**: Credit-based economy with multiple earning methods

---

## 🧪 Testing

The backend includes comprehensive automated tests covering all major systems:

```bash
# Run all tests
cd backend
pytest

# Run specific test file
pytest app/test/test_battle.py

# Run with coverage
pytest --cov=app

# Run with verbose output
pytest -v
```

**Test Coverage**: 18 comprehensive end-to-end tests covering:
- Authentication flow
- Battle system mechanics
- Market transactions
- Work system functionality
- Ship management
- User progression
- API endpoint validation

---

## 🔧 Development Guidelines

### Code Organization
- **CRUD Operations**: Business logic in `crud/` modules
- **API Routes**: Endpoint definitions in `routes/` modules
- **Data Models**: Pydantic schemas in `schemas/` (organized by feature)
- **Utilities**: Helper functions in `utils/` modules

### Authentication
- **JWT Tokens**: Used for all authenticated endpoints
- **Password Security**: bcrypt hashing for user passwords
- **Token Validation**: Automatic token verification via dependencies

### Error Handling
- **Comprehensive Logging**: System audit trails for debugging and monitoring
- **HTTP Status Codes**: Proper status codes for different error types
- **Validation**: Pydantic models ensure data integrity

### Performance Considerations
- **Database Optimization**: Efficient queries with SQLAlchemy ORM
- **Async Support**: FastAPI's asynchronous capabilities for better performance
- **Connection Management**: Proper database session handling

---

## 🚀 Deployment

The backend is designed for deployment on platforms like Render, Heroku, or similar:

### Environment Configuration
- Set `ENVIRONMENT=prod` for production
- Use strong JWT secret keys
- Configure production database URL
- Enable appropriate logging levels

### Health Checks
The `/health` endpoint provides system status including:
- Database connectivity
- Application status
- Version information

---

## 🔍 Monitoring & Logging

### System Logs
Comprehensive logging system with:
- **Security Events**: Login attempts, registration, authentication failures
- **Business Logic**: Battle results, market transactions, work sessions
- **System Health**: Database operations, errors, performance metrics

### Log Management
- **Structured Logging**: Consistent log formats for parsing
- **Log Levels**: Debug, Info, Warning, Error categorization
- **Audit Trail**: Complete history of user actions and system events

---

## 🤝 Contributing

When contributing to the backend:

1. **Follow Code Style**: Use consistent Python conventions
2. **Add Tests**: Include tests for new features
3. **Update Documentation**: Keep API documentation current
4. **Schema Validation**: Ensure proper Pydantic model definitions
5. **Error Handling**: Include appropriate error responses

---

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **JWT Guide**: https://jwt.io/introduction/

---

## 🔗 Navigation

- **← [Project Overview](../README.md)** - Main project documentation and overview
- **🗄️ [Database Documentation](../database/README.md)** - Database schema, models, and setup
- **🎨 [Frontend Documentation](../frontend/README.md)** - React frontend and UI components
- **🤖 [AI Agents Documentation](../AI_Agents/README.md)** - Autonomous AI players and match system

---
*For frontend integration, see [frontend/README.md](../frontend/README.md)*
