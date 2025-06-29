<template>
  <div>
    <NavBar />
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

        <p v-if="error" class="text-danger mt-3 text-center">{{ error }}</p>

        <p class="text-center mt-4">
          Already have an account?
          <router-link to="/login" class="login-link">Login</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/Nav.vue'

const form = ref({
  name: '',
  username: '',
  email: '',
  password: ''
})

const error = ref('')
const router = useRouter()

const registerParent = () => {
  if (form.value.email && form.value.password && form.value.username) {
    console.log('Dummy Register:', form.value)
    localStorage.setItem('userRole', 'parent')
    localStorage.setItem('username', form.value.username)

    alert('Registration successful! Redirecting to login...')
    router.push('/login')
  } else {
    error.value = 'Please fill in all fields'
  }
}
</script>

<style scoped>
.register-container {
  font-family: 'Comic Neue', cursive;
}

.card {
  background: linear-gradient(135deg, #fff0f5, #f0f8ff);
  border-radius: 20px;
}

.btn-success {
  background-color: #ff6a88;
  font-family: 'Fredoka One', cursive;
  font-weight: bold;
  border: none;
}

.btn-success:hover {
  background-color: #ff6a88;
}

.login-link {
  color: #007bff;
  text-decoration: none;
  font-weight: bold;
}

.login-link:hover {
  text-decoration: underline;
}
</style>
