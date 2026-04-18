<template>
  <div class="profile-page fade-in">
    <div class="row">
      <div class="col-left">
        <div class="profile-card card glass">
          <div class="avatar-large">{{ userInitial }}</div>
          <h3>{{ authStore.user?.email }}</h3>
          <p class="role-text">{{ authStore.user?.role }} Account</p>
          <div class="status-badge" :class="authStore.user?.role">
            {{ authStore.user?.role === 'ADMIN' ? 'System Administrator' : 'Professional Plan' }}
          </div>
        </div>
      </div>
      
      <div class="col-right">
        <div class="settings-card card">
          <div class="card-header">
            <h3>Account Settings</h3>
            <p>Manage your account preferences and security.</p>
          </div>
          
          <form @submit.prevent="handleUpdate" class="settings-form">
            <div class="form-group">
              <label>Email Address</label>
              <input type="email" v-model="email" disabled class="disabled-input" />
              <p class="helper-text">Contact support to change your email.</p>
            </div>

            <div class="form-group">
              <label>New Password</label>
              <div class="password-wrapper">
                <input 
                  :type="showPassword ? 'text' : 'password'" 
                  v-model="password" 
                  placeholder="Leave empty to keep current" 
                />
                <button type="button" class="toggle-pw" @click="showPassword = !showPassword">
                  {{ showPassword ? '🙈' : '👁️' }}
                </button>
              </div>
              <p class="helper-text">Minimum 8 characters with letters and numbers.</p>
            </div>

            <div class="form-actions">
              <button type="submit" class="btn btn-primary" :disabled="loading">
                <span v-if="loading" class="spinner-small"></span>
                {{ loading ? 'Updating...' : 'Save Changes' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import api from '../services/api'

const authStore = useAuthStore()
const toast = useToast()
const email = ref(authStore.user?.email)
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)

const userInitial = computed(() => {
  return authStore.user?.email?.[0].toUpperCase() || 'U'
})

const handleUpdate = async () => {
  if (password.value && password.value.length < 8) {
    toast.warning('Password must be at least 8 characters long')
    return
  }

  loading.value = true
  try {
    const payload = {}
    if (password.value) payload.password = password.value
    
    await api.put('/users/me', payload)
    toast.success('Profile updated successfully!')
    password.value = ''
    showPassword.value = false
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Failed to update profile')
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.row {
  display: flex;
  gap: 2.5rem;
}

@media (max-width: 900px) {
  .row { flex-direction: column; }
  .col-left { width: 100% !important; }
}

.col-left { width: 340px; }
.col-right { flex: 1; }

.profile-card {
  text-align: center;
  padding: 3.5rem 2rem;
  position: sticky;
  top: 100px;
}

.avatar-large {
  width: 110px;
  height: 110px;
  background: var(--gradient-primary);
  border-radius: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3.5rem;
  font-weight: 800;
  color: white;
  margin: 0 auto 1.5rem;
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
}

.profile-card h3 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  word-break: break-all;
}

.role-text {
  color: var(--text-secondary);
  font-size: 0.95rem;
  margin-bottom: 1.75rem;
}

.status-badge {
  padding: 0.5rem 1.25rem;
  border-radius: 99px;
  font-size: 0.85rem;
  font-weight: 700;
  display: inline-block;
}

.status-badge.ADMIN { background: rgba(239, 68, 68, 0.1); color: var(--error); }
.status-badge.USER { background: rgba(99, 102, 241, 0.1); color: var(--accent-primary); }

.card-header {
  margin-bottom: 2.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border);
}

.card-header h3 { margin-bottom: 0.5rem; }
.card-header p { color: var(--text-secondary); font-size: 0.95rem; }

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.form-group label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
}

.password-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.password-wrapper input { width: 100%; padding-right: 3rem; }

.toggle-pw {
  position: absolute;
  right: 1rem;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  color: var(--text-secondary);
  padding: 0;
}

.disabled-input {
  background: rgba(255, 255, 255, 0.03) !important;
  border-color: var(--border) !important;
  color: var(--text-secondary) !important;
  cursor: not-allowed;
}

.helper-text {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.form-actions {
  margin-top: 1rem;
  display: flex;
  justify-content: flex-end;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.8rem 2rem;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }
</style>
