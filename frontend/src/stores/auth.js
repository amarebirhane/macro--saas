import { defineStore } from 'pinia'
import { authService } from '../services/authService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    loading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === 'ADMIN',
    currentUser: (state) => state.user
  },

  actions: {
    async login(credentials) {
      this.loading = true
      this.error = null
      try {
        const data = await authService.login(credentials)
        this.token = data.access_token
        localStorage.setItem('token', this.token)
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
        // Auto login after registration
        return await this.login({ email: userData.email, password: userData.password })
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
        this.logout()
      }
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    }
  }
})
