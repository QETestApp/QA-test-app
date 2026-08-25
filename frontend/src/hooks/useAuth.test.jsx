import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { AuthProvider, useAuth } from './useAuth';

function TestConsumer() {
  const { isAuthenticated } = useAuth();
  return <div>{isAuthenticated ? 'auth' : 'guest'}</div>;
}

describe('AuthProvider', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('does not crash when localStorage contains malformed auth data', () => {
    localStorage.setItem('user', '{invalid json');
    render(
      <MemoryRouter>
        <AuthProvider>
          <TestConsumer />
        </AuthProvider>
      </MemoryRouter>
    );

    expect(screen.getByText('guest')).toBeInTheDocument();
  });
});
