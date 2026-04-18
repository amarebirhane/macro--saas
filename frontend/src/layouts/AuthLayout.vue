<template>
  <div class="auth-layout">
    <div class="background-blobs">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
    </div>
    
    <div class="auth-card fade-in glass">
      <div class="brand">
        <div class="logo">⚡</div>
        <h2>Micro-SaaS</h2>
      </div>
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-primary);
  overflow: hidden;
  position: relative;
}

.background-blobs {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.blob {
  position: absolute;
  width: 500px;
  height: 500px;
  background: var(--accent-primary);
  filter: blur(120px);
  opacity: 0.15;
  border-radius: 50%;
}

.blob-1 { top: -100px; right: -100px; }
.blob-2 { bottom: -100px; left: -100px; background: #a855f7; }

.auth-card {
  width: 100%;
  max-width: 440px;
  padding: 3rem;
  z-index: 10;
  position: relative;
}

.brand {
  text-align: center;
  margin-bottom: 2.5rem;
}

.logo {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.brand h2 {
  font-size: 1.75rem;
  font-weight: 700;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
