<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import GlassCard from '@/components/GlassCard.vue'

const route = useRoute()
const router = useRouter()
const cardId = route.query.cardId as string

const activeMode = ref('standard')

const modes = [
  { id: 'standard', name: '标准版', icon: '⚖️', desc: '专业真诚，温暖治愈。60%正面+40%客观提醒。' },
  { id: 'toxic', name: '毒舌版', icon: '🔥', desc: '犀利吐槽，直击痛点。开启毒舌模式，用犀利但真诚的语气说话。' },
  { id: 'money', name: '搞钱版', icon: '💰', desc: '专注搞钱，暴富指南。重点分析财运相关的所有纹路。' },
  { id: 'love', name: '恋爱版', icon: '❤️', desc: '恋爱版，正缘画像。重点分析感情线、婚姻线、桃花纹。' }
]

const confirmMode = () => {
  router.push({ 
    name: 'loading', 
    query: { 
      cardId,
      mode: activeMode.value 
    } 
  })
}
</script>

<template>
  <main class="flex flex-col items-center justify-center min-h-[calc(100vh-80px)] px-6">
    <div class="w-full max-w-lg">
      <div class="text-center mb-10 animate-in fade-in slide-in-from-top-4 duration-1000">
        <h2 class="text-3xl font-bold text-white mb-2">选择解读模式</h2>
        <p class="text-gray-400">请选择您希望 AI 呈现的分析风格</p>
      </div>

      <div class="grid grid-cols-1 gap-4 mb-10">
        <div 
          v-for="mode in modes" 
          :key="mode.id"
          @click="activeMode = mode.id"
          :class="[
            'p-5 rounded-3xl border-2 transition-all cursor-pointer relative overflow-hidden group',
            activeMode === mode.id 
              ? 'bg-primary-purple/10 border-primary-purple shadow-[0_0_20px_rgba(99,102,241,0.2)]' 
              : 'bg-white/5 border-white/5 hover:border-white/20'
          ]"
        >
          <div class="flex items-center gap-4 relative z-10">
            <div 
              :class="[
                'w-14 h-14 rounded-2xl flex items-center justify-center text-3xl shadow-lg transition-transform duration-500',
                activeMode === mode.id ? 'bg-gold-gradient scale-110 rotate-3' : 'bg-white/10 group-hover:scale-105'
              ]"
            >
              {{ mode.icon }}
            </div>
            <div class="flex-1">
              <h3 class="font-bold text-lg mb-1">{{ mode.name }}</h3>
              <p class="text-xs text-gray-400 leading-relaxed">{{ mode.desc }}</p>
            </div>
            <div v-if="activeMode === mode.id" class="text-primary-purple">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
            </div>
          </div>
          
          <!-- 背景装饰 -->
          <div 
            v-if="activeMode === mode.id"
            class="absolute -right-4 -bottom-4 text-8xl opacity-10 pointer-events-none"
          >
            {{ mode.icon }}
          </div>
        </div>
      </div>

      <button 
        @click="confirmMode"
        class="w-full py-5 bg-gold-gradient rounded-2xl font-bold text-xl shadow-[0_10px_30px_rgba(245,158,11,0.3)] hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-3"
      >
        <span>✨</span>
        开启智能分析
      </button>
      
      <p class="mt-6 text-center text-xs text-gray-600">
        选定模式后，AI 将为您生成专属分析报告
      </p>
    </div>
  </main>
</template>
