import { defineStore } from 'pinia'
import { authService } from '../services/authService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || sessionStorage.getItem('token') || null,
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
        
        if (rememberMe) {
          localStorage.setItem('token', this.token)
          sessionStorage.removeItem('token')
        } else {
          sessionStorage.setItem('token', this.token)
          localStorage.removeItem('token')
        }
        
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
        this.logout()
      }
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
      sessionStorage.removeItem('token')
    }
  }
})
