# 🎨 Bellum Astrum - Frontend Documentation

The frontend is a modern React-based web application providing an intuitive interface for the spaceship battle game. Built with TypeScript, Vite, and Tailwind CSS for optimal performance and user experience.

---

## 🛠️ Tech Stack

- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite for fast development and building
- **Styling**: Tailwind CSS v3 for modern, responsive design
- **HTTP Client**: Axios with automatic token injection
- **State Management**: React Context API for authentication and language
- **Routing**: React Router for single-page application navigation
- **Icons**: Unicode emoji and custom SVG icons
- **Internationalization**: Advanced translation system (PT-BR/EN-US)

---

## 🏗️ Project Structure

```
frontend/
├── .env                    # Environment variables (API URLs)
├── public/                 # Static assets
│   ├── flags/              # Language flag images
│   ├── logos/              # Application logos
│   └── index.html          # Main HTML template
├── src/                    # React source code
│   ├── components/         # Reusable React components
│   │   ├── common/         # Generic UI components
│   │   ├── layout/         # Layout components (Header, Footer, Sidebar)
│   │   └── ui/             # Specific UI elements
│   ├── contexts/           # React context providers
│   │   ├── AuthContext.tsx # Authentication state management
│   │   └── LanguageContext.tsx # Language/translation management
│   ├── hooks/              # Custom React hooks
│   │   ├── useAuth.ts      # Authentication hook
│   │   └── useUserData.ts  # User data fetching hook
│   ├── pages/              # Main application pages
│   │   ├── Auth/           # Authentication pages
│   │   ├── Battle.tsx      # Battle arena interface
│   │   ├── Dashboard.tsx   # User dashboard
│   │   ├── Market.tsx      # Ship marketplace
│   │   ├── Ships.tsx       # Fleet management
│   │   ├── Shipyard.tsx    # Ship repair interface
│   │   └── Work.tsx        # Work system interface
│   ├── utils/              # Utility functions
│   │   ├── api.ts          # API client configuration
│   │   ├── auth.ts         # Authentication utilities
│   │   └── translations.ts # Translation definitions
│   ├── App.tsx             # Main App component with routing
│   └── main.tsx           # Application entry point
├── package.json            # Dependencies and scripts
├── tailwind.config.ts      # Tailwind CSS configuration
├── tsconfig.json          # TypeScript configuration
└── vite.config.ts         # Vite build configuration
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites

- **Node.js**: Version 18+ required
- **npm**: Comes with Node.js
- **Backend**: Ensure backend server is running (see [backend/README.md](../backend/README.md))

### 2. Environment Configuration

Create `frontend/.env` with the following variables:

```env
# Environment (local, dev, prod)
VITE_ENVIRONMENT=local

# API Base URLs for different environments
VITE_API_BASE_URL_LOCAL=http://localhost:8000/api/v1
VITE_API_BASE_URL_DEV=https://your-dev-api.com/api/v1
VITE_API_BASE_URL_PROD=https://your-prod-api.com/api/v1
```

The application automatically uses the appropriate API URL based on the `VITE_ENVIRONMENT` variable.

### 3. Installation & Development

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at: **http://localhost:5173**

### 4. Build & Deployment

```bash
# Build for production
npm run build

# Preview production build locally
npm run preview

# Lint code
npm run lint
```

---

## 🎮 Application Features

### Authentication System
- **JWT-based Authentication**: Secure login with automatic token management
- **Registration/Login Forms**: User-friendly authentication interface
- **Protected Routes**: Automatic redirect for unauthenticated users
- **Token Persistence**: Login state maintained across sessions

### Game Interface Pages

#### **Dashboard**
Central hub showing user statistics and game overview:
- User profile information (nickname, level, rank, ELO)
- Battle statistics (wins, losses, damage dealt/taken)
- Ship information (active ships, total owned)
- Quick access to all game features

#### **Battle Arena**
Strategic combat interface:
- **Mode Selection**: NPC vs PvP battle modes
- **Opponent Selection**: Visual opponent cards with stats
- **Battle Execution**: Real-time battle processing
- **Battle Results**: Detailed combat logs and statistics
- **Battle History**: Modal with comprehensive battle details

#### **Fleet Management (Ships)**
Complete ship management interface:
- **Ship Overview**: Current fleet status and statistics
- **Ship Details**: Individual ship stats (Attack, Shield, HP, Fire Rate, Evasion)
- **Stat Format**: "Current / Base" values with rank bonuses applied
- **Rank Bonuses**: Dynamic display of user's rank-based stat bonuses
- **Ship Activation**: Battle formation management

#### **Marketplace**
Ship trading and acquisition:
- **Ship Gallery**: Visual grid of available ships with stats
- **Purchase System**: One-click buying with credit validation
- **Ship Icons**: Dynamic icons based on ship names
- **Real-time Updates**: Currency updates after transactions
- **Loading States**: User feedback during API operations

#### **Shipyard**
Ship repair and maintenance:
- **Repair Interface**: Fix damaged ships to restore full stats
- **Cooldown System**: 60-second repair cooldowns per ship
- **Status Display**: Real-time cooldown timers
- **Repair History**: Track maintenance activities

#### **Work System**
Economic recovery mechanism:
- **Work Interface**: Rank-based job system for earning credits
- **Cooldown Timer**: Real-time countdown display
- **Work History**: Statistics and earnings tracking
- **Progressive Income**: Different pay rates based on military rank

### UI/UX Features

#### **Responsive Design**
- **Mobile-First**: Optimized for all screen sizes
- **Grid Layouts**: Adaptive layouts using CSS Grid and Flexbox
- **Touch-Friendly**: Large click targets for mobile devices

#### **Modern Styling**
- **Tailwind CSS**: Utility-first styling for consistent design
- **Dark Theme**: Space-themed dark interface
- **Hover Effects**: Interactive element feedback
- **Loading States**: Skeleton loading and spinners

#### **Internationalization**
Complete multi-language support:
- **Languages**: Portuguese (PT-BR) and English (EN-US)
- **Advanced Translation System**: Nested keys and parameter interpolation
- **Language Switcher**: Easy language switching with flag indicators
- **Context-Aware**: Translations adapt to game context

---

## 🔧 Development Guidelines

### Component Structure
```typescript
// Example component structure
interface ComponentProps {
  // Define prop types
}

