<script setup lang="ts">
import { cn } from '@/utils/cn'

defineProps<{
  class?: string
  glow?: boolean
}>()
</script>

<template>
  <div :class="cn(
    'glass-card p-6 relative overflow-hidden',
    glow && 'glow-effect',
    $props.class
  )">
    <slot />
  </div>
</template>
