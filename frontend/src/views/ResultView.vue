<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import GlassCard from '../components/GlassCard.vue'
import axios from 'axios'
import html2canvas from 'html2canvas'

const route = useRoute()
const router = useRouter()
const cardId = route.query.cardId as string
const activeModeId = (route.query.mode as string) || 'standard'
const result = ref<any>(null)
const activeReportTab = ref('career')
const isLoading = ref(true)
const copied = ref(false)

const modes = [
  { id: 'standard', name: '标准版', icon: '⚖️' },
  { id: 'toxic', name: '毒舌版', icon: '🔥' },
  { id: 'money', name: '搞钱专项', icon: '💰' },
  { id: 'love', name: '恋爱版', icon: '❤️' }
]

const currentMode = computed(() => modes.find(m => m.id === activeModeId) || modes[0])

// 分享海报相关
const posterRef = ref<HTMLElement | null>(null)
const shareImageUrl = ref<string | null>(null)
const isGeneratingPoster = ref(false)

// 转换 SVG 为 DataURL 供 html2canvas 使用
const getRadarDataUrl = () => {
  const svgElement = document.querySelector('.main-radar-svg')
  if (!svgElement) return null
  
  const serializer = new XMLSerializer()
  let source = serializer.serializeToString(svgElement)
  
  // 确保包含命名空间
  if (!source.match(/^<svg[^>]+xmlns="http\:\/\/www\.w3\.org\/2000\/svg"/)) {
    source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"')
  }
  
  // 修正 RGBA 颜色在部分环境下的兼容性
  source = source.replace(/rgba\(255, 255, 255, 0\.1\)/g, '#334155')
  source = source.replace(/rgba\(245, 158, 11, 0\.15\)/g, 'rgba(245, 158, 11, 0.15)')
  source = source.replace(/rgba\(245, 158, 11, 0\.8\)/g, '#f59e0b')
  
  return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(source)
}

const generatePoster = async () => {
  if (!posterRef.value) return
  
  isGeneratingPoster.value = true
  try {
    // 获取模板引用
    const template = posterRef.value
    
    // 等待图片和雷达图完全渲染
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const canvas = await html2canvas(template, {
      useCORS: true,
      scale: 3,
      backgroundColor: '#0f172a',
      logging: false,
      width: 375,
      // 使用 onclone 在克隆的 DOM 中处理显隐，避免影响当前页面的 live DOM
      onclone: (clonedDoc) => {
        const clonedTemplate = clonedDoc.querySelector('[ref="posterRef"]') || 
                               clonedDoc.querySelector('.poster-template-inner')
        if (clonedTemplate instanceof HTMLElement) {
          clonedTemplate.style.display = 'block'
          clonedTemplate.style.visibility = 'visible'
          clonedTemplate.style.position = 'relative'
          clonedTemplate.style.left = '0'
          clonedTemplate.style.top = '0'
        }
      }
    })
    
    const url = canvas.toDataURL('image/png', 1.0)
    shareImageUrl.value = url
  } catch (error) {
    console.error('Failed to generate poster', error)
    alert('海报生成失败，请重试')
  } finally {
    isGeneratingPoster.value = false
  }
}

// 雷达图配置
const radarLabels = ['生命线', '智慧线', '感情线', '婚姻线', '事业线']
const radarData = computed(() => {
  if (!result.value || !result.value.dimensions) return []
  
  return radarLabels.map(label => {
    const dim = result.value.dimensions.find((d: any) => d.name.includes(label))
    return dim ? dim.score : 60 // 默认值 60
  })
})

const radarPoints = computed(() => {
  const size = 200
  const center = size / 2
  const radius = center * 0.8
  const angleStep = (Math.PI * 2) / radarLabels.length
  
  return radarData.value.map((score, i) => {
    const angle = i * angleStep - Math.PI / 2
    const r = (score / 100) * radius
    return {
      x: center + r * Math.cos(angle),
      y: center + r * Math.sin(angle)
    }
  })
})

const radarPath = computed(() => {
  if (radarPoints.value.length === 0) return ''
  return radarPoints.value.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ') + ' Z'
})

