<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const startAnalysis = () => {
  router.push('/card-input')
}
</script>

<template>
  <main class="flex flex-col items-center justify-center min-h-[calc(100vh-120px)] px-6">
    <!-- 顶部 Logo 区域 -->
    <div class="mb-8 animate-in fade-in zoom-in duration-1000">
      <div class="relative w-28 h-28 mx-auto">
        <div class="absolute inset-0 bg-primary-purple/20 blur-3xl rounded-full"></div>
        <div class="relative flex items-center justify-center w-28 h-28 bg-white/5 border border-white/10 rounded-[2rem] shadow-2xl backdrop-blur-sm group hover:scale-110 transition-transform duration-500">
          <span class="text-6xl group-hover:rotate-12 transition-transform duration-500">☯️</span>
        </div>
      </div>
    </div>

    <div class="text-center mb-10 animate-in fade-in slide-in-from-bottom-4 duration-1000 delay-200">
      <h1 class="text-3xl md:text-5xl font-bold mb-3 tracking-tight">
        <span class="text-white">掌镜</span><span class="text-primary-gold"> AI</span>
      </h1>
      <p class="text-lg md:text-xl text-gray-400 font-light tracking-[0.2em]">
        解密您的手相密码
      </p>
    </div>

    <div class="glass-card p-6 w-full max-w-sm text-center relative overflow-hidden group animate-in fade-in slide-in-from-bottom-8 duration-1000 delay-500">
      <div class="absolute inset-0 bg-primary-purple/5 group-hover:bg-primary-purple/10 transition-colors duration-500"></div>
      
      <div class="relative z-10">
        <div class="text-6xl mb-8 group-hover:scale-110 transition-transform duration-500">🔮</div>
        <button 
          @click="startAnalysis"
          class="w-full py-5 px-8 bg-gold-gradient rounded-2xl font-bold text-xl shadow-[0_10px_30px_rgba(245,158,11,0.3)] hover:scale-105 hover:shadow-[0_15px_40px_rgba(245,158,11,0.4)] active:scale-95 transition-all"
        >
          开始分析
        </button>
        <div class="mt-6 flex items-center justify-center gap-4 opacity-50 grayscale hover:grayscale-0 transition-all duration-500">
          <div class="flex flex-col items-center">
            <span class="text-xl">🔒</span>
            <span class="text-[10px] mt-1 font-mono uppercase tracking-widest">Secure</span>
          </div>
          <div class="w-px h-6 bg-white/10"></div>
          <div class="flex flex-col items-center">
            <span class="text-xl">🧠</span>
            <span class="text-[10px] mt-1 font-mono uppercase tracking-widest">AI Engine</span>
          </div>
          <div class="w-px h-6 bg-white/10"></div>
          <div class="flex flex-col items-center">
            <span class="text-xl">⚡</span>
            <span class="text-[10px] mt-1 font-mono uppercase tracking-widest">Fast</span>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
