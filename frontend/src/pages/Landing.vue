<template>
  <div class="landing-page fade-in">
    <!-- Navbar -->
    <nav class="landing-nav glass">
      <div class="container">
        <div class="brand">
          <img src="/logo.png" alt="Flash-SaaS" class="logo-img" />
          <span>Flash-Saas</span>
        </div>
        <div class="auth-links">
          <router-link :to="{ name: 'login' }" class="nav-link">Login</router-link>
          <router-link :to="{ name: 'register' }" class="btn btn-primary shadow-glow">Get Started</router-link>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <header class="hero">
      <div class="container grid-2">
        <div class="hero-content">
          <div class="badge fade-in">v1.2 Now Live</div>
          <h1 class="gradient-text">Build Your Next Idea at Flash Speed.</h1>
          <p class="subtitle">The complete boilerplate for modern Micro-SaaS projects. Authentication, RBAC, and beautiful Analytics included out of the box.</p>
          <div class="cta-group">
            <router-link :to="{ name: 'register' }" class="btn btn-primary btn-lg shadow-glow">Deploy Your SaaS Now</router-link>
            <a href="#features" class="btn btn-outline btn-lg">View Features</a>
          </div>
        </div>

        <div class="hero-preview fade-in">
          <div class="preview-card glass hover-scale">
            <div class="p-header">
              <div class="p-dots"><span></span><span></span><span></span></div>
              <div class="p-title">Live Preview</div>
            </div>
            <div class="p-body">
              <div class="p-stat">
                <span>Active Users</span>
                <span class="p-value">1,482</span>
              </div>
              <div class="p-chart">
                <div v-for="h in [30, 50, 40, 70, 60, 90]" :key="h" :style="{ height: h + '%' }" class="p-bar"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Features Section -->
    <section id="features" class="features-section">
      <div class="container">
        <h2 class="section-title">Why choose Flash-SaaS?</h2>
        <div class="features-grid">
           <div v-for="feature in features" :key="feature.title" class="feature-card card hover-scale">
             <div class="icon">{{ feature.icon }}</div>
             <h3>{{ feature.title }}</h3>
             <p>{{ feature.description }}</p>
           </div>
        </div>
      </div>
    </section>

    <!-- Interactive Pricing -->
    <section class="pricing-section">
      <div class="container">
        <h2 class="section-title">Scale Without Friction</h2>
        
        <div class="pricing-toggle">
          <span :class="{ active: !isYearly }">Monthly</span>
          <button class="toggle" @click="isYearly = !isYearly">
            <span :class="{ 'toggle-right': isYearly }"></span>
          </button>
          <span :class="{ active: isYearly }">Yearly <small class="save-badge">Save 20%</small></span>
        </div>

        <div class="pricing-grid">
          <div v-for="plan in plans" :key="plan.name" class="pricing-card card" :class="{ 'featured-card': plan.featured }">
            <div v-if="plan.featured" class="most-popular">Most Popular</div>
            <h3>{{ plan.name }}</h3>
            <div class="price">
              <span class="currency">$</span>
              <span class="amount">{{ isYearly ? plan.yearlyPrice : plan.monthlyPrice }}</span>
              <span class="period">/{{ isYearly ? 'year' : 'mo' }}</span>
            </div>
            <ul class="plan-features">
              <li v-for="f in plan.features" :key="f">✅ {{ f }}</li>
            </ul>
            <router-link :to="{ name: 'register' }" class="btn w-full" :class="plan.featured ? 'btn-primary' : 'btn-outline'">
              Choose {{ plan.name }}
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="landing-footer">
      <div class="container">
        <div class="footer-grid">
          <div class="footer-brand">
            <div class="brand">
              <img src="/logo.png" alt="Flash-SaaS" class="logo-img" />
              <span>Flash-SaaS</span>
            </div>
            <p>Empowering developers to build faster.</p>
          </div>
          <div class="footer-links">
            <div class="column">
              <h4>Product</h4>
              <a href="#">Features</a>
              <a href="#">Templates</a>
              <a href="#">Pricing</a>
            </div>
            <div class="column">
              <h4>Company</h4>
              <a href="#">About</a>
              <a href="#">Blog</a>
              <a href="#">Jobs</a>
            </div>
            <div class="column">
              <h4>Support</h4>
              <a href="#">Docs</a>
              <a href="#">Discord</a>
              <a href="#">API</a>
            </div>
          </div>
        </div>
        <div class="footer-bottom">
          <p>© 2026 Micro-SaaS Inc. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isYearly = ref(false)

const features = [
  { title: 'Secure Auth', description: 'JWT-based authentication with auto-refresh and role enforcement.', icon: '🔐' },
  { title: 'Role Management', description: 'Built-in RBAC for Users and Admins with granular permissions.', icon: '🛡️' },
  { title: 'Async DB', description: 'High-performance PostgreSQL with SQLModel and async interactions.', icon: '⚡' },
  { title: 'Premium UI', description: 'Sophisticated dark theme with glassmorphism and modern aesthetics.', icon: '🎨' },
]

