import { createRouter, createWebHistory } from 'vue-router'
import Session from 'supertokens-web-js/recipe/session'

// Lazy load components for better performance
const Home = () => import('@/views/Home.vue')
const Dashboard = () => import('@/views/Dashboard.vue')
const SignIn = () => import('@/views/SignIn.vue')
const SignUp = () => import('@/views/SignUp.vue')
const Profile = () => import('@/views/Profile.vue')
const Terms = () => import('@/views/Terms.vue')
const Privacy = () => import('@/views/Privacy.vue')

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/signin',
    name: 'signin',
    component: SignIn,
    meta: { requiresAuth: false }
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUp,
    meta: { requiresAuth: false }
  },
  {
    path: '/profile',
    name: 'profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/terms',
    name: 'terms',
    component: Terms,
    meta: { requiresAuth: false }
  },
  {
    path: '/privacy',
    name: 'privacy',
    component: Privacy,
    meta: { requiresAuth: false }
  },
  // Catch all route for 404
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  // Smooth scroll behavior
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  }
})

// Navigation guard for protected routes
router.beforeEach(async (to, from, next) => {
  const isProtectedRoute = to.matched.some(record => record.meta.requiresAuth)
  
  if (!isProtectedRoute) {
    next()
    return
  }

  try {
    const doesSessionExist = await Session.doesSessionExist()
    if (doesSessionExist) {
      next()
    } else {
      next({
        path: '/signin',
        query: { redirect: to.fullPath }
      })
    }
  } catch (err) {
    console.error('Auth check failed:', err)
    next({
      path: '/signin',
      query: { redirect: to.fullPath }
    })
  }
})

export default router
