/**
 * Courses page — full CRUD.
 */

import { useState, useEffect, useCallback } from 'react';
import { ENDPOINTS } from '../config/api';
import api from '../services/api';
import FormModal from '../components/FormModal';

const EMPTY_FORM = { course_name: '', course_code: '', duration: '', faculty: '' };

export default function Courses() {
  const [courses, setCourses] = useState([]);
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

  const fetchCourses = useCallback(async () => {
    setLoading(true);
    try {
      const params = { page, limit: 10 };
      if (search) params.course_name = search;
      const res = await api.get(ENDPOINTS.COURSES, { params });
      setCourses(res.data.data);
      setTotalPages(res.data.total_pages);
      setTotal(res.data.total);
    } catch (err) {
      console.error('Failed to fetch courses:', err);
    } finally {
      setLoading(false);
    }
  }, [page, search]);

  useEffect(() => { fetchCourses(); }, [fetchCourses]);

  const showAlertMsg = (message, type = 'success') => {
    setAlert({ message, type });
    setTimeout(() => setAlert(null), 3000);
  };

  const openCreate = () => { setEditing(null); setForm(EMPTY_FORM); setFormError(null); setShowForm(true); };

  const openEdit = (course) => {
    setEditing(course);
    setForm({
      course_name: course.course_name || '',
      course_code: course.course_code || '',
      duration: course.duration || '',
      faculty: course.faculty || '',
    });
    setFormError(null);
    setShowForm(true);
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setFormError(null);
    try {
      const payload = { ...form, duration: form.duration || null, faculty: form.faculty || null };
      if (editing) {
        await api.put(`${ENDPOINTS.COURSES}/${editing.id}`, payload);
        showAlertMsg('Course updated successfully');
      } else {
        await api.post(ENDPOINTS.COURSES, payload);
        showAlertMsg('Course created successfully');
      }
      setShowForm(false);
      fetchCourses();
    } catch (err) {
      setFormError(err.response?.data?.message || 'Operation failed');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (course) => {
    if (!window.confirm(`Delete course "${course.course_name}"?`)) return;
    try {
      await api.delete(`${ENDPOINTS.COURSES}/${course.id}`);
      showAlertMsg('Course deleted successfully');
      fetchCourses();
    } catch (err) {
      showAlertMsg(err.response?.data?.message || 'Delete failed', 'error');
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1>Courses</h1>
        <p>Manage course catalog — {total} total</p>
      </div>

      {alert && <div className={`alert alert-${alert.type}`}>{alert.type === 'success' ? '✅' : '⚠️'} {alert.message}</div>}

      <div className="table-container">
        <div className="table-toolbar">
          <div className="search-input">
            <span className="search-icon">🔍</span>
            <input type="text" placeholder="Search by course name..." value={search} onChange={(e) => { setSearch(e.target.value); setPage(1); }} />
          </div>
          <button className="btn btn-primary" onClick={openCreate}>+ Add Course</button>
        </div>

        {loading ? (
          <div className="loading-container"><div className="spinner" /><span>Loading courses...</span></div>
        ) : courses.length === 0 ? (
          <div className="empty-state"><div className="empty-icon">📚</div><p>No courses found</p></div>
        ) : (
          <>
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Course Name</th>
                  <th>Course Code</th>
                  <th>Duration</th>
                  <th>Faculty</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {courses.map((c) => (
                  <tr key={c.id}>
                    <td>{c.id}</td>
                    <td style={{ color: 'var(--text-primary)', fontWeight: 500 }}>{c.course_name}</td>
                    <td><span className="badge" style={{ background: 'rgba(99,102,241,0.1)', color: 'var(--accent-primary)' }}>{c.course_code}</span></td>
                    <td>{c.duration || '—'}</td>
                    <td>{c.faculty || '—'}</td>
                    <td>
                      <div className="table-actions">
                        <button className="btn-view" title="View" onClick={() => { setViewing(c); setShowView(true); }}>👁️</button>
                        <button className="btn-edit" title="Edit" onClick={() => openEdit(c)}>✏️</button>
                        <button className="btn-delete" title="Delete" onClick={() => handleDelete(c)}>🗑️</button>
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

      <FormModal isOpen={showForm} onClose={() => setShowForm(false)} title={editing ? 'Edit Course' : 'Add Course'}
        footer={<><button className="btn btn-secondary" onClick={() => setShowForm(false)}>Cancel</button><button className="btn btn-primary" onClick={handleSave} disabled={saving}>{saving ? 'Saving...' : editing ? 'Update' : 'Create'}</button></>}>
        {formError && <div className="alert alert-error">⚠️ {formError}</div>}
        <form onSubmit={handleSave}>
          <div className="form-group"><label>Course Name *</label><input className="form-input" value={form.course_name} onChange={(e) => setForm({ ...form, course_name: e.target.value })} required /></div>
          <div className="form-group"><label>Course Code *</label><input className="form-input" value={form.course_code} onChange={(e) => setForm({ ...form, course_code: e.target.value })} required placeholder="CSE, EE, MBA..." /></div>
          <div className="form-group"><label>Duration</label><input className="form-input" value={form.duration} onChange={(e) => setForm({ ...form, duration: e.target.value })} placeholder="4 Years, 2 Years..." /></div>
          <div className="form-group"><label>Faculty</label><input className="form-input" value={form.faculty} onChange={(e) => setForm({ ...form, faculty: e.target.value })} placeholder="Dr. Name" /></div>
        </form>
      </FormModal>

      <FormModal isOpen={showView} onClose={() => setShowView(false)} title="Course Details" footer={<button className="btn btn-secondary" onClick={() => setShowView(false)}>Close</button>}>
        {viewing && (
          <div className="detail-grid">
            <div className="detail-item"><div className="detail-label">ID</div><div className="detail-value">{viewing.id}</div></div>
            <div className="detail-item"><div className="detail-label">Course Name</div><div className="detail-value">{viewing.course_name}</div></div>
            <div className="detail-item"><div className="detail-label">Course Code</div><div className="detail-value">{viewing.course_code}</div></div>
            <div className="detail-item"><div className="detail-label">Duration</div><div className="detail-value">{viewing.duration || '—'}</div></div>
            <div className="detail-item full-width"><div className="detail-label">Faculty</div><div className="detail-value">{viewing.faculty || '—'}</div></div>
          </div>
        )}
      </FormModal>
    </div>
  );
}
