<template>
  <div class="dashboard">
    <div class="welcome-card">
      <h3>Welcome back{{ user ? ', ' + user.email : '' }}!</h3>
      <p>Here is your Micro-SaaS overview.</p>
      <div v-if="user?.role === 'ADMIN'" class="admin-badge">Admin Access</div>
    </div>
    
    <div class="stats-grid">
      <div class="stat-card">
        <h4>Total Usage</h4>
        <div class="value">0</div>
      </div>
      <div class="stat-card">
        <h4>Active Projects</h4>
        <div class="value">0</div>
      </div>
      <div class="stat-card">
        <h4>Subscription</h4>
        <div class="value status">Free Plan</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const user = computed(() => authStore.user)

onMounted(() => {
  if (!user.value) {
    authStore.fetchUser()
  }
})
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.welcome-card {
  padding: 2rem;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(0, 0, 0, 0));
  border: 1px solid var(--border-color);
  border-radius: 12px;
}

.welcome-card h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.welcome-card p {
  color: var(--text-secondary);
}

.admin-badge {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.25rem 0.75rem;
  background-color: rgba(239, 68, 68, 0.1);
  color: var(--error-color);
  border-radius: 99px;
  font-size: 0.875rem;
  font-weight: 500;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  padding: 1.5rem;
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
}

.stat-card h4 {
  color: var(--text-secondary);
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.stat-card .value {
  font-size: 2rem;
  font-weight: 600;
}

.stat-card .status {
  font-size: 1.25rem;
  color: var(--accent-color);
}
</style>
