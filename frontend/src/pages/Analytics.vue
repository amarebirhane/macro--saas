<template>
  <div class="analytics-page fade-in">
    <div class="analytics-header">
      <div class="title-area">
        <h3>Platform Analytics</h3>
        <p>Real-time system performance and user growth metrics.</p>
      </div>
      <div class="date-selector">
        <button v-for="range in ranges" :key="range" 
                :class="{ active: selectedRange === range }"
                @click="selectedRange = range">
          {{ range }}
        </button>
      </div>
    </div>

    <div class="main-chart card glass">
      <div class="chart-header">
        <div class="chart-title">
          <h4>User Growth</h4>
          <span class="growth-text positive">↑ 12.5% vs last period</span>
        </div>
        <div class="legend">
          <span class="legend-item"><span class="dot primary"></span> New Users</span>
          <span class="legend-item"><span class="dot secondary"></span> Returning</span>
        </div>
      </div>
      <div class="chart-container">
        <div class="chart-y-axis">
          <span>10k</span>
          <span>7.5k</span>
          <span>5k</span>
          <span>2.5k</span>
          <span>0</span>
        </div>
        <div class="chart-bars">
          <div v-for="(val, i) in chartData" :key="i" class="bar-wrapper">
            <div class="bar-pair">
              <div class="bar returning" :style="{ height: val.returning + '%' }">
                <div class="tooltip">{{ val.returning }}% Returning</div>
              </div>
              <div class="bar new" :style="{ height: val.new + '%' }">
                <div class="tooltip">{{ val.new }}% New</div>
              </div>
            </div>
            <span class="bar-label">{{ val.label }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card card">
        <div class="stat-icon">📈</div>
        <div class="stat-content">
          <p class="label">Conversion Rate</p>
          <p class="value">3.24%</p>
          <p class="trend positive">+0.42% <span class="time">this month</span></p>
        </div>
      </div>
      <div class="stat-card card">
        <div class="stat-icon">⏱️</div>
        <div class="stat-content">
          <p class="label">Avg. Session</p>
          <p class="value">12m 45s</p>
          <p class="trend positive">+2m 12s <span class="time">vs last week</span></p>
        </div>
      </div>
      <div class="stat-card card">
        <div class="stat-icon">⚠️</div>
        <div class="stat-content">
          <p class="label">Error Rate</p>
          <p class="value">0.12%</p>
          <p class="trend negative">+0.02% <span class="time">since yesterday</span></p>
        </div>
      </div>
      <div class="stat-card card">
        <div class="stat-icon">💸</div>
        <div class="stat-content">
          <p class="label">Total MRR</p>
          <p class="value">$24,450</p>
          <p class="trend positive">+8% <span class="time">growth</span></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const ranges = ['24h', '7d', '30d', '90d']
const selectedRange = ref('30d')

const chartData = ref([
  { label: 'Mon', new: 40, returning: 30 },
  { label: 'Tue', new: 55, returning: 35 },
  { label: 'Wed', new: 45, returning: 40 },
  { label: 'Thu', new: 80, returning: 50 },
  { label: 'Fri', new: 65, returning: 45 },
  { label: 'Sat', new: 90, returning: 60 },
  { label: 'Sun', new: 75, returning: 55 }
])
</script>

<style scoped>
.analytics-page {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.analytics-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.title-area h3 { margin-bottom: 0.25rem; }
.title-area p { color: var(--text-secondary); font-size: 0.95rem; }

.date-selector {
  display: flex;
  background: var(--bg-secondary);
  padding: 0.25rem;
  border-radius: 8px;
  border: 1px solid var(--border);
}

.date-selector button {
  padding: 0.4rem 1rem;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s;
}

.date-selector button.active {
  background: var(--accent-primary);
  color: white;
}

.main-chart {
  padding: 2rem;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 2.5rem;
}

.chart-title h4 { margin-bottom: 0.25rem; }
.growth-text { font-size: 0.85rem; font-weight: 700; }

.legend { display: flex; gap: 1.5rem; }
.legend-item { display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; color: var(--text-secondary); }
.dot { width: 8px; height: 8px; border-radius: 50%; }
.dot.primary { background: var(--accent-primary); }
.dot.secondary { background: rgba(99, 102, 241, 0.3); }

.chart-container {
  display: flex;
  height: 300px;
  gap: 2rem;
}

.chart-y-axis {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  color: var(--text-secondary);
  font-size: 0.75rem;
  padding-bottom: 2rem;
}

.chart-bars {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  border-bottom: 1px solid var(--border);
  padding-bottom: 0.5rem;
}

.bar-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.bar-pair {
  width: 32px;
  height: 240px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 2px;
}

.bar {
  width: 100%;
  border-radius: 4px;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
  cursor: pointer;
}

.bar.new { background: var(--accent-primary); }
.bar.returning { background: rgba(99, 102, 241, 0.3); }

.bar:hover { filter: brightness(1.2); transform: scaleX(1.1); }

/* Tooltip on bar hover */
.tooltip {
  position: absolute;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--bg-primary);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
  box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  z-index: 10;
}

.bar:hover .tooltip { opacity: 1; }

.bar-label {
  color: var(--text-secondary);
  font-size: 0.8rem;
  font-weight: 500;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.5rem;
}

.stat-icon {
  width: 48px;
  height: 48px;
  background: var(--bg-secondary);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  border: 1px solid var(--border);
}

.stat-content { flex: 1; }
.stat-content .label { font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.25rem; }
.stat-content .value { font-size: 1.5rem; font-weight: 700; margin-bottom: 0.25rem; }
.stat-content .trend { font-size: 0.75rem; font-weight: 700; }
.stat-content .time { font-weight: 400; color: var(--text-secondary); }

.positive { color: var(--success); }
.negative { color: var(--error); }
</style>
