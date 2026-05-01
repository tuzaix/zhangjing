<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="min-h-screen bg-bg-dark text-white font-sans selection:bg-primary-purple/30">
    <RouterView />
    
    <!-- 全局隐私标识 -->
    <footer class="py-6 px-6 text-center text-gray-500">
      <div class="flex flex-col items-center gap-3 max-w-xs mx-auto">
        <div class="flex items-center gap-2 px-3 py-1.5 bg-white/5 rounded-full border border-white/5">
          <span class="text-xs">🔒</span>
          <span class="text-[9px] font-medium tracking-wider uppercase opacity-80">Privacy First Service</span>
        </div>
        
        <p class="text-[9px] leading-relaxed opacity-60">
          图片将在分析完成后 24 小时内自动从服务器彻底删除。
        </p>
        
        <p class="text-[8px] font-mono tracking-tighter opacity-40 uppercase">
          &copy; 2026 ZHANGJING AI VISION.
        </p>
      </div>
    </footer>
  </div>
</template>

<style>
/* 全局样式已在 main.css 中定义 */
</style>
