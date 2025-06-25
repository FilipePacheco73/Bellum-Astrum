<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Copilot Instructions for Frontend

This project is a React + Vite + Tailwind CSS frontend for the Bellum Astrum backend API.

## General Guidelines
- Write all code, comments, and documentation in English.
- Use functional React components and hooks.
- Prefer TypeScript for type safety and maintainability.
- Use Tailwind CSS utility classes for styling; avoid custom CSS unless necessary.
- Organize code into logical folders: components, pages, services, contexts, locales, etc.
- Keep the UI responsive and accessible.

## API Integration
- Use fetch or axios for all API requests.
- Store API URLs and environment variables in a config file or `.env`.
- Handle loading, error, and empty states in all data-fetching components.
- Use context or hooks for global state (e.g., language, user session).

## Internationalization
- All user-facing strings must be translatable.
- Use the provided context and translation files for all text.
- Default language is English (en-US), but support for pt-BR is required.

## Collaboration
- Open issues or pull requests for significant changes.
- Test all features before merging.
- Keep documentation and instructions up to date.

For more details, see the main README.md or contact the repository maintainer.
