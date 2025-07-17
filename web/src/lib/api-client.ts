import axios from 'axios'
import type { AnalyzeResponse, ErrorAnalyzeResponse, VisualizeResponse } from './api-types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

export interface AnalyzeCodeRequest {
  code: string
  options?: Record<string, unknown>
}

export interface VisualizeCodeRequest {
  code: string
  highlight_line?: number
  show_flow?: boolean
}

export interface AnalyzeErrorRequest {
  code: string
  error_message: string
}

export const api = {
  async analyzeCode(request: AnalyzeCodeRequest): Promise<AnalyzeResponse> {
    const res = await apiClient.post<AnalyzeResponse>('/api/v1/analyze', request)
    return res.data
  },

  async visualizeCode(request: VisualizeCodeRequest): Promise<VisualizeResponse> {
    const res = await apiClient.post<VisualizeResponse>('/api/v1/visualize', request)
    return res.data
  },

  async analyzeError(request: AnalyzeErrorRequest): Promise<ErrorAnalyzeResponse> {
    const res = await apiClient.post<ErrorAnalyzeResponse>('/api/v1/analyze-error', request)
    return res.data
  },
}
