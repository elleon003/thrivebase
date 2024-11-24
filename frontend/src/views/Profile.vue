<template>
  <div class="profile-page">
    <div class="profile-header">
      <h1>Account Settings</h1>
      <p class="last-updated" v-if="user">
        Last updated: {{ formatDate(user.updatedAt) }}
      </p>
    </div>

    <div class="profile-content">
      <!-- Account Information Section -->
      <section class="profile-section">
        <h2>Account Information</h2>
        
        <form @submit.prevent="handleUpdateProfile" class="profile-form">
          <div class="form-group">
            <label for="email">Email Address</label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              :placeholder="user?.email"
              :disabled="isLoading"
            >
          </div>

          <div class="form-group">
            <label for="currentPassword">Current Password</label>
            <input
              id="currentPassword"
              v-model="formData.currentPassword"
              type="password"
              placeholder="Enter current password"
              :disabled="isLoading"
            >
          </div>

          <div class="form-group">
            <label for="newPassword">New Password</label>
            <input
              id="newPassword"
              v-model="formData.newPassword"
              type="password"
              placeholder="Enter new password"
              :disabled="isLoading"
            >
            <small class="password-hint" v-if="formData.newPassword">
              Password must be at least 8 characters long and include both letters and numbers
            </small>
          </div>

          <div class="form-actions">
            <button 
              type="submit" 
              class="btn-primary"
              :disabled="isLoading || !hasChanges"
            >
              {{ isLoading ? 'Saving Changes...' : 'Save Changes' }}
            </button>
          </div>

          <div v-if="updateMessage" :class="['update-message', updateMessage.type]">
            {{ updateMessage.text }}
          </div>
        </form>
      </section>

      <!-- Connected Banks Section -->
      <section class="profile-section">
        <h2>Connected Banks</h2>
        
        <div v-if="isLoadingBanks" class="loading-state">
          <div class="loader"></div>
          <p>Loading connected banks...</p>
        </div>

        <div v-else-if="connectedBanks.length === 0" class="empty-state">
          <p>No banks connected yet</p>
          <button @click="handlePlaidLink" class="btn-secondary">
            Connect a Bank
          </button>
        </div>

        <div v-else class="connected-banks">
          <div 
            v-for="bank in connectedBanks" 
            :key="bank.id"
            class="bank-item"
          >
            <div class="bank-info">
              <h3>{{ bank.name }}</h3>
              <p class="bank-status">
                <span class="status-indicator" :class="bank.status"></span>
                {{ bank.status === 'active' ? 'Connected' : 'Connection Issue' }}
              </p>
            </div>
            <div class="bank-actions">
              <button 
                @click="disconnectBank(bank.id)"
                class="btn-danger"
                :disabled="isLoading"
              >
                Disconnect
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Account Deletion Section -->
      <section class="profile-section danger-zone">
        <h2>Delete Account</h2>
        <p class="warning-text">
          This action cannot be undone. All your data will be permanently deleted.
        </p>
        <button 
          @click="showDeleteConfirmation = true"
          class="btn-danger"
          :disabled="isLoading"
        >
          Delete Account
        </button>
      </section>
    </div>

    <!-- Delete Account Confirmation Modal -->
    <div v-if="showDeleteConfirmation" class="modal-overlay">
      <div class="modal">
        <h2>Delete Account</h2>
        <p>Are you sure you want to delete your account? This action cannot be undone.</p>
        <div class="modal-actions">
          <button 
            @click="handleDeleteAccount"
            class="btn-danger"
            :disabled="isLoading"
          >
            Yes, Delete My Account
          </button>
          <button 
            @click="showDeleteConfirmation = false"
            class="btn-secondary"
            :disabled="isLoading"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, defineComponent } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { usePlaid } from '@/composables/usePlaid'
import { useRouter } from 'vue-router'

defineComponent({
  name: 'ProfilePage'
})

