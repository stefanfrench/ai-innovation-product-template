import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { VueQueryPlugin } from '@tanstack/vue-query'

import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)

// State management
app.use(createPinia())

// Data fetching
app.use(VueQueryPlugin)

// Routing
app.use(router)

app.mount('#app')
