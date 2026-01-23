/**
 * Simple API client for making HTTP requests.
 * Works with the Vite proxy in development.
 */

class ApiClient {
  private baseUrl: string

  constructor(baseUrl = '') {
    this.baseUrl = baseUrl
  }

  private async request<T>(
    method: string,
    url: string,
    data?: unknown
  ): Promise<T> {
    const response = await fetch(`${this.baseUrl}${url}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: data ? JSON.stringify(data) : undefined,
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({}))
      throw new Error(error.detail || `HTTP ${response.status}`)
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return undefined as T
    }

    return response.json()
  }

  get<T>(url: string): Promise<T> {
    return this.request<T>('GET', url)
  }

  post<T>(url: string, data: unknown): Promise<T> {
    return this.request<T>('POST', url, data)
  }

  put<T>(url: string, data: unknown): Promise<T> {
    return this.request<T>('PUT', url, data)
  }

  delete<T>(url: string): Promise<T> {
    return this.request<T>('DELETE', url)
  }
}

export const api = new ApiClient()
