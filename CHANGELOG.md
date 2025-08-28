# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.13] - 2025-08-28

### Improved
- **Backend API Documentation**: Complete overhaul of API endpoints documentation in README.md
  - Updated authentication endpoints to reflect actual implementation (routes in `/api/v1/users/` instead of `/api/v1/auth/`)
  - Added missing system endpoints (`/`, `/version`, `/health`)
  - Corrected ships management endpoints with proper paths and descriptions
  - Added user formation management endpoint (`PUT /api/v1/users/{user_id}/formation`)
  - Enhanced ships endpoints documentation with owned ships management
  - All API endpoints now accurately reflect the current codebase implementation
  - Improved endpoint descriptions with clearer functionality explanations

## [0.5.12] - 2025-08-27

### Added
- **System Architecture Documentation**: Comprehensive system architecture visualization
  - Added detailed Mermaid diagram illustrating complete system architecture
  - Visual representation of all component interactions (Frontend, Backend, Database, AI Agents)
  - Clear separation of layers with descriptive naming (User Interface, API, Data, Intelligence)
  - Component interaction flows showing data movement and API communications
  - Professional architecture documentation with technical specifications

- **AI Agents System Enhancements**: Major improvements to AI decision-making and memory systems
  - New centralized prompt system with `decision_prompts.py` and `personality_prompts.py`
  - Enhanced LLM response structure with token tracking and reasoning capture
  - Improved AI agent initialization with model sharing capabilities
  - Mandatory first-round status checks for better AI context understanding
  - Advanced memory storage with detailed token usage and AI reasoning tracking

- **Dynamic Version Management**: Automated version synchronization across project components
  - Backend version extraction from CHANGELOG.md with caching system
  - Frontend version synchronization to match project version
  - AI Agents version tracking with automatic CHANGELOG parsing
  - Consistent version display across all components

### Improved
- **AI Agents Documentation**: Complete overhaul of AI Agents README
  - Updated project structure to reflect current file organization
  - Corrected memory system documentation (JSON format instead of deprecated JSONL)
  - Updated AI personality configurations with current LLM settings (TinyLlama for all agents)
  - Enhanced memory query functions documentation with actual implemented features
  - Added performance optimization section with GPU acceleration details
  - Updated technology stack with CUDA optimization and quantization information

- **AI Decision-Making System**: Enhanced strategic decision processing
  - Standardized response format with ACTION/EXPLANATION structure
  - Improved fallback decision-making for LLM failures
  - Better error handling with detailed token tracking
  - Enhanced prompt engineering with personality-specific behaviors
  - Model sharing optimization to reduce memory usage

- **Infrastructure Documentation**: Accurate infrastructure representation
  - Updated database documentation to reflect Neon PostgreSQL hosting
  - Corrected AI memory system documentation (JSON storage, not SQLite)
  - Enhanced system architecture with proper technology stack representation
  - Improved component naming for better clarity and understanding

- **Configuration Management**: Enhanced AI agent configuration system
  - Optimized LLM configurations with GPU-specific settings
  - Improved memory management with 4-bit quantization
  - Enhanced model loading with automatic sharing between agent types
  - Better temperature control for different AI personalities

### Technical Improvements
- **Documentation Accuracy**: Synchronized documentation with actual implementation
  - Fixed discrepancies between documented and actual file structures
  - Updated LLM model references to reflect current TinyLlama-1.1B-Chat-v1.0 usage
  - Corrected memory format documentation to match JSON-based storage system
  - Enhanced technical specifications with accurate hardware requirements and optimization details

- **Code Architecture**: Significant refactoring and organization improvements
  - Removed deprecated prompt files (aggressive_prompts.py, defensive_prompts.py, tactical_prompts.py)
  - Centralized prompt management with modular personality system
  - Enhanced error handling throughout AI agent pipeline
  - Improved token counting and usage tracking for LLM operations
  - Better model resource management and sharing

- **Memory System Overhaul**: Complete redesign of AI agent memory management
  - Transitioned from JSONL to structured JSON format
  - Enhanced memory entries with token usage and AI reasoning
  - Improved memory querying with better performance
  - Added comprehensive cleanup and maintenance functions
  - Better memory summarization for decision context

### Fixed
- **File Format Consistency**: Standardized memory storage formats
  - Fixed JSONL references in run_ai_match.py to use JSON files
  - Corrected memory file extensions throughout codebase
  - Resolved memory file cleanup to target correct file types
  - Enhanced memory file structure for better reliability

## [0.5.11] - 2025-08-27

### Improved
- **Dependency Management**: Refactored requirements.txt for better deployment optimization
  - Simplified from 83 pinned dependencies to 16 direct dependencies
  - Organized dependencies by category (Backend, AI Agents, Development, Logging)
  - Changed from exact version pinning to minimum version constraints (>=) for better compatibility
  - Removed transitive dependencies to let pip handle automatic resolution
  - Improved installation speed and reduced potential version conflicts during deployment
  - Enhanced maintainability with clear categorization and documentation

### Technical Improvements
- **Build System**: Optimized package management for production deployment
  - Reduced requirements.txt file size by ~80% while maintaining full functionality
  - Implemented flexible versioning strategy allowing compatible updates
  - Improved container build times and deployment reliability
  - Better separation of concerns between direct and transitive dependencies

## [0.5.10] - 2025-08-14

### Improved
- **AI Agents Internationalization**: Complete English translation of AI system
  - Translated all prompts, documentation, and system messages from Portuguese to English
  - Updated AI agent personalities (Warrior, Guardian, Tactician) with English behavioral patterns
  - Standardized game mechanics explanations and strategic decision prompts in English
  - Enhanced code documentation and comments for international development standards

- **Documentation Enhancement**: Professional AI Agents documentation improvements
  - Enhanced README.md for AI Agents module with clearer technical specifications
  - Improved AI personality descriptions with behavioral patterns and LLM configurations
  - Better organized tool documentation with battle system, economy, and information management
  - Quick start guide with environment setup and training match execution
  - Analysis and monitoring guides with real-time statistics and log analysis examples

