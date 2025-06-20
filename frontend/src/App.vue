<script setup>
import { RouterLink, RouterView } from 'vue-router'

</script>

<template>
<div class="app-container">
    <Navbar v-if="!isAuthRoute" />
    <div class="content-container">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'; // Adjust the path if necessary

export default {
  name: 'App',
  components: {
    Navbar,
  },
  computed: {
    isAuthRoute() {
      return ['/login', '/register'].includes(this.$route.path);
    },
  },
};
</script>

<style scoped>

</style>
