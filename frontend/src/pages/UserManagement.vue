<template>
  <div class="user-management fade-in">
    <div class="table-card card">
      <div class="header">
        <h3>System Users</h3>
        <p>Total: {{ users.length }} users registered</p>
      </div>
      
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td class="id-cell">#{{ user.id.slice(0, 8) }}</td>
              <td>{{ user.email }}</td>
              <td>
                <span class="badge" :class="user.role">{{ user.role }}</span>
              </td>
              <td>
                <span :class="user.is_active ? 'active-dot' : 'inactive-dot'"></span>
                {{ user.is_active ? 'Active' : 'Suspended' }}
              </td>
              <td class="actions">
                <button @click="toggleStatus(user)" class="btn-icon">
                  {{ user.is_active ? '🚫' : '✅' }}
                </button>
                <button @click="deleteUser(user.id)" class="btn-icon">🗑️</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const users = ref([])

const fetchUsers = async () => {
  try {
    const response = await api.get('/admin/users')
    users.value = response.data
  } catch (err) {
    console.error(err)
  }
}

const toggleStatus = async (user) => {
  try {
    const newStatus = !user.is_active
    await api.put(`/admin/users/${user.id}`, { is_active: newStatus })
    user.is_active = newStatus
  } catch (err) {
    console.error(err)
  }
}

const deleteUser = async (user_id) => {
  if (!confirm('Are you sure you want to delete this user?')) return
  try {
    await api.delete(`/admin/users/${user_id}`)
    users.value = users.value.filter(u => u.id !== user_id)
  } catch (err) {
    console.error(err)
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
.header {
  margin-bottom: 2rem;
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
}

td {
  padding: 1rem;
  border-bottom: 1px solid var(--border);
}

.id-cell {
  font-family: monospace;
  color: var(--text-secondary);
}

.badge {
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 700;
}

.badge.ADMIN { background: rgba(239, 68, 68, 0.1); color: var(--error); }
.badge.USER { background: rgba(16, 185, 129, 0.1); color: var(--success); }

.active-dot, .inactive-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 0.5rem;
}

.active-dot { background: var(--success); }
.inactive-dot { background: var(--error); }

.actions {
  display: flex;
  gap: 0.5rem;
}

.btn-icon {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-icon:hover {
  background: var(--border);
}
</style>
