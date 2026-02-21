<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <!-- Hero -->
    <div class="text-center py-12">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">
        🚀 CapStack
      </h1>
      <p class="text-xl text-gray-600 mb-8">
        AI Product Innovation Template
      </p>
      <p class="text-gray-500 max-w-2xl mx-auto">
        A full-stack template with FastAPI, Vue 3, TypeScript, and the OpenAI SDK.
        Ready for AI-powered applications with WebSocket streaming.
      </p>
    </div>

    <!-- Feature Cards -->
    <div class="grid md:grid-cols-2 gap-6 mt-8">
      <RouterLink to="/chat" class="card hover:shadow-md transition-shadow cursor-pointer">
        <div class="flex items-start space-x-4">
          <span class="text-3xl">💬</span>
          <div>
            <h2 class="text-lg font-semibold text-gray-900">AI Chat</h2>
            <p class="text-gray-600 mt-1">
              Try the LLM integration with real-time WebSocket streaming.
            </p>
          </div>
        </div>
      </RouterLink>

      <RouterLink to="/items" class="card hover:shadow-md transition-shadow cursor-pointer">
        <div class="flex items-start space-x-4">
          <span class="text-3xl">📦</span>
          <div>
            <h2 class="text-lg font-semibold text-gray-900">Items CRUD</h2>
            <p class="text-gray-600 mt-1">
              Example database-backed API with full CRUD operations.
            </p>
          </div>
        </div>
      </RouterLink>

      <div class="card">
        <div class="flex items-start space-x-4">
          <span class="text-3xl">🔌</span>
          <div>
            <h2 class="text-lg font-semibold text-gray-900">API Docs</h2>
            <p class="text-gray-600 mt-1">
              FastAPI auto-generated docs at
              <a href="/docs" class="text-primary-600 hover:underline">/docs</a>
            </p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-start space-x-4">
          <span class="text-3xl">⚡</span>
          <div>
            <h2 class="text-lg font-semibold text-gray-900">Quick Start</h2>
            <p class="text-gray-600 mt-1">
              Run <code class="bg-gray-100 px-2 py-1 rounded">docker compose up</code> to start everything.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Tech Stack -->
    <div class="mt-12 text-center">
      <h3 class="text-sm font-medium text-gray-500 uppercase tracking-wider mb-4">
        Built With
      </h3>
      <div class="flex flex-wrap justify-center gap-3">
        <span class="px-3 py-1 bg-gray-100 rounded-full text-sm text-gray-700">FastAPI</span>
        <span class="px-3 py-1 bg-gray-100 rounded-full text-sm text-gray-700">Vue 3</span>
        <span class="px-3 py-1 bg-gray-100 rounded-full text-sm text-gray-700">TypeScript</span>
        <span class="px-3 py-1 bg-gray-100 rounded-full text-sm text-gray-700">OpenAI SDK</span>
        <span class="px-3 py-1 bg-gray-100 rounded-full text-sm text-gray-700">Tailwind CSS</span>
        <span class="px-3 py-1 bg-gray-100 rounded-full text-sm text-gray-700">SQLAlchemy</span>
        <span class="px-3 py-1 bg-gray-100 rounded-full text-sm text-gray-700">Docker</span>
      </div>
    </div>
  </div>
</template>
