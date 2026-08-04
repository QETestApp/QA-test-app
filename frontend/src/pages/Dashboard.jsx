/**
 * Dashboard page with module cards showing counts.
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import DashboardCard from '../components/DashboardCard';
import { ROUTES } from '../utils/constants';

export default function Dashboard() {
  const navigate = useNavigate();
  const [counts, setCounts] = useState({
    students: 0,
    courses: 0,
    attendance: 0,
    notices: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCounts = async () => {
      try {
        const [students, courses, attendance, notices] = await Promise.all([
          api.get('/students?limit=1'),
          api.get('/courses?limit=1'),
          api.get('/attendance?limit=1'),
          api.get('/notices?limit=1'),
        ]);
        setCounts({
          students: students.data.total || 0,
          courses: courses.data.total || 0,
          attendance: attendance.data.total || 0,
          notices: notices.data.total || 0,
        });
      } catch (err) {
        console.error('Failed to fetch counts:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchCounts();
  }, []);

  const cards = [
    {
      title: 'Student Management',
      count: counts.students,
      description: 'Manage student records, search, and CRUD operations',
      icon: '🎓',
      iconClass: 'students',
      route: ROUTES.STUDENTS,
    },
    {
      title: 'Course Management',
      count: counts.courses,
      description: 'Manage courses, codes, duration, and faculty',
      icon: '📚',
      iconClass: 'courses',
      route: ROUTES.COURSES,
    },
    {
      title: 'Attendance',
      count: counts.attendance,
      description: 'Track student attendance: Present, Absent, Late',
      icon: '📋',
      iconClass: 'attendance',
      route: ROUTES.ATTENDANCE,
    },
    {
      title: 'Notice Board',
      count: counts.notices,
      description: 'Post and manage notices and announcements',
      icon: '📢',
      iconClass: 'notices',
      route: ROUTES.NOTICES,
    },
  ];

  return (
    <div>
      <div className="page-header">
        <h1>Dashboard</h1>
        <p>Welcome to the QA Test Playground — your testing sandbox</p>
      </div>

      <div className="dashboard-grid">
        {cards.map((card) => (
          <DashboardCard
            key={card.title}
            title={card.title}
            count={loading ? '—' : card.count}
            description={card.description}
            icon={card.icon}
            iconClass={card.iconClass}
            onClick={() => navigate(card.route)}
          />
        ))}
      </div>
    </div>
  );
}
