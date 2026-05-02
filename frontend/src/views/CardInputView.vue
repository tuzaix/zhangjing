<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import GlassCard from '@/components/GlassCard.vue'
import CardInput from '@/components/CardInput.vue'
import axios from 'axios'

const router = useRouter()
const cardId = ref('')
const isVerifying = ref(false)
const errorMessage = ref('')
const historyCards = ref<string[]>([])

onMounted(() => {
  loadHistory()
})

const loadHistory = () => {
  const saved = localStorage.getItem('analysis_history')
  if (saved) {
    historyCards.value = JSON.parse(saved)
  }
}

const saveToHistory = (id: string) => {
  let history = [...historyCards.value]
  if (!history.includes(id)) {
    history.unshift(id)
    history = history.slice(0, 3) // Only keep last 3
    localStorage.setItem('analysis_history', JSON.stringify(history))
    historyCards.value = history
  }
}

const useHistory = (id: string) => {
  cardId.value = id
  handleVerify()
}

const handleVerify = async () => {
  if (cardId.value.replace(/-/g, '').length !== 16) {
    errorMessage.value = '请输入完整的 16 位卡密'
    return
  }

  isVerifying.value = true
  errorMessage.value = ''
  
  try {
    const response = await axios.post('/api/v1/card/verify', {
      card_id: cardId.value
    })
    
    const { status, has_cache, cached_mode } = response.data
    
    saveToHistory(cardId.value)
    
    if (status === 'not_activated') {
      router.push({ name: 'analysis-type', query: { cardId: cardId.value } })
    } else if (status === 'activated') {
      if (has_cache && cached_mode) {
        // 如果已有缓存，直接跳转结果页
        router.push({ 
          name: 'result', 
          query: { 
            cardId: cardId.value,
            mode: cached_mode
          } 
        })
      } else {
        // 否则进入分析类型选择（或者根据业务逻辑直接进入模式选择）
        router.push({ name: 'analysis-type', query: { cardId: cardId.value } })
      }
    }
  } catch (error: any) {
    // ... same error handling
    if (error.response && error.response.data && error.response.data.detail) {
      errorMessage.value = error.response.data.detail.message
    } else {
      errorMessage.value = '服务器连接失败，请稍后再试'
    }
  } finally {
    isVerifying.value = false
  }
}
</script>

<template>
  <main class="flex flex-col items-center justify-center min-h-[calc(100vh-80px)] px-2 sm:px-4">
    <div class="w-full max-w-lg">
      <h2 class="text-xl sm:text-2xl font-bold text-center mb-8">输入您的分析卡密</h2>
      
      <GlassCard class="text-center px-3 sm:px-6" glow>
        <div class="mb-8">
          <div class="w-20 h-20 bg-primary-gold/10 rounded-full flex items-center justify-center mx-auto mb-4 glow-effect animate-pulse">
            <span class="text-3xl">🔐</span>
          </div>
          <p class="text-gray-400">输入 16 位卡密，即可查看您的专属分析报告</p>
        </div>

        <div class="mb-8">
          <CardInput v-model="cardId" @complete="handleVerify" />
          
          <!-- 历史记录 -->
          <div v-if="historyCards.length > 0" class="mt-4 flex flex-wrap justify-center gap-2">
            <span class="text-xs text-gray-500 w-full mb-1">最近使用:</span>
            <button 
              v-for="id in historyCards" 
              :key="id"
              @click="useHistory(id)"
              class="text-xs bg-white/5 hover:bg-white/10 border border-white/10 py-1 px-3 rounded-full transition-colors font-mono"
            >
              {{ id.split('-')[0] }}-...-{{ id.split('-')[3] }}
            </button>
          </div>

          <p v-if="errorMessage" class="mt-4 text-status-danger text-sm animate-bounce">
            {{ errorMessage }}
          </p>
        </div>

        <button 
          @click="handleVerify"
          :disabled="isVerifying || cardId.replace(/-/g, '').length !== 16"
          class="w-full py-4 bg-gold-gradient rounded-xl font-bold text-lg shadow-lg disabled:opacity-50 disabled:grayscale transition-all hover:scale-[1.02] active:scale-[0.98]"
        >
          <span v-if="isVerifying" class="flex items-center justify-center gap-2">
            <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            验证中...
          </span>
          <span v-else>验证卡密</span>
        </button>
      </GlassCard>
      
      <div class="mt-8 flex items-center justify-center gap-4 text-sm">
        <!-- <a href="#" class="text-secondary-blue hover:text-white transition-colors">没有卡密？立即购买</a>
        <span class="text-gray-700">|</span>
        <a href="#" class="text-secondary-blue hover:text-white transition-colors">邀请好友免费得</a> -->
      </div>
    </div>
  </main>
</template>
