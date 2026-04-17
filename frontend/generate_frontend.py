import os

base = r"c:\Users\ASHROCK\Desktop\Micro-SaaS\frontend"

def write(path, content):
    os.makedirs(os.path.dirname(os.path.join(base, path)), exist_ok=True)
    with open(os.path.join(base, path), "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

write("package.json", """
{
  "name": "micro-saas-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.21",
    "vue-router": "^4.3.0",
    "pinia": "^2.1.7",
    "axios": "^1.6.8",
    "lucide-vue-next": "^0.364.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.4",
    "vite": "^5.2.0"
  }
}
""")

write("vite.config.js", """
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173
  }
})
""")

write("src/main.js", """
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
""")

write("src/assets/main.css", """
:root {
  --bg-primary: #0a0a0b;
  --bg-secondary: #141416;
  --text-primary: #ffffff;
  --text-secondary: #a0a0ab;
  --accent-color: #6366f1;
  --accent-hover: #4f46e5;
  --border-color: #27272a;
  --error-color: #ef4444;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

button {
  cursor: pointer;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s ease;
}

input {
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  font-family: inherit;
  transition: border-color 0.2s ease;
}

input:focus {
  outline: none;
  border-color: var(--accent-color);
}

.btn-primary {
  background-color: var(--accent-color);
  color: white;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
}

.btn-primary:hover {
  background-color: var(--accent-hover);
  transform: translateY(-1px);
}
""")

write("src/App.vue", """
<template>
  <router-view />
</template>

<script setup>
</script>
""")

write("src/router/index.js", """
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env?.BASE_URL || '/'),
  routes: [
    {
      path: '/auth',
      component: () => import('../layouts/AuthLayout.vue'),
      children: [
        { path: 'login', name: 'login', component: () => import('../pages/Login.vue') },
        { path: 'register', name: 'register', component: () => import('../pages/Register.vue') }
      ]
    },
    {
      path: '/',
      component: () => import('../layouts/MainLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '', redirect: '/dashboard' },
        { path: 'dashboard', name: 'dashboard', component: () => import('../pages/Dashboard.vue') }
      ]
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/auth/login')
  } else if (to.path.startsWith('/auth') && authStore.isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
""")

write("src/services/api.js", """
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
""")

write("src/services/authService.js", """
import api from './api'

export default {
  login(credentials) {
    const params = new URLSearchParams()
    params.append('username', credentials.email)
    params.append('password', credentials.password)
    
    return api.post('/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  },
  register(userData) {
    return api.post('/auth/register', userData)
  },
  getMe() {
    return api.get('/auth/me')
  }
}
""")

write("src/stores/auth.js", """
import { defineStore } from 'pinia'
import authService from '../services/authService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(email, password) {
      const response = await authService.login({ email, password })
      this.token = response.data.access_token
      localStorage.setItem('token', this.token)
      await this.fetchUser()
    },
    async register(email, password) {
      await authService.register({ email, password })
      await this.login(email, password)
    },
    async fetchUser() {
      if (!this.token) return
      try {
        const response = await authService.getMe()
        this.user = response.data
      } catch (e) {
        this.logout()
      }
    },
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    }
  }
})
""")

write("src/layouts/AuthLayout.vue", """
<template>
  <div class="auth-layout">
    <div class="auth-card">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle at 50% -20%, #1a1a2e, var(--bg-primary));
}

.auth-card {
  width: 100%;
  max-width: 400px;
  padding: 2.5rem;
  background: rgba(20, 20, 22, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.5);
}
</style>
""")

write("src/pages/Login.vue", """
<template>
  <div>
    <h1 class="title">Welcome Back</h1>
    <p class="subtitle">Sign in to your Micro-SaaS account</p>
    
    <form @submit.prevent="handleLogin" class="form">
      <div class="input-group">
        <label>Email</label>
        <input type="email" v-model="email" required placeholder="you@example.com" />
      </div>
      <div class="input-group">
        <label>Password</label>
        <input type="password" v-model="password" required placeholder="••••••••" />
      </div>
      <p v-if="error" class="error">{{ error }}</p>
      
      <button type="submit" class="btn-primary" :disabled="loading">
        {{ loading ? 'Signing in...' : 'Sign In' }}
      </button>
    </form>
    
    <p class="switch-link">
      Don't have an account? <router-link to="/auth/register">Sign up</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const router = useRouter()
const authStore = useAuthStore()

const handleLogin = async () => {
  try {
    loading.value = true
    error.value = ''
    await authStore.login(email.value, password.value)
    router.push('/dashboard')
  } catch (err) {
    error.value = 'Invalid email or password'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.title {
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.subtitle {
  color: var(--text-secondary);
  margin-bottom: 2rem;
}
.form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}
.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.input-group label {
  font-size: 0.875rem;
  color: var(--text-secondary);
}
.error {
  color: var(--error-color);
  font-size: 0.875rem;
}
.switch-link {
  margin-top: 2rem;
  text-align: center;
  font-size: 0.875rem;
  color: var(--text-secondary);
}
.switch-link a {
  color: var(--accent-color);
  text-decoration: none;
}
.switch-link a:hover {
  text-decoration: underline;
}
</style>
""")

write("src/pages/Register.vue", """
<template>
  <div>
    <h1 class="title">Create an Account</h1>
    <p class="subtitle">Join Micro-SaaS today</p>
    
    <form @submit.prevent="handleRegister" class="form">
      <div class="input-group">
        <label>Email</label>
        <input type="email" v-model="email" required placeholder="you@example.com" />
      </div>
      <div class="input-group">
        <label>Password</label>
        <input type="password" v-model="password" required placeholder="••••••••" />
      </div>
      <p v-if="error" class="error">{{ error }}</p>
      
      <button type="submit" class="btn-primary" :disabled="loading">
        {{ loading ? 'Creating...' : 'Sign Up' }}
      </button>
    </form>
    
    <p class="switch-link">
      Already have an account? <router-link to="/auth/login">Sign in</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const router = useRouter()
const authStore = useAuthStore()

const handleRegister = async () => {
  try {
    loading.value = true
    error.value = ''
    await authStore.register(email.value, password.value)
    router.push('/dashboard')
  } catch (err) {
    error.value = 'Registration failed. Email might be in use.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.title {
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.subtitle {
  color: var(--text-secondary);
  margin-bottom: 2rem;
}
.form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}
.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.error {
  color: var(--error-color);
  font-size: 0.875rem;
}
.switch-link {
  margin-top: 2rem;
  text-align: center;
  font-size: 0.875rem;
  color: var(--text-secondary);
}
.switch-link a {
  color: var(--accent-color);
  text-decoration: none;
}
</style>
""")

write("src/layouts/MainLayout.vue", """
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
""")

write("src/pages/Dashboard.vue", """
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
""")

print("Frontend scaffolding generated.")