### Technical Improvements
- **Code Quality and Standards**: International development best practices implementation
  - Standardized all variable names, comments, and documentation in English
  - Improved error handling with English error messages and logging
  - Enhanced type hints and docstrings for better code maintainability
  - Consistent naming conventions across all AI agent modules and configurations

- **System Maintenance**: Improved AI agent system organization
  - Refined match orchestrator with English method names and documentation
  - Updated LLM configuration with clearer model descriptions and parameter explanations
  - Enhanced prompt system organization with categorized behavioral templates
  - Improved logging system with standardized English message formats

## [0.5.9] - 2025-08-12

### Added
- **Autonomous AI Agents System**: Complete implementation of intelligent AI players
  - Multi-personality AI agents (Warrior, Guardian, Tactician) with distinct behavioral patterns
  - LLM-powered decision making using HuggingFace Transformers (DialoGPT, Mistral 7B, TinyLlama)
  - Strategic prompts system with personality-based behaviors and adaptive decision making
  - Automated match orchestration system for continuous AI vs AI tournaments
  - Real-time agent performance monitoring and battle result tracking

- **Advanced Logging System**: Dual logging architecture for comprehensive monitoring
  - Structured debug logging for system events, API calls, and error tracking
  - Dedicated AI decision logging for agent reasoning, tool usage, and strategic decisions
  - Custom formatters with timestamps, round tracking, and agent identification
  - Daily log rotation with organized file structure for historical analysis
  - Performance metrics and match result logging with JSON export

- **File-Based Memory System**: Intelligent agent learning and persistence
  - JSON Lines format memory storage for each AI agent with action history
  - Agent memory management with game state tracking before/after actions
  - Strategic decision reasoning storage for learning pattern analysis
  - Memory summarization for recent actions and performance insights
  - Cross-round learning capabilities with historical action analysis

### Technical Improvements
- **Architecture Refactoring**: Enhanced project structure and code organization
  - Modular AI agent configuration with personality definitions and LLM settings
  - Environment variable management for AI credentials and model configurations
  - Centralized prompt management system with aggressive, defensive, and tactical strategies
  - Tool calling system with comprehensive error handling and retry mechanisms
  - Match orchestration with configurable rounds, agent limits, and battle parameters

- **Documentation Enhancement**: Professional documentation overhaul
  - Complete README.md restructuring with current project status and AI capabilities
  - Enhanced tech stack presentation organized by functional areas
  - Updated project goals to reflect AI/ML learning objectives and data analytics
  - Standardized navigation sections across all component documentation
  - Professional formatting with emoji indicators and clear section hierarchy

- **Code Quality Improvements**: Development workflow and structure optimization
  - Removed legacy SQLite memory system in favor of transparent file-based storage
  - Cleaned up unused directory structures and optimized folder organization
  - Enhanced error handling throughout AI agent pipeline with comprehensive logging
  - Standardized English documentation across all project components
  - Cross-component documentation linking for improved developer navigation

### Fixed
- **Directory Structure**: Resolved incorrect folder creation and cleanup
  - Fixed AI_Agents creating nested folders in incorrect locations
  - Removed empty `memory` and `models` directories from codebase
  - Corrected log file path generation to use existing project log directories
  - Standardized memory file storage in dedicated `memories` directory

## [0.5.8] - 2025-08-09

### Fixed
- **User Data Consistency**: Resolved inconsistent user information display across pages
  - All pages now show correct user nickname and level instead of "Player Level 1" fallbacks
  - Dashboard, Battle, Ships, Market, and Work pages display unified user information
  - Enhanced useUserData hook with proper loading states and error handling
  - Automatic data synchronization across all game pages
  - Improved user experience with consistent sidebar information display

- **Translation System Enhancements**: Complete internationalization support
  - Fixed all remaining hardcoded Portuguese text in Battle page components
  - Enhanced translation system with parameter interpolation and nested key support
  - BattleLogModal and ToastNotification components fully translated
  - Comprehensive battle system translations for both Portuguese and English
  - Consistent language switching across all game interface elements

### Technical Improvements
- **Code Organization**: Enhanced component structure and data flow
  - Centralized user data management with reusable custom hooks
  - Improved translation context with advanced interpolation capabilities
  - Better separation of concerns between UI components and data logic
  - Enhanced error handling and loading states across all pages

- **Documentation Structure**: Reorganized README.md with improved navigation
  - Enhanced project overview with clearer game feature descriptions
  - Structured documentation links for Backend, Database, and Frontend components
  - Improved tech stack presentation with comprehensive technology listing
  - Better organized project goals section with educational objectives
  - Professional formatting with emoji icons and logical section flow

## [0.5.7] - 2025-08-09

### Added
- **Complete Work System**: Fully functional work page with comprehensive backend integration
  - Work.tsx page with real-time cooldown timer and status updates
  - API integration with /work/perform, /work/status, /work/history, /work/types endpoints
  - Dynamic work types based on user rank with appropriate income ranges
  - Work history with complete statistics (total sessions, earnings, averages)
  - Real-time cooldown countdown with automatic data refresh when timer completes
  - Responsive design with loading states and error handling
  - Complete Portuguese and English translations for all work-related interface elements
  - Navigation integration with 🔨 icon in sidebar menu

- **User Data Consistency System**: Centralized user data management across all pages
  - Created useUserData.ts custom hook for consistent user information loading
  - Eliminated "Player Level 1" fallback issues across Battle, Ships, and Market pages
  - All pages now display correct user nickname and level in sidebar
  - Unified user data loading with loading states and error handling
  - Automatic user data refresh functionality

