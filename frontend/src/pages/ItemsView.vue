<script setup lang="ts">
import { ref } from 'vue'
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { api } from '@/composables/useApi'

interface Item {
  id: number
  name: string
  description: string | null
}

const queryClient = useQueryClient()
const newItemName = ref('')
const newItemDescription = ref('')

// Fetch items
const { data: items, isLoading, error } = useQuery({
  queryKey: ['items'],
  queryFn: () => api.get<Item[]>('/api/items'),
})

// Create item mutation
const createMutation = useMutation({
  mutationFn: (item: { name: string; description: string }) =>
    api.post<Item>('/api/items', item),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['items'] })
    newItemName.value = ''
    newItemDescription.value = ''
  },
})

// Delete item mutation
const deleteMutation = useMutation({
  mutationFn: (id: number) => api.delete(`/api/items/${id}`),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['items'] })
  },
})

const createItem = () => {
  if (!newItemName.value.trim()) return
  createMutation.mutate({
    name: newItemName.value,
    description: newItemDescription.value,
  })
}
</script>

<template>
  <div class="max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold text-deep-purple mb-6">Items</h1>

    <!-- Create Form -->
    <div class="card mb-6">
      <h2 class="text-lg font-medium text-cap-gray-800 mb-4">Create New Item</h2>
      <form @submit.prevent="createItem" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-cap-gray-600 mb-1">Name</label>
          <input
            v-model="newItemName"
            type="text"
            class="input"
            placeholder="Item name"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-cap-gray-600 mb-1">Description</label>
          <input
            v-model="newItemDescription"
            type="text"
            class="input"
            placeholder="Optional description"
          />
        </div>
        <button
          type="submit"
          class="btn btn-primary"
          :disabled="createMutation.isPending.value"
        >
          {{ createMutation.isPending.value ? 'Creating...' : 'Create Item' }}
        </button>
      </form>
    </div>

    <!-- Items List -->
    <div class="card">
      <h2 class="text-lg font-medium text-cap-gray-800 mb-4">All Items</h2>

      <div v-if="isLoading" class="text-cap-gray-500">Loading...</div>
      <div v-else-if="error" class="text-tech-red">Error loading items</div>
      <div v-else-if="!items?.length" class="text-cap-gray-500">No items yet. Create one above!</div>

      <ul v-else class="divide-y divide-cap-gray-200">
        <li
          v-for="item in items"
          :key="item.id"
          class="py-4 flex items-center justify-between"
        >
          <div>
            <p class="font-medium text-cap-gray-800">{{ item.name }}</p>
            <p v-if="item.description" class="text-sm text-cap-gray-500">
              {{ item.description }}
            </p>
          </div>
          <button
            @click="deleteMutation.mutate(item.id)"
            class="text-tech-red hover:text-tech-red-700 text-sm font-medium"
            :disabled="deleteMutation.isPending.value"
          >
            Delete
          </button>
        </li>
      </ul>
    </div>

    <p class="text-sm text-cap-gray-400 mt-4">
      This demonstrates TanStack Query with Vue for data fetching, caching, and mutations.
    </p>
  </div>
</template>
