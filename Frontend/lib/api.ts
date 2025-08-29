import axios from "axios"

const API_BASE_URL = "http://localhost:8000"

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
})

export interface GenerateResponse {
  content: string
  image_url: string | null
}

export interface TrendsResponse {
  trends: string[]
}

export interface AnalyzeResponse {
  sentiment: number
  sentiment_label: string
}

export const contentApi = {
  generate: async (prompt: string, file?: string): Promise<GenerateResponse> => {
    const response = await api.post("/api/v1/content/generate", { prompt, file })
    return response.data
  },
}

export const trendsApi = {
  getTrends: async (): Promise<TrendsResponse> => {
    const response = await api.get("/api/v1/trends")
    return response.data
  },
}

export const analysisApi = {
  analyze: async (content: string): Promise<AnalyzeResponse> => {
    const response = await api.post("/api/v1/analysis", { content })
    return response.data
  },
}
