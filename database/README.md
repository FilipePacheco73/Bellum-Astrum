# 🗄️ Bellum Astrum - Database Documentation

The database module provides centralized database management for the Bellum Astrum game, featuring PostgreSQL with SQLAlchemy ORM and comprehensive lifecycle management.

---

## 🛠️ Tech Stack

- **Database**: PostgreSQL (Neon, local, or any PostgreSQL provider)
- **ORM**: SQLAlchemy with declarative models
- **Configuration**: Multi-environment support (local, dev, prod)
- **Migrations**: Automated table creation and data seeding
- **Management**: Command-line tools for database operations

---

## 🏗️ Database Structure

```
database/
├── .env                    # Database environment variables
├── __init__.py            # Clean exports for easy imports
├── config.py              # Database configuration and engine setup
├── session.py             # Session management and dependency injection
├── models.py              # SQLAlchemy models (all game entities)
├── base_data.py           # Initial seed data with environment variables
├── lifecycle.py           # Database initialization and health checks
├── setup.py               # Main command-line setup script
└── scripts/               # Quick utility scripts
    ├── init_db.py         # Quick database initialization
    ├── seed_db.py         # Quick data seeding
    └── reset_db.py        # Quick database reset
```

---

## 📊 Database Models

### Core Entities

#### **User**
Game user accounts with comprehensive statistics:
```sql
- id (Primary Key)
- nickname (Unique)
- email (Unique) 
- password_hash (bcrypt)
- created_at, updated_at
- credits (Currency)
- experience, level (Progression)
- rank (Military rank enum)
- elo_rating (PvP ranking)
- battles_won, battles_lost
- total_damage_dealt, total_damage_taken
- ships_destroyed, ships_lost
```

#### **Ship**
Ship templates with base characteristics (30 ships in 6 tiers):
```sql
- id (Primary Key)
- name, description
- tier (1-6 difficulty tiers)
- base_attack, base_shield, base_hp
- base_fire_rate, base_evasion
- base_value (Market price)
```

#### **OwnedShips**
User-owned ships with current stats and battle damage:
```sql
- id (Primary Key)
- user_id (Foreign Key to User)
- ship_id (Foreign Key to Ship)
- ship_number (Unique identifier per user)
- status (active, owned, destroyed, sold)
- actual_attack, actual_shield, actual_hp
- actual_fire_rate, actual_evasion, actual_value
- is_active (Battle formation status)
- activated_at, created_at, updated_at
```

### Battle & Combat System

#### **BattleHistory**
Records of battles with detailed logs:
```sql
- id (Primary Key)
- user1_id, user2_id (Foreign Keys)
- winner_id, loser_id
- battle_log (JSON battle details)
- user1_xp_gained, user2_xp_gained
- elo_change (ELO rating adjustments)
- created_at
```

#### **RankBonus**
Stores rank-based stat bonuses for progression system:
```sql
- id (Primary Key)
- rank (Military rank enum)
- attack_bonus, shield_bonus, hp_bonus
- fire_rate_bonus, evasion_bonus
```

### Economic & Management Systems

#### **ShipyardLog**
Tracks last shipyard usage per user/ship with cooldowns:
```sql
- id (Primary Key)
- user_id (Foreign Key)
- ship_id (Foreign Key)
- last_repair_at (Cooldown tracking)
- created_at
```

#### **WorkLog**
Tracks work system usage and earnings:
```sql
- id (Primary Key)
- user_id (Foreign Key)
- work_type (Based on rank)
- credits_earned
- created_at
```

### System Management

#### **SystemLogs**
Comprehensive audit logging for security and debugging:
```sql
- id (Primary Key)
- user_id (Optional Foreign Key)
- action (Log action type)
- details (JSON additional information)
- ip_address, user_agent
- created_at
```

---

## ⚙️ Setup & Installation

### 1. Environment Configuration

Create `database/.env` with the following variables:

