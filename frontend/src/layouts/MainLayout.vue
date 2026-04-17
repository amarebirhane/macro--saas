<template>
  <div class="app-layout">
    <aside class="sidebar">
      <div class="brand">Micro-SaaS</div>
      <nav class="nav">
        <router-link to="/dashboard" class="nav-item">Dashboard</router-link>
      </nav>
      <div class="spacer"></div>
      <button @click="handleLogout" class="nav-item logout">Logout</button>
    </aside>
    <main class="main-content">
      <header class="header">
        <h2>Dashboard</h2>
      </header>
      <div class="content-area">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/auth/login')
}
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 260px;
  background-color: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
}

.brand {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--accent-color);
  margin-bottom: 2rem;
}

.nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-item {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.2s ease;
  background: transparent;
  text-align: left;
  font-size: 1rem;
}

.nav-item:hover, .router-link-active {
  background-color: rgba(99, 102, 241, 0.1);
  color: var(--accent-color);
}

.spacer {
  flex: 1;
}

.logout:hover {
  background-color: rgba(239, 68, 68, 0.1);
  color: var(--error-color);
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.header {
  height: 70px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  padding: 0 2rem;
}

.content-area {
  padding: 2rem;
  flex: 1;
  overflow-y: auto;
}
</style>
