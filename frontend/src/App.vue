<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
</script>

<template>
  <div class="min-h-screen">
    <NavBar />
    <main class="container mx-auto px-4 py-8 pb-20">
      <RouterView />
    </main>
    <!-- Logo watermark -->
    <div class="fixed bottom-4 right-4 opacity-40 hover:opacity-70 transition-opacity">
      <img src="/cap-logo.png" alt="Capgemini" class="w-10 h-10" />
    </div>
  </div>
</template>