const Component: React.FC<ComponentProps> = ({ props }) => {
  // Component logic
  return (
    <div className="tailwind-classes">
      {/* Component JSX */}
    </div>
  );
};

export default Component;
```

### API Integration
```typescript
// API client usage
import { api } from '../utils/api';

const fetchData = async () => {
  try {
    const response = await api.get('/endpoint');
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};
```

### Translation Usage
```typescript
// Using translations
import { useLanguage } from '../contexts/LanguageContext';

const Component = () => {
  const { t } = useLanguage();
  
  return <h1>{t('page.title')}</h1>;
};
```

### Authentication
```typescript
// Using authentication
import { useAuth } from '../hooks/useAuth';

const Component = () => {
  const { user, login, logout, isAuthenticated } = useAuth();
  
  if (!isAuthenticated) {
    return <LoginForm />;
  }
  
  return <AuthenticatedContent />;
};
```

---

## 🌍 Internationalization System

### Translation Structure
```typescript
// translations.ts structure
export const translations = {
  pt: {
    page: {
      title: 'Título da Página',
      subtitle: 'Subtítulo com {parameter}'
    }
  },
  en: {
    page: {
      title: 'Page Title',
      subtitle: 'Subtitle with {parameter}'
    }
  }
};
```

### Translation Features
- **Nested Keys**: Organized translation hierarchy
- **Parameter Interpolation**: Dynamic text replacement
- **Fallbacks**: Graceful handling of missing translations
- **Context API**: Global translation state management

---

## 📱 Responsive Design

### Breakpoints (Tailwind CSS)
- **sm**: 640px and up (tablets)
- **md**: 768px and up (small laptops)
- **lg**: 1024px and up (laptops)
- **xl**: 1280px and up (desktops)
- **2xl**: 1536px and up (large screens)

### Mobile Optimizations
- **Touch Targets**: Minimum 44px touch targets
- **Readable Text**: Appropriate font sizes and line heights
- **Navigation**: Mobile-friendly menu systems
- **Performance**: Optimized images and lazy loading

---

## 🔌 API Integration

### HTTP Client Configuration
```typescript
// API client setup with authentication
const api = axios.create({
  baseURL: getApiBaseUrl(),
  headers: {
    'Content-Type': 'application/json',
  },
});

// Automatic token injection
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### Error Handling
- **Global Error Interceptors**: Centralized error handling
- **Loading States**: User feedback during API calls
- **Retry Logic**: Automatic retry for transient failures
- **Offline Support**: Graceful degradation when offline

---

## 🧪 Testing & Quality

### Code Quality
- **ESLint**: Code linting and style enforcement
- **TypeScript**: Static type checking
- **Prettier**: Code formatting (configured via ESLint)

### Development Tools
```bash
# Lint code
npm run lint

# Type checking
npx tsc --noEmit

# Build analysis
npm run build -- --analyze
```

---

## 🚀 Performance Optimization

### Build Optimization
- **Vite**: Fast build tool with Hot Module Replacement (HMR)
- **Tree Shaking**: Removes unused code
- **Code Splitting**: Automatic route-based splitting
- **Asset Optimization**: Optimized images and static assets

### Runtime Performance
- **React 19**: Latest React features and optimizations
- **Lazy Loading**: Route-based component loading
- **Memoization**: React.memo and useMemo for expensive operations
- **Efficient Rendering**: Optimized re-render patterns

---

## 🔒 Security Considerations

### Authentication Security
- **JWT Tokens**: Secure token storage and management
- **Route Protection**: Authenticated route guards
- **Token Expiration**: Automatic token refresh handling
- **HTTPS**: Secure communication with backend

### Data Protection
- **Input Validation**: Client-side validation with backend verification
- **XSS Prevention**: React's built-in XSS protection
- **CSRF Protection**: Token-based request validation

---

## 📚 Additional Resources

### Documentation
- **React Documentation**: https://react.dev/
- **TypeScript Handbook**: https://www.typescriptlang.org/docs/
- **Vite Guide**: https://vitejs.dev/guide/
- **Tailwind CSS**: https://tailwindcss.com/docs

### Development Tools
- **React DevTools**: Browser extension for debugging
- **Redux DevTools**: State inspection (if using Redux)
- **Vite DevTools**: Build and performance analysis

---

## 🤝 Contributing

When contributing to the frontend:

1. **Component Standards**: Follow React best practices and TypeScript conventions
2. **Styling Guidelines**: Use Tailwind CSS utility classes consistently
3. **Accessibility**: Ensure WCAG compliance for all interactive elements
4. **Translation Support**: Add translations for new text content
5. **Responsive Design**: Test on multiple screen sizes
6. **Performance**: Consider bundle size impact of new dependencies

---

## 🔗 Navigation

- **← [Project Overview](../README.md)** - Main project documentation and overview
- **⚙️ [Backend Documentation](../backend/README.md)** - FastAPI backend and API endpoints
- **🗄️ [Database Documentation](../database/README.md)** - Database schema, models, and setup

---
