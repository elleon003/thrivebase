import { ref } from 'vue'
import { loadScript } from '@/utils/loadScript'

export function usePlaid() {
  const isLoading = ref(false)
  const error = ref(null)

  const initPlaidLink = async () => {
    try {
      isLoading.value = true
      error.value = null

      // Load Plaid Link script if not already loaded
      await loadScript('https://cdn.plaid.com/link/v2/stable/link-initialize.js')

      // Get link token from our backend
      const response = await fetch('/api/v1/plaid/create_link_token')
      const { link_token } = await response.json()

      // Initialize Plaid Link
      const handler = window.Plaid.create({
        token: link_token,
        onSuccess: async (public_token, { institution, accounts }) => {
          // Exchange public token for access token
          await fetch('/api/v1/plaid/exchange_public_token', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
              public_token,
              institution_id: institution.institution_id,
              institution_name: institution.name,
              accounts: accounts.map(acc => ({
                id: acc.id,
                name: acc.name,
                type: acc.type,
                subtype: acc.subtype
              }))
            })
          })
        },
        onExit: (err, { status, link_session_id }) => {
          if (err) {
            error.value = err.message
            console.error('Plaid exit error:', { status, link_session_id, error: err })
          }
        },
        onEvent: (eventName, metadata) => {
          // Log events for debugging and analytics
          console.log('Plaid Link Event:', eventName, metadata)
        }
      })

      handler.open()
    } catch (err) {
      error.value = 'Failed to initialize Plaid Link'
      console.error('Plaid initialization error:', err)
    } finally {
      isLoading.value = false
    }
  }

  const disconnectBank = async (itemId) => {
    try {
      const response = await fetch(`/api/v1/plaid/disconnect/${itemId}`, {
        method: 'DELETE'
      })

      if (!response.ok) {
        throw new Error('Failed to disconnect bank account')
      }
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const getAccounts = async () => {
    try {
      const response = await fetch('/api/v1/plaid/accounts')
      if (!response.ok) {
        throw new Error('Failed to fetch accounts')
      }
      return await response.json()
    } catch (err) {
      error.value = err.message
      return []
    }
  }

  const getTransactions = async () => {
    try {
      const response = await fetch('/api/v1/baserow/user-transactions')
      if (!response.ok) {
        throw new Error('Failed to fetch transactions')
      }
      return await response.json()
    } catch (err) {
      error.value = err.message
      return []
    }
  }

  return {
    isLoading,
    error,
    initPlaidLink,
    disconnectBank,
    getAccounts,
    getTransactions
  }
}