const radarGridPaths = computed(() => {
  const size = 200
  const center = size / 2
  const radius = center * 0.8
  const angleStep = (Math.PI * 2) / radarLabels.length
  const levels = [0.2, 0.4, 0.6, 0.8, 1]
  
  return levels.map(level => {
    return radarLabels.map((_, i) => {
      const angle = i * angleStep - Math.PI / 2
      const r = level * radius
      return `${i === 0 ? 'M' : 'L'} ${center + r * Math.cos(angle)} ${center + r * Math.sin(angle)}`
    }).join(' ') + ' Z'
  })
})

const radarLabelPositions = computed(() => {
  const size = 200
  const center = size / 2
  const radius = center * 0.85
  const angleStep = (Math.PI * 2) / radarLabels.length
  
  return radarLabels.map((label, i) => {
    const angle = i * angleStep - Math.PI / 2
    return {
      text: label,
      x: center + radius * Math.cos(angle),
      y: center + radius * Math.sin(angle)
    }
  })
})

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(cardId)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy: ', err)
  }
}

const fetchResult = async () => {
  isLoading.value = true
  try {
    const response = await axios.get(`/api/v1/analysis/get/${cardId}?mode=${activeModeId}`)
    result.value = response.data.data
  } catch (error) {
    console.error('Failed to fetch result', error)
  } finally {
    isLoading.value = false
  }
}

const reportTabs = [
  { id: 'career', name: '职场', icon: '💼' },
  { id: 'wealth', name: '搞钱', icon: '💸' },
  { id: 'love', name: '恋爱', icon: '💕' }
]

onMounted(() => {
  fetchResult()
})
</script>

