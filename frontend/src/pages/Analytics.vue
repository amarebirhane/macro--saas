<template>
  <div class="analytics-page fade-in">
    <div class="row">
      <div class="card glass">
        <h3>System Growth</h3>
        <p>User registrations over the last 30 days.</p>
        <div class="chart-placeholder">
          <div v-for="h in [40, 60, 45, 80, 55, 90, 70]" :key="h" class="bar" :style="{ height: h + '%' }"></div>
        </div>
      </div>
    </div>

    <div class="stats-grid">
      <div class="card">
        <h4>Conversion Rate</h4>
        <p class="value">3.2%</p>
        <p class="trend positive">+0.4% this month</p>
      </div>
      <div class="card">
        <h4>Avg. Session</h4>
        <p class="value">12m 45s</p>
        <p class="trend positive">+2m vs last week</p>
      </div>
      <div class="card">
        <h4>Error Rate</h4>
        <p class="value">0.12%</p>
        <p class="trend negative">+0.02%</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.analytics-page {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.chart-placeholder {
  height: 250px;
  display: flex;
  align-items: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding: 0 1rem;
}

.bar {
  flex: 1;
  background: var(--gradient-primary);
  border-radius: 4px 4px 0 0;
  opacity: 0.8;
  transition: all 0.3s ease;
}

.bar:hover {
  opacity: 1;
  transform: scaleX(1.1);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.value {
  font-size: 2rem;
  font-weight: 700;
  margin: 0.5rem 0;
}

.trend {
  font-size: 0.85rem;
  font-weight: 600;
}

.positive { color: var(--success); }
.negative { color: var(--error); }
</style>
