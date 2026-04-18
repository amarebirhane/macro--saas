<template>
  <div class="landing-page fade-in">
    <!-- Navbar -->
    <nav class="landing-nav glass">
      <div class="container">
        <div class="brand">⚡ Micro-SaaS</div>
        <div class="auth-links">
          <router-link :to="{ name: 'login' }" class="nav-link">Login</router-link>
          <router-link :to="{ name: 'register' }" class="btn btn-primary">Start Free</router-link>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <header class="hero">
      <div class="container">
        <div class="hero-content">
          <h1 class="gradient-text">Build Your Next Idea at Flash Speed.</h1>
          <p class="subtitle">The complete boilerplate for modern Micro-SaaS projects. Authentication, RBAC, and beautiful Analytics included out of the box.</p>
          <div class="cta-group">
            <router-link :to="{ name: 'register' }" class="btn btn-primary btn-lg">Deploy in Seconds</router-link>
            <a href="#features" class="btn btn-outline">See Features</a>
          </div>
        </div>
      </div>
    </header>

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

    <!-- Footer -->
    <footer class="landing-footer">
      <div class="container">
        <p>© 2026 Micro-SaaS Inc. Built with FastAPI and Vue 3.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
const features = [
  { title: 'Secure Auth', description: 'JWT-based authentication with auto-refresh and role enforcement.', icon: '🔐' },
  { title: 'Role Management', description: 'Built-in RBAC for Users and Admins with granular permissions.', icon: '🛡️' },
  { title: 'Async DB', description: 'High-performance PostgreSQL with SQLModel and async interactions.', icon: '⚡' },
  { title: 'Premium UI', description: 'Sophisticated dark theme with glassmorphism and modern aesthetics.', icon: '🎨' },
]
</script>

<style scoped>
.landing-page {
  background: var(--bg-primary);
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.glass {
  background: rgba(9, 9, 11, 0.8);
  backdrop-filter: blur(12px);
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
  font-weight: 700;
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
  padding: 8rem 0;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.hero::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 600px;
  height: 600px;
  background: var(--accent-primary);
  filter: blur(150px);
  opacity: 0.1;
  z-index: 0;
}

.hero-content {
  position: relative;
  z-index: 10;
  max-width: 800px;
  margin: 0 auto;
}

.gradient-text {
  font-size: 4.5rem;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #fff 0%, var(--text-secondary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  font-size: 1.25rem;
  color: var(--text-secondary);
  margin-bottom: 3rem;
  line-height: 1.6;
}

.cta-group {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
}

.btn-lg {
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
}

.btn-outline {
  border: 1px solid var(--border);
}

.btn-outline:hover {
  background: var(--border);
}

.features-section {
  padding: 6rem 0;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 4rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  padding: 2.5rem;
  text-align: center;
}

.feature-card .icon {
  font-size: 3rem;
  margin-bottom: 1.5rem;
}

.feature-card h3 {
  margin-bottom: 1rem;
}

.feature-card p {
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.landing-footer {
  padding: 4rem 0;
  text-align: center;
  border-top: 1px solid var(--border);
  color: var(--text-secondary);
}

@media (max-width: 768px) {
  .gradient-text { font-size: 3rem; }
  .cta-group { flex-direction: column; }
}
</style>
