<template>
  <div class="legal-page">
    <div class="legal-content">
      <h1>Privacy Policy</h1>
      <div class="last-updated">Last Updated: {{ currentDate }}</div>

      <section>
        <h2>1. Introduction</h2>
        <p>
          At ThriveBase, we take your privacy seriously. This Privacy Policy explains how we collect, 
          use, disclose, and safeguard your information when you use our service.
        </p>
      </section>

      <section>
        <h2>2. Information We Collect</h2>
        <h3>2.1 Personal Information</h3>
        <p>
          We collect information that you provide directly to us, including:
        </p>
        <ul>
          <li>Name and email address when you create an account</li>
          <li>Financial information when you connect your bank accounts</li>
          <li>Transaction data and account balances</li>
          <li>Any other information you choose to provide</li>
        </ul>

        <h3>2.2 Automatically Collected Information</h3>
        <p>
          When you access our service, we automatically collect:
        </p>
        <ul>
          <li>Device information</li>
          <li>Log information</li>
          <li>Usage information</li>
          <li>Location information</li>
        </ul>
      </section>

      <section>
        <h2>3. How We Use Your Information</h2>
        <p>
          We use the information we collect to:
        </p>
        <ul>
          <li>Provide, maintain, and improve our services</li>
          <li>Process your transactions and send you related information</li>
          <li>Send you technical notices, updates, and support messages</li>
          <li>Respond to your comments and questions</li>
          <li>Detect, investigate, and prevent fraudulent transactions and other illegal activities</li>
          <li>Protect our rights and property</li>
        </ul>
      </section>

      <section>
        <h2>4. Information Sharing and Disclosure</h2>
        <p>
          We do not sell, trade, or rent your personal information to third parties. We may share your 
          information in the following circumstances:
        </p>
        <ul>
          <li>With your consent</li>
          <li>With third-party service providers who assist in our operations</li>
          <li>To comply with legal obligations</li>
          <li>To protect our rights and property</li>
        </ul>
      </section>

      <section>
        <h2>5. Data Security</h2>
        <p>
          We implement appropriate technical and organizational measures to protect your personal 
          information against unauthorized access, alteration, disclosure, or destruction. However, 
          no method of transmission over the Internet or electronic storage is 100% secure.
        </p>
      </section>

      <section>
        <h2>6. Third-Party Services</h2>
        <p>
          Our service integrates with Plaid to connect your bank accounts. When you use this feature, 
          you are also subject to Plaid's privacy policy. We recommend reviewing their privacy policy 
          to understand how they handle your information.
        </p>
      </section>

      <section>
        <h2>7. Your Rights</h2>
        <p>
          You have the right to:
        </p>
        <ul>
          <li>Access your personal information</li>
          <li>Correct inaccurate information</li>
          <li>Request deletion of your information</li>
          <li>Object to processing of your information</li>
          <li>Request restriction of processing</li>
          <li>Data portability</li>
        </ul>
      </section>

      <section>
        <h2>8. Changes to This Policy</h2>
        <p>
          We may update this Privacy Policy from time to time. We will notify you of any changes by 
          posting the new Privacy Policy on this page and updating the "Last Updated" date.
        </p>
      </section>

      <section>
        <h2>9. Contact Us</h2>
        <p>
          If you have any questions about this Privacy Policy, please contact us at:
        </p>
        <p>
          Email: privacy@thrivebase.com<br>
          Address: [Your Business Address]
        </p>
      </section>
    </div>
  </div>
</template>

<script setup>
import { defineComponent } from 'vue'

defineComponent({
  name: 'PrivacyPage'
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

ul {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}

li {
  margin-bottom: 0.5rem;
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

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  * {
    transition: none !important;
  }
}
</style>
