<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm px-4">
      <div class="container-fluid d-flex justify-content-between align-items-center">
        <router-link to="/" class="navbar-brand app-title">Skill Explorers</router-link>
        <div class="d-flex">
          <router-link to="/login" class="btn btn-outline-primary me-2">Login</router-link>
          <router-link to="/register" class="btn btn-primary">Register</router-link>
        </div>
      </div>
    </nav>
  <div class="container mt-5">
    <div class="card p-4 shadow-lg mx-auto position-relative" style="max-width: 500px;">
      <!-- Back Icon -->
      <button @click="goBack" class="back-icon-btn" aria-label="Go Back">
        <i class="bi bi-arrow-left"></i>
      </button>
      <h3 class="text-center mb-4">Forgot Username</h3>
      <p class="text-center text-muted">Enter your registered email, and we will send your username to your inbox.</p>
      
      <!-- Hide form on success and show message and login button instead -->
      <form @submit.prevent="submitEmail" v-if="!successMessage">
        <div class="mb-3">
            <input
            type="email"
            class="form-control"
            :class="{ 'is-invalid': error }"
            v-model="email"
            placeholder="Enter your registered email"
            required
            />
            <div v-if="error" class="invalid-feedback">{{ error }}</div>
        </div>
        <button class="btn btn-success w-100" type="submit" :disabled="isLoading">
            <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            <span v-else>Retrieve Username</span>
        </button>
      </form>

      <div v-if="successMessage" class="text-center">
        <p class="mt-3 text-success">
          {{ successMessage }}
        </p>
        <router-link to="/login" class="btn btn-primary mt-2">Go to Login</router-link>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const email = ref('')
const successMessage = ref('')
const error = ref('')
const isLoading = ref(false)

const goBack = () => {
  router.back()
}

const submitEmail = async () => {
  successMessage.value = ''
  error.value = ''

  if (!email.value) {
      error.value = "Email is required.";
      return;
  }

  isLoading.value = true;
  try {
    const res = await fetch('http://localhost:5000/forgot-username', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value })
    })

    const result = await res.json()

    if (!res.ok) {
      // Even on failure, show a generic message to prevent email enumeration
      throw new Error(result.error || 'Unable to retrieve username')
    }

    // On success, show the generic message.
    successMessage.value = 'If an account with that email exists, your username has been sent to it.';

  } catch (err) {
    // In case of an error (like user not found), we still show a generic success message
    // to prevent attackers from knowing which emails are registered.
    successMessage.value = 'If an account with that email exists, your username has been sent to it.';
    console.error(err.message); // Log the actual error for debugging
  } finally {
      isLoading.value = false;
  }
}
</script>
<style scoped>
.btn-success {
  background-color: #756bdb;
  font-family: 'Fredoka One', cursive;
  border: none;
}

.btn-success:hover {
  background-color: #756bdb;
}
.navbar {
  background-color: #756bdb !important;
}

.app-title {
  font-family: 'Fredoka One', cursive;
  font-size: 1.6rem;
  color: #f0f8ff !important;
  text-decoration: none;
}

.btn-outline-primary {
  background-color: white;
  border-color: #3b82f6;
  color: #756bdb;
  border: none;
  margin-left: 10px;
  padding: 10px 20px;
  font-family: 'Fredoka One', cursive;
  border-radius: 30px;
  cursor: pointer;
  transition: transform 0.3s, background-color 0.3s;
}

.btn-outline-primary:hover {
  transform: scale(1.05);
  background-color: #faf2f4;
}

.btn-primary {
  background-color: white;
  border-color: #3b82f6;
  color: #756bdb;
  border: none;
  margin-left: 10px;
  padding: 10px 20px;
  font-family: 'Fredoka One', cursive;
  border-radius: 30px;
  cursor: pointer;
  transition: transform 0.3s, background-color 0.3s;
}

.btn-primary:hover {
  transform: scale(1.05);
  background-color: #faf2f4;
}
.back-icon-btn {
  position: absolute;
  top: 15px;
  left: 15px;
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #756bdb;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.back-icon-btn:hover {
  transform: scale(1.1);
}
.invalid-feedback {
    display: block;
}
</style>
