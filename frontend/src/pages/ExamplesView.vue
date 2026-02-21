<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-deep-purple mb-2">Template Examples</h1>
      <p class="text-cap-gray-500">
        Working examples included in the template. Use them as reference when building your own features, then remove this route when you no longer need it.
      </p>
    </div>

    <div class="grid md:grid-cols-2 gap-6">
      <RouterLink to="/chat" class="card border-l-4 border-l-vibrant-blue hover:shadow-md transition-shadow cursor-pointer">
        <div class="flex items-start space-x-4">
          <span class="text-3xl">💬</span>
          <div>
            <h2 class="text-lg font-semibold text-cap-gray-800">AI Chat</h2>
            <p class="text-cap-gray-500 mt-1">
              LLM integration with real-time WebSocket streaming.
            </p>
            <p class="text-xs text-cap-gray-400 mt-2">
              Demonstrates: OpenAI SDK, WebSocket composable, streaming UI
            </p>
          </div>
        </div>
      </RouterLink>

      <RouterLink to="/items" class="card border-l-4 border-l-vibrant-blue hover:shadow-md transition-shadow cursor-pointer">
        <div class="flex items-start space-x-4">
          <span class="text-3xl">📦</span>
          <div>
            <h2 class="text-lg font-semibold text-cap-gray-800">Items CRUD</h2>
            <p class="text-cap-gray-500 mt-1">
              Database-backed API with create, read, and delete operations.
            </p>
            <p class="text-xs text-cap-gray-400 mt-2">
              Demonstrates: TanStack Query, REST API, SQLAlchemy models
            </p>
          </div>
        </div>
      </RouterLink>
    </div>
  </div>
</template>
