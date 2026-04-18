<template>
  <div class="profile-page fade-in">
    <div class="row">
      <div class="col-left">
        <div class="profile-card card glass">
          <div class="avatar-large">{{ userInitial }}</div>
          <h3>{{ authStore.user?.email }}</h3>
          <p class="role-text">{{ authStore.user?.role }} Account</p>
          <div class="status-badge">Professional Plan</div>
        </div>
      </div>
      
      <div class="col-right">
        <div class="settings-card card">
          <h3>Account Settings</h3>
          <form @submit.prevent="handleUpdate" class="settings-form">
            <div class="form-group">
              <label>Email Address</label>
              <input type="email" v-model="email" disabled />
              <p class="helper-text">Contact support to change your email.</p>
            </div>

            <div class="form-group">
              <label>New Password</label>
              <input type="password" v-model="password" placeholder="Leave empty to keep current" />
            </div>

            <div class="actions">
              <button type="submit" class="btn btn-primary" :disabled="loading">
                {{ loading ? 'Updating...' : 'Save Changes' }}
              </button>
            </div>
            
            <p v-if="message" class="success-msg">{{ message }}</p>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const authStore = useAuthStore()
const email = ref(authStore.user?.email)
const password = ref('')
const loading = ref(false)
const message = ref('')

const userInitial = computed(() => {
  return authStore.user?.email?.[0].toUpperCase() || 'U'
})

const handleUpdate = async () => {
  loading.value = true
  message.value = ''
  try {
    const payload = {}
    if (password.value) payload.password = password.value
    
    await api.put('/users/me', payload)
    message.value = 'Profile updated successfully!'
    password.value = ''
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.row {
  display: flex;
  gap: 2rem;
}

.col-left { width: 320px; }
.col-right { flex: 1; }

.profile-card {
  text-align: center;
  padding: 3rem 2rem;
}

.avatar-large {
  width: 100px;
  height: 100px;
  background: var(--gradient-primary);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  font-weight: 700;
  color: white;
  margin: 0 auto 1.5rem;
}

.role-text {
  color: var(--text-secondary);
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
}

.status-badge {
  background: rgba(99, 102, 241, 0.1);
  color: var(--accent-primary);
  padding: 0.5rem 1rem;
  border-radius: 99px;
  font-size: 0.85rem;
  font-weight: 600;
  display: inline-block;
}

.settings-card h3 {
  margin-bottom: 2rem;
}

.settings-form {
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
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-secondary);
}

.helper-text {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.success-msg {
  color: var(--success);
  font-size: 0.9rem;
  margin-top: 1rem;
}

input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
