<template>
  <div class="dashboard-page fade-in">
    <section class="welcome-section card glass">
      <div class="welcome-text">
        <h2>Greetings, {{ userEmail }}!</h2>
        <p>Welcome to your personal command center. Here's what's happening today.</p>
        <div v-if="authStore.isAdmin" class="admin-chip">Administrator</div>
      </div>
      <div class="welcome-image">🚀</div>
    </section>

    <div class="stats-grid">
      <div class="stat-card card hover-scale">
        <div class="stat-icon usage">📊</div>
        <div class="stat-info">
          <p class="label">Total Usage</p>
          <p class="value">1,284</p>
        </div>
      </div>
      <div class="stat-card card hover-scale">
        <div class="stat-icon projects">📁</div>
        <div class="stat-info">
          <p class="label">Active Projects</p>
          <p class="value">12</p>
        </div>
      </div>
      <div class="stat-card card hover-scale">
        <div class="stat-icon api">🔑</div>
        <div class="stat-info">
          <p class="label">API Requests</p>
          <p class="value">45.2k</p>
        </div>
      </div>
    </div>

    <section class="recent-activity card">
      <div class="section-header">
        <h3>Recent Activity</h3>
        <button class="btn-text">View All</button>
      </div>
      <div class="activity-list">
        <div v-for="i in 3" :key="i" class="activity-item">
          <div class="dot"></div>
          <div class="item-content">
            <p class="activity-title">New project "{{ ['SaaS App', 'Backend API', 'Portfolio'][i-1] }}" created</p>
            <p class="activity-time">{{ i * 2 }} hours ago</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const userEmail = computed(() => authStore.user?.email || 'User')
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
  font-size: 1.1rem;
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
}

.welcome-image {
  font-size: 4rem;
}

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
}

.hover-scale:hover {
  transform: translateY(-5px);
  border-color: var(--accent-primary);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.usage { background: rgba(99, 102, 241, 0.1); }
.projects { background: rgba(16, 185, 129, 0.1); }
.api { background: rgba(168, 85, 247, 0.1); }

.stat-info .label {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.stat-info .value {
  font-size: 1.75rem;
  font-weight: 700;
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
  font-size: 0.9rem;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.activity-item {
  display: flex;
  gap: 1rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border);
}

.activity-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.dot {
  width: 10px;
  height: 10px;
  background: var(--accent-primary);
  border-radius: 50%;
  margin-top: 0.5rem;
}

.activity-title {
  font-weight: 500;
}

.activity-time {
  font-size: 0.85rem;
  color: var(--text-secondary);
}
</style>
