import { Component, type ReactNode } from 'react';
import translations from '../locales/translations';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: any;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error, errorInfo: null };
  }

  componentDidCatch(error: Error, errorInfo: any) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    this.setState({
      error,
      errorInfo
    });
  }

  render() {
    if (this.state.hasError) {
      // Get language from localStorage or default to 'pt-BR'
      const language = (localStorage.getItem('language') as 'pt-BR' | 'en-US') || 'pt-BR';
      const t = translations[language].error_boundary;
      
      return (
        <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center p-4">
          <div className="max-w-2xl w-full bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
            <div className="text-center mb-6">
              <div className="text-red-400 text-6xl mb-4">💥</div>
              <h1 className="text-2xl font-bold text-red-400 mb-2">{t.title}</h1>
              <p className="text-slate-400">{t.subtitle}</p>
            </div>
            
            <div className="bg-slate-900/50 rounded-lg p-4 mb-6">
              <h2 className="text-lg font-semibold text-white mb-2">{t.error_details}</h2>
              <pre className="text-sm text-red-300 whitespace-pre-wrap overflow-auto max-h-40">
                {this.state.error && this.state.error.toString()}
              </pre>
              
              {this.state.errorInfo && (
                <details className="mt-4">
                  <summary className="text-slate-400 cursor-pointer hover:text-white">
                    {t.show_stack_trace}
                  </summary>
                  <pre className="text-xs text-slate-500 mt-2 whitespace-pre-wrap overflow-auto max-h-60">
                    {this.state.errorInfo.componentStack}
                  </pre>
                </details>
              )}
            </div>
            
            <div className="flex gap-4 justify-center">
              <button 
                onClick={() => window.location.reload()} 
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
              >
                {t.reload_page}
              </button>
              <button 
                onClick={() => window.location.href = '/'} 
                className="bg-slate-600 hover:bg-slate-700 text-white px-6 py-2 rounded-lg transition-colors"
              >
                {t.go_home}
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
