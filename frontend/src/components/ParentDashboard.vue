<template>
  <div class="dashboard-wrapper">
    <!-- Top NavBar -->
    <NavBar @toggle-sidebar="toggleSidebar" />

    <!-- Sidebar + Main Content -->
    <div class="layout-body">
      <Sidebar
        :role="role"
        :is-visible="isSidebarVisible"
        @navigate="navigateToPage"
      />
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/Nav.vue'
import Sidebar from '@/components/Sidebar.vue'

const router = useRouter()
const role = 'parent'
const isSidebarVisible = ref(false)

const toggleSidebar = () => {
  isSidebarVisible.value = !isSidebarVisible.value
}

const navigateToPage = (page) => {
  isSidebarVisible.value = false // auto-close on mobile after navigation
  router.push({ name: page })
}

onMounted(() => {
  const storedName = localStorage.getItem('username') || 'Parent'
})
</script>

<style scoped>
.dashboard-wrapper {
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: 'Comic Neue', sans-serif;
}

.layout-body {
  display: flex;
  flex: 1;
  overflow: hidden;
  background-color: #f3f4f6;
}

.main-content {
  flex-grow: 1;
  padding: 30px;
  overflow-y: auto;
  background-color: #ffffff;
  color: #1e293b;
  height: 100vh;
}
</style>
