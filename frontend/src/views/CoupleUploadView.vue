<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import GlassCard from '@/components/GlassCard.vue'
import { compressImage } from '@/utils/image'
import axios from 'axios'

/**
 * 情侣匹配上传照片页面组件
 * 负责收集男生和女生的手相照片并上传到后端进行分析
 */

const route = useRoute()
const router = useRouter()
const cardId = route.query.cardId as string

// 文件输入引用
const maleFileInput = ref<HTMLInputElement | null>(null)
const femaleFileInput = ref<HTMLInputElement | null>(null)

// 预览图 URL
const malePreviewUrl = ref<string | null>(null)
const femalePreviewUrl = ref<string | null>(null)

// 选中的文件对象
const maleFile = ref<File | null>(null)
const femaleFile = ref<File | null>(null)

const isUploading = ref(false)
const uploadProgress = ref(0)

/**
 * 触发文件选择框
 * @param side 'male' | 'female'
 */
const triggerUpload = (side: 'male' | 'female') => {
  if (side === 'male') {
    maleFileInput.value?.click()
  } else {
    femaleFileInput.value?.click()
  }
}

/**
 * 处理文件选择变更
 * @param e 事件对象
 * @param side 'male' | 'female'
 */
const handleFileChange = async (e: Event, side: 'male' | 'female') => {
  const input = e.target as HTMLInputElement
  if (input.files && input.files[0]) {
    const file = input.files[0]
    if (file.size > 10 * 1024 * 1024) {
      alert('图片大小不能超过 10MB')
      return
    }
    
    try {
      const compressed = await compressImage(file)
      if (side === 'male') {
        maleFile.value = compressed
        malePreviewUrl.value = URL.createObjectURL(compressed)
      } else {
        femaleFile.value = compressed
        femalePreviewUrl.value = URL.createObjectURL(compressed)
      }
    } catch (err) {
      console.error('Image compression failed', err)
      const fileUrl = URL.createObjectURL(file)
      if (side === 'male') {
        maleFile.value = file
        malePreviewUrl.value = fileUrl
      } else {
        femaleFile.value = file
        femalePreviewUrl.value = fileUrl
      }
    }
  }
}

// 检查是否可以提交（两张图都已选择）
const canSubmit = computed(() => maleFile.value && femaleFile.value)

/**
 * 开始分析，上传照片并跳转到模式选择
 */
const startAnalysis = async () => {
  if (!maleFile.value || !femaleFile.value) return
  isUploading.value = true
  
  const formData = new FormData()
  formData.append('male_hand', maleFile.value!)
  formData.append('female_hand', femaleFile.value!)
  formData.append('card_id', cardId)
  formData.append('type', 'couple')

  try {
    await axios.post('/api/v1/analysis/upload-couple', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent) => {
        uploadProgress.value = Math.round((progressEvent.loaded * 100) / (progressEvent.total || 1))
      }
    })
    router.push({ name: 'mode-select', query: { cardId, type: 'couple' } })
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
      <h2 class="text-2xl font-bold text-center mb-6 text-white">情侣双人匹配</h2>
      
      <div class="mb-8">
        <GlassCard class="border-primary-gold/30 bg-primary-gold/5 py-4">
          <div class="flex items-center gap-3 text-primary-gold px-4">
            <span class="text-2xl animate-pulse">👩‍❤️‍👨</span>
            <div>
              <h3 class="text-sm font-bold">请分别上传男生与女生的手相照片</h3>
              <p class="text-[10px] opacity-80 uppercase tracking-widest">Upload male and female palm photos</p>
            </div>
          </div>
        </GlassCard>
      </div>

      <div class="grid grid-cols-2 gap-4 mb-8">
        <!-- 男生上传 -->
        <div class="flex flex-col gap-2">
          <div class="flex items-center justify-center gap-1 mb-1">
            <span class="bg-blue-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded">1</span>
            <p class="text-center text-xs font-bold text-gray-400">男生左手照片</p>
          </div>
          <div 
            @click="triggerUpload('male')"
            class="aspect-[3/4] bg-white/5 border-2 border-dashed border-white/10 rounded-2xl flex flex-col items-center justify-center cursor-pointer hover:border-blue-400/50 transition-all overflow-hidden relative group"
            :class="{ 'border-blue-400/30': maleFile }"
          >
            <input ref="maleFileInput" type="file" accept="image/*" class="hidden" @change="handleFileChange($event, 'male')" />
            
            <template v-if="!malePreviewUrl">
              <span class="text-3xl mb-2 group-hover:scale-110 transition-transform">👦</span>
              <span class="text-[10px] text-gray-500 font-bold uppercase">男生左手照</span>
            </template>
            <template v-else>
              <img :src="malePreviewUrl" class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <span class="text-white text-xs font-bold bg-black/60 px-3 py-1 rounded-full">重新上传</span>
              </div>
              <div class="absolute top-2 right-2 bg-blue-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-[10px] font-bold shadow-lg">✓</div>
            </template>
          </div>
        </div>

        <!-- 女生上传 -->
        <div class="flex flex-col gap-2">
          <div class="flex items-center justify-center gap-1 mb-1">
            <span class="bg-pink-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded">2</span>
            <p class="text-center text-xs font-bold text-gray-400">女生左手照片</p>
          </div>
          <div 
            @click="triggerUpload('female')"
            class="aspect-[3/4] bg-white/5 border-2 border-dashed border-white/10 rounded-2xl flex flex-col items-center justify-center cursor-pointer hover:border-pink-400/50 transition-all overflow-hidden relative group"
            :class="{ 'border-pink-400/30': femaleFile }"
          >
            <input ref="femaleFileInput" type="file" accept="image/*" class="hidden" @change="handleFileChange($event, 'female')" />
            
            <template v-if="!femalePreviewUrl">
              <span class="text-3xl mb-2 group-hover:scale-110 transition-transform">👧</span>
              <span class="text-[10px] text-gray-500 font-bold uppercase">女生左手照</span>
            </template>
            <template v-else>
              <img :src="femalePreviewUrl" class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <span class="text-white text-xs font-bold bg-black/60 px-3 py-1 rounded-full">重新上传</span>
              </div>
              <div class="absolute top-2 right-2 bg-pink-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-[10px] font-bold shadow-lg">✓</div>
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
                正在匹配分析 {{ uploadProgress }}%
              </span>
            </template>
            <template v-else>
              {{ !maleFile ? '请先上传男生左手照' : (!femaleFile ? '还需上传女生左手照' : '开启情侣匹配分析') }}
            </template>
          </button>
          
          <div class="flex items-start gap-2 px-2">
            <span class="text-primary-gold text-xs">💡</span>
            <p class="text-[10px] text-gray-500 leading-relaxed">
              提示：请在光线充足的环境下拍摄，确保双方手掌纹路清晰可见。系统将深度分析两人的情感基调与命格契合度，为您揭秘正缘密码。
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
