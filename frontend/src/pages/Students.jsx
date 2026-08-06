/**
 * Students page — full CRUD with search, pagination, view/add/edit/delete modals.
 */

import { useState, useEffect, useCallback } from 'react';
import { ENDPOINTS } from '../config/api';
import api from '../services/api';
import FormModal from '../components/FormModal';

const EMPTY_FORM = {
  name: '',
  email: '',
  phone: '',
  course: '',
  semester: '',
  date_of_birth: '',
  address: '',
};

export default function Students() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [total, setTotal] = useState(0);

  // Modal states
  const [showForm, setShowForm] = useState(false);
  const [showView, setShowView] = useState(false);
  const [editing, setEditing] = useState(null);
  const [viewing, setViewing] = useState(null);
  const [form, setForm] = useState(EMPTY_FORM);
  const [formError, setFormError] = useState(null);
  const [saving, setSaving] = useState(false);
  const [alert, setAlert] = useState(null);

  const fetchStudents = useCallback(async () => {
    setLoading(true);
    try {
      const params = { page, limit: 10 };
      if (search) params.name = search;
      const res = await api.get(ENDPOINTS.STUDENTS, { params });
      setStudents(res.data.data);
      setTotalPages(res.data.total_pages);
      setTotal(res.data.total);
    } catch (err) {
      console.error('Failed to fetch students:', err);
    } finally {
      setLoading(false);
    }
  }, [page, search]);

  useEffect(() => {
    fetchStudents();
  }, [fetchStudents]);

  const showAlert = (message, type = 'success') => {
    setAlert({ message, type });
    setTimeout(() => setAlert(null), 3000);
  };

  const openCreate = () => {
    setEditing(null);
    setForm(EMPTY_FORM);
    setFormError(null);
    setShowForm(true);
  };

  const openEdit = (student) => {
    setEditing(student);
    setForm({
      name: student.name || '',
      email: student.email || '',
      phone: student.phone || '',
      course: student.course || '',
      semester: student.semester || '',
      date_of_birth: student.date_of_birth || '',
      address: student.address || '',
    });
    setFormError(null);
    setShowForm(true);
  };

  const openView = (student) => {
    setViewing(student);
    setShowView(true);
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setFormError(null);
    try {
      const payload = {
        ...form,
        semester: form.semester ? parseInt(form.semester) : null,
        date_of_birth: form.date_of_birth || null,
        phone: form.phone || null,
        course: form.course || null,
        address: form.address || null,
      };

      if (editing) {
        await api.put(`${ENDPOINTS.STUDENTS}/${editing.id}`, payload);
        showAlert('Student updated successfully');
      } else {
        await api.post(ENDPOINTS.STUDENTS, payload);
        showAlert('Student created successfully');
      }
      setShowForm(false);
      fetchStudents();
    } catch (err) {
      const data = err.response?.data;
      setFormError(data?.message || 'Operation failed');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (student) => {
    if (!window.confirm(`Delete student "${student.name}"?`)) return;
    try {
      await api.delete(`${ENDPOINTS.STUDENTS}/${student.id}`);
      showAlert('Student deleted successfully');
      fetchStudents();
    } catch (err) {
      showAlert(err.response?.data?.message || 'Delete failed', 'error');
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1>Students</h1>
        <p>Manage student records — {total} total</p>
      </div>

      {alert && (
        <div className={`alert alert-${alert.type}`}>
          {alert.type === 'success' ? '✅' : '⚠️'} {alert.message}
        </div>
      )}

      <div className="table-container">
        <div className="table-toolbar">
          <div className="search-input">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              placeholder="Search by name..."
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(1); }}
            />
          </div>
          <button className="btn btn-primary" onClick={openCreate}>
            + Add Student
          </button>
        </div>

        {loading ? (
          <div className="loading-container">
            <div className="spinner" />
            <span>Loading students...</span>
          </div>
        ) : students.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🎓</div>
            <p>No students found</p>
          </div>
        ) : (
          <>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Student ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Phone</th>
                  <th>Course</th>
                  <th>Semester</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {students.map((s) => (
                  <tr key={s.id}>
                    <td>{s.student_id}</td>
                    <td style={{ color: 'var(--text-primary)', fontWeight: 500 }}>{s.name}</td>
                    <td>{s.email}</td>
                    <td>{s.phone || '—'}</td>
                    <td>{s.course || '—'}</td>
                    <td>{s.semester || '—'}</td>
                    <td>
                      <div className="table-actions">
                        <button className="btn-view" title="View" onClick={() => openView(s)}>👁️</button>
                        <button className="btn-edit" title="Edit" onClick={() => openEdit(s)}>✏️</button>
                        <button className="btn-delete" title="Delete" onClick={() => handleDelete(s)}>🗑️</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="pagination">
              <div className="pagination-info">
                Page {page} of {totalPages} ({total} records)
              </div>
              <div className="pagination-controls">
                <button disabled={page <= 1} onClick={() => setPage(page - 1)}>← Prev</button>
                {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => {
                  const p = i + 1;
                  return (
                    <button key={p} className={p === page ? 'active' : ''} onClick={() => setPage(p)}>
                      {p}
                    </button>
                  );
                })}
                <button disabled={page >= totalPages} onClick={() => setPage(page + 1)}>Next →</button>
              </div>
            </div>
          </>
        )}
      </div>

      {/* Create / Edit Modal */}
      <FormModal
        isOpen={showForm}
        onClose={() => setShowForm(false)}
        title={editing ? 'Edit Student' : 'Add Student'}
        footer={
          <>
            <button className="btn btn-secondary" onClick={() => setShowForm(false)}>Cancel</button>
            <button className="btn btn-primary" onClick={handleSave} disabled={saving}>
              {saving ? 'Saving...' : editing ? 'Update' : 'Create'}
            </button>
          </>
        }
      >
        {formError && <div className="alert alert-error">⚠️ {formError}</div>}
        <form onSubmit={handleSave}>
          <div className="form-group">
            <label>Name *</label>
            <input className="form-input" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
          </div>
          <div className="form-group">
            <label>Email *</label>
            <input className="form-input" type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          </div>
          <div className="form-group">
            <label>Phone</label>
            <input className="form-input" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} placeholder="+1-555-0101" />
          </div>
          <div className="form-group">
            <label>Course</label>
            <input className="form-input" value={form.course} onChange={(e) => setForm({ ...form, course: e.target.value })} placeholder="CSE, EE, ME..." />
          </div>
          <div className="form-group">
            <label>Semester</label>
            <input className="form-input" type="number" min="1" max="12" value={form.semester} onChange={(e) => setForm({ ...form, semester: e.target.value })} />
          </div>
          <div className="form-group">
            <label>Date of Birth</label>
            <input className="form-input" type="date" value={form.date_of_birth} onChange={(e) => setForm({ ...form, date_of_birth: e.target.value })} />
          </div>
          <div className="form-group">
            <label>Address</label>
            <textarea className="form-input" value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} rows={2} />
          </div>
        </form>
      </FormModal>

      {/* View Modal */}
      <FormModal
        isOpen={showView}
        onClose={() => setShowView(false)}
        title="Student Details"
        footer={<button className="btn btn-secondary" onClick={() => setShowView(false)}>Close</button>}
      >
        {viewing && (
          <div className="detail-grid">
            <div className="detail-item"><div className="detail-label">Student ID</div><div className="detail-value">{viewing.student_id}</div></div>
            <div className="detail-item"><div className="detail-label">Name</div><div className="detail-value">{viewing.name}</div></div>
            <div className="detail-item"><div className="detail-label">Email</div><div className="detail-value">{viewing.email}</div></div>
            <div className="detail-item"><div className="detail-label">Phone</div><div className="detail-value">{viewing.phone || '—'}</div></div>
            <div className="detail-item"><div className="detail-label">Course</div><div className="detail-value">{viewing.course || '—'}</div></div>
            <div className="detail-item"><div className="detail-label">Semester</div><div className="detail-value">{viewing.semester || '—'}</div></div>
            <div className="detail-item"><div className="detail-label">Date of Birth</div><div className="detail-value">{viewing.date_of_birth || '—'}</div></div>
            <div className="detail-item full-width"><div className="detail-label">Address</div><div className="detail-value">{viewing.address || '—'}</div></div>
          </div>
        )}
      </FormModal>
    </div>
  );
}
