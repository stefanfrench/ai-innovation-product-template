<script setup lang="ts">
defineProps<{
  variant?: 'light' | 'dark'
}>()
</script>

<template>
  <div class="flex items-center space-x-3">
    <img src="/cap-logo.png" alt="Capgemini" class="w-9 h-9 flex-shrink-0" />
    <div class="leading-tight">
      <span
        class="font-bold text-base tracking-tight block"
        :class="variant === 'dark' ? 'text-cap-blue' : 'text-white'"
      >Capgemini Invent</span>
      <span
        class="font-light text-xs tracking-wide block"
        :class="variant === 'dark' ? 'text-cap-gray-500' : 'text-white/60'"
      >AI Product Innovation</span>
    </div>
  </div>
</template>