- **Enhanced Translation System**: Expanded internationalization support
  - Enhanced LanguageContext with nested translation keys support
  - Parameter interpolation in translations (e.g., '{seconds}s' replacement)
  - Work system translations with comprehensive Portuguese and English support
  - BattleLogModal and ToastNotification translation improvements
  - Translation fallback mechanism for missing keys

### Changed
- **Work Cooldown System**: Converted from hours to minutes for better gameplay experience
  - All rank cooldowns converted: RECRUIT (2h→120min) to FLEET_ADMIRAL (12h→720min)
  - Backend models updated from work_cooldown_hours to work_cooldown_minutes
  - API responses now return cooldown information in minutes
  - Time calculations updated throughout work system (seconds/60 instead of seconds/3600)

- **Ships Page Enhancements**: Improved ship statistics display format
  - Ship statistics now show "Current / Base" format for all stats
  - Attack, Shield, HP, and Evasion rounded to nearest integer
  - Fire Rate displayed with 1 decimal place precision
  - Evasion converted to percentage format with proper rounding
  - Rank bonus display section showing detailed bonus calculations
  - Enhanced fleet overview with dynamic bonus explanations

- **Dashboard Information Organization**: Improved data presentation
  - Eliminated duplicate "Naves Perdidas" and "Naves Destruídas" statistics
  - Battle statistics properly organized in dedicated "Battle Statistics" section
  - Ship information section now focuses on active ships and fleet status
  - Cleaner information hierarchy for better user experience

### Fixed
- **Critical Ships Page Issue**: Resolved white screen problem
  - Created /users/{user_id}/ships backend endpoint for proper ship data loading
  - Updated getUserOwnedShips() API function to use correct endpoint
  - Ships page now properly displays user's owned ships with all details and statistics
  - Fixed ship data loading for active and owned ships (excluding destroyed ships)

- **User Validation Security**: Enhanced nickname validation system
  - Backend validation prevents nicknames containing "admin" or "test_user" (case-insensitive)
  - Frontend Register.tsx with isValidNickname() client-side validation
  - PvP battle filtering excludes administrative and test user accounts
  - Visual feedback with red borders and error messages for invalid nicknames
  - Double validation (client + server) for enhanced security

- **Battle System Improvements**: Enhanced NPC and PvP opponent management
  - NPCs are now real users from database with "NPC" in nickname instead of hardcoded opponents
  - Dynamic NPC filtering based on nickname patterns
  - PvP mode shows only regular users (excluding NPCs, admin, test users)
  - NPCs display real statistics (level, ELO, victories, defeats)
  - Unified interface between NPCs and PvP opponents

- **Translation Issues**: Resolved hardcoded text across multiple pages
  - Battle page fully translated with all interface elements using translation keys
  - Fixed translation key display issues (e.g., "battle.notifications.victory_title")
  - BattleLogModal with complete translation support for all battle result elements
  - Consistent translation system implementation across all game pages

### Technical Improvements
- **Backend Schema Organization**: Enhanced code structure and maintainability
  - Consolidated ship-related schemas into single ship_schemas.py file
  - Removed duplicate owned_ship_schemas.py after migration
  - Updated all imports across ships.py, users.py, and battle.py routes
  - Improved code organization with centralized schema management

- **API Architecture**: Enhanced backend-frontend communication
  - New /users/{user_id}/ships endpoint for comprehensive ship data retrieval
  - Improved error handling and response validation across all work endpoints
  - Enhanced ship data structure with base and actual statistics support
  - Proper filtering of ship data by status (active, owned, excluding destroyed)

- **Hook Architecture**: Improved state management and code reusability
  - useUserData custom hook for centralized user data management
  - Consistent loading states and error handling across all pages
  - Automatic data refresh capabilities in user data hook
  - Eliminated code duplication in user data loading logic

- **Work System Backend**: Comprehensive work functionality implementation
  - Work cooldown system fully implemented with minute-based calculations
  - Work history tracking with detailed statistics and rank information
  - Dynamic work types based on user rank with appropriate income ranges
  - Complete logging system for all work activities and security events

## [0.5.6] - 2025-07-31

### Added
- **Shipyard System**: Complete ship repair functionality implementation
  - POST /shipyard/repair endpoint with ship_number parameter
  - 60-second cooldown system between repairs per ship
  - ShipyardLog model for tracking repair history and cooldowns
  - Comprehensive repair validation (ship ownership, status, cooldown)
  - Ship statistics restoration to base values (attack, shield, HP, evasion, fire_rate, value)
- **Complete Translation System**: Full internationalization support across multiple pages
  - Portuguese (pt-BR) and English (en-US) translations for Battle page interface
  - BattleLogModal and ToastNotification components fully translated
  - Enhanced LanguageContext with nested key support and parameter interpolation
  - Translation function (t) with fallback mechanism for missing translations
- **Battle System Enhancements**: Improved bonus application and ship data handling
  - Proper rank bonus application at battle start and removal at battle end
  - Enhanced battle flow with temporary bonus management during combat
  - Improved ship statistics degradation system using base values

### Changed
- **Backend Schema Organization**: Major cleanup and consolidation
  - Removed duplicate schemas.py file after comprehensive verification
  - All organized schema files confirmed complete and properly structured
  - Updated imports across all route files to use organized schema structure
  - Consolidated ship-related schemas into single ship_schemas.py file
- **Battle Interface**: Complete translation overhaul
  - All hardcoded Portuguese text replaced with translation keys
  - Battle modes, opponent selection, statistics, and actions fully localized
  - Battle log modal with complete translation support for all elements
  - Toast notifications with internationalization support
- **Dashboard Improvements**: Enhanced information organization
  - Eliminated duplicate "Naves Perdidas" and "Naves Destruídas" statistics
  - Cleaner information hierarchy with battle stats in dedicated sections
  - Improved user experience with organized data presentation
- **Ships Page Enhancements**: Improved statistics display and rank bonus system
  - Ship statistics now show "Current / Base" format with proper rounding
  - Comprehensive rank bonus display with detailed calculations
  - Enhanced fleet overview with rank-based bonus explanations

