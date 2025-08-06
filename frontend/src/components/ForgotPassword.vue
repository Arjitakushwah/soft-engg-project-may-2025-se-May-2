<template>
  <div class="container mt-5">
    <div class="card p-4 shadow-lg mx-auto" style="max-width: 500px;">
      <h3 class="text-center mb-4">Forgot Password</h3>
      <form @submit.prevent="submitEmail">
        <input type="email" class="form-control mb-3" v-model="email" placeholder="Enter your registered email" required />
        <button class="btn btn-success w-100">Send OTP</button>
    </form>
      <p v-if="message" class="mt-3 text-success text-center">{{ message }}</p>
      <p v-if="error" class="mt-3 text-danger text-center">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const message = ref('')
const error = ref('')

const submitEmail = async () => {
  try {
    const res = await fetch('http://localhost:5000/send-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value })
    })
    const result = await res.json()
    if (!res.ok) throw new Error(result.error)
    message.value = 'Password reset link sent to your email.'
  } catch (err) {
    error.value = err.message || 'Something went wrong.'
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