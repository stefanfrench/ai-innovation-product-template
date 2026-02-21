import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/pages/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/examples',
      name: 'examples',
      component: () => import('@/pages/ExamplesView.vue'),
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('@/pages/ChatView.vue'),
    },
    {
      path: '/items',
      name: 'items',
      component: () => import('@/pages/ItemsView.vue'),
    },
  ],
})

export default router
