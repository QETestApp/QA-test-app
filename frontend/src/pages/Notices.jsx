/**
 * Notices page — full CRUD.
 */

import { useState, useEffect, useCallback } from 'react';
import api from '../services/api';
import FormModal from '../components/FormModal';

const EMPTY_FORM = { title: '', description: '', created_by: '' };

export default function Notices() {
  const [notices, setNotices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [total, setTotal] = useState(0);

  const [showForm, setShowForm] = useState(false);
  const [showView, setShowView] = useState(false);
  const [editing, setEditing] = useState(null);
  const [viewing, setViewing] = useState(null);
  const [form, setForm] = useState(EMPTY_FORM);
  const [formError, setFormError] = useState(null);
  const [saving, setSaving] = useState(false);
  const [alert, setAlert] = useState(null);

  const fetchNotices = useCallback(async () => {
    setLoading(true);
    try {
      const params = { page, limit: 10 };
      if (search) params.title = search;
      const res = await api.get('/notices', { params });
      setNotices(res.data.data);
      setTotalPages(res.data.total_pages);
      setTotal(res.data.total);
    } catch (err) {
      console.error('Failed to fetch notices:', err);
    } finally {
      setLoading(false);
    }
  }, [page, search]);

  useEffect(() => { fetchNotices(); }, [fetchNotices]);

  const showAlertMsg = (message, type = 'success') => {
    setAlert({ message, type });
    setTimeout(() => setAlert(null), 3000);
  };

  const openCreate = () => { setEditing(null); setForm(EMPTY_FORM); setFormError(null); setShowForm(true); };

  const openEdit = (notice) => {
    setEditing(notice);
    setForm({
      title: notice.title || '',
      description: notice.description || '',
      created_by: notice.created_by || '',
    });
    setFormError(null);
    setShowForm(true);
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setFormError(null);
    try {
      const payload = { ...form, description: form.description || null, created_by: form.created_by || null };
      if (editing) {
        await api.put(`/notices/${editing.id}`, payload);
        showAlertMsg('Notice updated successfully');
      } else {
        await api.post('/notices', payload);
        showAlertMsg('Notice created successfully');
      }
      setShowForm(false);
      fetchNotices();
    } catch (err) {
      setFormError(err.response?.data?.message || 'Operation failed');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (notice) => {
    if (!window.confirm(`Delete notice "${notice.title}"?`)) return;
    try {
      await api.delete(`/notices/${notice.id}`);
      showAlertMsg('Notice deleted successfully');
      fetchNotices();
    } catch (err) {
      showAlertMsg(err.response?.data?.message || 'Delete failed', 'error');
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1>Notice Board</h1>
        <p>Manage notices and announcements — {total} total</p>
      </div>

      {alert && <div className={`alert alert-${alert.type}`}>{alert.type === 'success' ? '✅' : '⚠️'} {alert.message}</div>}

      <div className="table-container">
        <div className="table-toolbar">
          <div className="search-input">
            <span className="search-icon">🔍</span>
            <input type="text" placeholder="Search by title..." value={search} onChange={(e) => { setSearch(e.target.value); setPage(1); }} />
          </div>
          <button className="btn btn-primary" onClick={openCreate}>+ Add Notice</button>
        </div>

        {loading ? (
          <div className="loading-container"><div className="spinner" /><span>Loading notices...</span></div>
        ) : notices.length === 0 ? (
          <div className="empty-state"><div className="empty-icon">📢</div><p>No notices found</p></div>
        ) : (
          <>
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Title</th>
                  <th>Created By</th>
                  <th>Created At</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {notices.map((n) => (
                  <tr key={n.id}>
                    <td>{n.id}</td>
                    <td style={{ color: 'var(--text-primary)', fontWeight: 500, maxWidth: '300px' }}>{n.title}</td>
                    <td>{n.created_by || '—'}</td>
                    <td>{n.created_at ? new Date(n.created_at).toLocaleDateString() : '—'}</td>
                    <td>
                      <div className="table-actions">
                        <button className="btn-view" title="View" onClick={() => { setViewing(n); setShowView(true); }}>👁️</button>
                        <button className="btn-edit" title="Edit" onClick={() => openEdit(n)}>✏️</button>
                        <button className="btn-delete" title="Delete" onClick={() => handleDelete(n)}>🗑️</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div className="pagination">
              <div className="pagination-info">Page {page} of {totalPages} ({total} records)</div>
              <div className="pagination-controls">
                <button disabled={page <= 1} onClick={() => setPage(page - 1)}>← Prev</button>
                {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => {
                  const p = i + 1;
                  return <button key={p} className={p === page ? 'active' : ''} onClick={() => setPage(p)}>{p}</button>;
                })}
                <button disabled={page >= totalPages} onClick={() => setPage(page + 1)}>Next →</button>
              </div>
            </div>
          </>
        )}
      </div>

      <FormModal isOpen={showForm} onClose={() => setShowForm(false)} title={editing ? 'Edit Notice' : 'Add Notice'}
        footer={<><button className="btn btn-secondary" onClick={() => setShowForm(false)}>Cancel</button><button className="btn btn-primary" onClick={handleSave} disabled={saving}>{saving ? 'Saving...' : editing ? 'Update' : 'Create'}</button></>}>
        {formError && <div className="alert alert-error">⚠️ {formError}</div>}
        <form onSubmit={handleSave}>
          <div className="form-group"><label>Title *</label><input className="form-input" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required /></div>
          <div className="form-group"><label>Description</label><textarea className="form-input" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} rows={4} placeholder="Enter notice description..." /></div>
          <div className="form-group"><label>Created By</label><input className="form-input" value={form.created_by} onChange={(e) => setForm({ ...form, created_by: e.target.value })} placeholder="Author name (defaults to logged-in user)" /></div>
        </form>
      </FormModal>

      <FormModal isOpen={showView} onClose={() => setShowView(false)} title="Notice Details" footer={<button className="btn btn-secondary" onClick={() => setShowView(false)}>Close</button>}>
        {viewing && (
          <div className="detail-grid">
            <div className="detail-item"><div className="detail-label">ID</div><div className="detail-value">{viewing.id}</div></div>
            <div className="detail-item"><div className="detail-label">Created By</div><div className="detail-value">{viewing.created_by || '—'}</div></div>
            <div className="detail-item full-width"><div className="detail-label">Title</div><div className="detail-value">{viewing.title}</div></div>
            <div className="detail-item full-width"><div className="detail-label">Description</div><div className="detail-value" style={{ whiteSpace: 'pre-wrap' }}>{viewing.description || '—'}</div></div>
          </div>
        )}
      </FormModal>
    </div>
  );
}
