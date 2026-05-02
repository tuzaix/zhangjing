import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/card-input',
      name: 'card-input',
      component: () => import('../views/CardInputView.vue')
    },
    {
      path: '/analysis-type',
      name: 'analysis-type',
      component: () => import('../views/AnalysisTypeView.vue')
    },
    {
      path: '/upload',
      name: 'upload',
      component: () => import('../views/UploadView.vue')
    },
    {
      path: '/bestie-upload',
      name: 'bestie-upload',
      component: () => import('../views/BestieUploadView.vue')
    },
    {
      path: '/couple-upload',
      name: 'couple-upload',
      component: () => import('../views/CoupleUploadView.vue')
    },
    {
      path: '/mode-select',
      name: 'mode-select',
      component: () => import('../views/ModeSelectView.vue')
    },
    {
      path: '/loading',
      name: 'loading',
      component: () => import('../views/LoadingView.vue')
    },
    {
      path: '/result',
      name: 'result',
      component: () => import('../views/ResultView.vue')
    },
    {
      path: '/privacy-center',
      name: 'privacy-center',
      component: () => import('../views/PrivacyCenterView.vue')
    },
    {
      path: '/share',
      name: 'share',
      component: () => import('../views/ShareView.vue')
    },
    // 管理后台
    {
      path: '/admin/login',
      name: 'admin-login',
      component: () => import('../views/admin/AdminLoginView.vue')
    },
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: () => import('../views/admin/AdminDashboardView.vue'),
      beforeEnter: (to, from, next) => {
        const token = sessionStorage.getItem('admin_token')
        if (!token) {
          next({ name: 'admin-login' })
        } else {
          next()
        }
      }
    }
  ]
})

export default router