```env
# Environment (local, dev, prod)
ENVIRONMENT=local

# Database URLs for different environments
DATABASE_URL_LOCAL=postgresql://username:password@localhost:5432/bellum_astrum_local
DATABASE_URL_DEV=postgresql://username:password@dev-host:5432/bellum_astrum_dev
DATABASE_URL_PROD=postgresql://username:password@prod-host:5432/bellum_astrum_prod

# Database settings
DB_ECHO=False  # Set to True for SQL query logging

# JWT Configuration - Must match backend configuration
JWT_SECRET_KEY_LOCAL=your-local-jwt-secret-key-here
JWT_SECRET_KEY_DEV=your-dev-jwt-secret-key-here-change-this-in-production
JWT_SECRET_KEY_PROD=your-production-jwt-secret-key-here-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_HOURS_LOCAL=24
JWT_ACCESS_TOKEN_EXPIRE_HOURS_DEV=24
JWT_ACCESS_TOKEN_EXPIRE_HOURS_PROD=24
```

### 2. Database Creation

Ensure your PostgreSQL database exists before setup:

```sql
-- Local development example
CREATE DATABASE bellum_astrum_local;
CREATE USER bellum_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE bellum_astrum_local TO bellum_user;
```

### 3. Database Initialization

Use the provided command-line tools for database management:

```bash
# Check database connection
python database/setup.py health

# Initialize database (creates all tables)
python database/setup.py init

# Seed with sample data (ships, NPCs, ranks)
python database/setup.py seed

# Reset database (drop + init + seed) - DESTRUCTIVE
python database/setup.py reset
```

#### Quick Scripts (Alternative)
```bash
# Same functionality as setup.py but shorter commands
python database/scripts/init_db.py
python database/scripts/seed_db.py
python database/scripts/reset_db.py
```

---

## 📈 Initial Data & Seeding

### Ship Templates (30 Ships, 6 Tiers)

**Tier 1 (Starter)**:
- Scout, Interceptor, Courier, Patrol, Escort

**Tier 2 (Basic)**:
- Fighter, Corvette, Gunboat, Frigate, Destroyer

**Tier 3 (Intermediate)**:
- Cruiser, Battle Cruiser, Heavy Cruiser, Strike Cruiser, Assault Cruiser

**Tier 4 (Advanced)**:
- Battleship, Dreadnought, Heavy Battleship, Assault Battleship, War Battleship

**Tier 5 (Elite)**:
- Carrier, Supercarrier, Battle Carrier, Heavy Carrier, Assault Carrier

**Tier 6 (Legendary)**:
- Titan, Mothership, Superdreadnought, Leviathan, Colossus

### NPC Opponents (11 NPCs)
NPCs distributed across different military ranks for balanced progression:
- **Training NPCs**: Recruit to Lieutenant ranks
- **Challenge NPCs**: Commander to Admiral ranks
- **Elite NPCs**: Fleet Admiral rank opponents

### Military Ranks & Bonuses
11 ranks with Fibonacci-like level requirements and progressive stat bonuses:

| Rank | Level Required | Stat Bonus | Ships Limit |
|------|----------------|------------|-------------|
| Recruit | 1 | 0% | 1 |
| Ensign | 3 | 5% | 1 |
| Lieutenant | 5 | 10% | 2 |
| Lieutenant Commander | 8 | 15% | 2 |
| Commander | 13 | 20% | 3 |
| Captain | 21 | 25% | 3 |
| Commodore | 35 | 30% | 4 |
| Rear Admiral | 55 | 35% | 4 |
| Vice Admiral | 89 | 40% | 5 |
| Admiral | 144 | 50% | 5 |
| Fleet Admiral | 233 | 60% | 6 |

---

## 🔧 Database Management

### Health Checks
```bash
# Check database connectivity and status
python database/setup.py health
```

Returns:
- Database connection status
- Table count and structure validation
- Sample data verification
- Environment configuration

### Environment Switching
The system automatically uses the appropriate database based on the `ENVIRONMENT` variable:
- `local` → `DATABASE_URL_LOCAL`
- `dev` → `DATABASE_URL_DEV`
- `prod` → `DATABASE_URL_PROD`

### Migration Strategy
Currently using automated table creation through SQLAlchemy metadata. For production:
1. **Schema Changes**: Update models in `models.py`
2. **Data Updates**: Modify seed data in `base_data.py`
3. **Deployment**: Run `python database/setup.py init` on new environments

---

## 🔍 Advanced Features

### Session Management
- **Dependency Injection**: Automatic session handling for FastAPI
- **Connection Pooling**: Efficient database connection management
- **Transaction Support**: Proper commit/rollback handling

### Logging Integration
- **Audit Trail**: Complete history of user actions
- **Security Monitoring**: Login attempts, failed authentications
- **Performance Tracking**: Database query performance metrics

