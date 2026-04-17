<template>
  <div class="auth-layout">
    <div class="auth-card">
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
  background: radial-gradient(circle at 50% -20%, #1a1a2e, var(--bg-primary));
}

.auth-card {
  width: 100%;
  max-width: 400px;
  padding: 2.5rem;
  background: rgba(20, 20, 22, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.5);
}
</style>
