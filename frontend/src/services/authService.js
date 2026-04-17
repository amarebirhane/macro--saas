import api from './api'

export default {
  login(credentials) {
    const params = new URLSearchParams()
    params.append('username', credentials.email)
    params.append('password', credentials.password)
    
    return api.post('/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  },
  register(userData) {
    return api.post('/auth/register', userData)
  },
  getMe() {
    return api.get('/auth/me')
  }
}
