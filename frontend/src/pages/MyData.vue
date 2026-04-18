<template>
  <div class="my-data-page fade-in">
    <div class="header-card card glass">
      <div class="info">
        <h3>Your Data Storage</h3>
        <p>Manage and export your personal application data.</p>
      </div>
      <button class="btn btn-primary" @click="handleExport">Export All Data</button>
    </div>

    <div class="data-grid">
      <div class="data-section card">
        <h4>Stored Information</h4>
        <div class="data-row">
          <span class="label">Email</span>
          <span class="value">{{ authStore.user?.email }}</span>
        </div>
        <div class="data-row">
          <span class="label">Member Since</span>
          <span class="value">{{ formattedDate }}</span>
        </div>
        <div class="data-row">
          <span class="label">Role</span>
          <span class="value">{{ authStore.user?.role }}</span>
        </div>
      </div>

      <div class="data-section card">
        <h4>Privacy Settings</h4>
        <div class="toggle-group">
          <div class="toggle-item">
            <div class="text">
              <p class="title">Public Profile</p>
              <p class="desc">Allow others to see your stats</p>
            </div>
            <div class="toggle disabled"></div>
          </div>
          <div class="toggle-item">
            <div class="text">
              <p class="title">Data Analytics</p>
              <p class="desc">Share anonymous usage data</p>
            </div>
            <div class="toggle active"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const formattedDate = computed(() => {
  if (!authStore.user?.created_at) return 'N/A'
  return new Date(authStore.user.created_at).toLocaleDateString()
})

const handleExport = () => {
  alert('Exporting your data... This will take a few moments.')
}
</script>

<style scoped>
.my-data-page {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.header-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2.5rem;
}

.data-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.data-section h4 {
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
}

.data-row {
  display: flex;
  justify-content: space-between;
  padding: 1rem 0;
  border-bottom: 1px solid var(--border);
}

.data-row .label { color: var(--text-secondary); }
.data-row .value { font-weight: 500; }

.toggle-group {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.toggle-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.toggle-item .title { font-weight: 500; }
.toggle-item .desc { font-size: 0.85rem; color: var(--text-secondary); }

.toggle {
  width: 44px;
  height: 22px;
  background: var(--border);
  border-radius: 99px;
  position: relative;
  cursor: pointer;
}

.toggle::after {
  content: '';
  position: absolute;
  top: 3px;
  left: 3px;
  width: 16px;
  height: 16px;
  background: white;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.toggle.active {
  background: var(--accent-primary);
}

.toggle.active::after {
  left: 25px;
}
</style>