### Data Integrity
- **Foreign Key Constraints**: Proper relational data integrity
- **Unique Constraints**: Prevent duplicate nicknames and emails
- **Cascade Operations**: Proper handling of related data deletion

---

## 📊 Database Relationships

```mermaid
erDiagram
    User {
        int user_id PK
        string user_name UK
        string email UK
        string password_hash
        int currency_value
        int experience
        int level
        enum rank
        int elo_rating
        int battles_won
        int battles_lost
        int ships_destroyed
        int ships_lost
        float total_damage_dealt
        float total_damage_taken
        string default_formation
        timestamp created_at
        timestamp updated_at
    }
    
    Ship {
        int ship_id PK
        string ship_name UK
        float attack
        float shield
        float evasion
        float fire_rate
        float hp
        int value
    }
    
    OwnedShips {
        int owned_ship_id PK
        int user_id FK
        int ship_id FK
        int ship_number
        enum status
        float attack
        float shield
        float evasion
        float fire_rate
        float hp
        int value
        boolean is_active
        timestamp activated_at
        timestamp created_at
        timestamp updated_at
    }
    
    BattleHistory {
        int battle_id PK
        int user1_id FK
        int user2_id FK
        int winner_user_id FK
        json battle_log
        int user1_xp_gained
        int user2_xp_gained
        int user1_elo_change
        int user2_elo_change
        timestamp timestamp
    }
    
    SystemLogs {
        int log_id PK
        int user_id FK
        string action
        string log_category
        json details
        string ip_address
        string user_agent
        timestamp timestamp
    }
    
    ShipyardLog {
        int shipyard_log_id PK
        int user_id FK
        int ship_number
        int ship_id FK
        timestamp last_repair_at
        timestamp created_at
    }
    
    RankBonus {
        int id PK
        enum rank UK
        int min_level
        float attack
        float shield
        float hp
        float evasion
        float fire_rate
        float value
        int max_active_ships
        int work_income
        int work_cooldown_minutes
    }
    
    WorkLog {
        int id PK
        int user_id FK
        string work_type
        int income_earned
        timestamp performed_at
        enum rank_at_time
        timestamp cooldown_until
    }
    
    User ||--o{ OwnedShips : owns
    Ship ||--o{ OwnedShips : "template for"
    User ||--o{ BattleHistory : "participates in"
    User ||--o{ SystemLogs : generates
    User ||--o{ ShipyardLog : "uses shipyard"
    User ||--o{ WorkLog : performs
    RankBonus ||--o{ User : "provides bonuses to"
```

---

## 🚀 Performance Optimization

### Indexing Strategy
Key indexes for optimal performance:
- **User lookups**: nickname, email, level, rank
- **Ship queries**: tier, base_value
- **Battle history**: user IDs, created_at
- **Owned ships**: user_id + status, user_id + is_active

### Query Optimization
- **Eager Loading**: Proper join strategies for related data
- **Batch Operations**: Efficient bulk data operations
- **Connection Pooling**: Optimal database connection management

---

## 🧪 Testing & Development

### Test Database
For testing environments:
```bash
# Use separate test database
DATABASE_URL_LOCAL=postgresql://username:password@localhost:5432/bellum_astrum_test

# Quick reset for tests
python database/scripts/reset_db.py
```

### Development Tools
- **Database Inspection**: Use `DB_ECHO=True` for SQL query logging
- **Data Validation**: Built-in model validation through SQLAlchemy
- **Schema Export**: Models available for external documentation

---

## 🔒 Security Considerations

### Data Protection
- **Password Security**: bcrypt hashing for user passwords
- **SQL Injection Prevention**: SQLAlchemy ORM protects against injection attacks
- **Environment Variables**: Sensitive data stored in environment files

### Access Control
- **User Isolation**: Proper user_id filtering in all operations
- **Session Management**: Secure database session handling
- **Audit Logging**: Complete trail of database operations

---

## 📚 Additional Resources

- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **Database Design Best Practices**: Normalization and relationship guidelines

---

## 🔗 Navigation

- **← [Project Overview](../README.md)** - Main project documentation and overview  
- **⚙️ [Backend Documentation](../backend/README.md)** - FastAPI backend and API endpoints
- **🎨 [Frontend Documentation](../frontend/README.md)** - React frontend and UI components

---
