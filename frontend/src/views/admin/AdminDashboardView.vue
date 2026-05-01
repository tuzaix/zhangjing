<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const stats = ref<any>(null)
const cards = ref<any[]>([])
const totalCards = ref(0)
const interactions = ref<any[]>([])
const isLoading = ref(true)
const activeTab = ref('stats') // 'stats', 'cards', 'interactions'
const token = sessionStorage.getItem('admin_token')

// 卡密分页和筛选
const cardStatusFilter = ref('')
const cardPage = ref(1)
const cardLimit = ref(20)
const cardSortBy = ref('created_at')
const cardSortOrder = ref('desc')

const cardLimitOptions = [20, 50, 100, 200]

const generateCount = ref(10)
const isGenerating = ref(false)

if (!token) {
  router.push({ name: 'admin-login' })
}

const fetchCards = async () => {
  try {
    const skip = (cardPage.value - 1) * cardLimit.value
    let url = `/api/v1/admin/cards?token=${token}&skip=${skip}&limit=${cardLimit.value}&sort_by=${cardSortBy.value}&sort_order=${cardSortOrder.value}`
    if (cardStatusFilter.value) {
      url += `&status=${cardStatusFilter.value}`
    }
    const res = await axios.get(url)
    cards.value = res.data.items
    totalCards.value = res.data.total
  } catch (err) {
    console.error('Fetch cards failed', err)
  }
}

const toggleSort = (field: string) => {
  if (cardSortBy.value === field) {
    cardSortOrder.value = cardSortOrder.value === 'desc' ? 'asc' : 'desc'
  } else {
    cardSortBy.value = field
    cardSortOrder.value = 'desc'
  }
  cardPage.value = 1
  fetchCards()
}

const handleLimitChange = () => {
  cardPage.value = 1
  fetchCards()
}

const fetchAllData = async () => {
  isLoading.value = true
  try {
    const [statsRes, interactionsRes] = await Promise.all([
      axios.get(`/api/v1/admin/stats?token=${token}`),
      axios.get(`/api/v1/admin/interactions?token=${token}&limit=20`)
    ])
    stats.value = statsRes.data
    interactions.value = interactionsRes.data
    await fetchCards()
  } catch (err) {
    console.error('Fetch admin data failed', err)
    sessionStorage.removeItem('admin_token')
    router.push({ name: 'admin-login' })
  } finally {
    isLoading.value = false
  }
}

const handleExportCards = () => {
  let url = `/api/v1/admin/cards/export?token=${token}`
  if (cardStatusFilter.value) {
    url += `&status=${cardStatusFilter.value}`
  }
  window.open(url, '_blank')
}

const handleStatusChange = () => {
  cardPage.value = 1
  fetchCards()
}

const handlePrevPage = () => {
  if (cardPage.value > 1) {
    cardPage.value--
    fetchCards()
  }
}

const handleNextPage = () => {
  if (cardPage.value < Math.ceil(totalCards.value / cardLimit.value)) {
    cardPage.value++
    fetchCards()
  }
}

const handleGenerateCards = async () => {
  if (generateCount.value <= 0) return
  isGenerating.value = true
  try {
    await axios.post(`/api/v1/admin/cards/generate?token=${token}`, {
      count: generateCount.value
    })
    alert(`成功生成 ${generateCount.value} 张新卡密`)
    // 重置页码并刷新列表和统计数据
    cardPage.value = 1
    await fetchAllData()
  } catch (err) {
    console.error('Generate cards failed', err)
    alert('生成失败，请重试')
  } finally {
    isGenerating.value = false
  }
}

const logout = () => {
  sessionStorage.removeItem('admin_token')
  router.push({ name: 'admin-login' })
}

onMounted(() => {
  if (token) fetchAllData()
})

const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  const hh = String(date.getHours()).padStart(2, '0')
  const mm = String(date.getMinutes()).padStart(2, '0')
  return `${y}-${m}-${d} ${hh}:${mm}`
}

const copyToClipboard = async (text: string) => {
  try {
    await navigator.clipboard.writeText(text)
    alert('卡密已复制到剪贴板')
  } catch (err) {
    console.error('Failed to copy!', err)
  }
}
</script>