<template>
  <!-- 1. 加载中状态 -->
  <div v-if="isLoading" class="min-h-screen flex items-center justify-center">
    <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-gold"></div>
  </div>

  <!-- 2. 成功获取结果 -->
  <main v-else-if="result" class="min-h-screen pb-24 animate-in fade-in duration-700">
    <!-- 顶部卡密条 -->
    <div class="sticky top-0 z-20 w-full bg-bg-dark/60 backdrop-blur-md border-b border-white/5 py-4 px-6 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="text-xl">💡</span>
        <div class="hidden sm:block">
          <p class="text-xs text-gray-400">你的分析卡密</p>
          <p class="font-mono font-bold text-primary-gold">{{ cardId }}</p>
        </div>
        <div class="sm:hidden">
          <p class="font-mono font-bold text-primary-gold text-sm">{{ cardId.split('-')[0] }}-****-****-{{ cardId.split('-')[3] }}</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <button 
          @click="generatePoster"
          class="p-2 bg-white/5 border border-white/10 rounded-lg text-white active:scale-95 transition-all"
          title="分享"
        >
          <span>📤</span>
        </button>
        <button 
          @click="copyToClipboard"
          :class="[
            'px-4 py-1.5 rounded-lg text-sm font-bold transition-all duration-300',
            copied 
              ? 'bg-green-500/20 text-green-400 border border-green-500/30' 
              : 'bg-primary-gold/10 border border-primary-gold/20 text-primary-gold active:scale-95'
          ]"
        >
          {{ copied ? '已复制 ✓' : '复制卡密' }}
        </button>
      </div>
    </div>

    <!-- 头部标题区 -->
    <div class="text-center mt-8 mb-2 px-6 animate-in fade-in slide-in-from-top-4 duration-1000">
      <h1 class="text-3xl font-bold tracking-tight text-white mb-3">
        掌镜<span class="text-primary-gold">AI</span>手相解读
      </h1>
      <p class="text-[10px] text-gray-500 uppercase tracking-[0.4em] font-medium mt-2">
        Deep Vision Analysis Report
      </p>
      
      <!-- 当前版本标识 -->
      <div class="mt-6 inline-flex items-center gap-2 px-4 py-2 bg-primary-purple/10 border border-primary-purple/20 rounded-full shadow-lg">
        <span class="text-lg">{{ currentMode.icon }}</span>
        <span class="text-sm font-bold text-white">{{ currentMode.name }}</span>
        <span class="w-1 h-1 bg-white/30 rounded-full mx-1"></span>
        <span class="text-[10px] text-primary-purple/60 font-mono uppercase tracking-widest">Active Version</span>
      </div>
    </div>

    <!-- 模式切换 Tab (已移除实时切换，改为流程选择) -->
    <!-- <div class="px-4 mt-6">...</div> -->

    <!-- 核心综述 -->
    <div class="px-4 mt-8">
      <GlassCard class="bg-primary-purple/5 border-primary-purple/10" glow>
        <div class="flex items-center gap-4 mb-4">
          <div class="w-16 h-16 rounded-full bg-gold-gradient flex items-center justify-center text-2xl font-bold shadow-lg">
            {{ result.summary.overall_score }}
          </div>
          <div>
            <h3 class="text-xl font-bold">综合运势评分</h3>
            <p class="text-xs text-gray-400">基于 AI 手相深度分析</p>
          </div>
        </div>
        <p class="text-gray-300 leading-relaxed mb-6">{{ result.summary.personality }}</p>
        
        <!-- 核心建议 -->
        <div v-if="result?.suggestions?.length" class="border-t border-white/5 pt-4">
          <h4 class="text-sm font-bold text-primary-gold mb-3 flex items-center gap-2">
            <span>📋</span> 核心改进建议
          </h4>
          <ul class="space-y-2">
            <li v-for="(sug, idx) in result.suggestions" :key="idx" class="text-xs text-gray-400 flex gap-2">
              <span class="text-primary-gold font-bold">{{ Number(idx) + 1 }}.</span>
              <span>{{ sug }}</span>
            </li>
          </ul>
        </div>
      </GlassCard>
    </div>

    <!-- 雷达图展示 -->
    <div class="px-4 mt-8">
      <GlassCard class="bg-primary-gold/5 border-primary-gold/10 overflow-hidden">
        <h3 class="text-lg font-bold text-primary-gold mb-6 flex items-center gap-2">
          <span>📊</span> 命理维度雷达图
        </h3>
        <div class="flex justify-center items-center py-4">
          <svg width="280" height="280" viewBox="0 0 200 200" class="overflow-visible main-radar-svg">
            <!-- 网格线 -->
            <path 
              v-for="(path, i) in radarGridPaths" 
              :key="i" 
              :d="path" 
              fill="none" 
              stroke="rgba(255, 255, 255, 0.1)" 
              stroke-width="0.5"
            />
            <!-- 轴线 -->
            <line 
              v-for="(pos, i) in radarLabelPositions" 
              :key="'line-'+i"
              x1="100" y1="100" 
              :x2="pos.x" :y2="pos.y" 
              stroke="rgba(255, 255, 255, 0.1)" 
              stroke-width="0.5"
            />
            <!-- 数据区域 -->
            <path 
              :d="radarPath" 
              fill="rgba(245, 158, 11, 0.1)" 
              stroke="rgba(245, 158, 11, 0.8)" 
              stroke-width="2"
              class="animate-pulse-slow"
            />
            <!-- 数据点 -->
            <circle 
              v-for="(p, i) in radarPoints" 
              :key="'point-'+i"
              :cx="p.x" :cy="p.y" 
              r="3" 
              fill="#f59e0b"
            />
            <!-- 标签 -->
            <text 
              v-for="(pos, i) in radarLabelPositions" 
              :key="'label-'+i"
              :x="pos.x" :y="pos.y" 
              fill="rgba(255, 255, 255, 0.6)" 
              font-size="8" 
              text-anchor="middle"
              alignment-baseline="middle"
              :dy="pos.y < 100 ? -8 : 12"
              :dx="pos.x < 100 ? -5 : 5"
            >
              {{ pos.text }}
            </text>
          </svg>
        </div>
      </GlassCard>
    </div>

    <!-- 三大核心深度解读 (v3.5) -->
    <div v-if="result.specialized_reports" class="px-4 mt-8">
      <div class="flex gap-3 mb-4 overflow-x-auto pb-2 scrollbar-hide">
        <button 
          v-for="tab in reportTabs" 
          :key="tab.id"
          @click="activeReportTab = tab.id"
          :class="[
            'px-5 py-3 rounded-2xl font-bold text-sm flex items-center gap-2 transition-all duration-300 whitespace-nowrap border',
            activeReportTab === tab.id 
              ? 'bg-primary-purple/20 text-white border-primary-purple/50 shadow-[0_0_15px_rgba(99,102,241,0.3)]' 
              : 'bg-white/5 text-gray-400 border-white/5 hover:bg-white/10'
          ]"
        >
          <span :class="activeReportTab === tab.id ? 'scale-110' : ''" class="transition-transform duration-300">{{ tab.icon }}</span>
          <span>{{ tab.name }}进阶</span>
        </button>
      </div>

      <GlassCard class="bg-gradient-to-br from-primary-purple/10 to-transparent border-primary-purple/20">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-primary-gold flex items-center gap-2">
            <span>{{ reportTabs.find(t => t.id === activeReportTab)?.icon }}</span>
            {{ result?.specialized_reports?.[activeReportTab]?.title }}
          </h3>
          <span class="px-3 py-1 bg-primary-gold/10 text-primary-gold text-[10px] font-bold rounded-full border border-primary-gold/20">
            DEEP ANALYSIS
          </span>
        </div>
        
        <div class="space-y-4">
          <p class="text-gray-300 leading-relaxed text-sm md:text-base">
            {{ result?.specialized_reports?.[activeReportTab]?.content }}
          </p>
        </div>

        <!-- 装饰性元素 -->
        <div class="absolute -bottom-6 -right-6 text-8xl opacity-5 pointer-events-none grayscale">
          {{ reportTabs.find(t => t.id === activeReportTab)?.icon }}
        </div>
      </GlassCard>
    </div>

    <!-- 12 维度卡片 -->
    <div class="px-4 mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
      <GlassCard 
        v-for="dim in result.dimensions" 
        :key="dim.name"
        class="flex flex-col gap-3"
      >
        <div class="flex justify-between items-center">
          <h4 class="font-bold text-lg text-primary-gold">{{ dim.name }}</h4>
          <span class="text-xs font-mono text-gray-500">SCORE: {{ dim.score }}</span>
        </div>
        <div class="w-full h-1 bg-white/5 rounded-full overflow-hidden">
          <div class="h-full bg-primary-gold" :style="{ width: `${dim.score}%` }"></div>
        </div>
        <p class="text-sm text-gray-400 leading-relaxed">{{ dim.desc }}</p>
      </GlassCard>
    </div>

    <!-- 隐私中心入口 -->
    <div class="px-4 mt-12 text-center">
      <button 
        @click="router.push({ name: 'privacy-center', query: { cardId } })"
        class="text-gray-500 hover:text-white transition-colors flex items-center justify-center gap-2 mx-auto"
      >
        <span>🔒</span>
        <span>隐私中心：管理你的数据</span>
      </button>
    </div>

    <!-- 底部操作 -->
    <div class="fixed bottom-6 left-0 w-full px-6 z-30">
      <button 
        @click="generatePoster"
        :disabled="isGeneratingPoster"
        class="w-full py-4 bg-gold-gradient rounded-2xl font-bold text-lg shadow-[0_10px_30px_rgba(245,158,11,0.4)] flex items-center justify-center gap-3 active:scale-95 transition-all"
      >
        <template v-if="isGeneratingPoster">
          <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          生成中...
        </template>
        <template v-else>
          <span>📸</span>
          生成分析海报
        </template>
      </button>
    </div>
  </main>

  <!-- 3. 空状态 (无数据) -->
  <div v-else class="min-h-screen flex flex-col items-center justify-center px-6 text-center bg-[#0f172a]">
    <div class="relative mb-8">
      <div class="text-8xl animate-bounce-slow">🏜️</div>
      <div class="absolute inset-0 bg-primary-gold/20 blur-3xl rounded-full -z-10"></div>
    </div>
    <h2 class="text-2xl font-bold mb-3 text-white">暂无分析报告</h2>
    <p class="text-gray-400 mb-10 max-w-[280px] mx-auto leading-relaxed">
      由于图片清晰度不足或系统解析超时，未能生成您的深度报告。建议尝试在光线充足处重新拍摄。
    </p>
    <button 
      @click="router.push({ name: 'home' })"
      class="px-10 py-4 bg-gold-gradient text-black font-bold rounded-2xl shadow-[0_10px_30px_rgba(245,158,11,0.3)] active:scale-95 transition-all flex items-center gap-2"
    >
      <span>🏠</span>
      返回首页重试
    </button>
  </div>

  <!-- 分享海报生成模板 (隐藏，始终存在于 DOM 中供 html2canvas 使用) -->
  <div class="fixed left-[-9999px] top-0 invisible pointer-events-none">
    <div ref="posterRef" class="poster-template-inner w-[375px] bg-[#0f172a] text-white p-6 relative">
      <!-- 装饰背景 -->
      <div class="absolute inset-0 bg-gold-gradient opacity-5 pointer-events-none"></div>
      <!-- 头部 -->
      <div class="text-center mb-10 pt-6">
        <h2 class="text-3xl font-bold tracking-tight text-white mb-3">
          掌镜<span class="text-primary-gold">AI</span>手相解读
        </h2>
        <p class="text-[10px] text-gray-500 uppercase tracking-[0.4em] font-medium mt-2 mb-6">
          Deep Vision Analysis Report
        </p>
        
        <!-- 当前版本标识 (海报版) -->
        <div class="inline-flex items-center gap-2 px-4 py-2 bg-primary-purple/20 border border-primary-purple/30 rounded-full">
          <span class="text-xl -translate-y-3">{{ currentMode.icon }}</span>
          <span class="text-sm font-bold text-white -translate-y-2">{{ currentMode.name }}</span>
          <span class="w-1 h-1 bg-white/30 rounded-full mx-1 -translate-y-1"></span>
          <span class="text-[12px] text-primary-white/60 font-mono uppercase tracking-widest -translate-y-2">Active Version</span>
        </div>
      </div>

      <!-- 分数卡片 -->
      <div class="bg-white/5 border border-white/10 rounded-3xl p-6 mb-6 text-center">
        <div class="flex items-center justify-center w-24 h-24 rounded-full bg-gold-gradient text-5xl font-bold mb-4 shadow-xl mx-auto">
          <span class="-mt-8">{{ result?.summary?.overall_score }}</span>
        </div>
        <h3 class="text-lg font-bold mb-2">综合运势评分</h3>
        <p class="text-sm text-gray-400 leading-relaxed px-1">
          {{ result?.summary?.personality }}
        </p>
      </div>

      <!-- 核心建议 (移动到雷达图上方) -->
      <div v-if="result?.suggestions?.length" class="bg-white/5 border border-white/10 rounded-3xl p-6 mb-6">
        <h4 class="text-sm font-bold text-primary-gold mb-4 flex items-center gap-2">
          <span>📋</span> 核心改进建议
        </h4>
        <ul class="space-y-3">
          <li v-for="(sug, idx) in result.suggestions.slice(0, 3)" :key="idx" class="flex gap-2">
            <span class="text-primary-gold font-bold text-xs">{{ Number(idx) + 1 }}.</span>
            <span class="text-[12px] text-gray-300 leading-relaxed">{{ sug }}</span>
          </li>
        </ul>
      </div>

      <!-- 三大专项进阶解读 (新增) -->
      <div v-if="result?.specialized_reports" class="space-y-4 mb-6">
        <div v-for="tab in reportTabs" :key="tab.id" class="bg-white/5 border border-white/10 rounded-3xl p-6">
          <div class="flex items-center justify-between mb-3">
            <h4 class="text-sm font-bold text-primary-gold flex items-center gap-2">
              <span>{{ tab.icon }}</span>
              {{ result.specialized_reports[tab.id]?.title || tab.name + '进阶' }}
            </h4>
            <span class="text-[8px] text-primary-purple/60 font-mono uppercase tracking-widest">Deep Analysis</span>
          </div>
          <p class="text-[12px] text-gray-300 leading-relaxed">
            {{ result.specialized_reports[tab.id]?.content }}
          </p>
        </div>
      </div>

      <!-- 雷达图 (简化版) -->
      <div class="bg-white/5 border border-white/10 rounded-3xl p-6 mb-6">
        <h4 class="text-sm font-bold text-primary-gold mb-6 text-center uppercase tracking-widest">维度分布图</h4>
        <div class="flex justify-center py-2">
          <!-- 核心修复：使用 img 标签加载 SVG DataURL，确保 html2canvas 稳定识别 -->
          <img 
            v-if="getRadarDataUrl()" 
            :src="getRadarDataUrl()!" 
            width="300" 
            height="300" 
            class="max-w-full h-auto"
            style="font-size: 12px;"
          />
        </div>
      </div>

      <!-- 详细维度 -->
      <div class="space-y-4 mb-8">
        <div v-for="dim in result?.dimensions?.slice(0, 5)" :key="dim.name" class="bg-white/5 rounded-2xl p-4 border border-white/5">
          <div class="flex justify-between items-center mb-2">
            <span class="font-bold text-primary-gold text-sm">{{ dim.name }}</span>
            <span class="text-[12px] font-mono text-gray-500">{{ dim.score }}</span>
          </div>
          <p class="text-[12px] text-gray-400 leading-relaxed">{{ dim.desc }}</p>
        </div>
      </div>

      <!-- 底部脚注 -->
      <div class="border-t border-white/10 pt-8 pb-4 text-center">
        <div class="flex flex-col items-center gap-2">
          <div class="mt-2 opacity-50 text-[8px] text-gray-600 tracking-widest uppercase">
            Powered by AI Vision Engine v4.0<br/>
            © 2026 AI Hand Analysis Service
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 分享弹窗 (独立于主逻辑，通过 shareImageUrl 控制) -->
  <div v-if="shareImageUrl" class="fixed inset-0 z-[100] overflow-y-auto px-6 py-10 bg-black/90 backdrop-blur-md">
    <!-- 点击背景关闭 -->
    <div class="fixed inset-0" @click="shareImageUrl = null"></div>
    
    <!-- 内容容器：改为 items-start 以支持长图滚动 -->
    <div class="relative z-10 w-full max-w-sm mx-auto flex flex-col items-center gap-6 animate-in zoom-in duration-300 min-h-full">
      <div class="relative w-full shadow-2xl">
        <img 
          :src="shareImageUrl" 
          class="w-full h-auto rounded-2xl border border-white/20 select-auto"
          style="-webkit-touch-callout: default; user-select: auto;"
        />
      </div>
      
      <!-- 提示文案 -->
      <div class="flex flex-col items-center gap-2 text-white text-center pointer-events-none pb-4">
        <div class="flex items-center gap-2 px-4 py-2 bg-white/10 rounded-full backdrop-blur-md border border-white/10">
          <span class="animate-bounce text-lg">☝️</span>
          <span class="text-sm font-bold">长按图片保存到本地</span>
        </div>
        <p class="text-[10px] text-gray-400">保存后可分享至朋友圈或好友</p>
      </div>

      <!-- 关闭按钮 -->
      <button 
        @click="shareImageUrl = null"
        class="w-12 h-12 shrink-0 rounded-full bg-white/20 flex items-center justify-center text-white text-xl hover:bg-white/30 transition-all active:scale-90 mb-10"
      >
        ✕
      </button>
    </div>
  </div>
</template>

<style scoped>
@keyframes pulse-slow {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.6; }
}
@keyframes bounce-slow {
  0%, 100% { transform: translateY(-5%); }
  50% { transform: translateY(0); }
}
.animate-pulse-slow {
  animation: pulse-slow 4s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
.animate-bounce-slow {
  animation: bounce-slow 3s ease-in-out infinite;
}

/* 隐藏滚动条 */
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
