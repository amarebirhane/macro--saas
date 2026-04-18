import api from './api'

export const authService = {
  async login(credentials) {
    // We now use a JSON payload for LoginRequest
    // 'credentials' already contains { username_or_email, password } from the store/component
    const response = await api.post('/auth/login', credentials)
    return response.data
  },

  async register(userData) {
    const response = await api.post('/auth/register', userData)
    return response.data
  },

  async getMe() {
    const response = await api.get('/auth/me')
    return response.data
  },

  async refreshToken(refreshToken) {
    const response = await api.post('/auth/refresh', { refresh_token: refreshToken })
    return response.data
  }
}
