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
