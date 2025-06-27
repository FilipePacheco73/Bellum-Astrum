# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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