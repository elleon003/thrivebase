<template>
  <div class="auth-page">
    <div class="auth-container">
      <h1>Welcome Back</h1>
      <p class="auth-subtitle">Sign in to manage your finances</p>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <form @submit.prevent="handleEmailSignIn" class="auth-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            :disabled="isLoading"
            placeholder="Enter your email"
          >
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            :disabled="isLoading"
            placeholder="Enter your password"
          >
        </div>

        <button 
          type="submit" 
          class="btn-primary full-width"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>

      <div class="divider">
        <span>or</span>
      </div>

      <button 
        @click="handleGoogleSignIn" 
        class="btn-google"
        :disabled="isLoading"
      >
        <img 
          src="@/assets/google-logo.svg" 
          alt="" 
          class="google-icon"
        >
        Continue with Google
      </button>

      <p class="auth-footer">
        Don't have an account? 
        <router-link to="/signup">Sign Up</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, defineComponent } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { useRoute, useRouter } from 'vue-router'

defineComponent({
  name: 'SignInPage'
})

const route = useRoute()
const router = useRouter()
const { signIn, signInWithGoogle } = useAuth()

const email = ref('')
const password = ref('')
const error = ref('')
const isLoading = ref(false)

const handleEmailSignIn = async () => {
  try {
    isLoading.value = true
    error.value = ''

    const result = await signIn(email.value, password.value)
    
    if (result.success) {
      const redirectPath = route.query.redirect || '/dashboard'
      router.push(redirectPath)
    } else {
      error.value = result.error
    }
  } catch (err) {
    error.value = 'Failed to sign in. Please try again.'
    console.error('Sign in error:', err)
  } finally {
    isLoading.value = false
  }
}

const handleGoogleSignIn = async () => {
  try {
    isLoading.value = true
    error.value = ''
    await signInWithGoogle()
  } catch (err) {
    error.value = 'Failed to sign in with Google. Please try again.'
    console.error('Google sign in error:', err)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: calc(100vh - 4rem);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: linear-gradient(135deg, var(--primary) 0%, #006666 100%);
}

.auth-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.auth-container h1 {
  text-align: center;
  color: var(--primary);
  margin-bottom: 0.5rem;
}

.auth-subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 2rem;
}

.auth-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--text);
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #eee;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary);
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  text-align: center;
}

.divider {
  text-align: center;
  margin: 1.5rem 0;
  position: relative;
}

.divider::before,
.divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: calc(50% - 30px);
  height: 1px;
  background: #eee;
}

.divider::before {
  left: 0;
}

.divider::after {
  right: 0;
}

.divider span {
  background: white;
  padding: 0 10px;
  color: #666;
  font-size: 0.9rem;
}

.btn-google {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #eee;
  border-radius: 4px;
  background: white;
  color: var(--text);
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-google:hover {
  background: #f8f8f8;
}

.google-icon {
  width: 18px;
  height: 18px;
}

.auth-footer {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
  font-size: 0.9rem;
}

.auth-footer a {
  color: var(--primary);
  text-decoration: none;
  font-weight: 500;
}

.full-width {
  width: 100%;
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  .form-group input,
  .btn-google {
    transition: none;
  }
}

/* Focus styles */
.btn-google:focus {
  outline: none;
  border-color: var(--primary);
}

/* Loading state styles */
button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>
