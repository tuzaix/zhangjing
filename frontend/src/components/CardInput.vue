<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'

const props = defineProps<{
  modelValue: string
}>()

const emit = defineEmits(['update:modelValue', 'complete'])

const displayValue = ref('')
const inputRef = ref<HTMLInputElement | null>(null)

// 格式化输入逻辑
const onInput = (e: Event) => {
  const input = e.target as HTMLInputElement
  // 只保留字母和数字，并转为大写
  let value = input.value.toUpperCase().replace(/[^A-Z0-9]/g, '')
  
  // 限制长度为 16 位
  if (value.length > 16) {
    value = value.slice(0, 16)
  }

  // 格式化为 XXXX-XXXX-XXXX-XXXX
  const parts = value.match(/.{1,4}/g)
  const formatted = parts ? parts.join('-') : value
  
  displayValue.value = formatted
  emit('update:modelValue', formatted)

  if (value.length === 16) {
    emit('complete', formatted)
  }
}

// 监听外部传参变化
watch(() => props.modelValue, (newVal) => {
  if (newVal !== displayValue.value) {
    displayValue.value = newVal
  }
}, { immediate: true })

onMounted(() => {
  inputRef.value?.focus()
})
</script>

<template>
  <div class="w-full">
    <input
      ref="inputRef"
      type="text"
      v-model="displayValue"
      @input="onInput"
      placeholder="XXXX-XXXX-XXXX-XXXX"
      class="w-full bg-white/5 border-2 border-white/10 rounded-2xl px-6 py-4 text-center font-mono text-xl sm:text-2xl font-bold tracking-[0.2em] text-primary-gold placeholder:text-gray-700 focus:border-primary-gold focus:bg-primary-gold/5 outline-none transition-all shadow-inner"
    />
    <div class="mt-2 flex justify-between px-2">
      <div class="flex gap-1">
        <div v-for="i in 4" :key="i" class="h-1 w-8 rounded-full" :class="displayValue.replace(/-/g, '').length >= i * 4 ? 'bg-primary-gold' : 'bg-white/10'"></div>
      </div>
      <span class="text-[10px] text-gray-600 font-mono uppercase tracking-widest">
        {{ displayValue.replace(/-/g, '').length }} / 16 DIGITS
      </span>
    </div>
  </div>
</template>

<style scoped>
input::placeholder {
  letter-spacing: normal;
  font-size: 0.8em;
  opacity: 0.3;
}
</style>
