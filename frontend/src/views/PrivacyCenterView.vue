<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import GlassCard from '../components/GlassCard.vue'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const cardId = ref(route.query.cardId as string || '')
const isDeleting = ref(false)
const showConfirmModal = ref(false)

const privacyPromises = [
  { icon: '🛡️', title: '24小时自动删除', desc: '上传的原始图片在分析完成后 24 小时内会自动从服务器永久抹除。' },
  { icon: '🔒', title: '无身份收集', desc: '我们不要求注册，不收集你的手机号、社交账号或任何身份信息。' },
  { icon: '🧩', title: '数据脱敏', desc: '所有分析结果仅通过随机卡密关联，数据在存储时经过加密处理。' },
  { icon: '✂️', title: '随时主动删除', desc: '你可以随时通过此页面，凭卡密一键删除服务器上存储的所有关联数据。' }
]

const handleDelete = async () => {
  if (!cardId.value) {
    alert('请输入卡密以执行删除操作')
    return
  }
  
  showConfirmModal.value = true
}

const confirmDelete = async () => {
  isDeleting.value = true
  try {
    // 触发碎纸机动画的逻辑
    const cardElement = document.querySelector('.confirm-modal-content')
    if (cardElement) {
      cardElement.classList.add('shredding')
    }

    await axios.post('/api/v1/analysis/delete', {
      card_id: cardId.value,
      confirm: true
    })
    
    setTimeout(() => {
      alert('数据已从物理层彻底抹除，卡密已失效。')
      router.push('/')
    }, 800)
  } catch (error: any) {
    alert(error.response?.data?.detail?.message || '删除失败，请检查卡密是否正确')
    isDeleting.value = false
    showConfirmModal.value = false
  }
}
</script>

<template>
  <main class="min-h-screen pt-12 pb-24 px-6 animate-in fade-in duration-500">
    <div class="max-w-2xl mx-auto">
      <div class="text-center mb-12">
        <h1 class="text-3xl font-bold mb-4">隐私中心</h1>
        <p class="text-gray-400">你的隐私安全是我们最高优先级</p>
      </div>

      <!-- 隐私承诺卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-12">
        <GlassCard v-for="promise in privacyPromises" :key="promise.title" class="p-6">
          <div class="text-3xl mb-4">{{ promise.icon }}</div>
          <h3 class="font-bold text-lg mb-2">{{ promise.title }}</h3>
          <p class="text-sm text-gray-400 leading-relaxed">{{ promise.desc }}</p>
        </GlassCard>
      </div>

      <!-- 删除数据区 -->
      <GlassCard class="border-status-danger/20 bg-status-danger/5">
        <h3 class="text-xl font-bold text-status-danger mb-4 flex items-center gap-2">
          <span>⚠️</span> 危险区域
        </h3>
        <p class="text-sm text-gray-400 mb-6">
          在此输入你的卡密，我们将立即从服务器上彻底删除该卡密关联的所有分析报告和图片记录。此操作不可撤销，且删除后卡密将永久失效。
        </p>
        
        <div class="flex flex-col sm:flex-row gap-4">
          <input 
            v-model="cardId"
            type="text" 
            placeholder="输入 16 位卡密"
            class="flex-1 bg-white/5 border border-white/10 rounded-xl py-3 px-4 font-mono focus:border-status-danger outline-none transition-all"
          />
          <button 
            @click="handleDelete"
            class="bg-status-danger hover:bg-red-600 text-white font-bold py-3 px-8 rounded-xl transition-all active:scale-95"
          >
            永久删除我的数据
          </button>
        </div>
      </GlassCard>

      <div class="mt-12 text-center">
        <button @click="router.back()" class="text-gray-500 hover:text-white transition-colors flex items-center justify-center gap-2 mx-auto">
          <span>←</span> 返回上一页
        </button>
      </div>
    </div>

    <!-- 二次确认模态框 -->
    <div v-if="showConfirmModal" class="fixed inset-0 z-50 flex items-center justify-center px-6">
      <div class="absolute inset-0 bg-black/80 backdrop-blur-sm" @click="showConfirmModal = false"></div>
      <GlassCard class="max-w-md w-full p-8 z-10 text-center animate-in zoom-in duration-300 confirm-modal-content">
        <div class="text-5xl mb-6">🗑️</div>
        <h2 class="text-2xl font-bold mb-4">确认彻底删除？</h2>
        <p class="text-gray-400 mb-8 leading-relaxed">
          你即将删除卡密 <span class="text-white font-mono">{{ cardId }}</span> 的所有关联数据。删除后将无法恢复，且该卡密将无法再次使用。
        </p>
        <div class="flex flex-col gap-3">
          <button 
            @click="confirmDelete"
            :disabled="isDeleting"
            class="w-full py-4 bg-status-danger text-white font-bold rounded-xl shadow-lg hover:bg-red-600 transition-all"
          >
            {{ isDeleting ? '正在销毁数据...' : '是的，立即销毁' }}
          </button>
          <button 
            @click="showConfirmModal = false"
            class="w-full py-4 bg-white/5 hover:bg-white/10 font-bold rounded-xl transition-all"
          >
            取消
          </button>
        </div>
      </GlassCard>
    </div>
  </main>
</template>

<style scoped>
@keyframes shred {
  0% { transform: translateY(0) rotate(0deg); opacity: 1; }
  100% { transform: translateY(200px) rotate(5deg) scale(0.8); opacity: 0; filter: blur(10px); }
}
.shredding {
  animation: shred 800ms ease-in forwards;
  pointer-events: none;
}
</style>