### Fixed
- **Critical BattleLogModal Issue**: Resolved destroyed ships showing "N/A" for base values
  - Fixed getCurrentShipData() function to handle destroyed ships properly
  - Implemented proper ship data retrieval for battle result display
  - Enhanced ship lookup logic to show correct base stats even for destroyed ships
- **Battle System Bonus Management**: Fixed rank bonus application inconsistencies
  - Proper bonus application at battle start and removal before degradation
  - Corrected ship statistics degradation to use base values consistently
  - Fixed potential inconsistencies in final ship values after battles
- **Translation Display Issues**: Resolved all hardcoded text and translation key problems
  - Fixed translation key display issues (e.g., "battle.notifications.victory_title")
  - Eliminated all hardcoded strings across battle interface components
  - Consistent translation system implementation across all pages
- **User Validation Security**: Enhanced nickname validation and PvP filtering
  - Validation to prevent "Admin" and "test_user" nicknames in registration
  - PvP battle filtering to exclude administrative and test accounts
  - Client-side and server-side validation with proper visual feedback

### Technical Improvements
- **API Integration**: Enhanced backend-frontend communication
  - Shipyard repair endpoint with comprehensive validation and error handling
  - Improved ship data retrieval for battle logs and statistics display
  - Better error handling for ship repair cooldowns and validation
- **Translation Architecture**: Robust internationalization system
  - Nested translation key support for better organization
  - Dynamic parameter replacement in translation strings
  - Comprehensive fallback mechanism for missing translations
  - Enhanced type safety in translation functions
- **Code Quality and Organization**: Improved maintainability and structure
  - Removed duplicate schema files and consolidated imports
  - Better separation of concerns in translation and battle logic
  - Enhanced error handling and user feedback systems
  - Improved component structure and reduced code duplication

## [0.5.5] - 2025-07-28

### Added
- **Market System Overhaul**: Complete redesign of the Market page with real-time functionality
  - Real-time ship data loading from backend API (/ships/ endpoint)
  - User authentication and currency display integration
  - Purchase functionality with /market/buy/{ship_id} endpoint
  - Dynamic ship icons based on ship names and comprehensive ship statistics display
  - Credit validation before purchases with loading states and user feedback
- **Ships Page Enhancement**: Major improvements to "Minhas Naves" (My Ships) page
  - Real backend integration with /users/{user_id}/ships endpoint
  - Ship statistics now display "Current / Base" format with proper rounding
  - Rank bonus system implementation showing detailed bonus calculations
  - Fleet overview with rank-based bonus explanations
  - User rank and level integration with dynamic bonus calculations
- **Security Improvements**: Enhanced user validation and PvP filtering
  - Validation to prevent "Admin" and "test_user" nicknames in registration
  - PvP battle filtering to exclude administrative and test accounts
  - Client-side and server-side validation with visual feedback
- **Battle System Updates**: Improved NPC and user management
  - NPCs now use real database users with "NPC" in nickname
  - Dynamic filtering between NPC battles and PvP modes
  - Real statistics and progression for NPC opponents

### Changed
- **Backend Schema Organization**: Consolidated ship-related schemas
  - Moved all ship schemas to single `ship_schemas.py` file
  - Updated imports across ships.py, users.py, and battle.py modules
  - Removed redundant `owned_ship_schemas.py` file
- **Dashboard Improvements**: Removed duplicate information display
  - Eliminated duplicate "Naves Perdidas" and "Naves Destruídas" statistics
  - Cleaner information hierarchy with battle stats in dedicated section
  - Improved user experience with organized data presentation
- **Translation System**: Expanded internationalization support
  - Market-specific translations for Portuguese (pt-BR) and English (en-US)
  - Ship statistics labels, actions, and error messages
  - Rank bonus system translations and explanations

### Fixed
- **Ships Page White Screen**: Resolved critical display issue
  - Created proper backend endpoint `/users/{user_id}/ships`
  - Fixed API integration with real data instead of placeholders
  - Proper error handling and loading states
- **User Interface Consistency**: Improved visual feedback and user experience
  - Fixed ship statistics formatting and display
  - Proper loading states during purchases and data fetching
  - Enhanced error messages and user guidance

### Technical Improvements
- **API Integration**: Enhanced backend-frontend communication
  - Parallel API calls for ships and user data
  - JWT token decoding for user identification
  - Real-time currency updates after transactions
- **Code Organization**: Better structure and maintainability
  - Consolidated schemas and reduced file redundancy
  - Improved import structure and dependency management
  - Enhanced error boundaries and retry functionality
- **Database Operations**: Optimized queries and data handling
  - Efficient filtering of owned ships by status
  - Proper user data retrieval with rank and level information
  - Enhanced security logging for administrative actions

## [0.5.4] - 2025-07-26

### Added
- **Frontend UI/UX**: New session-expired modal, global ErrorBoundary, and a modern Footer with dynamic version display.
- **Internationalization**: Expanded translations for dashboard, sidebar, error messages, and ranks; new utility for translating ranks.
- **Dashboard**: Detailed statistics, experience progress, account and ship info, quick actions, and improved layout.
- **Responsiveness**: Layout and style adjustments for smaller screens and core components (Home, Login, Register).
- **Backend User API Schema**: `UserResponse` schema now includes `experience`, `level`, and `rank` fields, providing the frontend with all user progression data.

### Changed
- **Navbar & Sidebar**: Unified Navbar, global language dropdown, Sidebar now receives user data and dynamic descriptions.
- **Layouts**: Refactored `GameLayout` and `PageLayout` components for better reuse and consistent visuals.
- **Contexts**: `AuthContext` now stores nickname and controls session-expired modal; `LanguageContext` persists language in localStorage.
- **Styles**: Global CSS and component styles improved for better visual experience and accessibility.

