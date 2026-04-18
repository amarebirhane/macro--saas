import api from './api'

export const authService = {
  async login(credentials) {
    // Standard OAuth2 Form Data for FastAPI
    const formData = new URLSearchParams()
    formData.append('username', credentials.email)
    formData.append('password', credentials.password)
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    return response.data
  },

  async register(userData) {
    const response = await api.post('/auth/register', userData)
    return response.data
  },

  async getMe() {
    const response = await api.get('/auth/me')
    return response.data
  }
}