<template>
  <div class="min-h-screen bg-bg-dark flex">
    <!-- 侧边栏 -->
    <aside class="w-64 border-r border-white/5 flex flex-col p-6 shrink-0">
      <div class="mb-12">
        <h2 class="text-xl font-bold text-white tracking-tight">掌镜AI · 管理后台</h2>
        <p class="text-[10px] text-gray-500 uppercase tracking-widest font-mono mt-1">Admin Panel v4.0</p>
      </div>
      
      <nav class="flex-1 space-y-2">
        <button 
          @click="activeTab = 'stats'"
          :class="[
            'w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all',
            activeTab === 'stats' ? 'bg-primary-purple text-white shadow-lg' : 'text-gray-400 hover:bg-white/5 hover:text-white'
          ]"
        >
          <span>📊</span>
          <span class="text-sm font-bold">概览看板</span>
        </button>
        
        <button 
          @click="activeTab = 'cards'"
          :class="[
            'w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all',
            activeTab === 'cards' ? 'bg-primary-purple text-white shadow-lg' : 'text-gray-400 hover:bg-white/5 hover:text-white'
          ]"
        >
          <span>🔐</span>
          <span class="text-sm font-bold">卡密管理</span>
        </button>
        
        <button 
          @click="activeTab = 'interactions'"
          :class="[
            'w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all',
            activeTab === 'interactions' ? 'bg-primary-purple text-white shadow-lg' : 'text-gray-400 hover:bg-white/5 hover:text-white'
          ]"
        >
          <span>🔥</span>
          <span class="text-sm font-bold">互动数据</span>
        </button>
      </nav>
      
      <button 
        @click="logout"
        class="flex items-center gap-3 px-4 py-3 text-gray-500 hover:text-status-danger transition-colors mt-auto border-t border-white/5 pt-6"
      >
        <span>🚪</span>
        <span class="text-sm font-bold">退出登录</span>
      </button>
    </aside>

    <!-- 主内容区 -->
    <main class="flex-1 overflow-y-auto p-10">
      <div v-if="isLoading" class="h-full flex items-center justify-center">
        <div class="animate-spin text-4xl text-primary-purple">⏳</div>
      </div>
      
      <div v-else class="max-w-6xl mx-auto">
        <!-- 头部信息 -->
        <header class="flex justify-between items-end mb-10">
          <div>
            <h1 class="text-3xl font-bold text-white">
              {{ activeTab === 'stats' ? '概览看板' : (activeTab === 'cards' ? '卡密管理' : '互动数据') }}
            </h1>
            <p class="text-gray-500 mt-1">最后更新: {{ formatDate(new Date().toISOString()) }}</p>
          </div>
          <button @click="fetchAllData" class="p-2 bg-white/5 border border-white/10 rounded-lg text-xs hover:bg-white/10 transition-all">刷新数据</button>
        </header>

        <!-- 1. 概览看板 -->
        <section v-if="activeTab === 'stats'" class="animate-in fade-in slide-in-from-bottom-4 duration-700">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
            <div class="bg-white/5 border border-white/5 p-6 rounded-3xl">
              <p class="text-xs text-gray-500 font-bold uppercase tracking-widest mb-1">总发卡量</p>
              <h2 class="text-4xl font-bold text-primary-gold">{{ stats.cards.total }}</h2>
            </div>
            <div class="bg-white/5 border border-white/5 p-6 rounded-3xl">
              <p class="text-xs text-gray-500 font-bold uppercase tracking-widest mb-1">已激活</p>
              <h2 class="text-4xl font-bold text-white">{{ stats.cards.activated }}</h2>
            </div>
            <div class="bg-white/5 border border-white/5 p-6 rounded-3xl">
              <p class="text-xs text-gray-500 font-bold uppercase tracking-widest mb-1">待激活</p>
              <h2 class="text-4xl font-bold text-gray-400">{{ stats.cards.not_activated }}</h2>
            </div>
            <div class="bg-white/5 border border-white/5 p-6 rounded-3xl">
              <p class="text-xs text-gray-500 font-bold uppercase tracking-widest mb-1">总分析次数</p>
              <h2 class="text-4xl font-bold text-primary-purple">{{ stats.analyses.total_interpretations }}</h2>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="bg-white/5 border border-white/5 p-8 rounded-3xl">
              <h3 class="text-lg font-bold mb-6 flex items-center gap-2">
                <span>📈</span> 解读模式分布
              </h3>
              <div class="space-y-4">
                <div v-for="(count, mode) in stats.analyses.mode_stats" :key="mode" class="space-y-1">
                  <div class="flex justify-between text-xs font-bold uppercase">
                    <span class="text-gray-400">{{ mode }}</span>
                    <span class="text-white">{{ count }}</span>
                  </div>
                  <div class="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
                    <div class="h-full bg-primary-purple" :style="{ width: `${(count / stats.analyses.total_interpretations) * 100}%` }"></div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="bg-white/5 border border-white/5 p-8 rounded-3xl flex flex-col items-center justify-center text-center">
              <span class="text-6xl mb-4">🚀</span>
              <h3 class="text-xl font-bold text-white mb-2">系统状态正常</h3>
              <p class="text-gray-500 text-sm max-w-xs">AI 引擎连接稳定，Redis 缓存预热中，所有数据均已安全加密存储。</p>
            </div>
          </div>
        </section>

        <!-- 2. 卡密管理 -->
        <section v-if="activeTab === 'cards'" class="animate-in fade-in slide-in-from-bottom-4 duration-700">
          <div class="flex flex-col md:flex-row gap-6 mb-8">
            <div class="flex-1 bg-white/5 border border-white/5 p-8 rounded-3xl">
              <h3 class="text-lg font-bold mb-6">批量生成卡密</h3>
              <div class="flex items-center gap-4">
                <div class="flex-1 max-w-xs">
                  <input 
                    v-model="generateCount"
                    type="number" 
                    class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white outline-none focus:border-primary-purple"
                    placeholder="生成数量"
                  />
                </div>
                <button 
                  @click="handleGenerateCards"
                  :disabled="isGenerating"
                  class="px-8 py-3 bg-gold-gradient rounded-xl font-bold text-black active:scale-95 transition-all disabled:opacity-50"
                >
                  {{ isGenerating ? '生成中...' : '开始生成' }}
                </button>
              </div>
            </div>

            <div class="bg-white/5 border border-white/5 p-8 rounded-3xl flex flex-col justify-center">
              <h3 class="text-lg font-bold mb-4">导出数据</h3>
              <button 
                @click="handleExportCards"
                class="w-full flex items-center justify-center gap-2 px-8 py-4 bg-white/5 border border-white/10 rounded-xl font-bold text-white hover:bg-white/10 active:scale-95 transition-all"
              >
                <span>📥</span>
                导出 CSV 文件
              </button>
            </div>
          </div>

          <div class="mb-6 flex flex-col md:flex-row justify-between items-center gap-4">
            <div class="flex items-center gap-4 bg-white/5 p-2 rounded-2xl border border-white/5 w-full md:w-auto">
              <button 
                v-for="status in [
                  { id: '', name: '全部', count: stats?.cards?.total },
                  { id: 'not_activated', name: '待激活', count: stats?.cards?.not_activated },
                  { id: 'activated', name: '已激活', count: stats?.cards?.activated },
                  { id: 'expired', name: '已过期', count: stats?.cards?.expired }
                ]" 
                :key="status.id"
                @click="cardStatusFilter = status.id; handleStatusChange()"
                :class="[
                  'px-6 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2',
                  cardStatusFilter === status.id ? 'bg-primary-purple text-white shadow-lg' : 'text-gray-500 hover:text-white'
                ]"
              >
                <span>{{ status.name }}</span>
                <span :class="[
                  'text-[10px] px-1.5 py-0.5 rounded-md',
                  cardStatusFilter === status.id ? 'bg-white/20 text-white' : 'bg-white/5 text-gray-500'
                ]">
                  {{ status.count || 0 }}
                </span>
              </button>
            </div>
            
            <div class="flex items-center gap-4">
              <div class="flex items-center gap-2 bg-white/5 border border-white/10 rounded-xl px-3 py-1.5">
                <span class="text-[10px] text-gray-500 font-bold uppercase tracking-wider">每页展示</span>
                <select 
                  v-model="cardLimit" 
                  @change="handleLimitChange"
                  class="bg-transparent text-xs font-bold text-primary-gold outline-none cursor-pointer"
                >
                  <option v-for="opt in cardLimitOptions" :key="opt" :value="opt" class="bg-bg-dark text-white">
                    {{ opt }}
                  </option>
                </select>
              </div>

              <span class="text-xs text-gray-500 font-mono uppercase tracking-widest">
                Total: {{ totalCards }}
              </span>
              <div class="flex items-center gap-2">
                <button 
                  @click="handlePrevPage"
                  :disabled="cardPage === 1"
                  class="p-2 bg-white/5 border border-white/10 rounded-lg text-white disabled:opacity-20 active:scale-90 transition-all"
                >
                  ◀
                </button>
                <span class="text-sm font-bold w-12 text-center text-primary-gold">{{ cardPage }}</span>
                <button 
                  @click="handleNextPage"
                  :disabled="cardPage >= Math.ceil(totalCards / cardLimit)"
                  class="p-2 bg-white/5 border border-white/10 rounded-lg text-white disabled:opacity-20 active:scale-90 transition-all"
                >
                  ▶
                </button>
              </div>
            </div>
          </div>

          <div class="bg-white/5 border border-white/5 rounded-3xl overflow-hidden">
            <table class="w-full text-left">
              <thead>
                <tr class="border-b border-white/5 bg-white/5">
                  <th class="px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-widest">卡密 ID</th>
                  <th class="px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-widest">状态</th>
                  <th 
                    @click="toggleSort('created_at')"
                    class="px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-widest cursor-pointer hover:text-white transition-colors group"
                  >
                    <div class="flex items-center gap-1">
                      创建时间
                      <span :class="['transition-opacity', cardSortBy === 'created_at' ? 'opacity-100' : 'opacity-20 group-hover:opacity-50']">
                        {{ cardSortBy === 'created_at' && cardSortOrder === 'asc' ? '🔼' : '🔽' }}
                      </span>
                    </div>
                  </th>
                  <th 
                    @click="toggleSort('activated_at')"
                    class="px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-widest cursor-pointer hover:text-white transition-colors group"
                  >
                    <div class="flex items-center gap-1">
                      激活时间
                      <span :class="['transition-opacity', cardSortBy === 'activated_at' ? 'opacity-100' : 'opacity-20 group-hover:opacity-50']">
                        {{ cardSortBy === 'activated_at' && cardSortOrder === 'asc' ? '🔼' : '🔽' }}
                      </span>
                    </div>
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/5">
                <tr v-for="card in cards" :key="card.card_id" class="hover:bg-white/5 transition-colors">
                  <td class="px-6 py-4">
                    <div class="flex items-center gap-2">
                      <span class="font-mono text-primary-gold text-sm">{{ card.card_id }}</span>
                      <button 
                        @click="copyToClipboard(card.card_id)"
                        class="p-1 hover:bg-white/10 rounded-md transition-all group/copy"
                        title="复制卡密"
                      >
                        <span class="text-xs opacity-40 group-hover/copy:opacity-100">📋</span>
                      </button>
                    </div>
                  </td>
                  <td class="px-6 py-4">
                    <span :class="[
                      'text-[10px] font-bold px-2 py-0.5 rounded-full uppercase',
                      card.status === 'not_activated' ? 'bg-gray-500/20 text-gray-400' : 'bg-green-500/20 text-green-400'
                    ]">
                      {{ card.status === 'not_activated' ? '待激活' : '已激活' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-xs text-gray-400">{{ formatDate(card.created_at) }}</td>
                  <td class="px-6 py-4 text-xs text-gray-400">{{ formatDate(card.activated_at) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- 3. 互动数据 -->
        <section v-if="activeTab === 'interactions'" class="animate-in fade-in slide-in-from-bottom-4 duration-700">
          <div class="bg-white/5 border border-white/5 rounded-3xl overflow-hidden">
            <table class="w-full text-left">
              <thead>
                <tr class="border-b border-white/5 bg-white/5">
                  <th class="px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-widest">卡密 ID</th>
                  <th class="px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-widest">首次互动</th>
                  <th class="px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-widest">查看次数</th>
                  <th class="px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-widest">最近查看</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/5">
                <tr v-for="log in interactions" :key="log.card_id" class="hover:bg-white/5 transition-colors">
                  <td class="px-6 py-4 font-mono text-sm text-white">{{ log.card_id }}</td>
                  <td class="px-6 py-4 text-xs text-gray-400">{{ formatDate(log.created_at) }}</td>
                  <td class="px-6 py-4 font-mono text-primary-purple font-bold">{{ log.view_count }}</td>
                  <td class="px-6 py-4 text-xs text-gray-400">{{ formatDate(log.last_view_at) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<style scoped>
/* 滚动条美化 */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.1);
}
</style>
