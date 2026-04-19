// ── Sidebar Toggle ──────────────────────────────
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');

if (sidebarToggle && sidebar) {
  sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });

  // Close sidebar when clicking outside on mobile
  document.addEventListener('click', (e) => {
    if (window.innerWidth <= 768 &&
        sidebar.classList.contains('open') &&
        !sidebar.contains(e.target) &&
        !sidebarToggle.contains(e.target)) {
      sidebar.classList.remove('open');
    }
  });
}

// ── Dark Mode Toggle ─────────────────────────────
const themeToggle = document.getElementById('themeToggle');
if (themeToggle) {
  const icon = themeToggle.querySelector('i');
  const stored = localStorage.getItem('theme');
  if (stored === 'dark') {
    document.body.classList.add('dark-mode');
    if (icon) icon.className = 'fas fa-sun';
  }

  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    if (icon) icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  });
}

// ── Auto-dismiss alerts after 5s ─────────────────
document.querySelectorAll('.alert').forEach(alert => {
  setTimeout(() => {
    alert.style.opacity = '0';
    alert.style.transform = 'translateX(-10px)';
    alert.style.transition = 'all 0.3s';
    setTimeout(() => alert.remove(), 300);
  }, 5000);
});

// ── Active nav highlight by current path ─────────
const currentPath = window.location.pathname;
document.querySelectorAll('.nav-item').forEach(item => {
  if (item.href && item.href !== window.location.origin + '/') {
    if (currentPath.startsWith(new URL(item.href).pathname)) {
      item.classList.add('active');
    }
  }
});
