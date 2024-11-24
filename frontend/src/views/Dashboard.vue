<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>Welcome back{{ user?.email ? `, ${user.email.split('@')[0]}` : '' }}</h1>
      <div class="header-actions">
        <button 
          v-if="!hasConnectedAccounts" 
          @click="initPlaidConnection" 
          class="btn-primary"
          :disabled="isLoading"
        >
          Connect Your Bank
        </button>
        <button 
          v-else 
          @click="initPlaidConnection" 
          class="btn-secondary"
        >
          Connect Another Bank
        </button>
      </div>
    </header>

    <div v-if="isLoading" class="loading-state">
      <div class="loader"></div>
      <p>Loading your financial data...</p>
    </div>

    <div v-else-if="error" class="error-message">
      {{ error }}
      <button @click="clearError" class="btn-text">Dismiss</button>
    </div>

    <template v-else>
      <!-- No Connected Accounts State -->
      <div v-if="!hasConnectedAccounts" class="empty-state">
        <div class="empty-state-icon">🏦</div>
        <h2>Connect Your First Bank Account</h2>
        <p>Link your accounts to start tracking your finances and create a personalized budget.</p>
        <button @click="initPlaidConnection" class="btn-primary">Get Started</button>
      </div>

      <!-- Connected Accounts -->
      <div v-else class="accounts-section">
        <h2>Your Connected Accounts</h2>
        <div class="accounts-grid">
          <div 
            v-for="account in accounts" 
            :key="account.id" 
            class="account-card"
          >
            <div class="account-header">
              <h3>{{ account.name }}</h3>
              <button 
                @click="disconnectAccount(account.id)" 
                class="btn-icon" 
                aria-label="Disconnect account"
              >
                ✕
              </button>
            </div>
            <div class="account-balance">
              <span class="balance-label">Current Balance</span>
              <span class="balance-amount">${{ formatCurrency(account.balance) }}</span>
            </div>
            <div class="account-type">
              {{ account.type }} Account
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Transactions Preview -->
      <div v-if="hasConnectedAccounts" class="transactions-preview">
        <h2>Recent Transactions</h2>
        <div class="transactions-list">
          <div 
            v-for="transaction in recentTransactions" 
            :key="transaction.id"
            class="transaction-item"
          >
            <div class="transaction-info">
              <span class="transaction-name">{{ transaction.name }}</span>
              <span class="transaction-date">{{ formatDate(transaction.date) }}</span>
            </div>
            <span 
              :class="['transaction-amount', transaction.amount < 0 ? 'negative' : 'positive']"
            >
              ${{ formatCurrency(Math.abs(transaction.amount)) }}
            </span>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, defineComponent } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { usePlaid } from '@/composables/usePlaid'

defineComponent({
  name: 'DashboardPage'
})

const { user } = useAuth()
const { initPlaidLink, disconnectBank, getAccounts, getTransactions } = usePlaid()

const accounts = ref([])
const recentTransactions = ref([])
const isLoading = ref(true)
const error = ref(null)

const hasConnectedAccounts = computed(() => accounts.value.length > 0)

onMounted(async () => {
  await loadDashboardData()
})

const loadDashboardData = async () => {
  try {
    isLoading.value = true
    error.value = null
    
    const [accountsData, transactionsData] = await Promise.all([
      getAccounts(),
      getTransactions()
    ])
    
    accounts.value = accountsData
    recentTransactions.value = transactionsData.slice(0, 5) // Show only 5 most recent
  } catch (err) {
    error.value = 'Failed to load your financial data. Please try again.'
    console.error('Dashboard data loading error:', err)
  } finally {
    isLoading.value = false
  }
}

const initPlaidConnection = async () => {
  try {
    await initPlaidLink()
    await loadDashboardData() // Refresh data after new connection
  } catch (err) {
    error.value = 'Failed to connect to your bank. Please try again.'
    console.error('Plaid connection error:', err)
  }
}

const disconnectAccount = async (accountId) => {
  try {
    await disconnectBank(accountId)
    await loadDashboardData() // Refresh data after disconnection
  } catch (err) {
    error.value = 'Failed to disconnect account. Please try again.'
    console.error('Account disconnection error:', err)
  }
}

const clearError = () => {
  error.value = null
}

const formatCurrency = (amount) => {
  return amount.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric'
  })
}
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.loading-state {
  text-align: center;
  padding: 3rem;
}

.loader {
  border: 3px solid var(--background);
  border-radius: 50%;
  border-top: 3px solid var(--primary);
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.empty-state-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.accounts-section {
  margin-bottom: 2rem;
}

.accounts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.account-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.account-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.account-balance {
  margin-bottom: 1rem;
}

.balance-label {
  display: block;
  font-size: 0.875rem;
  color: #666;
}

.balance-amount {
  display: block;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary);
}

.account-type {
  font-size: 0.875rem;
  color: #666;
}

.transactions-preview {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-top: 2rem;
}

.transaction-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid #eee;
}

.transaction-item:last-child {
  border-bottom: none;
}

.transaction-info {
  display: flex;
  flex-direction: column;
}

.transaction-name {
  font-weight: 500;
}

.transaction-date {
  font-size: 0.875rem;
  color: #666;
}

.transaction-amount {
  font-weight: 600;
}

.transaction-amount.positive {
  color: #28a745;
}

.transaction-amount.negative {
  color: #dc3545;
}

.btn-icon {
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  padding: 0.25rem;
  font-size: 1.25rem;
  line-height: 1;
}

.btn-icon:hover {
  color: var(--primary);
}

.btn-text {
  background: none;
  border: none;
  color: #721c24;
  text-decoration: underline;
  cursor: pointer;
  padding: 0.25rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .accounts-grid {
    grid-template-columns: 1fr;
  }
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  .loader {
    animation: none;
  }
}
</style>
