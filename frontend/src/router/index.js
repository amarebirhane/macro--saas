import { createRouter, createWebHistory } from 'vue-router'
import { setupGuards } from './guards'

const routes = [
  {
    path: '/',
    name: 'landing',
    component: () => import('../pages/Landing.vue')
  },
  {
    path: '/auth',
    component: () => import('../layouts/AuthLayout.vue'),
    children: [
      {
        path: 'login',
        name: 'login',
        component: () => import('../pages/Login.vue')
      },
      {
        path: 'register',
        name: 'register',
        component: () => import('../pages/Register.vue')
      }
    ]
  },
  {
    path: '/',
    component: () => import('../layouts/DashboardLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: { name: 'dashboard' }
      },
      {
        path: 'dashboard',
        name: 'dashboard',
        component: () => import('../pages/Dashboard.vue')
      },
      {
        path: 'profile',
        name: 'profile',
        component: () => import('../pages/Profile.vue')
      },
      {
        path: 'my-data',
        name: 'my-data',
        component: () => import('../pages/MyData.vue')
      },
      // Admin Routes
      {
        path: 'admin',
        meta: { requiresAdmin: true },
        children: [
          {
            path: '',
            name: 'admin-dashboard',
            component: () => import('../pages/AdminDashboard.vue')
          },
          {
            path: 'users',
            name: 'admin-users',
            component: () => import('../pages/UserManagement.vue')
          },
          {
            path: 'analytics',
            name: 'admin-analytics',
            component: () => import('../pages/Analytics.vue')
          }
        ]
      }
    ]
  },
  {
    path: '/403',
    name: 'error-403',
    component: () => import('../pages/Error403.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('../pages/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

setupGuards(router)

// Dynamic Document Titles
router.afterEach((to) => {
  const baseTitle = 'Flash-SaaS'
  const routeName = to.name ? to.name.toString() : ''
  const subTitle = routeName 
    ? routeName.charAt(0).toUpperCase() + routeName.slice(1).replace('-', ' ') 
    : ''
  
  document.title = subTitle ? `${subTitle} | ${baseTitle}` : baseTitle
})

export default router
