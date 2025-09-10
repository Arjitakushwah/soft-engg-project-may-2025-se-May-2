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
  // Get the data passed from the backend in the URL
  const { token, role, username } = route.query;

  // Check if the necessary data is present
  if (token && role) {
    // Store user data in the browser's local storage for session persistence
    localStorage.setItem('access_token', token);
    localStorage.setItem('userRole', role);
    localStorage.setItem('username', username);

    // Your specific logic to also store a 'parent' object
    if (role === 'parent') {
      localStorage.setItem('parent', JSON.stringify({
        username: username,
        name: username
      }));
    }

    console.log(`User ${username} logged in as ${role}`);

    // **FIXED LOGIC:** Redirect the user based on their role
    if (role === 'parent') {
      router.push({ name: 'ParentHome' }); // Redirects to the parent dashboard
    } else if (role === 'child') {
      router.push({ name: 'ChildHome' }); // Redirects to the child dashboard
    } else {
      // Fallback if the role is neither 'parent' nor 'child'
      console.error('Authentication failed: Invalid role received.');
      router.push('/login?error=invalid_role');
    }
  } else {
    // Handle the error case where the token or role is missing
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
