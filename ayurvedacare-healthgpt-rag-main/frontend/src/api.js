import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const chatAPI = {
  sendMessage: async (query) => {
    const response = await api.post('/chat', { query })
    return response.data
  },

  getStatus: async () => {
    const response = await api.get('/status')
    return response.data
  },
}

export default api
