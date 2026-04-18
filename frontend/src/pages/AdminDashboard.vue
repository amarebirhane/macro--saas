<template>
  <div class="admin-dashboard fade-in">
    <div class="stats-grid">
      <div v-for="stat in stats" :key="stat.label" class="stat-card card">
        <div class="stat-icon" :style="{ background: stat.bg, color: stat.color }">{{ stat.icon }}</div>
        <div class="details">
          <p class="label">{{ stat.label }}</p>
          <p class="value">{{ stat.value }}</p>
        </div>
      </div>
    </div>

    <div class="admin-sections">
      <section class="quick-actions card">
        <h3>Administrative Actions</h3>
        <div class="action-buttons">
          <button @click="$router.push({ name: 'admin-users' })" class="btn btn-primary">Manage Users</button>
          <button @click="$router.push({ name: 'admin-analytics' })" class="btn glass">Detailed Reports</button>
          <button class="btn glass">System Log</button>
        </div>
      </section>

      <section class="system-status card">
        <h3>System Health</h3>
        <div class="health-item">
          <span>API Server</span>
          <span class="status online">Healthy</span>
        </div>
        <div class="health-item">
          <span>Database</span>
          <span class="status online">Connected</span>
        </div>
        <div class="health-item">
          <span>Storage</span>
          <span class="status warning">82% Full</span>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const stats = ref([
  { label: 'Total Users', value: '0', icon: '👥', bg: 'rgba(99, 102, 241, 0.1)', color: 'var(--accent-primary)' },
  { label: 'Active Today', value: '0', icon: '🔥', bg: 'rgba(16, 185, 129, 0.1)', color: 'var(--success)' },
  { label: 'Admins', value: '0', icon: '🛡️', bg: 'rgba(239, 68, 68, 0.1)', color: 'var(--error)' }
])

onMounted(async () => {
  try {
    const response = await api.get('/admin/analytics')
    stats.value[0].value = response.data.total_users
    stats.value[1].value = response.data.active_users
    stats.value[2].value = response.data.admin_count
  } catch (err) {
    console.error(err)
  }
})
</script>

<style scoped>
.admin-dashboard {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 2rem;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
}

.stat-card .value {
  font-size: 2rem;
  font-weight: 700;
}

.admin-sections {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.quick-actions h3, .system-status h3 {
  margin-bottom: 2rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.health-item {
  display: flex;
  justify-content: space-between;
  padding: 1rem 0;
  border-bottom: 1px solid var(--border);
}

.status {
  font-weight: 600;
  font-size: 0.9rem;
}

.status.online { color: var(--success); }
.status.warning { color: gold; }
</style>
