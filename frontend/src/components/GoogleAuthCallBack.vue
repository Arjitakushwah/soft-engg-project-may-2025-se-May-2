<template>
    <div class="callback-container">
      <div class="spinner-border text-purple" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3">Finalizing your login, please wait...</p>
    </div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  
  const route = useRoute();
  const router = useRouter();
  
  onMounted(() => {

    const { token, role, username } = route.query;
  
    if (token && role) {

      localStorage.setItem('access_token', token);
      localStorage.setItem('userRole', role);
      localStorage.setItem('username', username);
      if (role === 'parent') {
      localStorage.setItem('parent', JSON.stringify({
        username: username,
        name: username
         
      }))
    } 
      console.log(`User ${username} logged in as ${role}`);
  
      router.push('/parent/home');
    } else {

      console.error('Google authentication failed: Missing token or role from callback.');
      router.push('/register?error=google_auth_failed');
    }
  });
  </script>
  
  <style scoped>
  .callback-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 80vh;
    font-family: 'Comic Neue', cursive;
    color: #555;
  }
  
  .spinner-border.text-purple {
      
  color: #756bdb !important;
  }
  </style>
  