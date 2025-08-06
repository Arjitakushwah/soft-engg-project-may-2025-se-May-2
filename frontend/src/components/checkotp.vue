<template>
  <div class="container mt-5">
    <div class="card p-4 shadow-lg mx-auto" style="max-width: 500px;">
      <h3 class="text-center mb-4">Verify OTP</h3>

      <form @submit.prevent="submitOtp">
        <div class="otp-inputs d-flex justify-content-between mb-4">
          <input
            v-for="(digit, index) in otpDigits"
            :key="index"
            ref="otpInput"
            v-model="otpDigits[index]"
            @input="moveToNext(index)"
            maxlength="1"
            type="text"
            class="otp-box text-center"
          />
        </div>
        <button class="btn btn-success w-100">Verify</button>
      </form>

      <p v-if="message" class="mt-3 text-success text-center">{{ message }}</p>
      <p v-if="error" class="mt-3 text-danger text-center">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const otpDigits = ref(['', '', '', '', '', ''])
const otpInput = ref([])

const message = ref('')
const error = ref('')

const moveToNext = (index) => {
  if (otpDigits.value[index].length === 1 && index < 5) {
    nextTick(() => otpInput.value[index + 1]?.focus())
  }
}

const submitOtp = async () => {
  const otp = otpDigits.value.join('')
  if (otp.length !== 6) {
    error.value = 'Please enter all 6 digits.'
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
  }
}
</script>

<style>
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
</style>
