import axios from 'axios'

const BASE = '/api'

export const api = {
  async getAutomata() {
    const { data } = await axios.get(`${BASE}/automatas`)
    return data
  },

  async getDefinition(key) {
    const { data } = await axios.get(`${BASE}/automatas/${key}`)
    return data
  },

  async simulate(key, tokens) {
    const { data } = await axios.post(`${BASE}/simulate/${key}`, { tokens })
    return data
  }
}