### Fixed
- **Authentication**: Fixed login/logout flow, session expiration handling, and automatic user state updates.
- **TypeScript Errors**: Adjusted types and interfaces to match backend and avoid TypeScript warnings.
- **Translations**: Fixed fallback logic and ensured dynamic text updates across all components.
- **Backend API Consistency**: Aligned backend user data and types with frontend requirements for seamless integration and type safety.

### Technical Improvements
- **Componentization**: New utilities for ranks and version, modularized translations, and improved code organization.
- **User Experience**: Enhanced visual feedback for errors, loading states, and quick actions.
- **Backend Authentication & Error Logging**: Improved JWT error logging in `auth_utils.py` for better debugging and security event tracking.

## [0.5.3] - 2025-07-22

### Fixed
- **Frontend Build Errors**: Resolved TypeScript compilation errors preventing deployment
  - Removed unused translation imports and variables from Battle, Market, Ships, and Users pages
  - Fixed `'t' is declared but its value is never read` TypeScript errors
  - All frontend pages now compile successfully without TypeScript warnings
- **Security Vulnerabilities**: Updated frontend dependencies to address security issues
  - Fixed critical severity vulnerability in form-data package (4.0.0 - 4.0.3)
  - Updated package-lock.json with secure dependency versions
  - Frontend now passes `npm audit` without critical vulnerabilities
- **Render Deployment**: Corrected build configuration for successful cloud deployment
  - Fixed Build Command from `npm build` to `npm run build` 
  - Added environment variables for production deployment
  - Enhanced package.json with `build-simple` script as fallback option

### Changed
- **Code Cleanup**: Removed unused internationalization imports in page components
  - Streamlined import statements for better tree-shaking
  - Removed unused `useLanguage` hook and translation objects
  - Cleaner component code without unnecessary dependencies
- **Deployment Configuration**: Added comprehensive deployment configuration
  - New `render.yaml` with proper build commands and environment variables
  - Production-ready configuration for Render cloud platform
  - Environment-specific API URL configuration for different deployment stages

### Technical Improvements
- **TypeScript Compliance**: All frontend code now passes TypeScript strict compilation
- **Build Optimization**: Faster build times with removed unused imports
- **Security Hardening**: Updated dependencies to latest secure versions
- **Cloud Deployment**: Ready for production deployment on Render platform

## [0.5.2] - 2025-07-21

### Added
- **Backend Configuration Module**: New dedicated configuration management for backend
  - Created `backend/app/config.py` for centralized backend configuration
  - Environment-based configuration with support for local, dev, and prod environments
  - JWT secret key validation and database URL management
- **Backend Database Module**: Separate database session management for backend
  - Created `backend/app/database.py` with backend-specific database configuration
  - Improved database health check with detailed status information
  - Enhanced session management and connection handling
- **Multi-Environment Support**: Enhanced environment configuration system
  - Frontend API configuration now supports multiple environments via `VITE_ENVIRONMENT`
  - Database configuration supports environment-specific URLs (`DATABASE_URL_LOCAL`, `DATABASE_URL_DEV`, `DATABASE_URL_PROD`)
  - Centralized environment variable management in database config

### Changed
- **Import Structure Refactoring**: Major cleanup of import paths throughout the application
  - Updated all CRUD modules to use `database.models` instead of `database` for model imports
  - All routes now import database session from `backend.app.database` instead of `database`
  - Authentication utilities updated to use backend configuration
  - Consistent import patterns across all backend modules
- **Configuration Architecture**: Improved separation of concerns
  - Database module configuration separated from backend configuration
  - Environment variables now loaded from appropriate locations
  - Removed redundant environment loading in database setup script
- **Health Check Enhancement**: Improved API health check endpoint
  - Health check now returns detailed database status information
  - Better error handling and status reporting
  - Enhanced debugging information for database connectivity
- **Frontend API Configuration**: Enhanced API URL management
  - Dynamic API base URL selection based on environment
  - Support for multiple deployment environments
  - Improved configuration flexibility for different stages

### Fixed
- **Import Resolution Issues**: Resolved all import conflicts and circular dependencies
  - Fixed database model imports across all CRUD operations
  - Corrected session dependency imports in all route modules
  - Resolved authentication utility import paths
- **Configuration Consistency**: Standardized configuration loading
  - Fixed environment variable loading in database and backend modules
  - Resolved configuration conflicts between modules
  - Ensured consistent environment handling across the application
- **Test Compatibility**: Updated test suite for new architecture
  - Fixed health check test to match new response format
  - Updated database engine imports in test modules
  - Ensured test compatibility with refactored import structure

### Technical Improvements
- **Modular Architecture**: Better separation between database and backend concerns
  - Database module handles pure data layer operations
  - Backend module manages API-specific configuration and sessions
  - Clear boundaries between different architectural layers
- **Environment Management**: Robust multi-environment support
  - Local development with automatic database initialization
  - Staging and production environment configuration
  - Flexible deployment options with environment-specific settings
- **Code Organization**: Improved maintainability and structure
  - Consistent import patterns and module organization
  - Better configuration management and validation
  - Enhanced error handling and debugging capabilities

## [0.5.1] - 2025-07-15

### Added
- **Constants Update**: Added `SELL_VALUE_MULTIPLIER` and `ELO_BASE_CHANGE` constants for ship sell value and Elo rating calculations.
- **Battle System Enhancements**: Integrated constants for damage calculation, XP gain, and Elo updates.
  - Damage now considers `SHIELD_DAMAGE_REDUCTION` and `DAMAGE_VARIATION_RANGE`.
  - XP gain uses `DIFFICULTY_MULTIPLIERS` for level-based scaling.
  - Elo updates leverage `ELO_BASE_CHANGE` and `ELO_EXPECTED_SCORE_DIVISOR`.
- **Market System Update**: Ship sell value now calculated using `SELL_VALUE_MULTIPLIER`.
- **Documentation Improvements**: Updated `README.md` to reflect the latest features and technical details.

