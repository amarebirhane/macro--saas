<template>
  <div class="auth-content">
    <div class="header">
      <h3>Set up your account</h3>
      <p>Start your 14-day premium experience</p>
    </div>

    <form @submit.prevent="handleRegister" class="auth-form">
      <div class="form-row">
        <div class="form-group">
          <label for="reg-first">First Name</label>
          <input 
            id="reg-first"
            type="text" 
            v-model="firstName" 
            required 
            placeholder="John"
            :disabled="authStore.loading"
          />
        </div>
        <div class="form-group">
          <label for="reg-last">Last Name</label>
          <input 
            id="reg-last"
            type="text" 
            v-model="lastName" 
            required 
            placeholder="Doe"
            :disabled="authStore.loading"
          />
        </div>
      </div>

      <div class="form-group">
        <label for="reg-username">Username</label>
        <div class="input-wrapper">
          <span class="input-prefix">@</span>
          <input 
            id="reg-username"
            type="text" 
            v-model="username" 
            required 
            placeholder="johndoe"
            :disabled="authStore.loading"
          />
        </div>
      </div>

      <div class="form-group">
        <label for="reg-email">Work Email</label>
        <input 
          id="reg-email"
          type="email" 
          v-model="email" 
          required 
          placeholder="name@company.com"
          :disabled="authStore.loading"
          autocomplete="email"
        />
      </div>

      <div class="form-group">
        <label for="reg-password">Choose Password</label>
        <div class="input-wrapper">
          <input 
            id="reg-password"
            :type="showPassword ? 'text' : 'password'" 
            v-model="password" 
            required 
            placeholder="Min. 8 characters"
            :disabled="authStore.loading"
            autocomplete="new-password"
          />
          <button type="button" class="toggle-pw" @click="showPassword = !showPassword" tabindex="-1">
            {{ showPassword ? '🙈' : '👁️' }}
          </button>
        </div>
      </div>

      <div class="form-group">
        <label for="reg-confirm">Confirm Password</label>
        <input 
          id="reg-confirm"
          type="password" 
          v-model="confirmPassword" 
          required 
          placeholder="••••••••"
          :disabled="authStore.loading"
          autocomplete="new-password"
        />
      </div>

      <div v-if="authStore.error" class="error-msg fade-in">
        {{ authStore.error }}
      </div>

      <button id="register-submit" type="submit" class="btn btn-primary w-full" :disabled="authStore.loading">
        <span v-if="authStore.loading" class="btn-loading">
          <span class="spinner"></span> Creating Account...
        </span>
        <span v-else>Launch Your SaaS →</span>
      </button>

      <p class="terms">
        By continuing, you agree to our <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>.
      </p>
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
import { useToast } from '../composables/useToast'

const firstName = ref('')
const lastName = ref('')
const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const authStore = useAuthStore()
const router = useRouter()
const toast = useToast()

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    toast.warning('Passwords do not match')
    return
  }

  if (password.value.length < 8) {
    toast.warning('Password must be at least 8 characters')
    return
  }

  // Simple username validation
  if (!/^[a-z0-9_]{3,20}$/.test(username.value)) {
    toast.warning('Username must be 3-20 lowercase alphanumeric characters')
    return
  }

  try {
    await authStore.register({ 
      first_name: firstName.value,
      last_name: lastName.value,
      username: username.value,
      email: email.value, 
      password: password.value 
    })
    toast.success('Welcome aboard! Your session has started.')
    router.push({ name: 'dashboard' })
  } catch (err) {
    // Error handled in store/toast
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
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
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

.input-prefix {
  position: absolute;
  left: 0.75rem;
  color: var(--text-secondary);
  font-weight: 600;
}

#reg-username {
  padding-left: 1.75rem;
}

.input-wrapper input {
  width: 100%;
}

#reg-password {
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

.terms {
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-align: center;
  line-height: 1.4;
  margin-top: 0.5rem;
}

.terms a {
  color: var(--accent-primary);
  text-decoration: none;
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
