<template>
  <div class="dashboard-wrapper">
    <NavBar @toggle-sidebar="toggleSidebar" />

    <div class="layout-body">
      <Sidebar
        :role="role"
        :class="{ 'is-visible': isSidebarVisible }"
        @navigate="navigateToPage"
      />

      <div
        v-if="isSidebarVisible"
        class="sidebar-overlay"
        @click="toggleSidebar"
      ></div>

      <div class="main-wrapper">
        <main class="main-content">
          <router-view />
        </main>

        <footer class="footer">
          <p>&copy; 2025 Skill Explorers. Let's make learning fun!</p>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/Nav.vue'
import Sidebar from '@/components/Sidebar.vue'

const router = useRouter()
const role = 'child'
const isSidebarVisible = ref(false)

const toggleSidebar = () => {
  isSidebarVisible.value = !isSidebarVisible.value
}

const navigateToPage = (page) => {
  isSidebarVisible.value = false // auto-close on mobile after navigation
  router.push({ name: page })
}

const goToEditProfile = () => {
  router.push({ name: 'ChildEditProfile' })
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
  background: #F8F8FF;
}

.layout-body {
  display: flex;
  flex: 1;
  overflow: hidden; /* Prevent overflow on the main body */
}

.main-wrapper {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow-y: auto; /* The main content area scrolls */
}

.main-content {
  padding: 2rem; /* Consistent padding */
  flex-grow: 1; 
}

.dashboard-footer {
  padding: 1rem 2rem;
  background-color: #ffffff;
  color: #64748b;
  border-top: 1px solid #e2e8f0;
  flex-shrink: 0; /* Prevent footer from shrinking */
}

.footer-content-padded {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-link {
  color: #475569;
  text-decoration: none;
  margin: 0 0.5rem;
  transition: color 0.2s;
}

.footer-link:hover {
  color: #1e293b;
}

.footer-copyright {
  font-size: 0.875rem;
}

.sidebar-overlay {
  display: none; /* Hidden on desktop */
}

/* === FOOTER === */
.footer {
  padding: 1rem 2rem;

  border-top: 1px solid #e2e8f0;
  flex-shrink: 0; /* Prevent footer from shrinking */

    background-color: #333;
    color: white;
    text-align: center;
    margin-top: 30px;
    font-family: 'Fredoka One', cursive;
}

/* --- Responsive Styles for Mobile & Tablet --- */
@media (max-width: 768px) {
  /* On mobile, the sidebar is positioned absolutely to slide over content */
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100%;
    z-index: 1000;
    transform: translateX(-100%);
    transition: transform 0.3s ease-in-out;
  }

  .sidebar.is-visible {
    transform: translateX(0);
  }
  
  /* Show the overlay on mobile when the sidebar is visible */
  .sidebar-overlay {
    display: block;
    position: fixed;
    inset: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 999;
  }
}
</style>