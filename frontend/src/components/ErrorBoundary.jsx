import { Component } from 'react';

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('React error boundary caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '2rem', fontFamily: 'sans-serif', background: '#fff', color: '#333', minHeight: '100vh' }}>
          <h2>Something went wrong.</h2>
          <p>The app hit an unexpected render error. Please refresh the page.</p>
          <details style={{ marginTop: '1rem', fontSize: '0.85rem', color: '#666' }}>
            <summary>Error details (for debugging)</summary>
            <pre style={{ marginTop: '0.5rem', whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
              {this.state.error?.message}
              {'\n'}
              {this.state.error?.stack}
            </pre>
          </details>
        </div>
      );
    }

    return this.props.children;
  }
}
