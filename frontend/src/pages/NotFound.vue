<template>
  <div class="not-found-container fade-in">
    <div class="content card glass">
      <div class="emoji">🌌</div>
      <h1>404</h1>
      <h2>Page Not Found</h2>
      <p>The coordinate you're looking for doesn't exist in this sector.</p>
      <button @click="$router.push({ name: 'dashboard' })" class="btn btn-primary">
        Return to Base
      </button>
    </div>
  </div>
</template>

<style scoped>
.not-found-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: radial-gradient(circle at top right, rgba(99, 102, 241, 0.05), transparent),
              radial-gradient(circle at bottom left, rgba(168, 85, 247, 0.05), transparent);
}

.content {
  text-align: center;
  padding: 4rem;
  max-width: 500px;
  width: 100%;
}

.emoji {
  font-size: 5rem;
  margin-bottom: 1.5rem;
  display: block;
}

h1 {
  font-size: 6rem;
  font-weight: 800;
  margin: 0;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1;
}

h2 {
  font-size: 1.75rem;
  margin-bottom: 1rem;
}

p {
  color: var(--text-secondary);
  margin-bottom: 2.5rem;
  font-size: 1.1rem;
}

.btn {
  padding: 0.8rem 2rem;
  font-size: 1rem;
}
</style>
