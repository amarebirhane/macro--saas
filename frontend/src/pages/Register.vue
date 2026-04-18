<template>
  <div class="auth-content">
    <div class="header">
      <h3>Create Account</h3>
      <p>Start your 14-day free trial today</p>
    </div>

    <form @submit.prevent="handleRegister" class="auth-form">
      <div class="form-group">
        <label>Email Address</label>
        <input 
          type="email" 
          v-model="email" 
          required 
          placeholder="name@company.com"
          :disabled="authStore.loading"
        />
      </div>

      <div class="form-group">
        <label>Password</label>
        <input 
          type="password" 
          v-model="password" 
          required 
          placeholder="••••••••"
          :disabled="authStore.loading"
        />
      </div>

      <div v-if="authStore.error" class="error-msg fade-in">
        {{ authStore.error }}
      </div>

      <button type="submit" class="btn btn-primary w-full" :disabled="authStore.loading">
        <span v-if="authStore.loading">Creating account...</span>
        <span v-else>Register Now</span>
      </button>
    </form>

    <div class="footer">
      <p>Already have an account? <router-link :to="{ name: 'login' }">Sign in</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const email = ref('')
const password = ref('')
const authStore = useAuthStore()
const router = useRouter()

const handleRegister = async () => {
  try {
    await authStore.register({ email: email.value, password: password.value })
    router.push({ name: 'dashboard' })
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
  gap: 1.5rem;
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

.error-msg {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error);
  padding: 0.75rem;
  border-radius: var(--radius);
  font-size: 0.85rem;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.w-full { width: 100%; }

.footer {
  margin-top: 2rem;
  text-align: center;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.footer a {
  color: var(--accent-primary);
  font-weight: 500;
}
</style>
