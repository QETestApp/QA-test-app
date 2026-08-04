/**
 * DashboardCard — clickable module card for the dashboard.
 */

export default function DashboardCard({ title, count, description, icon, iconClass, onClick }) {
  return (
    <div className="dashboard-card" onClick={onClick} role="button" tabIndex={0}>
      <div className={`card-icon ${iconClass || ''}`}>{icon}</div>
      <div className="card-count">{count}</div>
      <h3>{title}</h3>
      <p className="card-desc">{description}</p>
    </div>
  );
}
