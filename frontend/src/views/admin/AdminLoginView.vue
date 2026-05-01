<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const username = ref('')
const password = ref('')
const isLoading = ref(false)
const error = ref('')

const handleLogin = async () => {
  if (!username.value || !password.value) return
  
  isLoading.value = true
  error.value = ''
  
  try {
    const response = await axios.post('/api/v1/admin/login', {
      username: username.value,
      password: password.value
    })
    
    sessionStorage.setItem('admin_token', response.data.token)
    router.push({ name: 'admin-dashboard' })
  } catch (err: any) {
    error.value = err.response?.data?.detail || '登录失败，请检查用户名和密码'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-bg-dark px-6">
    <div class="w-full max-w-md">
      <div class="text-center mb-10">
        <h1 class="text-3xl font-bold text-white mb-2 tracking-tight">管理后台登录</h1>
        <p class="text-gray-500 uppercase text-xs tracking-widest font-mono">ZHANGJING AI VISION ADMIN</p>
      </div>
      
      <div class="glass-card p-8 border-white/5 bg-white/5">
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">用户名</label>
            <input 
              v-model="username"
              type="text" 
              class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-primary-purple transition-all outline-none"
              placeholder="请输入用户名"
              required
            />
          </div>
          
          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">密码</label>
            <input 
              v-model="password"
              type="password" 
              class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-primary-purple transition-all outline-none"
              placeholder="请输入密码"
              required
            />
          </div>
          
          <p v-if="error" class="text-status-danger text-xs bg-status-danger/10 p-3 rounded-lg border border-status-danger/20 animate-pulse">
            {{ error }}
          </p>
          
          <button 
            type="submit"
            :disabled="isLoading"
            class="w-full py-4 bg-gold-gradient rounded-xl font-bold text-lg shadow-lg hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-2"
          >
            <span v-if="isLoading" class="animate-spin text-xl">⏳</span>
            {{ isLoading ? '登录中...' : '进入后台' }}
          </button>
        </form>
      </div>
      
      <p class="mt-8 text-center">
        <router-link to="/" class="text-gray-500 hover:text-white transition-colors text-sm">返回首页</router-link>
      </p>
    </div>
  </div>
</template>
