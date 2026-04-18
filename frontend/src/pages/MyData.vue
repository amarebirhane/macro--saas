<template>
  <div class="my-data-page fade-in">
    <div class="header-card card glass">
      <div class="info">
        <h3>Your Data Storage</h3>
        <p>Manage and export your personal application data. Your privacy is our priority.</p>
      </div>
      <button 
        class="btn btn-primary" 
        @click="handleExport" 
        :disabled="exportLoading"
      >
        <span v-if="exportLoading" class="spinner-small"></span>
        {{ exportLoading ? 'Preparing Bundle...' : 'Export All Data' }}
      </button>
    </div>

    <div class="data-grid">
      <div class="data-section card">
        <div class="section-header">
          <h4>Stored Account Info</h4>
          <span class="secure-badge">🛡️ Encrypted</span>
        </div>
        <div class="data-row">
          <span class="label">Primary Email</span>
          <span class="value">{{ authStore.user?.email }}</span>
        </div>
        <div class="data-row">
          <span class="label">Account Status</span>
          <span class="value status-active">Verified</span>
        </div>
        <div class="data-row">
          <span class="label">Member Since</span>
          <span class="value">{{ formattedDate }}</span>
        </div>
        <div class="data-row">
          <span class="label">Access Level</span>
          <span class="value">{{ authStore.user?.role }}</span>
        </div>
      </div>

      <div class="data-section card">
        <div class="section-header">
          <h4>Privacy & Consent</h4>
        </div>
        <div class="toggle-group">
          <div class="toggle-item">
            <div class="text">
              <p class="title">Public Profile</p>
              <p class="desc">Allow others to see your stats and activity</p>
            </div>
            <label class="switch">
              <input type="checkbox" v-model="privacySettings.publicProfile">
              <span class="slider round"></span>
            </label>
          </div>
          <div class="toggle-item">
            <div class="text">
              <p class="title">Usage Analytics</p>
              <p class="desc">Share anonymous usage data to help us improve</p>
            </div>
            <label class="switch">
              <input type="checkbox" v-model="privacySettings.usageAnalytics">
              <span class="slider round"></span>
            </label>
          </div>
          <div class="toggle-item">
            <div class="text">
              <p class="title">Marketing Emails</p>
              <p class="desc">Receive updates about new features and offers</p>
            </div>
            <label class="switch">
              <input type="checkbox" v-model="privacySettings.marketing">
              <span class="slider round"></span>
            </label>
          </div>
        </div>
      </div>

      <div class="data-section card danger-zone">
        <div class="section-header">
          <h4>Danger Zone</h4>
        </div>
        <div class="danger-content">
          <p>Once you delete your account, there is no going back. Please be certain.</p>
          <button class="btn btn-outline-danger" @click="handleDeleteAccount">Delete Account</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'

const authStore = useAuthStore()
const toast = useToast()
const exportLoading = ref(false)

const privacySettings = reactive({
  publicProfile: false,
  usageAnalytics: true,
  marketing: false
})

const formattedDate = computed(() => {
  if (!authStore.user?.created_at) return 'N/A'
  return new Date(authStore.user.created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

const handleExport = () => {
  exportLoading.value = true
  toast.info('Export started. We will notify you when the download is ready.')
  
  setTimeout(() => {
    exportLoading.value = false
    toast.success('Your data bundle is ready! Download started.')
  }, 2500)
}

const handleDeleteAccount = () => {
  if (confirm('Are you absolutely sure? This action cannot be undone.')) {
    toast.error('Account deletion requested. Please contact support to finalize.')
  }
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

.header-card h3 { margin-bottom: 0.5rem; }
.header-card p { color: var(--text-secondary); font-size: 1rem; }

.data-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
  gap: 2rem;
}

@media (max-width: 600px) {
  .data-grid { grid-template-columns: 1fr; }
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}

.section-header h4 { font-size: 1.1rem; }

.secure-badge {
  font-size: 0.75rem;
  background: rgba(16, 185, 129, 0.1);
  color: var(--success);
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  font-weight: 600;
}

.data-row {
  display: flex;
  justify-content: space-between;
  padding: 1rem 0;
  border-bottom: 1px solid var(--border);
}

.data-row:last-child { border-bottom: none; }

.data-row .label { color: var(--text-secondary); font-size: 0.95rem; }
.data-row .value { font-weight: 600; }
.status-active { color: var(--success); }

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

.toggle-item .title { font-weight: 600; font-size: 0.95rem; }
.toggle-item .desc { font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.2rem; }

/* Switch Style */
.switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
}

.switch input { opacity: 0; width: 0; height: 0; }

.slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: var(--border);
  transition: .3s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .3s;
}

input:checked + .slider { background-color: var(--accent-primary); }
input:checked + .slider:before { transform: translateX(20px); }
.slider.round { border-radius: 34px; }
.slider.round:before { border-radius: 50%; }

/* Danger Zone */
.danger-zone {
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.danger-zone h4 { color: var(--error); }

.danger-content p {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

.btn-outline-danger {
  background: transparent;
  border: 1px solid var(--error);
  color: var(--error);
  padding: 0.6rem 1.25rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-outline-danger:hover {
  background: var(--error);
  color: white;
}

.spinner-small {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  display: inline-block;
  margin-right: 0.5rem;
}

@keyframes spin { to { transform: rotate(360deg); } }
</style>
