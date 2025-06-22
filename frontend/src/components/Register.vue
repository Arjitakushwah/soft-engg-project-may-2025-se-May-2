<template>
  <div class="register-container container mt-5">
    <div class="card shadow-lg p-4 mx-auto" style="max-width: 500px;">
      <h2 class="text-center mb-4">Register as Parent</h2>

      <form @submit.prevent="registerParent">
        <div class="mb-3">
          <input type="text" class="form-control" v-model="form.name" placeholder="Full Name" required />
        </div>
        <div class="mb-3">
          <input type="text" class="form-control" v-model="form.username" placeholder="Username" required />
        </div>
        <div class="mb-3">
          <input type="email" class="form-control" v-model="form.email" placeholder="Email" required />
        </div>
        <div class="mb-3">
          <input type="password" class="form-control" v-model="form.password" placeholder="Password" required />
        </div>

        <button type="submit" class="btn btn-success w-100">Register</button>
      </form>

      <!-- Error Message -->
      <p v-if="error" class="text-danger mt-3 text-center">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const form = ref({ name: '', username: '', email: '', password: '' })
const error = ref('')
const router = useRouter()

const registerParent = async () => {
  const res = await fetch('http://127.0.0.1:5000/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form.value)
  })
  const data = await res.json()
  if (!res.ok) {
    error.value = data.error || 'Registration failed'
  } else {
    router.push('/login')
  }
}
</script>

<style scoped>
.register-container {
  font-family: 'Comic Neue', cursive;
}

.card {
  background: linear-gradient(135deg, #f0fff0, #e0f7fa);
  border-radius: 20px;
}

.btn-success {
  background-color: #28a745;
  font-family: 'Fredoka One', cursive;
  font-weight: bold;
  border: none;
}

.btn-success:hover {
  background-color: #218838;
}
</style>
