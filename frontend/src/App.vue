<template>
  <div class="app">
    <nav v-if="showNav" class="nav">
      <router-link to="/" class="nav-logo">ThriveBase</router-link>
      <div class="nav-links">
        <template v-if="isAuthenticated">
          <router-link to="/dashboard">Dashboard</router-link>
          <router-link to="/profile">Profile</router-link>
          <button @click="handleSignOut" class="btn-secondary">Sign Out</button>
        </template>
        <template v-else>
          <router-link to="/signin" class="btn-primary">Sign In</router-link>
        </template>
      </div>
    </nav>

    <main>
      <router-view></router-view>
    </main>

    <footer class="footer">
      <div class="footer-content">
        <div class="footer-logo">ThriveBase</div>
        <p class="footer-tagline">Line up your money with your life, not the other way around</p>
        <div class="footer-links">
          <router-link to="/privacy">Privacy Policy</router-link>
          <router-link to="/terms">Terms of Service</router-link>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const route = useRoute()
const { isAuthenticated, signOut } = useAuth()

// Hide nav on auth pages
const showNav = computed(() => !['signin', 'signup'].includes(route.name))

const handleSignOut = async () => {
  await signOut()
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Sans+Pro:wght@400;600&display=swap');

:root {
  --teal: #008080;
  --light-red: #ff6b6b;
  --powder-blue: #b0e0e6;
  --jet: #333333;
  --ivory: #fffff0;
  
  --primary: var(--teal);
  --secondary: var(--light-red);
  --accent: var(--powder-blue);
  --text: var(--jet);
  --background: var(--ivory);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Source Sans Pro', sans-serif;
  color: var(--text);
  background: var(--background);
  line-height: 1.6;
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.nav {
  background: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-logo {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 1.5rem;
  color: var(--primary);
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.nav-links a {
  text-decoration: none;
  color: var(--text);
  font-weight: 500;
}

main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.footer {
  background: var(--primary);
  color: white;
  padding: 2rem;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.footer-logo {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.footer-tagline {
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.footer-links a {
  color: white;
  text-decoration: none;
  font-size: 0.9rem;
}

/* Button Styles */
.btn-primary {
  background: var(--primary);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background: #006666;
}

.btn-secondary {
  background: transparent;
  color: var(--text);
  padding: 0.5rem 1rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 600;
  border: 1px solid var(--text);
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: var(--text);
  color: white;
}

/* Accessibility Improvements */
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}

/* Focus styles */
:focus {
  outline: 3px solid var(--accent);
  outline-offset: 2px;
}

/* Screen reader only class */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
</style>
