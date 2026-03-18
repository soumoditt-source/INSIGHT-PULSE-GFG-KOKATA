// API Service Layer for InsightPulse AI
// This service handles all backend communication

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export class APIClient {
  private baseURL: string

  constructor(baseURL = API_BASE) {
    this.baseURL = baseURL
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const cleanBase = this.baseURL.endsWith('/') ? this.baseURL.slice(0, -1) : this.baseURL
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`
    const url = `${cleanBase}${cleanEndpoint}`
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      })

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`)
      }

      return response.json()
    } catch (error) {
      console.error('API Request Error:', error)
      throw error
    }
  }

  // Data Management
  async uploadDataset(file: File): Promise<{ datasetId: string }> {
    const formData = new FormData()
    formData.append('file', file)

    const res = await fetch(`${this.baseURL}/upload`, {
      method: 'POST',
      body: formData,
    })
    return res.json()
  }

  async getDatasetInfo() {
    return this.request('/health') // We don't have a dataset info by ID, we have global state
  }

  // Chat/Query
  async generateQuery(query: string, session_id?: string) {
    return this.request('/generate', {
      method: 'POST',
      body: JSON.stringify({ query, session_id }),
    })
  }

  // ML Analysis
  async analyzeWithML(task: string = "auto") {
    return this.request('/analyze', {
      method: 'POST',
      body: JSON.stringify({ task }),
    })
  }

  // Data Profiling
  async profileDataset() {
    return this.request('/profile')
  }

  // Visualization
  async getVisualization() {
    // Backend doesn't have a specific viz endpoint by ID yet, use analyze or generate
    return this.request('/analyze', { method: 'POST', body: JSON.stringify({ task: 'auto' }) })
  }

  // Status
  async getSystemStatus() {
    return this.request('/health')
  }

  async getProfile() {
    return this.request('/profile')
  }

  async getDistributions() {
    return this.request('/distributions')
  }
  async getForecast() {
    return this.request('/forecast')
  }
  async runMLAnalysis(task: string = "auto") {
    return this.request('/analyze', {
      method: 'POST',
      body: JSON.stringify({ task }),
    })
  }
}

// Singleton instance
export const apiClient = new APIClient()
