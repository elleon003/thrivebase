import { ref } from 'vue'
import { useRouter } from 'vue-router'
import SuperTokens from 'supertokens-web-js'

const isAuthenticated = ref(false)
const user = ref(null)

export function useAuth() {
  const router = useRouter()

  const checkAuthStatus = async () => {
    try {
      const session = await SuperTokens.doesSessionExist()
      isAuthenticated.value = session
      if (session) {
        await getUserInfo()
      }
    } catch (error) {
      console.error('Error checking auth status:', error)
      isAuthenticated.value = false
    }
  }

  const getUserInfo = async () => {
    try {
      const response = await fetch('/api/v1/users/me')
      if (response.ok) {
        user.value = await response.json()
      }
    } catch (error) {
      console.error('Error fetching user info:', error)
    }
  }

  const signIn = async (email, password) => {
    try {
      const response = await fetch('/api/v1/auth/signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      })

      if (response.ok) {
        await checkAuthStatus()
        router.push('/dashboard')
        return { success: true }
      }

      const error = await response.json()
      return {
        success: false,
        error: error.message || "Invalid credentials"
      }
    } catch (error) {
      console.error('Sign in error:', error)
      return {
        success: false,
        error: error.message
      }
    }
  }

  const signUp = async (email, password) => {
    try {
      const response = await fetch('/api/v1/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      })

      if (response.ok) {
        return await signIn(email, password)
      }

      const error = await response.json()
      return {
        success: false,
        error: error.message || "Email already exists"
      }
    } catch (error) {
      console.error('Sign up error:', error)
      return {
        success: false,
        error: error.message
      }
    }
  }

  const signInWithGoogle = async () => {
    try {
      const response = await fetch('/api/v1/auth/oauth/google/url')
      const { url } = await response.json()
      window.location.href = url
    } catch (error) {
      console.error('Google sign in error:', error)
      return {
        success: false,
        error: error.message
      }
    }
  }

  const signOut = async () => {
    try {
      await SuperTokens.signOut()
      isAuthenticated.value = false
      user.value = null
      router.push('/')
    } catch (error) {
      console.error('Sign out error:', error)
    }
  }

  const updateProfile = async (data) => {
    try {
      const response = await fetch('/api/v1/users/profile', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })

      if (response.ok) {
        await getUserInfo()
        return { success: true }
      }

      const error = await response.json()
      return {
        success: false,
        error: error.detail
      }
    } catch (error) {
      console.error('Update profile error:', error)
      return {
        success: false,
        error: error.message
      }
    }
  }

  return {
    isAuthenticated,
    user,
    checkAuthStatus,
    signIn,
    signUp,
    signInWithGoogle,
    signOut,
    updateProfile
  }
}