const plans = [
  { name: 'Starter', monthlyPrice: 0, yearlyPrice: 0, features: ['1 Project', '1,000 requests/mo', 'Community Support'], featured: false },
  { name: 'Pro', monthlyPrice: 29, yearlyPrice: 280, features: ['Unlimited Projects', '100,000 requests/mo', 'Priority Support', 'Custom Domains'], featured: true },
  { name: 'Enterprise', monthlyPrice: 99, yearlyPrice: 950, features: ['Infinite scalability', 'Unlimited requests', '24/7 Phone Support', 'SLA Guarantee'], featured: false },
]
</script>

<style scoped>
.landing-page {
  background: var(--bg-primary);
  min-height: 100vh;
}

.container {
  max-width: 1240px;
  margin: 0 auto;
  padding: 0 2rem;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 4rem;
  align-items: center;
}

.glass {
  background: rgba(9, 9, 11, 0.7);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border);
}

.landing-nav {
  height: 80px;
  display: flex;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
}

.landing-nav .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.brand {
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-img {
  width: 32px;
  height: 32px;
  object-fit: contain;
}

.auth-links {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-link:hover {
  color: var(--accent-primary);
}

.hero {
  padding: 10rem 0;
  position: relative;
}

.hero-preview {
  display: flex;
  justify-content: center;
}

.preview-card {
  width: 320px;
  padding: 1.5rem;
  border-radius: 20px;
  border: 1px solid var(--border);
}

.p-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.p-dots { display: flex; gap: 4px; }
.p-dots span { width: 8px; height: 8px; border-radius: 50%; background: var(--border); }
.p-title { font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; font-weight: 600; }

.p-stat { display: flex; flex-direction: column; margin-bottom: 1rem; }
.p-value { font-size: 2rem; font-weight: 700; color: var(--accent-primary); }

.p-chart {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  height: 80px;
}

.p-bar {
  flex: 1;
  background: var(--gradient-primary);
  border-radius: 4px 4px 0 0;
  opacity: 0.8;
}

.hero-content {
  text-align: left;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: rgba(99, 102, 241, 0.1);
  color: var(--accent-primary);
  border-radius: 99px;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.gradient-text {
  font-size: 4.5rem;
  line-height: 1.05;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #fff 0%, #a0a0ab 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 800;
  letter-spacing: -0.04em;
}

.subtitle {
  font-size: 1.25rem;
  color: var(--text-secondary);
  margin-bottom: 3rem;
  line-height: 1.6;
}

.cta-group {
  display: flex;
  gap: 1.5rem;
}

.shadow-glow:hover {
  box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
}

.pricing-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 4rem;
}

.save-badge {
  color: var(--success);
  font-weight: 700;
  font-size: 0.7rem;
  text-transform: uppercase;
  background: rgba(16, 185, 129, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
}

.toggle {
  width: 50px;
  height: 26px;
  background: var(--border);
  border-radius: 99px;
  padding: 3px;
  position: relative;
}

.toggle span {
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  display: block;
  transition: all 0.3s ease;
}

.toggle-right {
  transform: translateX(24px);
  background: var(--accent-primary) !important;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.pricing-card {
  padding: 3rem;
  position: relative;
}

.featured-card {
  border-color: var(--accent-primary);
  box-shadow: 0 0 30px rgba(99, 102, 241, 0.1);
}

.most-popular {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--accent-primary);
  color: white;
  padding: 0.25rem 1rem;
  border-radius: 99px;
  font-size: 0.75rem;
  font-weight: 700;
}

.price { margin: 1.5rem 0; }
.currency { font-size: 1.5rem; color: var(--text-secondary); vertical-align: top; }
.amount { font-size: 3.5rem; font-weight: 800; }
.period { color: var(--text-secondary); }

.plan-features {
  list-style: none;
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.footer-grid {
  display: grid;
  grid-template-columns: 1fr 2fr;
  padding-bottom: 4rem;
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}

.footer-links h4 { margin-bottom: 1.5rem; font-size: 1rem; }
.footer-links a { display: block; margin-bottom: 0.75rem; color: var(--text-secondary); transition: all 0.2s; }
.footer-links a:hover { color: var(--accent-primary); }

.footer-bottom {
  border-top: 1px solid var(--border);
  padding: 2rem 0;
  text-align: center;
  color: #555;
  font-size: 0.85rem;
}

@media (max-width: 968px) {
  .grid-2 { grid-template-columns: 1fr; text-align: center; }
  .cta-group { justify-content: center; }
  .gradient-text { font-size: 3rem; }
  .footer-grid { grid-template-columns: 1fr; gap: 3rem; text-align: center; }
  .footer-links { gap: 2rem; }
}
</style>
