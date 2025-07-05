<template>
  <div class="parent-dashboard-bg">
    <NavBar @logout="handleLogout" />
    <div class="dashboard-body">
      <Sidebar :role="role" @navigate="navigateToPage" />
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/Nav.vue'
import Sidebar from '@/components/Sidebar.vue'

const router = useRouter()
const role = 'parent'
onMounted(() => {
  const storedName = localStorage.getItem('username') || "Parent"

})
const handleLogout = () => {
  localStorage.clear()
  router.push('/login')
}
const navigateToPage = (page) => {
  router.push({ name: page })
}
</script>

<style scoped>
.parent-dashboard-bg {
  font-family: 'Comic Neue', cursive;
  background: linear-gradient(to bottom right, #f0f8ff, #ffe6f0);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.dashboard-body {
  display: flex;
  flex: 1;
}

.main-content {
  flex: 1;
  padding: 2rem;
  background-color: #fff;
  border-radius: 0 20px 20px 0;
  box-shadow: 0 4px 10px rgba(255, 106, 136, 0.08);
}
</style>
