<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <nav class="bg-white border-b border-gray-200">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center space-x-2">
          <span class="text-2xl">🚀</span>
          <span class="font-bold text-xl text-gray-900">CapStack</span>
        </RouterLink>

        <!-- Navigation Links -->
        <div class="flex items-center space-x-4">
          <RouterLink
            to="/"
            class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
            active-class="text-primary-600 bg-primary-50"
          >
            Home
          </RouterLink>
          <RouterLink
            to="/chat"
            class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
            active-class="text-primary-600 bg-primary-50"
          >
            AI Chat
          </RouterLink>
          <RouterLink
            to="/items"
            class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
            active-class="text-primary-600 bg-primary-50"
          >
            Items
          </RouterLink>
        </div>
      </div>
    </div>
  </nav>
</template>
