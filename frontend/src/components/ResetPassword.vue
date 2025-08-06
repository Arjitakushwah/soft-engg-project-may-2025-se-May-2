<template>
  <div class="container mt-5">
    <div class="card p-4 shadow-lg mx-auto" style="max-width: 500px;">
      <h3 class="text-center mb-4">Reset Password</h3>

      <form @submit.prevent="submitNewPassword">
        <!-- New Password Field -->
            <div class="mb-3 position-relative">
            <input
                :type="showPassword ? 'text' : 'password'"
                class="form-control"
                v-model="newPassword"
                placeholder="New Password"
                required
            />
            <span class="toggle-icon" @click="showPassword = !showPassword">
                {{ showPassword ? 'Hide' : 'Show' }}
            </span>
            </div>

            <!-- Confirm Password Field -->
            <div class="mb-3 position-relative">
            <input
                :type="showConfirmPassword ? 'text' : 'password'"
                class="form-control"
                v-model="confirmPassword"
                placeholder="Confirm New Password"
                required
            />
            <span class="toggle-icon" @click="showConfirmPassword = !showConfirmPassword">
                {{ showConfirmPassword ? 'Hide' : 'Show' }}
            </span>
            </div>
            <button class="btn btn-success w-100">Reset Password</button>
      </form>

      <p v-if="message" class="mt-3 text-success text-center">{{ message }}</p>
      <p v-if="error" class="mt-3 text-danger text-center">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const newPassword = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const message = ref('')
const error = ref('')

const submitNewPassword = async () => {
  if (newPassword.value.length < 6) {
    error.value = 'Password must be at least 6 characters.'
    return
  }

  if (newPassword.value !== confirmPassword.value) {
    error.value = 'Passwords do not match.'
    return
  }

  try {
    const res = await fetch('http://localhost:5000/reset-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: newPassword.value })
    })
    const result = await res.json()
    if (!res.ok) throw new Error(result.error)

    message.value = 'Password reset successfully!'
    error.value = ''

    // ✅ Redirect to /login after short delay
    setTimeout(() => {
      router.push('/login')
    }, 1500) // 1.5s delay so user can see success message

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

.toggle-icon {
  position: absolute;
  top: 50%;
  right: 15px;
  transform: translateY(-50%);
  cursor: pointer;
  user-select: none;
  font-size: 18px;
}
</style>
