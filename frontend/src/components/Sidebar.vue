<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <div class="logo">⚡</div>
      <span class="brand-name">Micro-SaaS</span>
    </div>

    <nav class="nav-groups">
      <div class="nav-group">
        <p class="group-label">General</p>
        <router-link :to="{ name: 'dashboard' }" class="nav-link">
          <LayoutDashboardIcon :size="20" />
          <span>Dashboard</span>
        </router-link>
        <router-link :to="{ name: 'my-data' }" class="nav-link">
          <DatabaseIcon :size="20" />
          <span>My Data</span>
        </router-link>
        <router-link :to="{ name: 'profile' }" class="nav-link">
          <UserIcon :size="20" />
          <span>Profile</span>
        </router-link>
      </div>

      <div v-if="authStore.isAdmin" class="nav-group">
        <p class="group-label">Administration</p>
        <router-link :to="{ name: 'admin-dashboard' }" class="nav-link">
          <ShieldCheckIcon :size="20" />
          <span>Admin Overview</span>
        </router-link>
        <router-link :to="{ name: 'admin-users' }" class="nav-link">
          <UsersIcon :size="20" />
          <span>Manage Users</span>
        </router-link>
        <router-link :to="{ name: 'admin-analytics' }" class="nav-link">
          <BarChart3Icon :size="20" />
          <span>System Analytics</span>
        </router-link>
      </div>
    </nav>

    <div class="sidebar-footer">
      <div class="user-info">
        <div class="avatar">{{ userInitial }}</div>
        <div class="details">
          <p class="email">{{ authStore.user?.email }}</p>
          <p class="role-badge" :class="authStore.user?.role">{{ authStore.user?.role }}</p>
        </div>
      </div>
      <button @click="handleLogout" class="logout-btn">
        <LogOutIcon :size="18" />
        <span>Logout</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { 
  LayoutDashboardIcon, 
  DatabaseIcon, 
  UserIcon, 
  ShieldCheckIcon, 
  UsersIcon, 
  BarChart3Icon,
  LogOutIcon
} from 'lucide-vue-next'

const authStore = useAuthStore()
const router = useRouter()

const userInitial = computed(() => {
  return authStore.user?.email?.[0].toUpperCase() || 'U'
})

const handleLogout = () => {
  authStore.logout()
  router.push({ name: 'login' })
}
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  height: 100vh;
  background-color: var(--bg-secondary);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
}

.sidebar-header {
  padding: 2rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.brand-name {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.nav-groups {
  flex: 1;
  padding: 0 1rem;
  overflow-y: auto;
}

.nav-group {
  margin-bottom: 2rem;
}

.group-label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--text-secondary);
  letter-spacing: 0.05em;
  padding: 0 1rem;
  margin-bottom: 0.75rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: var(--text-secondary);
  border-radius: var(--radius);
  transition: all 0.2s ease;
  margin-bottom: 0.25rem;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.03);
  color: var(--text-primary);
}

.nav-link.router-link-active {
  background: rgba(99, 102, 241, 0.1);
  color: var(--accent-primary);
}

.sidebar-footer {
  padding: 1.5rem;
  border-top: 1px solid var(--border);
  background: var(--bg-card);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.avatar {
  width: 40px;
  height: 40px;
  background: var(--gradient-primary);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: white;
}

.details .email {
  font-size: 0.85rem;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 160px;
}

.role-badge {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  display: inline-block;
  margin-top: 2px;
}

.role-badge.ADMIN { background: rgba(239, 68, 68, 0.1); color: var(--error); }
.role-badge.USER { background: rgba(16, 185, 129, 0.1); color: var(--success); }

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text-secondary);
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.05);
  color: var(--error);
  border-color: rgba(239, 68, 68, 0.2);
}
</style>
