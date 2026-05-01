<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import GlassCard from '../components/GlassCard.vue'
import axios from 'axios'
import html2canvas from 'html2canvas'

const route = useRoute()
const router = useRouter()
const cardId = route.query.cardId as string

const result = ref<any>(null)
const isLoading = ref(true)
const isGenerating = ref(false)
const shareImageUrl = ref<string | null>(null)
const cardRef = ref<HTMLElement | null>(null)

const cardTemplates = [
  { id: 1, name: '高光时刻', desc: '人生巅峰预测', icon: '✨', quote: '你的手相显示出极强的创造力，未来三个月将迎来事业的重大突破。' },
  { id: 2, name: '精准预言', desc: '具体事件预测', icon: '🎯', quote: '感情线清晰且深长，预示着你将遇到一段长久且稳定的缘分。' },
  { id: 3, name: '性格标签', desc: '核心性格总结', icon: '🏷️', quote: '外柔内刚，你拥有超乎常人的洞察力和决策力。' },
  { id: 4, name: '反差萌', desc: '有趣的性格反差', icon: '🐱', quote: '看似高冷的外表下，藏着一颗极其温柔且热爱生活的心。' },
  { id: 5, name: '情感共鸣', desc: '感情线深度解读', icon: '💖', quote: '珍惜当下的每一份感动，你的幸福指数正在稳步上升。' },
  { id: 6, name: '锦鲤体质', icon: '🐟', desc: '好运指数', quote: '好运连连，近期在偏财方面会有意外的惊喜。' }
]

const selectedCard = ref(cardTemplates[0])

const fetchResult = async () => {
  isLoading.value = true
  try {
    const response = await axios.get(`/api/v1/analysis/get/${cardId}`)
    result.value = response.data.data
  } catch (error) {
    console.error('Failed to fetch result', error)
  } finally {
    isLoading.value = false
  }
}

const generateCard = async () => {
  if (!cardRef.value) return
  
  isGenerating.value = true
  try {
    const canvas = await html2canvas(cardRef.value, {
      useCORS: true,
      scale: 2,
      backgroundColor: '#0f172a',
    })
    shareImageUrl.value = canvas.toDataURL('image/png')
    
    // 记录分享行为
    try {
      await axios.post('/api/v1/analysis/share/record', {
        card_id: cardId,
        template_id: selectedCard.value.id
      })
    } catch (e) {
      console.error('Failed to record share', e)
    }
  } catch (error) {
    console.error('Failed to generate card image', error)
    alert('生成失败，请重试')
  } finally {
    isGenerating.value = false
  }
}

onMounted(() => {
  fetchResult()
})
</script>

<template>
  <main class="min-h-screen pt-12 pb-24 px-6 animate-in fade-in duration-500">
    <div class="max-w-2xl mx-auto">
      <div class="text-center mb-12">
        <h1 class="text-3xl font-bold mb-4">生成分享卡片</h1>
        <p class="text-gray-400">挑选一个你喜欢的模板，分享给好友吧</p>
      </div>

      <!-- 预览区 (将被捕捉的 DOM) -->
      <div class="mb-12 flex justify-center">
        <div 
          ref="cardRef"
          class="w-full max-w-[320px] aspect-[3/4] glass-card p-6 flex flex-col items-center justify-between text-center relative overflow-hidden border-primary-gold/30"
        >
          <div class="absolute inset-0 bg-gold-gradient opacity-5"></div>
          
          <div class="z-10 w-full pt-4">
            <div class="text-5xl mb-4">{{ selectedCard.icon }}</div>
            <h2 class="text-2xl font-bold text-primary-gold mb-1">{{ selectedCard.name }}</h2>
            <p class="text-xs text-gray-400">{{ selectedCard.desc }}</p>
          </div>

          <div class="z-10 w-full space-y-4">
            <div class="p-4 bg-white/5 rounded-xl border border-white/10">
              <p class="text-sm italic leading-relaxed text-gray-200">
                "{{ selectedCard.quote }}"
              </p>
            </div>
            
            <div class="pt-4 border-t border-white/10 flex flex-col items-center gap-1">
              <div class="flex items-center gap-2 mb-1">
                <span class="text-xs text-gray-500">综合运势评分</span>
                <span class="text-lg font-bold text-primary-gold" v-if="result">{{ result.summary.overall_score }}</span>
              </div>
              <p class="text-[10px] text-gray-500 uppercase tracking-widest">Verification Card</p>
              <p class="font-mono text-sm text-primary-gold">
                {{ cardId.split('-')[0] }}-****-****-{{ cardId.split('-')[3] }}
              </p>
              <p class="text-[8px] text-gray-600 mt-2">AI Hand Analysis Service v4.0</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 模板选择 -->
      <div class="grid grid-cols-3 gap-3 mb-12">
        <button 
          v-for="template in cardTemplates" 
          :key="template.id"
          @click="selectedCard = template"
          :class="[
            'p-4 rounded-xl border transition-all flex flex-col items-center gap-2',
            selectedCard.id === template.id 
              ? 'bg-primary-gold/20 border-primary-gold scale-105' 
              : 'bg-white/5 border-white/10 hover:border-white/30'
          ]"
        >
          <span class="text-2xl">{{ template.icon }}</span>
          <span class="text-xs font-bold">{{ template.name }}</span>
        </button>
      </div>

      <div class="flex flex-col gap-4">
        <button 
          @click="generateCard"
          :disabled="isGenerating || isLoading"
          class="w-full py-4 bg-gold-gradient rounded-2xl font-bold text-lg shadow-lg flex items-center justify-center gap-3 active:scale-95 transition-all"
        >
          <span v-if="isGenerating" class="animate-spin text-xl">🌀</span>
          <span>{{ isGenerating ? '正在绘图中...' : '保存到相册 / 分享' }}</span>
        </button>
        <button @click="router.back()" class="py-4 text-gray-500 hover:text-white transition-colors">
          取消
        </button>
      </div>
    </div>

    <!-- 生成结果模态框 -->
    <div v-if="shareImageUrl" class="fixed inset-0 z-50 flex items-center justify-center px-6">
      <div class="absolute inset-0 bg-black/90 backdrop-blur-sm" @click="shareImageUrl = null"></div>
      <div class="relative z-10 w-full max-w-sm flex flex-col items-center gap-6 animate-in zoom-in duration-300">
        <img :src="shareImageUrl" class="w-full rounded-2xl shadow-2xl border border-white/10" />
        <p class="text-white font-bold flex items-center gap-2">
          <span>☝️</span> 长按图片保存并分享
        </p>
        <button 
          @click="shareImageUrl = null"
          class="w-12 h-12 rounded-full bg-white/10 flex items-center justify-center text-white text-xl hover:bg-white/20 transition-colors"
        >
          ✕
        </button>
      </div>
    </div>
  </main>
</template>

<style scoped>
/* 确保截图时背景色正确 */
.glass-card {
  background: rgba(255, 255, 255, 0.05);
}
</style>
