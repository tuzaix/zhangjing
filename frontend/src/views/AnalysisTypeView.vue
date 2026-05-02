<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import GlassCard from '@/components/GlassCard.vue'

const route = useRoute()
const router = useRouter()
const cardId = route.query.cardId as string

const analysisTypes = [
  { 
    id: 'personal', 
    name: '个人版', 
    icon: '👤', 
    desc: '深度解析个人先天命格与后天运势，提供全方位的成长建议。',
    path: 'upload'
  },
  { 
    id: 'bestie', 
    name: '闺蜜匹配', 
    icon: '👯‍♀️', 
    desc: '分析双人性格契合度，解密友谊长存的密码。',
    path: 'bestie-upload'
  },
  { 
    id: 'couple', 
    name: '情侣匹配', 
    icon: '👩‍❤️‍👨', 
    desc: '对比双方掌纹特质，分析情感匹配度与正缘画像。',
    path: 'couple-upload'
  }
]

const selectedType = ref('personal')

const handleConfirm = () => {
  const typeItem = analysisTypes.find(t => t.id === selectedType.value)
  if (typeItem) {
    router.push({ 
      name: typeItem.path, 
      query: { cardId, type: typeItem.id } 
    })
  }
}
</script>

<template>
  <main class="flex flex-col items-center justify-center min-h-[calc(100vh-120px)] px-6">
    <div class="w-full max-w-lg">
      <div class="text-center mb-10 animate-in fade-in slide-in-from-top-4 duration-1000">
        <h2 class="text-3xl font-bold text-white mb-2">选择分析类型</h2>
        <p class="text-gray-400">请选择您希望进行的 AI 匹配服务</p>
      </div>

      <div class="grid grid-cols-1 gap-4 mb-10">
        <div 
          v-for="item in analysisTypes" 
          :key="item.id"
          @click="selectedType = item.id"
          :class="[
            'p-6 rounded-3xl border-2 transition-all cursor-pointer relative overflow-hidden group',
            selectedType === item.id 
              ? 'bg-primary-purple/10 border-primary-purple shadow-[0_0_20px_rgba(99,102,241,0.2)]' 
              : 'bg-white/5 border-white/5 hover:border-white/20'
          ]"
        >
          <div class="flex items-center gap-4 relative z-10">
            <div 
              :class="[
                'w-16 h-16 rounded-2xl flex items-center justify-center text-4xl shadow-lg transition-transform duration-500',
                selectedType === item.id ? 'bg-gold-gradient scale-110 rotate-3' : 'bg-white/10 group-hover:scale-105'
              ]"
            >
              {{ item.icon }}
            </div>
            <div class="flex-1">
              <div class="flex items-center gap-2">
                <h3 class="font-bold text-xl">{{ item.name }}</h3>
              </div>
              <p class="text-sm text-gray-400 leading-relaxed mt-1">{{ item.desc }}</p>
            </div>
          </div>
          
          <!-- 背景装饰 -->
          <div 
            v-if="selectedType === item.id"
            class="absolute -right-4 -bottom-4 text-9xl opacity-10 pointer-events-none"
          >
            {{ item.icon }}
          </div>
        </div>
      </div>

      <button 
        @click="handleConfirm"
        class="w-full py-5 bg-gold-gradient rounded-2xl font-bold text-xl shadow-[0_10px_30px_rgba(245,158,11,0.3)] hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-3"
      >
        <span>确认选择</span>
      </button>
    </div>
  </main>
</template>
