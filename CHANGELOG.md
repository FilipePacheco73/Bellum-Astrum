# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.5] - 2025-07-01

### Added
- **Comprehensive Logging System**: Complete audit trail and monitoring infrastructure
  - New `SystemLogs` table with comprehensive event tracking
  - Logging utilities with categorized event types (USER_ACTION, SYSTEM, GAME_EVENT, SECURITY, PERFORMANCE, AUDIT)
  - Detailed performance monitoring with execution time tracking
  - Security event logging for authentication and authorization
  - Comprehensive error logging with stack traces and context
- **Enhanced Database Schema**: Improved data integrity and performance
  - Added constraints and indexes to all tables for better data validation
  - Foreign key relationships between users, ships, and owned_ships tables
  - Proper string length limits and data type constraints
  - Optimized indexes for common query patterns
- **Improved Authentication System**: Consolidated authentication utilities
  - Moved authentication functions to dedicated `utils` module
  - Enhanced JWT token verification with security logging
  - Better error handling for expired and invalid tokens
  - Comprehensive security event tracking
- **Battle System Improvements**: Enhanced game mechanics and balance
  - Fixed evasion calculation bug (was percentage-based, now properly decimal-based)
  - Updated ship seed data with proper evasion values (0.05-0.31 range)
  - Improved battle logging with detailed combat information
  - Better error handling and validation in battle system

### Fixed
- **Critical Battle Bug**: Fixed evasion calculation that was causing battles to be unbalanced
  - Evasion was incorrectly calculated as percentage (5-31%) instead of decimal (0.05-0.31)
  - Updated all ship seed data to use proper decimal evasion values
  - Fixed battle logic to properly handle evasion probabilities
- **Authentication Module**: Resolved import issues and consolidated auth utilities
  - Removed duplicate `utils_auth.py` file
  - Consolidated all authentication functions in `utils/auth_utils.py`
  - Fixed import paths across all route modules
- **Database Schema Issues**: Enhanced data integrity and validation
  - Added proper constraints to prevent invalid data entry
  - Fixed foreign key relationships and cascade behaviors
  - Improved error handling for database operations
- **Error Handling**: Comprehensive error tracking and user feedback
  - All API endpoints now include proper error logging
  - Enhanced error messages with context and debugging information
  - Better exception handling with categorized error types

### Changed
- **Code Organization**: Major refactoring for better maintainability
  - Restructured `utils` module with proper separation of concerns
  - Added comprehensive `__init__.py` files for better module organization
  - Improved import structure and dependency management
- **Database Performance**: Optimized queries and data structures
  - Added strategic indexes for common query patterns
  - Improved constraint validation for better data integrity
  - Enhanced database schema with proper data types and limits
- **Security Enhancements**: Improved authentication and authorization
  - Enhanced JWT token handling with proper expiration management
  - Better security event logging and monitoring
  - Improved password hashing and verification
- **API Improvements**: Enhanced error handling and logging across all endpoints
  - All routes now include comprehensive logging
  - Better error messages and status codes
  - Improved request/response validation

### Technical Improvements
- **Logging Infrastructure**: Complete audit and monitoring system
  - Structured logging with JSON details and metadata
  - Performance monitoring with execution time tracking
  - Security event tracking for compliance and monitoring
  - Comprehensive error logging with context and stack traces
- **Database Optimization**: Enhanced performance and data integrity
  - Strategic indexes for improved query performance
  - Proper constraints and validation rules
  - Optimized foreign key relationships
- **Code Quality**: Improved maintainability and organization
  - Better module structure and import management
  - Enhanced error handling and validation
  - Improved code documentation and type hints

## [0.2.4] - 2025-06-28

### Added
- **New Authentication System**: Complete authentication flow with login/logout functionality
  - JWT-based token authentication with automatic storage and validation
  - `AuthContext` and `PrivateRoute` components for secure route protection
  - Login page with email validation and error handling
- **Game Layout System**: New game interface architecture
  - `GameLayout` component with starfield background animation and header
  - `Sidebar` component with navigation menu and user info display
  - `SidebarContext` for sidebar state management
- **Enhanced UI Components**: 
  - Updated `Navbar` with language switcher and dynamic positioning
  - `Button` component for consistent styling across the app
  - Starfield CSS animations added to `App.css`
- **Complete Page Redesigns**: All game pages converted to use new GameLayout
  - Dashboard with user statistics and activity feed
  - Ships page with fleet management interface
  - Market page with tabs for ships, upgrades, and resources
  - Battle page with ship selection and opponent choice
  - Users page with leaderboard and online players
- **API Integration**: 
  - Axios configuration with automatic token injection
  - Complete API client setup for backend communication

### Fixed
- **Dashboard Critical Bug**: Fixed blank screen issue after login caused by data structure mismatch between frontend and backend
  - Updated `UserData` interface to match backend response fields (`currency_value`, `victories`, `defeats`, `elo_rank`, etc.)
  - Fixed `Cannot read properties of undefined (reading 'toLocaleString')` error that was causing the Dashboard to crash
  - Dashboard now correctly displays user statistics with proper field mappings
- **Registration Error Handling**: Enhanced user registration with detailed error messages
  - Better validation for email format and password length
  - Specific error messages for duplicate email/nickname
  - Improved UI feedback for registration process
