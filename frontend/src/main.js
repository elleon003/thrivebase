import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { initializeSuperTokens } from './config/supertokens'

// Initialize SuperTokens
initializeSuperTokens()

const app = createApp(App)

// Add global error handler
app.config.errorHandler = (err, instance, info) => {
  console.error('Global error:', err)
  console.error('Error info:', info)
  // You might want to send this to an error tracking service
}

// Add global properties
app.config.globalProperties.$formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount)
}

app.config.globalProperties.$formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Use plugins
app.use(createPinia())
app.use(router)

// Mount the app
app.mount('#app')

// Add global navigation error handler
router.onError((error) => {
  console.error('Navigation error:', error)
  // Handle navigation errors (e.g., redirect to error page)
})

// Add global HTTP request interceptor for authentication
const originalFetch = window.fetch
window.fetch = async (...args) => {
  try {
    const response = await originalFetch(...args)
    
    if (response.status === 401) {
      // Handle unauthorized access
      router.push('/signin')
    }
    
    return response
  } catch (error) {
    console.error('Fetch error:', error)
    throw error
  }
}
