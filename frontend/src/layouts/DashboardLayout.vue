<template>
  <div class="dashboard-layout">
    <Sidebar />
    <main class="main-content">
      <header class="top-nav glass">
        <div class="page-info">
          <h1 class="page-title">{{ currentPageTitle }}</h1>
        </div>
        <div class="actions">
          <div class="notification-bell">🔔</div>
          <div class="user-status">
            <span class="pulse"></span>
            Online
          </div>
        </div>
      </header>
      
      <div class="view-container">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'

const route = useRoute()

const currentPageTitle = computed(() => {
  return route.name?.toString().split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ') || 'Dashboard'
})
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.top-nav {
  height: var(--header-height);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2.5rem;
  position: sticky;
  top: 0;
  z-index: 50;
  border-bottom: 1px solid var(--border);
}

.page-title {
  font-size: 1.5rem;
  font-weight: 700;
}

.actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.user-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text-secondary);
  background: var(--bg-secondary);
  padding: 0.4rem 0.8rem;
  border-radius: 99px;
  border: 1px solid var(--border);
}

.pulse {
  width: 8px;
  height: 8px;
  background: var(--success);
  border-radius: 50%;
  display: inline-block;
  box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

.view-container {
  padding: 2.5rem;
  flex: 1;
}
</style>
