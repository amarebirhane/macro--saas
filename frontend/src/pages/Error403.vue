<template>
  <div class="error-page">
    <div class="content fade-in">
      <div class="icon">🚫</div>
      <h1>403 - Forbidden</h1>
      <p>You don't have permission to access this area of the application.</p>
      <router-link to="/dashboard" class="btn btn-primary">
        Back to Dashboard
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.error-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  background: var(--bg-primary);
}

.icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

p {
  color: var(--text-secondary);
  margin-bottom: 2rem;
  max-width: 400px;
}

.content {
  padding: 3rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}
</style>