### Fixed
- **Changelog Consistency**: Ensured all recent changes are properly documented.
- **Code Refactoring**: Replaced hardcoded values in `progression_utils.py` with constants from `constants.py` for better maintainability.

## [0.5.0] - 2025-07-13

### Added
- **Complete Work System**: Full soft recovery system for players who lose all ships and money
  - New `WorkLog` table to track all work activities and cooldowns
  - Rank-based work types: each rank has a specific job (maintenance, patrol, trading, escort, reconnaissance, command, strategy)
  - Progressive income system: higher ranks earn more credits (700-17500 range) with 20% variance
  - Rank-based cooldown system: balanced cooldowns from 2h (RECRUIT) to 12h (FLEET_ADMIRAL)
  - Work utility functions for income calculation, type management, and variance
  - Complete CRUD operations for work performance, status, and history with proper timezone handling
  - New API endpoints: `/work/perform`, `/work/status`, `/work/history`, `/work/types`
  - Comprehensive work schemas for request/response validation
  - Integrated logging system for all work activities
- **Enhanced Multi-Ship Battle System**: Advanced battle mechanics with formation strategies
  - Support for 1v1 to 20v20 battles with multiple ships per side
  - Formation strategies: DEFENSIVE, AGGRESSIVE, TACTICAL with auto-defaults
  - Enhanced `BattleRequest` schema supporting arrays of ship numbers and formations
  - Ship activation limits based on user rank (1-20 ships depending on rank)
  - New ship deactivation endpoint `/battle/deactivate-ship` with proper validation
  - Ship limits information endpoint `/battle/ship-limits` for UI integration
  - Enhanced battle logging with formation and multi-ship details
- **Extended User System**: Enhanced user capabilities and tactical features
  - Added `default_formation` field to User model for tactical preferences
  - Updated authentication system to return full User objects instead of limited UserObj
  - Enhanced user schemas with `UserShipLimitsResponse` for ship management
  - Improved rank-based ship activation limits with progression utils
  - Formation preferences integrated into NPC and user profiles
- **Enhanced RankBonus System**: Extended rank bonuses for multiple game mechanics
  - Added `work_income` field to RankBonus table for rank-based earnings (700-17500 range)
  - Added `work_cooldown_hours` field for rank-specific work intervals (2-12h)
  - Added `max_active_ships` field for rank-based ship activation limits (1-20)
  - Updated base data seeding with comprehensive work and combat configurations
  - Automatic seeding of work income, cooldown, and ship limit values for all ranks
- **Expanded NPC Fleet System**: Enhanced NPC ship assignments and diversity
  - NPCs now have multiple ships based on their rank (up to 20 ships for Fleet Admiral)
  - Rank-appropriate ship distributions across all tiers (Tier 1-6)
  - Enhanced NPC battle capabilities with formation preferences per character
  - Improved ship seeding with proper rank-based assignments and formations
  - Each NPC has a unique formation strategy (Admin: TACTICAL, Astro: AGGRESSIVE, etc.)
- **Enhanced Database Models and Lifecycle**: Improved data integrity and functionality
  - WorkLog model with comprehensive work tracking and timezone support
  - User model enhanced with default formation preferences
  - RankBonus model extended with work income, cooldown, and ship limits
  - Updated lifecycle.py to handle WorkLog table creation and cleanup
  - Improved clear_all_data function to include WorkLog entries
  - Enhanced models with proper constraints and indexes for new fields

### Changed
- **Authentication System**: Enhanced user authentication for work system
  - Updated `get_current_user` to return full User object instead of UserObj
  - Fixed timezone handling in datetime comparisons for work cooldowns
  - Improved error handling and user validation in work operations
- **Battle System Architecture**: Major refactoring for multi-ship battles
  - Updated battle routes to use `BattleRequest` schema instead of query parameters
  - Enhanced battle system to support formation strategies and multiple ships
  - Improved ship activation/deactivation system with proper limits validation
  - Enhanced error handling with detailed error messages across all routes
- **Database Schema**: Extended existing models for work functionality
  - RankBonus model now includes work-related and ship limit fields
  - User model now includes `default_formation` field for tactical preferences
  - Enhanced base data with comprehensive work system configuration
  - Updated lifecycle management to handle new work tables and constraints
- **Test Coverage**: Comprehensive testing for work and battle systems
  - Added 6 new tests covering all work system functionality
  - Updated battle tests to use new `BattleRequest` schema format
  - Tests for work status, types, performance, history, and cooldown validation
  - Enhanced test suite with work system and multi-ship battle integration tests
  - All tests now passing with full system coverage including new features
- **NPC System**: Enhanced NPC data and capabilities
  - NPCs now have formation preferences and multiple ships
  - Rank-appropriate ship distributions for realistic fleet compositions
  - Enhanced battle capabilities with formation strategies

### Fixed
- **Timezone Issues**: Resolved datetime comparison problems in work system
  - Fixed offset-naive vs offset-aware datetime comparison errors
  - Properly handled timezone conversion for cooldown calculations
  - Enhanced datetime handling across all work-related operations
- **Import Errors**: Fixed SQLAlchemy function imports in work CRUD
  - Added proper `func` import from SQLAlchemy for aggregation functions
  - Fixed work history calculation issues with income totals
  - Resolved work statistics calculation errors
- **Authentication Bugs**: Corrected user object handling in work routes
  - Fixed 'UserObj' has no attribute 'rank' error
  - Enhanced user authentication to provide complete user data
  - Improved work system integration with authentication layer
- **Error Message Improvements**: Enhanced error reporting across all endpoints
  - Updated exception handling to include specific error details
  - Improved error messages in battle, market, and ship routes
  - Better debugging information for failed operations

