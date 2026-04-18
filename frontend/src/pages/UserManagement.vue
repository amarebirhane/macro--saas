<template>
  <div class="user-management fade-in">
    <div class="table-card card">
      <div class="header">
        <div class="title-area">
          <h3>System Users</h3>
          <p v-if="!loading">Total: {{ users.length }} users registered</p>
          <div v-else class="skeleton skeleton-text"></div>
        </div>
        <div class="search-area">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Search by name, username, or email..." 
            class="search-input"
          />
        </div>
      </div>
      
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>User</th>
              <th>Username</th>
              <th>Role</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody v-if="loading">
            <tr v-for="i in 5" :key="i">
              <td><div class="skeleton skeleton-user-cell"></div></td>
              <td><div class="skeleton skeleton-username"></div></td>
              <td><div class="skeleton skeleton-badge"></div></td>
              <td><div class="skeleton skeleton-status"></div></td>
              <td><div class="skeleton skeleton-actions"></div></td>
            </tr>
          </tbody>
          <tbody v-else-if="filteredUsers.length > 0">
            <tr v-for="user in filteredUsers" :key="user.id" class="user-row">
              <td class="user-cell">
                <div class="user-info">
                  <div class="mini-avatar">{{ getInitials(user) }}</div>
                  <div class="name-email">
                    <span class="full-name">{{ user.first_name }} {{ user.last_name }}</span>
                    <span class="email-sub">{{ user.email }}</span>
                  </div>
                </div>
              </td>
              <td>
                <span class="username-cell">@{{ user.username || '—' }}</span>
              </td>
              <td>
                <span class="badge" :class="user.role">{{ user.role }}</span>
              </td>
              <td>
                <div class="status-cell">
                  <span :class="user.is_active ? 'active-dot' : 'inactive-dot'"></span>
                  {{ user.is_active ? 'Active' : 'Suspended' }}
                </div>
              </td>
              <td class="actions">
                <button 
                  @click="toggleStatus(user)" 
                  class="btn-icon" 
                  :title="user.is_active ? 'Suspend' : 'Activate'"
                  :disabled="actionLoading === user.id"
                >
                  <span v-if="actionLoading === user.id" class="small-spinner"></span>
                  <span v-else>{{ user.is_active ? '🚫' : '✅' }}</span>
                </button>
                <button 
                  @click="deleteUser(user.id)" 
                  class="btn-icon delete" 
                  title="Delete User"
                  :disabled="actionLoading === user.id"
                >
                  🗑️
                </button>
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr>
              <td colspan="5" class="empty-state">
                <div class="empty-content">
                  <span>🛰️</span>
                  <p>No users found matching your search</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'
import { useToast } from '../composables/useToast'

const users = ref([])
const loading = ref(true)
const searchQuery = ref('')
const actionLoading = ref(null)
const toast = useToast()

const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value
  const q = searchQuery.value.toLowerCase()
  return users.value.filter(u => 
    u.email.toLowerCase().includes(q) || 
    u.username?.toLowerCase().includes(q) ||
    u.first_name?.toLowerCase().includes(q) ||
    u.last_name?.toLowerCase().includes(q) ||
    u.id.toLowerCase().includes(q)
  )
})

const getInitials = (user) => {
  if (user.first_name && user.last_name) {
    return `${user.first_name[0]}${user.last_name[0]}`.toUpperCase()
  }
  return user.email[0].toUpperCase()
}

const fetchUsers = async () => {
  loading.value = true
  try {
    const response = await api.get('/admin/users')
    // The backend now returns PaginatedResponse, we need to handle res.data.items or check if it's still returning list
    // Based on previous finalization, /admin/users returns PaginatedResponse
    if (response.data && response.data.items) {
      users.value = response.data.items
    } else {
      users.value = response.data
    }
  } catch (err) {
    toast.error('Failed to fetch users')
    console.error(err)
  } finally {
    loading.value = false
  }
}

const toggleStatus = async (user) => {
  actionLoading.value = user.id
  try {
    const newStatus = !user.is_active
    await api.put(`/admin/users/${user.id}`, { is_active: newStatus })
    user.is_active = newStatus
    toast.success(`User ${newStatus ? 'activated' : 'suspended'} successfully`)
  } catch (err) {
    toast.error('Failed to update user status')
    console.error(err)
  } finally {
    actionLoading.value = null
  }
}

const deleteUser = async (user_id) => {
  if (!confirm('Are you sure you want to permanently delete this user?')) return
  
  actionLoading.value = user_id
  try {
    await api.delete(`/admin/users/${user_id}`)
    users.value = users.value.filter(u => u.id !== user_id)
    toast.success('User deleted successfully')
  } catch (err) {
    toast.error('Failed to delete user')
    console.error(err)
  } finally {
    actionLoading.value = null
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2rem;
  gap: 1rem;
}

.title-area h3 {
  margin-bottom: 0.25rem;
}

.title-area p {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.search-input {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  padding: 0.6rem 1rem;
  border-radius: 8px;
  width: 350px;
  font-size: 0.9rem;
}

.search-input:focus {
  border-color: var(--accent-primary);
  outline: none;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  text-align: left;
  padding: 1rem;
  color: var(--text-secondary);
  font-size: 0.85rem;
  text-transform: uppercase;
  border-bottom: 1px solid var(--border);
  letter-spacing: 0.05em;
}

td {
  padding: 1rem;
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
}

.user-row:hover {
  background: rgba(255, 255, 255, 0.02);
}

.user-cell {
  min-width: 250px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.mini-avatar {
  width: 36px;
  height: 36px;
  background: var(--gradient-primary);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.name-email {
  display: flex;
  flex-direction: column;
}

.full-name {
  font-weight: 600;
  font-size: 0.95rem;
}

.email-sub {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.username-cell {
  font-weight: 600;
  color: var(--accent-primary);
  font-size: 0.9rem;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
}

.badge.ADMIN { background: rgba(239, 68, 68, 0.1); color: var(--error); border: 1px solid rgba(239, 68, 68, 0.2); }
.badge.USER { background: rgba(16, 185, 129, 0.1); color: var(--success); border: 1px solid rgba(16, 185, 129, 0.2); }

.status-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.active-dot, .inactive-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.active-dot { background: var(--success); box-shadow: 0 0 8px var(--success); }
.inactive-dot { background: var(--error); }

.actions {
  display: flex;
  gap: 0.75rem;
}

.btn-icon {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-icon:hover:not(:disabled) {
  background: var(--border);
  transform: translateY(-2px);
}

.btn-icon.delete:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.1);
  border-color: var(--error);
}

.btn-icon:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.small-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255,255,255,0.2);
  border-top-color: var(--text-primary);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  padding: 4rem 1rem;
  text-align: center;
}

.empty-content span { font-size: 3rem; margin-bottom: 1rem; display: block; }
.empty-content p { color: var(--text-secondary); }

/* Skeletons */
.skeleton {
  background: linear-gradient(90deg, var(--bg-secondary) 25%, var(--border) 50%, var(--bg-secondary) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skeleton-text { height: 1rem; width: 100px; }
.skeleton-user-cell { height: 2.5rem; width: 200px; }
.skeleton-username { height: 1.25rem; width: 80px; }
.skeleton-badge { height: 1.5rem; width: 60px; border-radius: 6px; }
.skeleton-status { height: 1.25rem; width: 90px; }
.skeleton-actions { height: 2.25rem; width: 80px; border-radius: 8px; }
</style>
