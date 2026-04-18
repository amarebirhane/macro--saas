<template>
  <div class="profile-page fade-in">
    <div class="row">
      <div class="col-left">
        <div class="profile-card card glass">
          <div class="avatar-large">{{ initials }}</div>
          <h3>{{ authStore.user?.first_name }} {{ authStore.user?.last_name }}</h3>
          <p class="username-display">@{{ authStore.user?.username }}</p>
          <div class="status-badge" :class="authStore.user?.role">
            {{ authStore.user?.role === 'ADMIN' ? 'System Administrator' : 'Professional Plan' }}
          </div>
          <div class="profile-bio">
            <p>{{ authStore.user?.email }}</p>
          </div>
        </div>
      </div>
      
      <div class="col-right">
        <div class="settings-card card">
          <div class="card-header">
            <h3>Account Settings</h3>
            <p>Manage your public profile and account security.</p>
          </div>
          
          <form @submit.prevent="handleUpdate" class="settings-form">
            <div class="form-row">
              <div class="form-group">
                <label>First Name</label>
                <input type="text" v-model="formData.first_name" placeholder="John" />
              </div>
              <div class="form-group">
                <label>Last Name</label>
                <input type="text" v-model="formData.last_name" placeholder="Doe" />
              </div>
            </div>

            <div class="form-group">
              <label>Username</label>
              <div class="username-wrapper">
                <span class="at-symbol">@</span>
                <input type="text" v-model="formData.username" placeholder="johndoe" />
              </div>
            </div>

            <div class="form-group">
              <label>Email Address</label>
              <input type="email" v-model="formData.email" disabled class="disabled-input" />
              <p class="helper-text">Contact support to change your verified email.</p>
            </div>

            <div class="divider"></div>

            <div class="form-group">
              <label>Change Password</label>
              <div class="password-wrapper">
                <input 
                  :type="showPassword ? 'text' : 'password'" 
                  v-model="formData.password" 
                  placeholder="Enter new password to change" 
                />
                <button type="button" class="toggle-pw" @click="showPassword = !showPassword">
                  {{ showPassword ? '🙈' : '👁️' }}
                </button>
              </div>
              <p class="helper-text">Leave blank to keep your current password.</p>
            </div>

            <div class="form-actions">
              <button type="submit" class="btn btn-primary" :disabled="loading">
                <span v-if="loading" class="spinner-small"></span>
                {{ loading ? 'Saving...' : 'Save Changes' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import api from '../services/api'

const authStore = useAuthStore()
const toast = useToast()
const loading = ref(false)
const showPassword = ref(false)

const formData = reactive({
  first_name: authStore.user?.first_name || '',
  last_name: authStore.user?.last_name || '',
  username: authStore.user?.username || '',
  email: authStore.user?.email || '',
  password: ''
})

const initials = computed(() => {
  if (authStore.user?.first_name && authStore.user?.last_name) {
    return `${authStore.user.first_name[0]}${authStore.user.last_name[0]}`.toUpperCase()
  }
  return authStore.user?.email?.[0].toUpperCase() || 'U'
})

const handleUpdate = async () => {
  if (formData.password && formData.password.length < 8) {
    toast.warning('New password must be at least 8 characters long')
    return
  }

  loading.value = true
  try {
    const payload = {
      first_name: formData.first_name,
      last_name: formData.last_name,
      username: formData.username
    }
    
    if (formData.password) {
      payload.password = formData.password
    }
    
    await api.put('/users/me', payload)
    
    // Refresh user data in store
    await authStore.fetchUser()
    
    toast.success('Your profile has been updated!')
    formData.password = ''
    showPassword.value = false
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Failed to update profile')
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (!authStore.user) {
    authStore.fetchUser()
  }
})
</script>

<style scoped>
.profile-page {
  padding-bottom: 4rem;
}

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
  padding: 3rem 2rem;
  position: sticky;
  top: 100px;
}

.avatar-large {
  width: 100px;
  height: 100px;
  background: var(--gradient-primary);
  border-radius: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  font-weight: 800;
  color: white;
  margin: 0 auto 1.5rem;
  box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);
}

.profile-card h3 {
  font-size: 1.5rem;
  margin-bottom: 0.25rem;
}

.username-display {
  color: var(--accent-primary);
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.status-badge {
  padding: 0.5rem 1.25rem;
  border-radius: 99px;
  font-size: 0.85rem;
  font-weight: 700;
  display: inline-block;
  margin-bottom: 1.5rem;
}

.status-badge.ADMIN { background: rgba(239, 68, 68, 0.1); color: var(--error); }
.status-badge.USER { background: rgba(99, 102, 241, 0.1); color: var(--accent-primary); }

.profile-bio {
  color: var(--text-secondary);
  font-size: 0.95rem;
  border-top: 1px solid var(--border);
  padding-top: 1.5rem;
  margin-top: 0.5rem;
}

.card-header {
  margin-bottom: 2.5rem;
}

.card-header h3 { margin-bottom: 0.5rem; }
.card-header p { color: var(--text-secondary); font-size: 0.95rem; }

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
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

.divider {
  height: 1px;
  background: var(--border);
  margin: 1rem 0;
}

.username-wrapper, .password-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.at-symbol {
  position: absolute;
  left: 1rem;
  font-weight: 700;
  color: var(--text-secondary);
}

.username-wrapper input {
  padding-left: 2.2rem;
}

.username-wrapper input, .password-wrapper input {
  width: 100%;
}

.password-wrapper input {
  padding-right: 3.5rem;
}

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
  background: rgba(255, 255, 255, 0.05) !important;
  color: var(--text-secondary) !important;
  cursor: not-allowed;
  opacity: 0.8;
}

.helper-text {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.form-actions {
  margin-top: 1.5rem;
  display: flex;
  justify-content: flex-end;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.8rem 2.5rem;
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