const router = useRouter()
const { user, updateProfile } = useAuth()
const { initPlaidLink, disconnectBank, getAccounts } = usePlaid()

const formData = ref({
  email: '',
  currentPassword: '',
  newPassword: ''
})

const connectedBanks = ref([])
const isLoading = ref(false)
const isLoadingBanks = ref(false)
const updateMessage = ref(null)
const showDeleteConfirmation = ref(false)

const hasChanges = computed(() => {
  return formData.value.email || 
         formData.value.currentPassword || 
         formData.value.newPassword
})

onMounted(async () => {
  await loadConnectedBanks()
})

const loadConnectedBanks = async () => {
  try {
    isLoadingBanks.value = true
    const accounts = await getAccounts()
    connectedBanks.value = accounts.map(account => ({
      id: account.id,
      name: account.institution_name,
      status: account.status
    }))
  } catch (err) {
    console.error('Failed to load connected banks:', err)
  } finally {
    isLoadingBanks.value = false
  }
}

const handlePlaidLink = async () => {
  try {
    await initPlaidLink()
    await loadConnectedBanks() // Refresh the list after new connection
  } catch (err) {
    console.error('Failed to initialize Plaid:', err)
  }
}

const handleUpdateProfile = async () => {
  try {
    isLoading.value = true
    updateMessage.value = null

    const result = await updateProfile({
      email: formData.value.email || undefined,
      currentPassword: formData.value.currentPassword,
      newPassword: formData.value.newPassword || undefined
    })

    if (result.success) {
      updateMessage.value = {
        type: 'success',
        text: 'Profile updated successfully'
      }
      // Reset form
      formData.value = {
        email: '',
        currentPassword: '',
        newPassword: ''
      }
    } else {
      updateMessage.value = {
        type: 'error',
        text: result.error
      }
    }
  } catch (err) {
    updateMessage.value = {
      type: 'error',
      text: 'Failed to update profile. Please try again.'
    }
    console.error('Profile update error:', err)
  } finally {
    isLoading.value = false
  }
}

const handleDeleteAccount = async () => {
  try {
    isLoading.value = true
    // Implementation for account deletion
    // This would need to be implemented in the backend
    router.push('/')
  } catch (err) {
    console.error('Account deletion error:', err)
  } finally {
    isLoading.value = false
    showDeleteConfirmation.value = false
  }
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.profile-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.profile-header {
  margin-bottom: 2rem;
}

.last-updated {
  color: #666;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.profile-section {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.profile-section h2 {
  margin-bottom: 1.5rem;
  color: var(--primary);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
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

.form-actions {
  margin-top: 2rem;
}

.update-message {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 4px;
  text-align: center;
}

.update-message.success {
  background: #d4edda;
  color: #155724;
}

.update-message.error {
  background: #f8d7da;
  color: #721c24;
}

.loading-state {
  text-align: center;
  padding: 2rem;
}

.loader {
  border: 3px solid #f3f3f3;
  border-radius: 50%;
  border-top: 3px solid var(--primary);
  width: 24px;
  height: 24px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.bank-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.bank-info h3 {
  margin: 0;
  color: var(--text);
}

.bank-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.25rem;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-indicator.active {
  background: #28a745;
}

.status-indicator.error {
  background: #dc3545;
}

.danger-zone {
  border: 1px solid #dc3545;
}

.danger-zone h2 {
  color: #dc3545;
}

.warning-text {
  color: #721c24;
  margin-bottom: 1rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 400px;
  width: 90%;
}

.modal h2 {
  color: #dc3545;
  margin-bottom: 1rem;
}

.modal-actions {
  margin-top: 2rem;
  display: flex;
  gap: 1rem;
}

.btn-danger {
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.75rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.btn-danger:hover {
  background: #c82333;
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  .loader {
    animation: none;
  }
  
  .form-group input,
  .btn-danger {
    transition: none;
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .profile-page {
    padding: 1rem;
  }

  .modal-actions {
    flex-direction: column;
  }
}
</style>
