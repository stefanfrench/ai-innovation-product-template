import { describe, it, expect, vi, beforeEach } from 'vitest'
import { api } from '@/composables/useApi'

describe('ApiClient', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('makes GET requests and returns JSON', async () => {
    const mockData = [{ id: 1, name: 'Test' }]
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: true,
      status: 200,
      json: () => Promise.resolve(mockData),
    } as Response)

    const result = await api.get('/api/items')

    expect(fetch).toHaveBeenCalledWith('/api/items', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      body: undefined,
    })
    expect(result).toEqual(mockData)
  })

  it('throws on non-ok responses', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: false,
      status: 404,
      json: () => Promise.resolve({ detail: 'Not found' }),
    } as Response)

    await expect(api.get('/api/items/999')).rejects.toThrow('Not found')
  })

  it('handles 204 No Content', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: true,
      status: 204,
      json: () => Promise.resolve(null),
    } as Response)

    const result = await api.delete('/api/items/1')

    expect(result).toBeUndefined()
  })
})
