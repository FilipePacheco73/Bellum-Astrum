# Copilot Instructions
This project uses GitHub Copilot to assist with code suggestions and documentation. Please follow these guidelines to ensure consistency and maintainability:

## General Guidelines
- Write clear, concise, and well-documented code.
- Use English for all code comments, documentation, and commit messages.
- Follow the existing code style and structure.
- Prefer explicitness over cleverness for readability.

## Backend Specifics
- Use FastAPI, SQLAlchemy, and Pydantic best practices.
- Keep API endpoints RESTful and well-documented.
- Validate all data using Pydantic schemas.
- Organize code into logical modules: routes, schemas, crud, database, and tests.
- Write modular, reusable functions and classes.
- Ensure all database models and migrations are up to date.
- Add or update automated tests for new features or bug fixes.

## Collaboration
- Open issues or pull requests for any significant changes.
- Review and test code before merging.
- Keep the documentation (README, instructions, etc.) updated.

## Internationalization
- All user-facing strings should be easy to translate in the future.
- Use English as the default language for all backend messages and errors.