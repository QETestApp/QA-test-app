/**
 * Sidebar navigation component.
 */

import { NavLink } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { ROUTES } from '../utils/constants';

const navItems = [
  { path: ROUTES.DASHBOARD, label: 'Dashboard', icon: '📊' },
  { path: ROUTES.STUDENTS, label: 'Students', icon: '🎓' },
  { path: ROUTES.COURSES, label: 'Courses', icon: '📚' },
  { path: ROUTES.ATTENDANCE, label: 'Attendance', icon: '📋' },
  { path: ROUTES.NOTICES, label: 'Notices', icon: '📢' },
];

export default function Sidebar() {
  const { user, logout } = useAuth();

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-brand">
          <div className="brand-icon">🧪</div>
          <div>
            <div className="brand-text">QA Playground</div>
            <div className="brand-sub">Test Environment</div>
          </div>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section">
          <div className="nav-section-title">Navigation</div>
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              className={({ isActive }) =>
                `nav-link${isActive ? ' active' : ''}`
              }
            >
              <span className="nav-icon">{item.icon}</span>
              <span>{item.label}</span>
            </NavLink>
          ))}
        </div>
      </nav>

      <div className="sidebar-footer">
        <div style={{ padding: '8px 12px', marginBottom: '8px' }}>
          <div style={{ fontSize: '0.8125rem', fontWeight: 600, color: 'var(--text-primary)' }}>
            {user?.name}
          </div>
          <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)' }}>
            {user?.email}
          </div>
        </div>
        <button className="logout-btn" onClick={logout}>
          <span className="nav-icon">🚪</span>
          <span>Logout</span>
        </button>
      </div>
    </aside>
  );
}