- **Authentication Flow**: Enhanced authentication debugging and error handling
- **Route Protection**: Improved PrivateRoute component for better authentication state management

### Changed
- **Complete Frontend Architecture Overhaul**: 
  - Migrated from basic routing to context-based authentication system
  - Replaced `SpaceBackground` with integrated starfield animations
  - Updated all pages to use consistent GameLayout instead of PageLayout
- **UI/UX Improvements**:
  - Dashboard now displays ELO rank and damage statistics instead of level/experience system
  - Updated stats cards to show relevant game metrics: victories, currency, damage dealt, and defeats
  - Improved user info display with ELO rating and total damage caused
  - Modern glass-morphism design with backdrop blur effects
- **Navigation System**: Complete sidebar navigation with game-themed icons and descriptions
- **Responsive Design**: Enhanced mobile and desktop layouts across all components
- **Translation System**: Expanded translations for new authentication and game features

### Technical Improvements
- **Code Organization**: Better separation of concerns with context providers
- **Type Safety**: Enhanced TypeScript interfaces for better data handling
- **Performance**: Optimized component rendering and state management
- **Error Handling**: Comprehensive error boundaries and user feedback
- **Backend Enhancements**: Improved user registration endpoint with detailed error handling for duplicate emails/nicknames

## [0.2.3] - 2025-06-26

### Added
- CORS middleware added to FastAPI backend to allow cross-origin requests from the frontend.
- New `PageLayout` component for consistent backgrounds and layout in all main frontend pages.
- New `Button` component for consistent button styles in the frontend.
- Language switcher with flag icons in the Navbar.

### Changed
- Register page and all main pages now use `PageLayout` for consistent UI.
- Register page: improved form, error/success feedback, and backend integration.
- Improved and fixed translations for both English and Portuguese.
- Updated TailwindCSS to v3, removed old config files, and migrated to `tailwind.config.ts`.
- Updated and cleaned up CSS for better dark mode and responsive design.
- Updated dependencies: React 19, React Router v7, TailwindCSS v3, and related types.
- Improved `postcss.config.cjs` for Tailwind v3.
- Backend now accepts cross-origin requests from any origin by default (for development).

### Fixed
- Registration endpoint in the frontend fixed to `/users/register` for backend compatibility.
- User registration now works correctly between frontend and backend.
- Error handling for registration and CORS/OPTIONS requests improved.

### Removed
- Removed legacy and duplicate config files (`tailwind.config.js`, old `package-lock.json`, etc).

## [0.2.2] - 2025-06-26

### Added
- Password hashing and authentication for user registration and login.
- JWT-based authentication for user login.
- Environment variable support for admin and NPC user seeding.

### Changed
- Refactored backend automated tests for a realistic battle flow: creating two users, buying distinct ships, activating, battling, and selling the ships.
- Tests now dynamically fetch available ships to avoid ID conflicts and ensure database state independence.
- Pydantic models updated to use `model_config = ConfigDict(...)` for Pydantic v2 compatibility.
- User creation now requires email and password, and stores hashed passwords.
- User CRUD and routes updated to support secure registration and login.
- Seed logic for users and ships improved for robustness and security.
- Fixed usage of `datetime.utcnow()` to `datetime.now(UTC)` in `battle_crud.py`, eliminating Python deprecation warnings.
- Updated requirements.txt to reflect new dependencies.
- Backend .env loading path fixed for environment variables in backend modules.
- Improved environment variable usage for admin and NPC seeding.
- Generalized .env loading for authentication and seeding logic.

### Removed
- Unnecessary seed calls and dependencies in automated tests.
- Legacy or duplicate code in user and ship creation flows.

## [0.2.1] - 2025-06-24

### Changed
- Improved Register page UI: better spacing, font size, and responsive layout for the form fields.
- Register form container now supports custom width and minHeight for better visual balance.
- Updated `.gitignore`: reorganized sections for backend, frontend, logs, and IDE/system files; translated all comments to English; added explicit patterns for subfolders.
- Started internationalization (i18n) support in the frontend (language context and translation files).

## [0.2.0] - 2025-06-18

### Changed
- Reorganized backend codebase: all backend files are now in `backend/app/`.
- Standardized imports to always reference the project root (`from backend.app...`).
- Database path is now absolute, preventing SQLite access errors.
- Project structure prepared for frontend development.

## [0.1.2] - 2025-06-18

### Changed
- Project name updated to Bellum Astrum

## [0.1.1] - 2025-06-15

### Added
- Battle system with ship activation routes
- Tests for seeding, buying, and selling ships
- Expanded response models and schemas
- More detailed market and battle route responses

### Changed
- Refactored CRUD operations for better organization:
  - Battle CRUD operations
  - Market CRUD operations
  - Ship CRUD operations
  - User CRUD operations
- Updated requirements.txt with latest dependencies

### Removed
- Unnecessary database files from repository

### Fixed
- Updated .gitignore to properly exclude database files

## [0.1.0] - 2025-06-10

### Added
- Initial project structure with FastAPI backend
- Basic CRUD operations implementation
- Core data models and schemas
- Market functionality for buying and selling ships
- Seeding endpoints for ships and users
- Initial documentation (README.md)
- MIT License file
- Basic .gitignore configuration