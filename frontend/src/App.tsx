import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Users from './pages/Users';
import Ships from './pages/Ships';
import Market from './pages/Market';
import Battle from './pages/Battle';
import Register from './pages/Register';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import { AuthProvider } from './contexts/AuthContext';
import { SidebarProvider } from './contexts/SidebarContext';
import PrivateRoute from './components/PrivateRoute';
import './App.css';

function AppContent() {
  const location = useLocation();
  
  // Routes that use the sidebar layout (game pages)
  const sidebarRoutes = ['/dashboard', '/users', '/ships', '/market', '/battle'];
  const useSidebar = sidebarRoutes.includes(location.pathname);

  return (
    <>
      {!useSidebar && <Navbar />}
      <div className={useSidebar ? "text-slate-50" : "max-w-4xl mx-auto pt-20 text-slate-50"}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<Navigate to="/" replace />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          } />
          <Route path="/users" element={<Users />} />
          <Route path="/ships" element={<Ships />} />
          <Route path="/market" element={<Market />} />
          <Route path="/battle" element={<Battle />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </>
  );
}

function App() {
  return (
    <AuthProvider>
      <SidebarProvider>
        <Router>
          <AppContent />
        </Router>
      </SidebarProvider>
    </AuthProvider>
  );
}

export default App;
