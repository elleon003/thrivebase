<template>
  <div class="home">
    <section class="hero">
      <div class="hero-content">
        <h1>Line up your money with your life</h1>
        <p class="hero-tagline">
          A modern budgeting solution for modern pay schedules. 
          Perfect for freelancers, gig workers, and anyone with variable income.
        </p>
        <div class="cta-container">
          <button @click="scrollToSignup" class="btn-primary">Join the Waitlist</button>
          <router-link to="/signin" class="btn-secondary">Sign In</router-link>
        </div>
      </div>
    </section>

    <section class="features">
      <div class="feature-card">
        <div class="feature-icon">🔄</div>
        <h3>Flexible Scheduling</h3>
        <p>Budget around your actual pay schedule, not just monthly cycles</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🔒</div>
        <h3>Bank-Level Security</h3>
        <p>Your data is protected with industry-leading encryption</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Smart Insights</h3>
        <p>Understand your spending patterns and optimize your budget</p>
      </div>
    </section>

    <section id="signup" class="newsletter-signup" ref="signupSection">
      <div class="signup-content">
        <h2>Be the first to know when we launch</h2>
        <p>Join our waitlist to get early access and exclusive features</p>
        
        <form @submit.prevent="handleSignup" class="signup-form">
          <div class="form-group">
            <label for="email" class="sr-only">Email address</label>
            <input
              type="email"
              id="email"
              v-model="email"
              placeholder="Enter your email"
              required
              :disabled="isSubmitting"
              aria-label="Email address"
            >
          </div>
          <button 
            type="submit" 
            class="btn-primary" 
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? 'Signing up...' : 'Join Waitlist' }}
          </button>
        </form>

        <div v-if="signupMessage" :class="['signup-message', signupMessage.type]">
          {{ signupMessage.text }}
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, defineComponent } from 'vue'

defineComponent({
  name: 'HomePage'
})

const email = ref('')
const isSubmitting = ref(false)
const signupMessage = ref(null)
const signupSection = ref(null)

const handleSignup = async () => {
  isSubmitting.value = true
  signupMessage.value = null

  try {
    const response = await fetch('/api/v1/users/newsletter-signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email: email.value })
    })

    if (response.ok) {
      signupMessage.value = {
        type: 'success',
        text: 'Thanks for signing up! We\'ll keep you updated on our launch.'
      }
      email.value = ''
    } else {
      throw new Error('Signup failed')
    }
  } catch (error) {
    console.error('Newsletter signup error:', error)
    signupMessage.value = {
      type: 'error',
      text: 'Something went wrong. Please try again.'
    }
  } finally {
    isSubmitting.value = false
  }
}

const scrollToSignup = () => {
  signupSection.value?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<style scoped>
.home {
  max-width: 100%;
  overflow-x: hidden;
}

.hero {
  padding: 4rem 2rem;
  text-align: center;
  background: linear-gradient(135deg, var(--primary) 0%, #006666 100%);
  color: white;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.hero-tagline {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.cta-container {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.features {
  padding: 4rem 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  padding: 2rem;
  text-align: center;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  margin-bottom: 1rem;
  color: var(--primary);
}

.newsletter-signup {
  padding: 4rem 2rem;
  background: var(--background);
}

.signup-content {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

.signup-form {
  margin-top: 2rem;
  display: flex;
  gap: 1rem;
  max-width: 500px;
  margin: 2rem auto;
}

.form-group {
  flex: 1;
}

input[type="email"] {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid var(--primary);
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

input[type="email"]:focus {
  outline: none;
  border-color: var(--accent);
}

.signup-message {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 4px;
}

.signup-message.success {
  background: #d4edda;
  color: #155724;
}

.signup-message.error {
  background: #f8d7da;
  color: #721c24;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero h1 {
    font-size: 2.5rem;
  }

  .signup-form {
    flex-direction: column;
  }

  .cta-container {
    flex-direction: column;
    align-items: stretch;
  }

  .features {
    grid-template-columns: 1fr;
    padding: 2rem 1rem;
  }
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  .feature-card {
    transform: none !important;
  }
}
</style>
