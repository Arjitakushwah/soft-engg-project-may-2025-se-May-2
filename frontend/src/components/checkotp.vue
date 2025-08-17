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
    <div class="card p-4 shadow-lg mx-auto" style="max-width: 500px; position: relative;">
      
      <button @click="goBack" class="back-icon-btn" aria-label="Go Back">
        <i class="bi bi-arrow-left"></i>
      </button>

      <h3 class="text-center mb-4">Verify OTP</h3>

      <form @submit.prevent="submitOtp">
        <div class="otp-inputs d-flex justify-content-between mb-4">
          <input
            v-for="(digit, index) in otpDigits"
            :key="index"
            ref="otpInput"
            v-model="otpDigits[index]"
            @input="(e) => moveToNext(index, e)"
            @keydown="allowOnlyDigits($event)"
            maxlength="1"
            type="text"
            class="otp-box text-center"
          />
        </div>
        <button class="btn btn-success w-100" :disabled="loading">
          {{ loading ? 'Verifying...' : 'Verify' }}
        </button>
      </form>

      <p v-if="message" class="mt-3 text-success text-center">{{ message }}</p>
      <p v-if="error" class="mt-3 text-danger text-center">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const otpDigits = ref(['', '', '', '', '', ''])
const otpInput = ref([])
const message = ref('')
const error = ref('')
const loading = ref(false)

const goBack = () => {
  router.back()
}

const allowOnlyDigits = (e) => {
  if (!/[0-9]/.test(e.key) && e.key !== 'Backspace') {
    e.preventDefault()
  }
}

const moveToNext = (index, e) => {
  if (e.inputType === 'deleteContentBackward' && otpDigits.value[index] === '' && index > 0) {
    nextTick(() => otpInput.value[index - 1]?.focus())
    return
  }

  if (otpDigits.value[index].length === 1 && index < 5) {
    nextTick(() => otpInput.value[index + 1]?.focus())
  }
}

const submitOtp = async () => {
  if (loading.value) return
  loading.value = true
  error.value = ''
  message.value = ''

  const otp = otpDigits.value.join('')
  if (otp.length !== 6) {
    error.value = 'Please enter all 6 digits.'
    loading.value = false
    return
  }

  try {
    const res = await fetch('http://localhost:5000/verify-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ otp })
    })
    const result = await res.json()
    if (!res.ok) throw new Error(result.error)
    message.value = 'OTP verified successfully. You can now reset your password.'
  } catch (err) {
    error.value = err.message || 'Invalid OTP.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  nextTick(() => otpInput.value[0]?.focus())
})
</script>

<style scoped>
.otp-inputs .otp-box {
  width: 50px;
  height: 50px;
  font-size: 24px;
  border: 2px solid #ccc;
  border-radius: 10px;
  outline: none;
  transition: border-color 0.3s ease;
}

.otp-inputs .otp-box:focus {
  border-color: #ff6a88;
  box-shadow: 0 0 5px rgba(255, 106, 136, 0.5);
}

.btn-success {
  background-color: #ff6a88;
  font-family: 'Fredoka One', cursive;
  border: none;
}

.btn-success:hover {
  background-color: #ff6a88;
}

.navbar {
  background-color: #f0eae9 !important;
}

.app-title {
  font-family: 'Fredoka One', cursive;
  font-size: 1.6rem;
  color: #ff6a88 !important;
  text-decoration: none;
}

.btn-outline-primary {
  background-color: white;
  border-color: #3b82f6;
  color: #ff6a88;
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
  color: #ff6a88;
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
  color: #ff6a88;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.back-icon-btn:hover {
  transform: scale(1.1);
}

@media (max-width: 576px) {
  .otp-inputs .otp-box {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }

  .back-icon-btn {
    top: 10px;
    left: 10px;
  }
}
</style>
