<template>
  <div class="app-container">
    <Navbar v-if="!isAuthRoute" />
    <!-- Apply extra padding only if not on '/' -->
    <div :class="['page-content', { 'with-padding': route.path !== '/' }]">
      <router-view></router-view>
    </div>
  </div>
</template>


<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from './components/Navbar.vue'

const route = useRoute()

// ✅ Correct way to define computed in script setup
const isAuthRoute = computed(() => {
  return ['/', '/login', '/register'].includes(route.path)
})
</script>

<style>
.app-container {
  margin: 0;
  padding: 0;
}

.with-padding {
  padding-top: 90px;
}
</style>
