<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import GlassCard from '@/components/GlassCard.vue'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const cardId = route.query.cardId as string
const mode = (route.query.mode as string) || 'standard'
const type = (route.query.type as string) || 'personal'

const currentStep = ref(0)
const progress = ref(0)
const steps = [
  { name: '图像识别中', duration: 3000 },
  { name: '纹路提取中', duration: 4000 },
  { name: 'AI 分析中', duration: 6000 },
  { name: '报告生成中', duration: 3000 }
]

let timer: any = null

const startAnimation = () => {
  let startTime = Date.now()
  const totalDuration = steps.reduce((acc, step) => acc + step.duration, 0)

  timer = setInterval(() => {
    const elapsed = Date.now() - startTime
    progress.value = Math.min((elapsed / totalDuration) * 100, 99)

    // Calculate current step
    let accumulated = 0
    for (let i = 0; i < steps.length; i++) {
      accumulated += steps[i].duration
      if (elapsed < accumulated) {
        currentStep.value = i
        break
      }
    }
  }, 50)
}

const triggerAnalysis = async () => {
  try {
    await axios.post('/api/v1/analysis/start', {
      card_id: cardId,
      mode: mode,
      type: type
    })
    
    // Once backend is done, wait for animation to finish or jump
    setTimeout(() => {
      progress.value = 100
      setTimeout(() => {
        router.push({ 
          name: 'result', 
          query: { 
            cardId,
            mode: mode
          } 
        })
      }, 500)
    }, 15000) // Match the total animation duration roughly
  } catch (error) {
    console.error('Analysis failed', error)
    alert('分析启动失败，请重试')
    router.back()
  }
}

onMounted(() => {
  startAnimation()
  triggerAnalysis()
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<template>
  <main class="flex flex-col items-center justify-center min-h-[calc(100vh-80px)] px-4">
    <div class="w-full max-w-lg text-center">
      <div class="mb-12 relative">
        <!-- 核心动画容器 -->
        <div class="w-48 h-48 mx-auto relative">
          <div class="absolute inset-0 rounded-full border-4 border-primary-purple/20"></div>
          <div 
            class="absolute inset-0 rounded-full border-4 border-primary-purple border-t-transparent animate-spin"
            :style="{ animationDuration: '2s' }"
          ></div>
          
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="text-4xl animate-bounce">
              <span v-if="currentStep === 0">🔍</span>
              <span v-if="currentStep === 1">🧬</span>
              <span v-if="currentStep === 2">🧠</span>
              <span v-if="currentStep === 3">📄</span>
            </div>
          </div>
        </div>

        <!-- 扫描线效果 -->
        <div v-if="currentStep < 2" class="absolute top-0 left-1/2 -translate-x-1/2 w-64 h-64 overflow-hidden pointer-events-none">
          <div class="w-full h-1 bg-primary-purple/50 shadow-[0_0_15px_rgba(99,102,241,0.8)] animate-scan"></div>
        </div>
      </div>

      <h2 class="text-2xl font-bold mb-4">{{ steps[currentStep].name }}</h2>
      <p class="text-gray-400 mb-8">
        {{ type === 'personal' ? 'AI 正在深度解析你的命运纹路，请稍候...' : 'AI 正在深度解析双方的命运契合度，请稍候...' }}
      </p>

      <div class="w-full h-2 bg-white/5 rounded-full overflow-hidden mb-4">
        <div 
          class="h-full bg-gold-gradient transition-all duration-300"
          :style="{ width: `${progress}%` }"
        ></div>
      </div>
      
      <div class="flex justify-between text-xs text-gray-500 font-mono">
        <span>PROGRESS: {{ Math.floor(progress) }}%</span>
        <span>STATUS: ACTIVE</span>
      </div>

      <GlassCard class="mt-12 text-left bg-primary-purple/5 border-primary-purple/10">
        <h4 class="text-sm font-bold text-primary-purple mb-2">💡 专家提示</h4>
        <p class="text-xs text-gray-400 leading-relaxed">
          分析过程中请勿关闭页面。AI 智能引擎正在识别超过 120 个手相特征点，以确保为您提供最精准的分析报告。
        </p>
      </GlassCard>
    </div>
  </main>
</template>

<style scoped>
@keyframes scan {
  0% { transform: translateY(0); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateY(256px); opacity: 0; }
}
.animate-scan {
  animation: scan 2s linear infinite;
}
</style>
