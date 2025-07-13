<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm px-4">
      <div class="container-fluid d-flex justify-content-between align-items-center">
        <router-link to="/" class="navbar-brand app-title">Skill Explorers</router-link>
        <div class="d-flex">
          <router-link to="/login" class="btn btn-outline-primary me-2">Login</router-link>
          <router-link to="/register" class="btn btn-primary">Register</router-link>
        </div>
      </div>
    </nav>
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
        <p v-if="success" class="text-success mt-3 text-center">{{ success }}</p>

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

const form = ref({
  name: '',
  username: '',
  email: '',
  password: ''
})

const error = ref('')
const success = ref('')
const router = useRouter()

const registerParent = async () => {
  error.value = ''
  success.value = ''

  if (!form.value.name || !form.value.username || !form.value.email || !form.value.password) {
    error.value = 'Please fill in all fields'
    return
  }

  try {
    const response = await fetch('http://localhost:5000/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: form.value.name,
        username: form.value.username,
        email: form.value.email,
        password: form.value.password
      })
    })

    const result = await response.json()

    if (!response.ok) {
      error.value = result.error || 'Registration failed'
    } else {
      success.value = 'Registration successful! Redirecting to login...'
      localStorage.setItem('userRole', 'parent')
      localStorage.setItem('username', form.value.username)

      form.value = {
        name: '',
        username: '',
        email: '',
        password: ''
      }

      setTimeout(() => {
        router.push('/login')
      }, 2000)
    }
  } catch (err) {
    error.value = 'Network error. Please try again.'
    console.error(err)
  }
}

</script>

<style scoped>
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
