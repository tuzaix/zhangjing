<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import GlassCard from '@/components/GlassCard.vue'
import { compressImage } from '@/utils/image'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const cardId = route.query.cardId as string

const leftFileInput = ref<HTMLInputElement | null>(null)
const rightFileInput = ref<HTMLInputElement | null>(null)

const leftPreviewUrl = ref<string | null>(null)
const rightPreviewUrl = ref<string | null>(null)

const leftFile = ref<File | null>(null)
const rightFile = ref<File | null>(null)

const isUploading = ref(false)

const triggerUpload = (side: 'left' | 'right') => {
  if (side === 'left') {
    leftFileInput.value?.click()
  } else {
    rightFileInput.value?.click()
  }
}

const handleFileChange = async (e: Event, side: 'left' | 'right') => {
  const input = e.target as HTMLInputElement
  if (input.files && input.files[0]) {
    const file = input.files[0]
    if (file.size > 10 * 1024 * 1024) {
      alert('图片大小不能超过 10MB')
      return
    }
    
    try {
      const compressed = await compressImage(file)
      if (side === 'left') {
        leftFile.value = compressed
        leftPreviewUrl.value = URL.createObjectURL(compressed)
      } else {
        rightFile.value = compressed
        rightPreviewUrl.value = URL.createObjectURL(compressed)
      }
    } catch (err) {
      console.error('Image compression failed', err)
      if (side === 'left') {
        leftFile.value = file
        leftPreviewUrl.value = URL.createObjectURL(file)
      } else {
        rightFile.value = file
        rightPreviewUrl.value = URL.createObjectURL(file)
      }
    }
  }
}

const canSubmit = computed(() => leftFile.value && rightFile.value)

const startAnalysis = async () => {
  if (!leftFile.value || !rightFile.value) return
  isUploading.value = true
  
  const formData = new FormData()
  formData.append('left_hand', leftFile.value)
  formData.append('right_hand', rightFile.value)
  formData.append('card_id', cardId)

  try {
    await axios.post('/api/v1/analysis/upload-both', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    router.push({ name: 'mode-select', query: { cardId } })
  } catch (error: any) {
    alert(error.response?.data?.detail?.message || '图片上传失败，请重试')
  } finally {
    isUploading.value = false
  }
}
</script>

<template>
  <main class="flex flex-col items-center justify-start min-h-[calc(100vh-80px)] px-4 py-8">
    <div class="w-full max-w-lg">
      <h2 class="text-2xl font-bold text-center mb-6">上传双手照片</h2>
      
      <div class="mb-8">
        <GlassCard class="border-primary-gold/30 bg-primary-gold/5 py-4">
          <div class="flex items-center gap-3 text-primary-gold px-4">
            <span class="text-2xl animate-pulse">⚠️</span>
            <div>
              <h3 class="text-sm font-bold">必须上传双手照片方可分析</h3>
              <p class="text-[10px] opacity-80 uppercase tracking-widest">Two hands required for analysis</p>
            </div>
          </div>
        </GlassCard>
      </div>

      <div class="grid grid-cols-2 gap-4 mb-8">
        <!-- 左手上传 -->
        <div class="flex flex-col gap-2">
          <div class="flex items-center justify-center gap-1 mb-1">
            <span class="bg-primary-gold text-black text-[10px] font-bold px-1.5 py-0.5 rounded">1</span>
            <p class="text-center text-xs font-bold text-gray-400">左手 (先天)</p>
          </div>
          <div 
            @click="triggerUpload('left')"
            class="aspect-[3/4] bg-white/5 border-2 border-dashed border-white/10 rounded-2xl flex flex-col items-center justify-center cursor-pointer hover:border-primary-gold/50 transition-all overflow-hidden relative group"
            :class="{ 'border-primary-gold/30': leftFile }"
          >
            <input ref="leftFileInput" type="file" accept="image/*" class="hidden" @change="handleFileChange($event, 'left')" />
            
            <template v-if="!leftPreviewUrl">
              <span class="text-3xl mb-2 group-hover:scale-110 transition-transform">🤚</span>
              <span class="text-[10px] text-gray-500 font-bold uppercase">点击上传左手</span>
            </template>
            <template v-else>
              <img :src="leftPreviewUrl" class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <span class="text-white text-xs font-bold bg-black/60 px-3 py-1 rounded-full">重新上传</span>
              </div>
              <div class="absolute top-2 right-2 bg-primary-gold text-black rounded-full w-5 h-5 flex items-center justify-center text-[10px] font-bold shadow-lg">✓</div>
            </template>
          </div>
        </div>

        <!-- 右手上传 -->
        <div class="flex flex-col gap-2">
          <div class="flex items-center justify-center gap-1 mb-1">
            <span class="bg-primary-gold text-black text-[10px] font-bold px-1.5 py-0.5 rounded">2</span>
            <p class="text-center text-xs font-bold text-gray-400">右手 (后天)</p>
          </div>
          <div 
            @click="triggerUpload('right')"
            class="aspect-[3/4] bg-white/5 border-2 border-dashed border-white/10 rounded-2xl flex flex-col items-center justify-center cursor-pointer hover:border-primary-gold/50 transition-all overflow-hidden relative group"
            :class="{ 'border-primary-gold/30': rightFile }"
          >
            <input ref="rightFileInput" type="file" accept="image/*" class="hidden" @change="handleFileChange($event, 'right')" />
            
            <template v-if="!rightPreviewUrl">
              <span class="text-3xl mb-2 group-hover:scale-110 transition-transform">✋</span>
              <span class="text-[10px] text-gray-500 font-bold uppercase">点击上传右手</span>
            </template>
            <template v-else>
              <img :src="rightPreviewUrl" class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <span class="text-white text-xs font-bold bg-black/60 px-3 py-1 rounded-full">重新上传</span>
              </div>
              <div class="absolute top-2 right-2 bg-primary-gold text-black rounded-full w-5 h-5 flex items-center justify-center text-[10px] font-bold shadow-lg">✓</div>
            </template>
          </div>
        </div>
      </div>

      <GlassCard class="p-6">
        <div class="flex flex-col gap-4">
          <button 
            @click="startAnalysis"
            :disabled="!canSubmit || isUploading"
            :class="[
              'w-full py-4 rounded-xl font-bold text-lg shadow-lg transition-all active:scale-[0.98]',
              canSubmit ? 'bg-gold-gradient text-black' : 'bg-white/5 text-gray-600 grayscale cursor-not-allowed'
            ]"
          >
            <template v-if="isUploading">
              <span class="flex items-center justify-center gap-2">
                <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                同步分析中...
              </span>
            </template>
            <template v-else>
              {{ !leftFile ? '请先上传左手' : (!rightFile ? '还需上传右手' : '开始双手对比分析') }}
            </template>
          </button>
          
          <div class="flex items-start gap-2 px-2">
            <span class="text-primary-gold text-xs">💡</span>
            <p class="text-[10px] text-gray-500 leading-relaxed">
              提示：请在光线充足的环境下拍摄，确保手掌纹路清晰可见。系统将对比双手纹路，为您提供更精准的运势报告。
            </p>
          </div>
        </div>
      </GlassCard>
      
      <p class="mt-8 text-center text-xs text-gray-600">
        上传即表示你同意我们的 <a href="#" class="underline">隐私政策</a> 和 <a href="#" class="underline">服务条款</a>
      </p>
    </div>
  </main>
</template>
