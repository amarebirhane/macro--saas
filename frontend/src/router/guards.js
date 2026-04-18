import { useAuthStore } from '../stores/auth'

export const setupGuards = (router) => {
  router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore()
    
    // Recovery of session if token exists but user is null
    if (authStore.token && !authStore.user) {
      await authStore.fetchUser()
    }

    const isAuthenticated = authStore.isAuthenticated
    const userRole = authStore.user?.role

    // 1. Check if route requires authentication
    if (to.meta.requiresAuth && !isAuthenticated) {
      return next({ name: 'login', query: { redirect: to.fullPath } })
    }

    // 2. Check if route requires specific role (Admin)
    if (to.meta.requiresAdmin && userRole !== 'ADMIN') {
      return next({ name: 'error-403' })
    }

    // 3. Prevent logged-in users from accessing auth pages or Landing (optional)
    if (to.path.startsWith('/auth') && isAuthenticated) {
      return next({ name: 'dashboard' })
    }
    
    // Redirect to dashboard if logged in and trying to access landing
    if (to.name === 'landing' && isAuthenticated) {
      return next({ name: 'dashboard' })
    }

    next()
  })
}
