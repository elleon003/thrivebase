import SuperTokens from 'supertokens-web-js'

export const SuperTokensConfig = {
  appInfo: {
    appName: 'ThriveBase',
    apiDomain: 'http://localhost:8000',
    websiteDomain: 'http://localhost:5173',
    apiBasePath: '/api/v1/auth',
    websiteBasePath: '/auth'
  }
}

// Initialize SuperTokens
export function initializeSuperTokens() {
  SuperTokens.init({
    ...SuperTokensConfig,
    // Override default paths to match our backend API
    endpoints: {
      signInUp: '/api/v1/auth/signin',
      signOut: '/api/v1/auth/signout',
      refreshToken: '/api/v1/auth/refresh',
      thirdPartySignInUp: '/api/v1/auth/oauth/signin'
    }
  })
}

// Helper functions
export async function doesSessionExist() {
  return await SuperTokens.doesSessionExist()
}

export async function signOut() {
  await SuperTokens.signOut()
}

export async function getAccessToken() {
  return await SuperTokens.getAccessToken()
}