### Technical Details
- **Work Income Formula**: Rank-based income system with 20% variance for randomization
  - RECRUIT: 700 credits base, 2h cooldown
  - ENSIGN: 1000 credits base, 3h cooldown
  - LIEUTENANT: 1400 credits base, 3h cooldown
  - LIEUTENANT_COMMANDER: 1900 credits base, 4h cooldown
  - COMMANDER: 2600 credits base, 4h cooldown
  - CAPTAIN: 3500 credits base, 5h cooldown
  - COMMODORE: 4750 credits base, 6h cooldown
  - REAR_ADMIRAL: 6500 credits base, 7h cooldown
  - VICE_ADMIRAL: 8750 credits base, 8h cooldown
  - ADMIRAL: 12500 credits base, 10h cooldown
  - FLEET_ADMIRAL: 17500 credits base, 12h cooldown
- **Recovery System**: Designed to allow quick ship purchase for basic players
  - RECRUIT can buy cheapest ship (1500 credits) in approximately 2-3 work sessions
  - Higher ranks can recover faster with better income but longer cooldowns for balance
  - No currency or ship requirements - works as true "soft reset" system
- **Ship Activation Limits**: Progressive system based on rank
  - RECRUIT: 1 ship, ENSIGN: 2 ships, LIEUTENANT: 3 ships
  - LIEUTENANT_COMMANDER: 4 ships, COMMANDER: 5 ships, CAPTAIN: 6 ships
  - COMMODORE: 8 ships, REAR_ADMIRAL: 10 ships, VICE_ADMIRAL: 12 ships
  - ADMIRAL: 15 ships, FLEET_ADMIRAL: 20 ships maximum
- **Formation Strategies**: Three tactical approaches for battles
  - DEFENSIVE: Focus on shield and damage mitigation
  - AGGRESSIVE: Emphasis on attack power and first strike
  - TACTICAL: Balanced approach with strategic positioning
- **Database Integration**: Seamless integration with existing progression system
  - Work types align with military rank progression theme
  - Cooldowns and income scale appropriately with rank advancement
  - Full audit trail of all work activities for game balance monitoring

## [0.4.0] - 2025-07-12

### Added
- **Progression System**: Complete user progression system with experience, levels, and ranks
  - New `UserRank` enum with 11 ranks from Recruit to Fleet Admiral
  - User model now includes `experience`, `level`, and `rank` fields
  - Fibonacci-based level requirements for rank progression
  - New `RankBonus` table to store rank-based stat bonuses
  - Progression utilities in `backend/app/utils/progression_utils.py`
