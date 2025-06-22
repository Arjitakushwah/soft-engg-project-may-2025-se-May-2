<template>
  <div class="login-container container mt-5">
    <div class="card shadow-lg p-4 mx-auto" style="max-width: 450px;">
      <h2 class="text-center mb-4">Login</h2>

      <!-- Role Selection -->
      <div class="mb-3 d-flex justify-content-center gap-3">
        <div class="form-check">
          <input class="form-check-input" type="radio" value="parent" v-model="role" id="roleParent" />
          <label class="form-check-label" for="roleParent">Parent</label>
        </div>
        <div class="form-check">
          <input class="form-check-input" type="radio" value="child" v-model="role" id="roleChild" />
          <label class="form-check-label" for="roleChild">Child</label>
        </div>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="login">
        <div class="mb-3">
          <input type="text" class="form-control" v-model="username" placeholder="Username" required />
        </div>
        <div class="mb-3">
          <input type="password" class="form-control" v-model="password" placeholder="Password" required />
        </div>
        <button type="submit" class="btn btn-primary w-100">Login as {{ role }}</button>
      </form>

      <!-- Error Message -->
      <p class="text-danger mt-3 text-center" v-if="error">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const role = ref('child') // default
const error = ref('')
const router = useRouter()

const login = async () => {
  const res = await fetch('http://127.0.0.1:5000/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: username.value,
      password: password.value,
      role: role.value // ✅ Send role to backend
    })
  })

  const data = await res.json()
  if (!res.ok) {
    error.value = data.error || 'Login failed'
  } else {
    localStorage.setItem('token', data.access_token)
    if (data.redirect_to) router.push(data.redirect_to)
  }
}
</script>

<style scoped>
.login-container {
  font-family: 'Comic Neue', cursive;
}

.card {
  background: linear-gradient(135deg, #fff0f5, #f0f8ff);
  border-radius: 20px;
}

.btn-primary {
  background-color: #ff6a88;
  border: none;
  font-weight: bold;
  font-family: 'Fredoka One', cursive;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #ff4870;
}
</style>
