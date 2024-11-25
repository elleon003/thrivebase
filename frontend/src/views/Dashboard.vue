<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>Welcome back{{ user?.email ? `, ${user.email.split('@')[0]}` : '' }}</h1>
      <div class="header-actions">
        <button 
          v-if="!hasConnectedInstitutions" 
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
      <div v-if="!hasConnectedInstitutions" class="empty-state">
        <div class="empty-state-icon">🏦</div>
        <h2>Connect Your First Bank Account</h2>
        <p>Link your accounts to start tracking your finances and create a personalized budget.</p>
        <button @click="initPlaidConnection" class="btn-primary">Get Started</button>
      </div>

      <!-- Account Summary -->
      <div v-else class="summary-section">
        <div class="summary-card">
          <h3>Total Balance</h3>
          <div class="summary-amount">${{ formatCurrency(accountSummary.summary.total_current_balance) }}</div>
          <div class="summary-detail">
            Available: ${{ formatCurrency(accountSummary.summary.total_available_balance) }}
          </div>
        </div>
      </div>

      <!-- Connected Institutions -->
      <div v-if="hasConnectedInstitutions" class="institutions-section">
        <div 
          v-for="institution in institutions" 
          :key="institution.item_id" 
          class="institution-container"
        >
          <div class="institution-header">
            <h2>{{ institution.institution_name }}</h2>
            <div class="institution-actions">
              <button 
                @click="refreshBalances(institution.item_id)" 
                class="btn-icon" 
                title="Refresh balances"
                :disabled="isRefreshing"
              >
                🔄
              </button>
              <button 
                @click="disconnectInstitution(institution.item_id)" 
                class="btn-icon" 
                title="Disconnect institution"
              >
                ✕
              </button>
            </div>
          </div>

          <div class="accounts-grid">
            <div 
              v-for="account in getInstitutionAccounts(institution.item_id)" 
              :key="account.id" 
              class="account-card"
            >
              <h3>{{ account.name }}</h3>
              <div class="account-balance">
                <span class="balance-label">Current Balance</span>
                <span class="balance-amount">${{ formatCurrency(account.balance_current) }}</span>
                <span v-if="account.balance_available !== null" class="balance-available">
                  Available: ${{ formatCurrency(account.balance_available) }}
                </span>
              </div>
              <div class="account-type">
                {{ account.type }}{{ account.subtype ? ` - ${account.subtype}` : '' }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Transactions -->
      <div v-if="hasConnectedInstitutions" class="transactions-preview">
        <h2>Recent Transactions</h2>
        <div class="transactions-list">
          <div 
            v-for="transaction in recentTransactions" 
            :key="transaction.id"
            class="transaction-item"
          >
            <div class="transaction-info">
              <span class="transaction-name">{{ transaction.description }}</span>
              <span class="transaction-details">
                {{ transaction.account_name }} • {{ formatDate(transaction.date) }}
              </span>
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
import { ref, computed, onMounted } from 'vue'
import { useAuth } from '../composables/useAuth'
import { usePlaid } from '../composables/usePlaid'

const { user } = useAuth()
const { 
  initPlaidLink, 
  disconnectBank, 
  getConnectedInstitutions,
  getAccountSummary,
  updateAccountBalances,
  getTransactions 
} = usePlaid()

const institutions = ref([])
const accountSummary = ref({
  accounts: [],
  summary: {
    total_current_balance: 0,
    total_available_balance: 0,
    total_accounts: 0
  }
})
const recentTransactions = ref([])
const isLoading = ref(true)
const isRefreshing = ref(false)
const error = ref(null)

const hasConnectedInstitutions = computed(() => institutions.value.length > 0)

const getInstitutionAccounts = (itemId) => {
  return accountSummary.value.accounts.filter(account => account.plaid_item_id === itemId)
}

onMounted(async () => {
  await loadDashboardData()
})

const loadDashboardData = async () => {
  try {
    isLoading.value = true
    error.value = null
    
    const [institutionsData, summaryData, transactionsData] = await Promise.all([
      getConnectedInstitutions(),
      getAccountSummary(),
      getTransactions()
    ])
    
    institutions.value = institutionsData
    accountSummary.value = summaryData
    recentTransactions.value = transactionsData.slice(0, 5) // Show only 5 most recent
  } catch (err) {
    error.value = 'Failed to load your financial data. Please try again.'
    console.error('Dashboard data loading error:', err)
  } finally {
    isLoading.value = false
  }
}

const refreshBalances = async (itemId) => {
  try {
    isRefreshing.value = true
    await updateAccountBalances(itemId)
    await loadDashboardData() // Refresh all data
  } catch (err) {
    error.value = 'Failed to refresh account balances. Please try again.'
    console.error('Balance refresh error:', err)
  } finally {
    isRefreshing.value = false
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

const disconnectInstitution = async (itemId) => {
  if (!confirm('Are you sure you want to disconnect this institution? This will remove all associated accounts.')) {
    return
  }
  
  try {
    await disconnectBank(itemId)
    await loadDashboardData() // Refresh data after disconnection
  } catch (err) {
    error.value = 'Failed to disconnect institution. Please try again.'
    console.error('Institution disconnection error:', err)
  }
}

const clearError = () => {
  error.value = null
}

const formatCurrency = (amount) => {
  return Number(amount).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
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

.summary-section {
  margin-bottom: 2rem;
}

.summary-card {
  background: var(--primary);
  color: white;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
}

.summary-amount {
  font-size: 2rem;
  font-weight: 600;
  margin: 0.5rem 0;
}

.summary-detail {
  font-size: 0.875rem;
  opacity: 0.9;
}

.institutions-section {
  margin-bottom: 2rem;
}

.institution-container {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.institution-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.institution-actions {
  display: flex;
  gap: 0.5rem;
}

.accounts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.account-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
}

.account-balance {
  margin: 1rem 0;
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

.balance-available {
  display: block;
  font-size: 0.875rem;
  color: #666;
  margin-top: 0.25rem;
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

.transaction-details {
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
  padding: 0.5rem;
  font-size: 1.25rem;
  line-height: 1;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.btn-icon:hover:not(:disabled) {
  background-color: #f0f0f0;
  color: var(--primary);
}

.btn-icon:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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

  .institution-header {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  .loader {
    animation: none;
  }

  .btn-icon {
    transition: none;
  }
}
</style>