- **Enhanced Battle System**: Major improvements to battle mechanics
  - Rank bonuses now apply to ship stats during battles
  - NPC-specific handling in battles (NPCs don't lose money, ships auto-restore)
  - Experience and level-up system integrated into battle outcomes
  - Improved ELO system with NPC-specific handling
  - Dynamic XP gain based on opponent level difference
  - Automatic rank promotion checks after battles
- **Expanded Game Data**: Significantly enhanced ship and NPC variety
  - 30 ships organized in 6 tiers with 5 different strategies each
  - 11 NPCs with appropriate levels, ranks, and ship assignments
  - Hardcoded ship assignments based on user rank and level
  - Comprehensive rank bonus system for all stats
- **NPC Battle Mechanics**: Special handling for NPC opponents
  - NPCs don't lose or gain currency in battles
  - Human players lose money when defeated by NPCs but NPCs don't gain it
  - Human players gain money when defeating NPCs but NPCs don't lose it
  - NPC ships automatically restore to full condition after battles
  - Destroyed NPC ships are automatically repaired and reactivated
  - ELO changes only affect human players when fighting NPCs

### Changed
- **Battle Algorithm**: Completely overhauled battle system
  - Now uses rank-modified stats instead of base ship stats
  - Improved damage calculation with rank bonuses
  - Better battle logging with rank and level information
  - Enhanced ship degradation system (only affects human players)
- **Database Schema**: Updated user and ship data structure
  - Currency values changed from float to int for consistency
  - Default starting currency increased from 1500 to 2000 credits
  - Added experience, level, and rank tracking to users
  - Enhanced base data with proper level/rank distributions
- **Test Coverage**: Extended test suite to include NPC battles
  - New test for battle against NPC opponents
  - Verification of NPC-specific battle mechanics
  - Enhanced battle log analysis and validation
- **Data Seeding**: Improved database initialization
  - Rank bonuses are now seeded automatically
  - Hardcoded ship assignments based on user progression
  - Better NPC distribution across different ranks and levels

### Fixed
- **Schema Consistency**: Fixed currency type inconsistencies across all schema files
- **Battle Statistics**: Corrected ship destruction counting logic
- **GitHub Actions**: Updated release workflow to use specific action version
- **Database Setup**: Fixed missing file ending in `database/setup.py`

### Technical Details
- **Progression Formula**: Exponential XP growth (base 100, factor 1.5) with Fibonacci-like rank thresholds
- **Rank Bonuses**: Multiplicative bonuses from 0% (Recruit) to 60% (Fleet Admiral) for all ship stats
- **Battle Balance**: NPCs provide challenging opponents while maintaining game economy balance
  - NPCs neither gain nor lose currency to preserve economic stability
  - Human players face consequences (lose money) but NPCs don't accumulate wealth
- **Code Organization**: New utility modules for progression calculations and rank management

## [0.3.3] - 2025-07-12

### Added
- Shipyard system: endpoints, CRUD, schemas, and logs for ship repair with cooldown.
- New endpoint `/api/v1/shipyard/repair` for authenticated user ship repair.
- Models and table `ShipyardLog` to track shipyard usage.
- Automated tests for the full flow: buy, activate, battle, repair, and sell ships.
- Standardized Copilot instructions in `.github/instructions/copilot-instructions.md`.
- GitHub Actions workflow for automatic release based on the changelog.

### Changed
- Refactored market and battle endpoints to require JWT authentication.
- Route parameters updated to avoid exposing user_id directly (now uses authenticated user).
- Updated tests to reflect required authentication and new ship flow.

### Removed
- Duplicate Copilot instruction files from `backend/.github/` and `frontend/.github/`.

### Fixed
- Fixed authentication and authorization issues in market, battle, and shipyard endpoints.
- Adjusted logs and responses to correctly reflect the authenticated user and involved ship.

## [0.3.2] - 2025-07-09

### Changed
- **Database Backend**: Removed all fallback and support for SQLite. The backend now requires a PostgreSQL-compatible `DATABASE_URL` (e.g., Neon) and will raise an error if not set.
- **Environment Variables**: All database modules now require `DATABASE_URL` to be set via environment variables. `.env` loading is explicit and configurable via `ENV_FILE`.
- **Test Improvements**: The automated test suite now begins with a health check using the `/health` API endpoint, ensuring the FastAPI app and database are both accessible before running other tests. All test comments are now in English for consistency.
- **Code Cleanup**: Removed all references to `DATABASE_NAME` and SQLite logic from the codebase, including imports and error handling.

### Added
- **API Health Check Test**: Added a test to `test_routes.py` that validates the `/health` endpoint as the first test, ensuring the application and database are both running.

### Fixed
- **Import Errors**: Fixed import errors related to removed `DATABASE_NAME` and SQLite fallback logic.
- **Test Consistency**: Ensured all test comments and fixtures are in English and that the health check is always executed first.

## [0.3.1] - 2025-07-09

### Added
- **Modularized Schemas**: All Pydantic schemas are now organized into domain-specific modules under `backend/app/schemas/` (`user_schemas.py`, `ship_schemas.py`, `market_schemas.py`, `battle_schemas.py`, `log_schemas.py`, `owned_ship_schemas.py`).
- **Schema Documentation**: All schema files now include comprehensive English docstrings for improved API documentation.
- **Log CRUD Layer**: New `log_crud.py` file for log operations, fully integrated with the logging system.
- **Log Endpoints**: New `routes/logs.py` route file with endpoints to create, list, retrieve by ID, and delete logs (`/api/v1/logs`).
- **Test Coverage**: Automated tests in `test_routes.py` expanded to cover all log endpoints.

### Changed
- **Environment Variable Management**: Backend `.env` moved to `backend/.env` and a dedicated `.env` created in `database/.env`. All modules updated to load environment variables from the correct location.
- **Logging Refactor**: Logging utilities now use the CRUD layer for log creation, ensuring traceability and auditability.
- **Pydantic v2+ Compatibility**: Replaced `.dict()` with `.model_dump()` in all CRUD operations to avoid warnings and ensure compatibility.
- **Updated Imports**: All routes and CRUDs now import schemas from the new modular structure.

### Removed
- **Ship Endpoints**: Ship creation, update, and delete endpoints removed from the API routes as requested.

### Fixed
- **Test Coverage**: All automated tests pass and cover the new endpoints and refactored code.
- **Pydantic Warnings**: All Pydantic deprecation warnings resolved.

### Technical Details
- **Modular Structure**: Backend and database are now organized for easy extension and maintainability.
- **Documentation & Auditing**: Improved internal documentation and event traceability via CRUD-based logs.
- **Changelog Updated**: All changes are reflected in this version.

## [0.3.0] - 2025-07-02

### Added
- **Centralized Database Module**: Complete reorganization of database management
  - New `database/` module with clean imports and exports
  - Centralized configuration in `database/config.py`
  - Session management and dependency injection in `database/session.py`
  - All SQLAlchemy models consolidated in `database/models.py`
  - Initial data management in `database/base_data.py`
  - Database lifecycle management in `database/lifecycle.py`
  - Command-line setup script `database/setup.py` with full CRUD operations
  - Quick utility scripts in `database/scripts/` for common operations
- **Enhanced Database Management Tools**:
  - Database initialization with optional seeding
  - Database health checks with proper SQLAlchemy 2.0+ compatibility
  - Database reset and data clearing functionality
  - Comprehensive logging of all database operations
  - Environment variable support with fallback defaults
- **Improved Application Architecture**:
  - FastAPI application lifespan management for proper database cleanup
  - Health check endpoint (`/health`) for monitoring API and database status
  - Removed automatic database initialization from API startup (now managed separately)
  - Clean separation between API and database management concerns

### Changed
- **Database Import Structure**: All database-related imports now use clean `from database import ...` syntax
- **CRUD Layer Refactoring**: Updated all CRUD operations to use centralized database imports
- **Route Handler Updates**: All API routes now use centralized database session management
- **Application Startup**: Removed automatic database seeding from FastAPI startup (now manual)
- **Dependency Management**: Added `python-dotenv` to requirements for environment variable support

### Removed
- **Legacy Database Structure**: Removed old `backend/app/database/` module
- **Duplicate Database Code**: Eliminated redundant database configuration and model files
- **Seed Route**: Removed `/api/v1/seed` endpoints (now handled by command-line tools)
- **Automatic Database Initialization**: No longer automatically creates/seeds database on API startup

### Fixed
- **Database Health Check**: Fixed SQLAlchemy 2.0+ compatibility issue with `text()` wrapper for raw SQL
- **Environment Variable Loading**: Proper fallback handling when `python-dotenv` is not installed
- **Import Path Issues**: Resolved all import conflicts between old and new database modules
- **Session Management**: Improved database session lifecycle and cleanup

### Technical Details
- **Database Models**: All models now in `database/models.py` with comprehensive constraints and indexes
- **Base Data**: Centralized seed data in `database/base_data.py` with environment variable support
- **Command Line Tools**: 
  - `python database/setup.py init --seed` - Initialize with data
  - `python database/setup.py reset --seed` - Reset and seed
  - `python database/setup.py health` - Check database status
- **Clean Architecture**: Database module now provides clean, organized access to all components
- **Lifecycle Management**: Proper database initialization, health monitoring, and cleanup
- **Development Workflow**: Improved development experience with dedicated database management tools

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
  - Updated stats cards to show relevant game metrics: victories, currency, damage, and defeats
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