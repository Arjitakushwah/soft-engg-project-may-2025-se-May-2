<template>
  <div class="container mt-5">
    <div class="card p-4 shadow-lg mx-auto" style="max-width: 500px;">
      <h3 class="text-center mb-4">Forgot Username</h3>
      <form @submit.prevent="submitEmail">
        <input
          type="email"
          class="form-control mb-3"
          v-model="email"
          placeholder="Enter your registered email"
          required
        />
        <button class="btn btn-success w-100" type="submit">Retrieve Username</button>
      </form>
      <p v-if="username" class="mt-3 text-success text-center">
        Your username is: <strong>{{ username }}</strong>
      </p>
      <p v-if="error" class="mt-3 text-danger text-center">{{ error }}</p>
    </div>
  </div>
</template>

<script setup lang="js">
import { ref } from 'vue'

const email = ref('')
const username = ref('')
const error = ref('')

const submitEmail = async () => {
  username.value = ''
  error.value = ''

  try {
    const res = await fetch('http://localhost:5000/forgot-username', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value })
    })

    const result = await res.json()

    if (!res.ok) {
      throw new Error(result.error || 'Unable to retrieve username')
    }

    username.value = result.username
  } catch (err) {
    error.value = err.message || 'Something went wrong'
  }
}
</script>
<style>
.btn-success {
  background-color: #ff6a88;
  font-family: 'Fredoka One', cursive;
  border: none;
}

.btn-success:hover {
  background-color: #ff6a88;
}
</style>
