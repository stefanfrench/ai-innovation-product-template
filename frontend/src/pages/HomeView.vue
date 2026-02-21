<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <!-- Hero -->
    <div class="text-center py-12">
      <h1 class="text-4xl font-bold text-deep-purple mb-4">
        CapStack
      </h1>
      <p class="text-xl text-cap-blue mb-8 font-medium">
        AI Product Innovation Template
      </p>
      <p class="text-cap-gray-500 max-w-2xl mx-auto">
        A full-stack template with FastAPI, Vue 3, TypeScript, and the OpenAI SDK.
        Ready for AI-powered applications with WebSocket streaming.
      </p>
    </div>

    <!-- Feature Cards -->
    <div class="grid md:grid-cols-2 gap-6 mt-8">
      <RouterLink to="/chat" class="card border-l-4 border-l-vibrant-blue hover:shadow-md transition-shadow cursor-pointer">
        <div class="flex items-start space-x-4">
          <span class="text-3xl">💬</span>
          <div>
            <h2 class="text-lg font-semibold text-cap-gray-800">AI Chat</h2>
            <p class="text-cap-gray-500 mt-1">
              Try the LLM integration with real-time WebSocket streaming.
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
              Example database-backed API with full CRUD operations.
            </p>
          </div>
        </div>
      </RouterLink>

      <div class="card border-l-4 border-l-cap-blue">
        <div class="flex items-start space-x-4">
          <span class="text-3xl">🔌</span>
          <div>
            <h2 class="text-lg font-semibold text-cap-gray-800">API Docs</h2>
            <p class="text-cap-gray-500 mt-1">
              FastAPI auto-generated docs at
              <a href="/docs" class="text-vibrant-blue hover:underline">/docs</a>
            </p>
          </div>
        </div>
      </div>

      <div class="card border-l-4 border-l-cap-blue">
        <div class="flex items-start space-x-4">
          <span class="text-3xl">⚡</span>
          <div>
            <h2 class="text-lg font-semibold text-cap-gray-800">Quick Start</h2>
            <p class="text-cap-gray-500 mt-1">
              Run <code class="bg-cap-gray-100 px-2 py-1 rounded text-cap-blue-600 text-sm">docker compose up</code> to start everything.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Tech Stack -->
    <div class="mt-12 text-center">
      <h3 class="text-sm font-medium text-cap-gray-400 uppercase tracking-wider mb-4">
        Built With
      </h3>
      <div class="flex flex-wrap justify-center gap-3">
        <span class="px-3 py-1 bg-cap-blue-50 text-cap-blue-600 rounded-full text-sm font-medium">FastAPI</span>
        <span class="px-3 py-1 bg-cap-blue-50 text-cap-blue-600 rounded-full text-sm font-medium">Vue 3</span>
        <span class="px-3 py-1 bg-cap-blue-50 text-cap-blue-600 rounded-full text-sm font-medium">TypeScript</span>
        <span class="px-3 py-1 bg-cap-blue-50 text-cap-blue-600 rounded-full text-sm font-medium">OpenAI SDK</span>
        <span class="px-3 py-1 bg-cap-blue-50 text-cap-blue-600 rounded-full text-sm font-medium">Tailwind CSS</span>
        <span class="px-3 py-1 bg-cap-blue-50 text-cap-blue-600 rounded-full text-sm font-medium">SQLAlchemy</span>
        <span class="px-3 py-1 bg-cap-blue-50 text-cap-blue-600 rounded-full text-sm font-medium">Docker</span>
      </div>
    </div>
  </div>
</template>
