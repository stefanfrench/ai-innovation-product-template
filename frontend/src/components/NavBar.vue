<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <nav class="bg-cap-blue">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Text mark -->
        <RouterLink to="/" class="leading-tight">
          <span class="font-bold text-base tracking-tight block text-white">Capgemini Invent</span>
          <span class="font-light text-xs tracking-wide block text-white/60">AI Product Innovation</span>
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
            to="/examples"
            class="text-white/80 hover:text-white hover:bg-white/10 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            active-class="!text-white bg-white/15"
          >
            Examples
          </RouterLink>
        </div>
      </div>
    </div>
  </nav>
</template>
