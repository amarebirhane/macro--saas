<template>
  <div class="dashboard-page fade-in">
    <section class="welcome-section card glass">
      <div class="welcome-text">
        <h2>Greetings, {{ userName }}!</h2>
        <p>Welcome to your personal command center. Here's a look at your account activity.</p>
        <div v-if="authStore.isAdmin" class="admin-chip">Administrator Access</div>
      </div>
      <div class="welcome-image">🚀</div>
    </section>

    <div class="stats-grid">
      <div v-for="stat in stats" :key="stat.label" class="stat-card card hover-scale">
        <div class="stat-icon" :class="stat.iconClass">{{ stat.icon }}</div>
        <div class="stat-info">
          <p class="label">{{ stat.label }}</p>
          <p class="value" v-if="!loading">{{ stat.value }}</p>
          <div v-else class="skeleton skeleton-value"></div>
        </div>
      </div>
    </div>

    <div class="bottom-grid">
      <section class="recent-activity card">
        <div class="section-header">
          <h3>Recent Activity</h3>
          <button class="btn-text" @click="$router.push({ name: 'my-data' })">View All</button>
        </div>
        <div v-if="loading" class="activity-list">
          <div v-for="i in 3" :key="i" class="activity-item">
            <div class="skeleton skeleton-dot"></div>
            <div class="skeleton-lines">
              <div class="skeleton skeleton-line"></div>
              <div class="skeleton skeleton-line-short"></div>
            </div>
          </div>
        </div>
        <div v-else class="activity-list">
          <div v-for="(item, i) in recentActivity" :key="i" class="activity-item">
            <div class="dot" :class="item.type"></div>
            <div class="item-content">
              <p class="activity-title">{{ item.title }}</p>
              <p class="activity-time">{{ item.time }}</p>
            </div>
          </div>
        </div>
      </section>

      <section class="quick-actions card">
        <h3>Quick Actions</h3>
        <div class="action-list">
          <button class="action-btn" @click="$router.push({ name: 'my-data' })">
            <span class="action-icon">📁</span>
            <div>
              <p class="action-label">My Data</p>
              <p class="action-desc">Manage your records</p>
            </div>
          </button>
          <button class="action-btn" @click="$router.push({ name: 'profile' })">
            <span class="action-icon">👤</span>
            <div>
              <p class="action-label">Profile Settings</p>
              <p class="action-desc">Update your account</p>
            </div>
          </button>
          <button v-if="authStore.isAdmin" class="action-btn admin" @click="$router.push({ name: 'admin-dashboard' })">
            <span class="action-icon">🛡️</span>
            <div>
              <p class="action-label">Admin Panel</p>
              <p class="action-desc">Manage users & system</p>
            </div>
          </button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const authStore = useAuthStore()
const userName = computed(() => {
  if (authStore.user?.first_name) return authStore.user.first_name
  if (authStore.user?.username) return authStore.user.username
  return authStore.user?.email?.split('@')[0] || 'User'
})
const loading = ref(true)

const stats = ref([
  { label: 'Total Usage', value: '—', icon: '📊', iconClass: 'usage' },
  { label: 'Active Projects', value: '—', icon: '📁', iconClass: 'projects' },
  { label: 'API Requests', value: '—', icon: '🔑', iconClass: 'api' }
])

const recentActivity = ref([
  { title: 'Account created successfully', time: 'Just now', type: 'success' },
  { title: 'Profile setup completed', time: '5 minutes ago', type: 'info' },
  { title: 'Dashboard accessed', time: '10 minutes ago', type: 'default' }
])

onMounted(async () => {
  try {
    if (authStore.isAdmin) {
      const res = await api.get('/admin/analytics')
      stats.value[0].value = res.data.total_users?.toLocaleString() ?? '—'
      stats.value[1].value = res.data.admin_count ?? '—'
      stats.value[2].value = res.data.active_users?.toLocaleString() ?? '—'
      stats.value[0].label = 'Total Users'
      stats.value[1].label = 'Admin Users'
      stats.value[2].label = 'Active Users'
    } else {
      // Simulate user-level stats
      stats.value[0].value = '1,284'
      stats.value[1].value = '12'
      stats.value[2].value = '45.2k'
    }
  } catch (err) {
    console.error('Failed to load stats:', err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.dashboard-page {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.welcome-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2.5rem;
}

.welcome-text h2 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.welcome-text p {
  color: var(--text-secondary);
  font-size: 1.05rem;
}

.admin-chip {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.25rem 0.75rem;
  background: rgba(239, 68, 68, 0.1);
  color: var(--error);
  border-radius: 99px;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.welcome-image { font-size: 4rem; }

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem 2rem;
  transition: transform 0.2s, border-color 0.2s;
}

.hover-scale:hover {
  transform: translateY(-4px);
  border-color: var(--accent-primary);
}

.stat-icon {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.usage { background: rgba(99, 102, 241, 0.1); }
.projects { background: rgba(16, 185, 129, 0.1); }
.api { background: rgba(168, 85, 247, 0.1); }

.stat-info .label {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.stat-info .value {
  font-size: 1.75rem;
  font-weight: 700;
}

/* Skeleton loaders */
.skeleton {
  background: linear-gradient(90deg, var(--bg-secondary) 25%, var(--border) 50%, var(--bg-secondary) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 6px;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skeleton-value { height: 2rem; width: 80px; margin-top: 4px; }
.skeleton-dot { width: 10px; height: 10px; border-radius: 50%; margin-top: 0.5rem; flex-shrink: 0; }
.skeleton-lines { flex: 1; display: flex; flex-direction: column; gap: 0.5rem; }
.skeleton-line { height: 14px; width: 80%; }
.skeleton-line-short { height: 12px; width: 40%; }

.bottom-grid {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 2rem;
}

@media (max-width: 900px) {
  .bottom-grid { grid-template-columns: 1fr; }
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.btn-text {
  background: transparent;
  border: none;
  color: var(--accent-primary);
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.activity-item {
  display: flex;
  gap: 1rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid var(--border);
}

.activity-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-top: 0.4rem;
  flex-shrink: 0;
}

.dot.success { background: var(--success); }
.dot.info { background: var(--accent-primary); }
.dot.default { background: var(--text-secondary); }

.activity-title { font-weight: 500; font-size: 0.9rem; }
.activity-time { font-size: 0.8rem; color: var(--text-secondary); margin-top: 0.2rem; }

/* Quick Actions */
.quick-actions h3 { margin-bottom: 1.5rem; }

.action-list { display: flex; flex-direction: column; gap: 0.75rem; }

.action-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  cursor: pointer;
  text-align: left;
  transition: border-color 0.2s, transform 0.2s;
  width: 100%;
}

.action-btn:hover {
  border-color: var(--accent-primary);
  transform: translateX(4px);
}

.action-btn.admin:hover {
  border-color: var(--error);
}

.action-icon { font-size: 1.5rem; }
.action-label { font-weight: 600; font-size: 0.9rem; }
.action-desc { font-size: 0.8rem; color: var(--text-secondary); margin-top: 0.1rem; }
</style>
