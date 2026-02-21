<script setup lang="ts">
import { ref } from 'vue'
import { useWebSocket } from '@/composables/useWebSocket'

const prompt = ref('')
const messages = ref<{ role: 'user' | 'assistant'; content: string }[]>([])
const currentResponse = ref('')

const { isConnected, send, connect } = useWebSocket('/api/llm/stream', {
  onMessage: (data) => {
    if (data.chunk) {
      currentResponse.value += data.chunk
    } else if (data.done) {
      messages.value.push({ role: 'assistant', content: currentResponse.value })
      currentResponse.value = ''
    } else if (data.error) {
      messages.value.push({ role: 'assistant', content: `Error: ${data.error}` })
      currentResponse.value = ''
    }
  },
})

// Auto-connect on mount
connect()

const sendMessage = () => {
  if (!prompt.value.trim() || !isConnected.value) return

  messages.value.push({ role: 'user', content: prompt.value })
  send({
    prompt: prompt.value,
    system_prompt: 'You are a helpful AI assistant.',
  })
  prompt.value = ''
}
</script>

<template>
  <div class="max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold text-gray-900 mb-6">💬 AI Chat</h1>

    <!-- Connection Status -->
    <div class="mb-4 flex items-center space-x-2">
      <span
        class="w-2 h-2 rounded-full"
        :class="isConnected ? 'bg-green-500' : 'bg-red-500'"
      ></span>
      <span class="text-sm text-gray-600">
        {{ isConnected ? 'Connected' : 'Disconnected' }}
      </span>
    </div>

    <!-- Messages -->
    <div class="card mb-4 h-96 overflow-y-auto space-y-4">
      <div v-if="messages.length === 0" class="text-center text-gray-400 py-12">
        Start a conversation with the AI
      </div>

      <div
        v-for="(message, index) in messages"
        :key="index"
        class="flex"
        :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
      >
        <div
          class="max-w-[80%] px-4 py-2 rounded-lg"
          :class="
            message.role === 'user'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-100 text-gray-900'
          "
        >
          <p class="whitespace-pre-wrap">{{ message.content }}</p>
        </div>
      </div>

      <!-- Streaming response -->
      <div v-if="currentResponse" class="flex justify-start">
        <div class="max-w-[80%] px-4 py-2 rounded-lg bg-gray-100 text-gray-900">
          <p class="whitespace-pre-wrap">{{ currentResponse }}</p>
          <span class="inline-block w-2 h-4 bg-gray-400 animate-pulse ml-1"></span>
        </div>
      </div>
    </div>

    <!-- Input -->
    <form @submit.prevent="sendMessage" class="flex space-x-4">
      <input
        v-model="prompt"
        type="text"
        placeholder="Type your message..."
        class="input flex-1"
        :disabled="!isConnected"
      />
      <button
        type="submit"
        class="btn btn-primary"
        :disabled="!isConnected || !prompt.trim()"
      >
        Send
      </button>
    </form>

    <p class="text-sm text-gray-500 mt-4">
      This uses WebSocket streaming via Azure OpenAI. Configure your LLM provider in the backend .env file.
    </p>
  </div>
</template>
