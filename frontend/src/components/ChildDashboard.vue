<!-- src/views/ChildDashboard.vue -->
<template>
  <div class="dashboard-wrapper">
    <!-- Navbar -->
    <NavBar />

    <!-- Layout -->
    <div class="layout-body">
      <!-- Sidebar -->
      <Sidebar :role="role" @navigate="navigateToPage" />

      <!-- Dynamic Main Content -->
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// Components
import NavBar from '@/components/Nav.vue'
import Sidebar from '@/components/Sidebar.vue'

const role = 'child'
const router = useRouter()

// Used by Sidebar to navigate to the correct child route
const navigateToPage = (page) => {
  router.push({ name: page })
}

onMounted(() => {
  const storedName = localStorage.getItem('username') || 'Child'
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
  background-color: #f3f4f6;
}

.main-content {
  flex-grow: 1;
  padding: 30px;
  overflow-y: auto;
  background-color: #ffffff; /* example: white background */
  color: #1e293b; /* optional: adjust text color */
}

</style>
