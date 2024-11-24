<template>
  <div class="legal-page">
    <div class="legal-content">
      <h1>Terms of Service</h1>
      <div class="last-updated">Last Updated: {{ currentDate }}</div>

      <section>
        <h2>1. Acceptance of Terms</h2>
        <p>
          By accessing and using ThriveBase ("the Service"), you agree to be bound by these Terms of Service 
          and all applicable laws and regulations. If you do not agree with any of these terms, you are 
          prohibited from using the Service.
        </p>
      </section>

      <section>
        <h2>2. Use of Service</h2>
        <p>
          ThriveBase provides financial management and budgeting tools. You agree to use the Service only 
          for its intended purposes and in compliance with all applicable laws and regulations.
        </p>
        <h3>2.1 Account Security</h3>
        <p>
          You are responsible for maintaining the confidentiality of your account credentials and for all 
          activities that occur under your account. You must immediately notify us of any unauthorized use 
          of your account.
        </p>
      </section>

      <section>
        <h2>3. Data Privacy</h2>
        <p>
          Your use of the Service is also governed by our Privacy Policy. By using the Service, you consent 
          to the collection and use of information as detailed in our Privacy Policy.
        </p>
      </section>

      <section>
        <h2>4. Third-Party Services</h2>
        <p>
          The Service integrates with third-party services including Plaid for bank account connections. 
          Your use of such third-party services is governed by their respective terms of service and 
          privacy policies.
        </p>
      </section>

      <section>
        <h2>5. Modifications to Service</h2>
        <p>
          We reserve the right to modify or discontinue the Service at any time, with or without notice. 
          We shall not be liable to you or any third party for any modification, suspension, or 
          discontinuance of the Service.
        </p>
      </section>

      <section>
        <h2>6. Limitation of Liability</h2>
        <p>
          To the fullest extent permitted by law, ThriveBase shall not be liable for any indirect, 
          incidental, special, consequential, or punitive damages resulting from your use or inability 
          to use the Service.
        </p>
      </section>

      <section>
        <h2>7. Governing Law</h2>
        <p>
          These Terms shall be governed by and construed in accordance with the laws of the jurisdiction 
          in which ThriveBase operates, without regard to its conflict of law provisions.
        </p>
      </section>

      <section>
        <h2>8. Contact Information</h2>
        <p>
          For any questions about these Terms, please contact us at support@thrivebase.com
        </p>
      </section>
    </div>
  </div>
</template>

<script setup>
import { defineComponent } from 'vue'

defineComponent({
  name: 'TermsPage'
})

const currentDate = new Date().toLocaleDateString('en-US', {
  year: 'numeric',
  month: 'long',
  day: 'numeric'
})
</script>

<style scoped>
.legal-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.legal-content {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

h1 {
  color: var(--primary);
  margin-bottom: 0.5rem;
}

.last-updated {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 2rem;
}

section {
  margin-bottom: 2rem;
}

h2 {
  color: var(--primary);
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

h3 {
  color: var(--text);
  font-size: 1.2rem;
  margin: 1rem 0;
}

p {
  margin-bottom: 1rem;
  line-height: 1.6;
}

/* Responsive Design */
@media (max-width: 768px) {
  .legal-page {
    padding: 1rem;
  }

  .legal-content {
    padding: 1.5rem;
  }
}
</style>
