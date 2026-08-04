/**
 * Attendance page — full CRUD.
 */

import { useState, useEffect, useCallback } from 'react';
import api from '../services/api';
import FormModal from '../components/FormModal';

const EMPTY_FORM = { student_id: '', date: '', status: 'Present' };

export default function Attendance() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState('');
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

  const fetchRecords = useCallback(async () => {
    setLoading(true);
    try {
      const params = { page, limit: 10 };
      if (filterStatus) params.status = filterStatus;
      const res = await api.get('/attendance', { params });
      setRecords(res.data.data);
      setTotalPages(res.data.total_pages);
      setTotal(res.data.total);
    } catch (err) {
      console.error('Failed to fetch attendance:', err);
    } finally {
      setLoading(false);
    }
  }, [page, filterStatus]);

  useEffect(() => { fetchRecords(); }, [fetchRecords]);

  const showAlertMsg = (message, type = 'success') => {
    setAlert({ message, type });
    setTimeout(() => setAlert(null), 3000);
  };

  const openCreate = () => { setEditing(null); setForm(EMPTY_FORM); setFormError(null); setShowForm(true); };

  const openEdit = (record) => {
    setEditing(record);
    setForm({
      student_id: record.student_id || '',
      date: record.date || '',
      status: record.status || 'Present',
    });
    setFormError(null);
    setShowForm(true);
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setFormError(null);
    try {
      const payload = { ...form, student_id: parseInt(form.student_id) };
      if (editing) {
        await api.put(`/attendance/${editing.id}`, payload);
        showAlertMsg('Attendance updated successfully');
      } else {
        await api.post('/attendance', payload);
        showAlertMsg('Attendance recorded successfully');
      }
      setShowForm(false);
      fetchRecords();
    } catch (err) {
      setFormError(err.response?.data?.message || 'Operation failed');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (record) => {
    if (!window.confirm('Delete this attendance record?')) return;
    try {
      await api.delete(`/attendance/${record.id}`);
      showAlertMsg('Attendance record deleted');
      fetchRecords();
    } catch (err) {
      showAlertMsg(err.response?.data?.message || 'Delete failed', 'error');
    }
  };

  const getStatusBadge = (status) => {
    const cls = status === 'Present' ? 'badge-present' : status === 'Absent' ? 'badge-absent' : 'badge-late';
    return <span className={`badge ${cls}`}>{status}</span>;
  };

  return (
    <div>
      <div className="page-header">
        <h1>Attendance</h1>
        <p>Track student attendance — {total} records</p>
      </div>

      {alert && <div className={`alert alert-${alert.type}`}>{alert.type === 'success' ? '✅' : '⚠️'} {alert.message}</div>}

      <div className="table-container">
        <div className="table-toolbar">
          <div style={{ display: 'flex', gap: '12px', alignItems: 'center', flex: 1 }}>
            <select className="form-select" style={{ width: 'auto', minWidth: '140px' }} value={filterStatus} onChange={(e) => { setFilterStatus(e.target.value); setPage(1); }}>
              <option value="">All Status</option>
              <option value="Present">Present</option>
              <option value="Absent">Absent</option>
              <option value="Late">Late</option>
            </select>
          </div>
          <button className="btn btn-primary" onClick={openCreate}>+ Record Attendance</button>
        </div>

        {loading ? (
          <div className="loading-container"><div className="spinner" /><span>Loading attendance...</span></div>
        ) : records.length === 0 ? (
          <div className="empty-state"><div className="empty-icon">📋</div><p>No attendance records found</p></div>
        ) : (
          <>
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Student ID</th>
                  <th>Date</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {records.map((r) => (
                  <tr key={r.id}>
                    <td>{r.id}</td>
                    <td>{r.student_id}</td>
                    <td>{r.date}</td>
                    <td>{getStatusBadge(r.status)}</td>
                    <td>
                      <div className="table-actions">
                        <button className="btn-view" title="View" onClick={() => { setViewing(r); setShowView(true); }}>👁️</button>
                        <button className="btn-edit" title="Edit" onClick={() => openEdit(r)}>✏️</button>
                        <button className="btn-delete" title="Delete" onClick={() => handleDelete(r)}>🗑️</button>
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

      <FormModal isOpen={showForm} onClose={() => setShowForm(false)} title={editing ? 'Edit Attendance' : 'Record Attendance'}
        footer={<><button className="btn btn-secondary" onClick={() => setShowForm(false)}>Cancel</button><button className="btn btn-primary" onClick={handleSave} disabled={saving}>{saving ? 'Saving...' : editing ? 'Update' : 'Record'}</button></>}>
        {formError && <div className="alert alert-error">⚠️ {formError}</div>}
        <form onSubmit={handleSave}>
          <div className="form-group"><label>Student ID *</label><input className="form-input" type="number" min="1" value={form.student_id} onChange={(e) => setForm({ ...form, student_id: e.target.value })} required placeholder="Enter student database ID (1, 2, 3...)" /></div>
          <div className="form-group"><label>Date *</label><input className="form-input" type="date" value={form.date} onChange={(e) => setForm({ ...form, date: e.target.value })} required /></div>
          <div className="form-group">
            <label>Status *</label>
            <select className="form-select" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
              <option value="Present">Present</option>
              <option value="Absent">Absent</option>
              <option value="Late">Late</option>
            </select>
          </div>
        </form>
      </FormModal>

      <FormModal isOpen={showView} onClose={() => setShowView(false)} title="Attendance Details" footer={<button className="btn btn-secondary" onClick={() => setShowView(false)}>Close</button>}>
        {viewing && (
          <div className="detail-grid">
            <div className="detail-item"><div className="detail-label">Record ID</div><div className="detail-value">{viewing.id}</div></div>
            <div className="detail-item"><div className="detail-label">Student ID</div><div className="detail-value">{viewing.student_id}</div></div>
            <div className="detail-item"><div className="detail-label">Date</div><div className="detail-value">{viewing.date}</div></div>
            <div className="detail-item"><div className="detail-label">Status</div><div className="detail-value">{getStatusBadge(viewing.status)}</div></div>
          </div>
        )}
      </FormModal>
    </div>
  );
}
