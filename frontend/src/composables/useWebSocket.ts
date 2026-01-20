import { ref, onUnmounted } from 'vue'

interface WebSocketOptions {
  onMessage?: (data: any) => void
  onError?: (error: Event) => void
  onClose?: () => void
  reconnect?: boolean
  reconnectDelay?: number
}

/**
 * WebSocket composable for real-time communication.
 * Handles connection, reconnection, and message parsing.
 *
 * Usage:
 * ```ts
 * const { isConnected, send, connect, disconnect } = useWebSocket('/api/llm/stream', {
 *   onMessage: (data) => console.log('Received:', data),
 * })
 * ```
 */
export function useWebSocket(url: string, options: WebSocketOptions = {}) {
  const {
    onMessage,
    onError,
    onClose,
    reconnect = true,
    reconnectDelay = 3000,
  } = options

  const isConnected = ref(false)
  const socket = ref<WebSocket | null>(null)

  let reconnectTimeout: ReturnType<typeof setTimeout> | null = null

  const getWebSocketUrl = (path: string): string => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.host
    return `${protocol}//${host}${path}`
  }

  const connect = () => {
    if (socket.value?.readyState === WebSocket.OPEN) return

    const wsUrl = getWebSocketUrl(url)
    socket.value = new WebSocket(wsUrl)

    socket.value.onopen = () => {
      isConnected.value = true
    }

    socket.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        onMessage?.(data)
      } catch {
        onMessage?.(event.data)
      }
    }

    socket.value.onerror = (error) => {
      onError?.(error)
    }

    socket.value.onclose = () => {
      isConnected.value = false
      onClose?.()

      // Auto-reconnect
      if (reconnect) {
        reconnectTimeout = setTimeout(connect, reconnectDelay)
      }
    }
  }

  const disconnect = () => {
    if (reconnectTimeout) {
      clearTimeout(reconnectTimeout)
      reconnectTimeout = null
    }
    socket.value?.close()
    socket.value = null
    isConnected.value = false
  }

  const send = (data: unknown) => {
    if (socket.value?.readyState === WebSocket.OPEN) {
      socket.value.send(JSON.stringify(data))
    }
  }

  // Cleanup on unmount
  onUnmounted(() => {
    disconnect()
  })

  return {
    isConnected,
    connect,
    disconnect,
    send,
  }
}
