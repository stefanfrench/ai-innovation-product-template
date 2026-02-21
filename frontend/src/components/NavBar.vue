<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <nav class="bg-cap-blue">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center space-x-2">
          <span class="font-bold text-xl text-white tracking-tight">CapStack</span>
          <span class="text-vibrant-blue-200 text-sm font-light hidden sm:inline">| AI Product Innovation</span>
        </RouterLink>

        <!-- Navigation Links -->
        <div class="flex items-center space-x-1">
          <RouterLink
            to="/"
            class="text-white/80 hover:text-white hover:bg-white/10 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            active-class="!text-white bg-white/15"
          >
            Home
          </RouterLink>
          <RouterLink
            to="/chat"
            class="text-white/80 hover:text-white hover:bg-white/10 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            active-class="!text-white bg-white/15"
          >
            AI Chat
          </RouterLink>
          <RouterLink
            to="/items"
            class="text-white/80 hover:text-white hover:bg-white/10 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            active-class="!text-white bg-white/15"
          >
            Items
          </RouterLink>
        </div>
      </div>
    </div>
  </nav>
</template>
