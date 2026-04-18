<template>
  <div class="auth-content">
    <div class="header">
      <h3>Welcome back</h3>
      <p>Sign in to access your dashboard</p>
    </div>

    <form @submit.prevent="handleLogin" class="auth-form">
      <div class="form-group">
        <label>Email or Username</label>
        <input
          id="login-identifier"
          type="text"
          v-model="identifier"
          required
          placeholder="email@company.com or username"
          :disabled="authStore.loading"
          autocomplete="username"
        />
      </div>

      <div class="form-group">
        <label>Password</label>
        <div class="input-wrapper">
          <input
            id="login-password"
            :type="showPassword ? 'text' : 'password'"
            v-model="password"
            required
            placeholder="••••••••"
            :disabled="authStore.loading"
            autocomplete="current-password"
          />
          <button type="button" class="toggle-pw" @click="showPassword = !showPassword" tabindex="-1">
            {{ showPassword ? '🙈' : '👁️' }}
          </button>
        </div>
      </div>

      <div class="form-row">
        <label class="checkbox-label">
          <input type="checkbox" v-model="rememberMe" id="remember-me" />
          <span>Remember me</span>
        </label>
        <span class="forgot-link">Forgot password?</span>
      </div>

      <div v-if="authStore.error" class="error-msg fade-in">
        {{ authStore.error }}
      </div>

      <button id="login-submit" type="submit" class="btn btn-primary w-full" :disabled="authStore.loading">
        <span v-if="authStore.loading" class="btn-loading">
          <span class="spinner"></span> Verifying...
        </span>
        <span v-else>Sign In →</span>
      </button>
    </form>

    <div class="footer">
      <p>Don't have an account? <router-link :to="{ name: 'register' }">Create one</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const rememberMe = ref(false)
const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const handleLogin = async () => {
  try {
    await authStore.login({ email: email.value, password: password.value }, rememberMe.value)
    const redirectPath = route.query.redirect || { name: 'dashboard' }
    router.push(redirectPath)
  } catch (err) {
    // Error handled in store
  }
}
</script>

<style scoped>
.header {
  margin-bottom: 2rem;
}

.header h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.header p {
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text-secondary);
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper input {
  width: 100%;
  padding-right: 3rem;
}

.toggle-pw {
  position: absolute;
  right: 0.75rem;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  color: var(--text-secondary);
  padding: 0;
}

.form-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  cursor: pointer;
  color: var(--text-secondary);
}

.checkbox-label input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: var(--accent-primary);
  cursor: pointer;
}

.forgot-link {
  font-size: 0.85rem;
  color: var(--accent-primary);
  cursor: pointer;
  font-weight: 500;
}

.forgot-link:hover { text-decoration: underline; }

.error-msg {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error);
  padding: 0.75rem;
  border-radius: var(--radius);
  font-size: 0.85rem;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.btn-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  display: inline-block;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.w-full { width: 100%; }

.footer {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.footer a {
  color: var(--accent-primary);
  font-weight: 500;
}
</style>
