<script setup lang="ts">
import { RouterLink } from 'vue-router'
import CapgeminiLogo from '@/components/CapgeminiLogo.vue'
</script>

<template>
  <div class="max-w-3xl mx-auto text-center py-20">
    <!-- Logo -->
    <div class="flex justify-center mb-8">
      <CapgeminiLogo variant="dark" />
    </div>

    <!-- Hero -->
    <h1 class="text-5xl font-bold text-deep-purple mb-6 tracking-tight">
      Your Product Name
    </h1>
    <p class="text-xl text-cap-gray-500 mb-10 max-w-xl mx-auto leading-relaxed">
      A short description of what your AI-powered product does.
      Replace this text with your own.
    </p>

    <!-- CTA -->
    <RouterLink to="/examples" class="btn btn-primary text-lg px-8 py-3">
      View Template Examples
    </RouterLink>

    <!-- Footer note -->
    <p class="mt-16 text-sm text-cap-gray-400">
      Built with the
      <a
        href="https://github.com/your-org/ai-innovation-product-template"
        target="_blank"
        class="text-vibrant-blue hover:underline"
      >AI Product Innovation Template</a>
    </p>
  </div>
</template>
