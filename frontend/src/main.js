import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Global Error Handler for Resilience
app.config.errorHandler = (err, instance, info) => {
  console.error('[Global Error]:', err)
  console.error('[Component Info]:', info)
  
  // Attempt to show a toast if possible
  try {
    const { useToast } = import.meta.glob('./composables/useToast.js', { eager: true })['./composables/useToast.js']
    const toast = useToast()
    toast.error('An unexpected UI error occurred. Please refresh if issues persist.')
  } catch (e) {
    // Fallback if toast system isn't ready
  }
}

app.mount('#app')
