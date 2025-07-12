
<!--
  Copilot Custom Instructions for Bellum Astrum
  For details: https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file
-->

# Copilot Instructions

## Frontend (React + Vite + Tailwind CSS)
- Write all code, comments, and documentation in English.
- Use functional React components and React hooks.
- Prefer TypeScript for type safety and maintainability.
- Use Tailwind CSS utility classes for styling; avoid custom CSS unless necessary.
- Organize code into logical folders: components, pages, services, contexts, locales, etc.
- Keep the UI responsive and accessible.

### API Integration
- Use fetch or axios for all API requests.
- Store API URLs and environment variables in a config file or `.env`.
- Handle loading, error, and empty states in all data-fetching components.
- Use context or hooks for global state (e.g., language, user session).

### Internationalization
- All user-facing strings must be translatable.
- Use the provided context and translation files for all text.
- Default language is English (en-US), but support for pt-BR is required.

## Backend (FastAPI + SQLAlchemy)
- Write all code, comments, and documentation in English.
- Follow PEP8 and use type hints where possible.
- Organize code into logical modules: routes, schemas, crud, utils, etc.
- Use SQLAlchemy ORM for database access.
- Handle errors and exceptions gracefully, returning appropriate HTTP status codes.
- Write docstrings for all public functions and classes.
- Use environment variables for secrets and configuration.

## Database (Neon)
- The main database is hosted on Neon (PostgreSQL as a Service).
- Use SQLAlchemy for all ORM/database interactions.
- Do not hardcode credentials; always use environment variables.
- For local development, use a `.env` file or secrets manager to store database URLs.
- Ensure migrations are tracked and up to date (suggested: Alembic).

## Collaboration
- Open issues or pull requests for significant changes.
- Test all features before merging.
- Keep documentation and instructions up to date.

For more details, see the main README.md or contact the repository maintainer.