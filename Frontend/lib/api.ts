import axios from "axios"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"

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

export const contentApi = {
  generate: async (prompt: string, file?: string): Promise<GenerateResponse> => {
    const response = await api.post("/api/v1/content/generate", { prompt, file })
    return response.data
  },
}
