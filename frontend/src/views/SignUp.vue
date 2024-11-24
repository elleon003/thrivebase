<template>
  <div class="auth-page">
    <div class="auth-container">
      <h1>Create Account</h1>
      <p class="auth-subtitle">Start your journey to better finances</p>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <form @submit.prevent="handleEmailSignUp" class="auth-form">
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
            placeholder="Create a password"
            pattern="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
            title="Password must be at least 8 characters long and include both letters and numbers"
          >
          <small class="password-hint">
            Password must be at least 8 characters long and include both letters and numbers
          </small>
        </div>

        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            required
            :disabled="isLoading"
            placeholder="Confirm your password"
          >
        </div>

        <div class="form-group terms-group">
          <label class="checkbox-label">
            <input
              type="checkbox"
              v-model="acceptedTerms"
              required
              :disabled="isLoading"
            >
            <span>
              I agree to the 
              <router-link to="/terms" target="_blank">Terms of Service</router-link>
              and
              <router-link to="/privacy" target="_blank">Privacy Policy</router-link>
            </span>
          </label>
        </div>

        <button 
          type="submit" 
          class="btn-primary full-width"
          :disabled="isLoading || !isPasswordValid || !doPasswordsMatch || !acceptedTerms"
        >
          {{ isLoading ? 'Creating Account...' : 'Create Account' }}
        </button>
      </form>

      <div class="divider">
        <span>or</span>
      </div>

      <button 
        @click="handleGoogleSignUp" 
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
        Already have an account? 
        <router-link to="/signin">Sign In</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineComponent } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { useRouter } from 'vue-router'

defineComponent({
  name: 'SignUpPage'
})

const router = useRouter()
const { signUp, signInWithGoogle } = useAuth()

const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const acceptedTerms = ref(false)
const error = ref('')
const isLoading = ref(false)

const isPasswordValid = computed(() => {
  const regex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/
  return regex.test(password.value)
})

const doPasswordsMatch = computed(() => {
  return password.value === confirmPassword.value
})

const handleEmailSignUp = async () => {
  if (!isPasswordValid.value) {
    error.value = 'Password must be at least 8 characters long and include both letters and numbers'
    return
  }

  if (!doPasswordsMatch.value) {
    error.value = 'Passwords do not match'
    return
  }

  try {
    isLoading.value = true
    error.value = ''

    const result = await signUp(email.value, password.value)
    
    if (result.success) {
      router.push('/dashboard')
    } else {
      error.value = result.error
    }
  } catch (err) {
    error.value = 'Failed to create account. Please try again.'
    console.error('Sign up error:', err)
  } finally {
    isLoading.value = false
  }
}

const handleGoogleSignUp = async () => {
  try {
    isLoading.value = true
    error.value = ''
    await signInWithGoogle()
  } catch (err) {
    error.value = 'Failed to sign up with Google. Please try again.'
    console.error('Google sign up error:', err)
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

.password-hint {
  display: block;
  margin-top: 0.5rem;
  color: #666;
  font-size: 0.875rem;
}

.terms-group {
  margin-top: 1rem;
}

.checkbox-label {
  display: flex;
  gap: 0.5rem;
  align-items: flex-start;
  font-size: 0.9rem;
  color: #666;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  margin-top: 0.25rem;
}

.checkbox-label a {
  color: var(--primary);
  text-decoration: none;
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
