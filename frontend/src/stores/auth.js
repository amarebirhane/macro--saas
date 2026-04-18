import { defineStore } from 'pinia'
import { authService } from '../services/authService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || sessionStorage.getItem('token') || null,
    refreshToken: localStorage.getItem('refresh_token') || sessionStorage.getItem('refresh_token') || null,
    loading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === 'ADMIN',
    currentUser: (state) => state.user
  },

  actions: {
    async login(credentials, rememberMe = false) {
      this.loading = true
      this.error = null
      try {
        const payload = {
          username_or_email: credentials.email || credentials.username_or_email,
          password: credentials.password
        }
        const data = await authService.login(payload)
        this.token = data.access_token
        this.refreshToken = data.refresh_token
        
        const storage = rememberMe ? localStorage : sessionStorage
        const other = rememberMe ? sessionStorage : localStorage
        
        storage.setItem('token', this.token)
        storage.setItem('refresh_token', this.refreshToken)
        
        other.removeItem('token')
        other.removeItem('refresh_token')
        
        await this.fetchUser()
        return true
      } catch (err) {
        this.error = err.response?.data?.detail || 'Login failed'
        throw err
      } finally {
        this.loading = false
      }
    },

    async register(userData) {
      this.loading = true
      this.error = null
      try {
        await authService.register(userData)
        // Auto login after registration (session only by default)
        return await this.login({ email: userData.email, password: userData.password }, false)
      } catch (err) {
        this.error = err.response?.data?.detail || 'Registration failed'
        throw err
      } finally {
        this.loading = false
      }
    },

    async fetchUser() {
      if (!this.token) return
      try {
        const data = await authService.getMe()
        this.user = data
      } catch (err) {
        // If fetchUser fails, we might still have a chance with refresh
        console.warn('Failed to fetch user, might be expired.')
      }
    },

    async refreshSession() {
      if (!this.refreshToken) throw new Error('No refresh token available')
      
      try {
        const data = await authService.refreshToken(this.refreshToken)
        this.token = data.access_token
        this.refreshToken = data.refresh_token
        
        // Persist to whichever storage was used
        const storage = localStorage.getItem('refresh_token') ? localStorage : sessionStorage
        storage.setItem('token', this.token)
        storage.setItem('refresh_token', this.refreshToken)
        
        return this.token
      } catch (err) {
        this.logout()
        throw err
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.refreshToken = null
      localStorage.removeItem('token')
      localStorage.removeItem('refresh_token')
      sessionStorage.removeItem('token')
      sessionStorage.removeItem('refresh_token')
    }
  }
})
