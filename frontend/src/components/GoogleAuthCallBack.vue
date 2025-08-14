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
    // Extract the token, role, and username from the URL query parameters
    // These are sent by your Flask backend after a successful Google login.
    const { token, role, username } = route.query;
  
    if (token && role) {
      // If the token and role exist, the login was successful.
      // Store the authentication details in the browser's localStorage.
      localStorage.setItem('access_token', token);
      localStorage.setItem('userRole', role);
      localStorage.setItem('username', username);
      if (role === 'parent') {
      localStorage.setItem('parent', JSON.stringify({
        username: username,
        name: username
         // Assuming name is same as username for now
      }))
    } 
      console.log(`User ${username} logged in as ${role}`);
  
      // Redirect the user to their dashboard.
      // This assumes parents are redirected to '/parent/home'.
      router.push('/parent/home');
    } else {
      // If the details are missing, it means the Google login failed.
      // Redirect the user back to the register page with an error message in the URL.
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
      /* Match the theme color from your other pages */
              color: #756bdb !important;
  }
  </style>
  