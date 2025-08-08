<template>
  <div :class="role === 'child' ? 'background-wrapper-child' : 'background-wrapper-default'">
    <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm px-4">
      <div class="container-fluid d-flex justify-content-between align-items-center">
        <router-link to="/" class="navbar-brand app-title">Skill Explorers</router-link>
        <div class="d-flex">
          <router-link to="/login" class="btn btn-outline-primary me-2">Login</router-link>
          <router-link to="/register" class="btn btn-primary">Register</router-link>
        </div>
      </div>
    </nav>
    <div class="login-container container mt-5">
      <div class="card shadow-lg p-4 mx-auto" style="max-width: 450px;">
        <h2 class="text-center mb-4">Login</h2>
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
        <form @submit.prevent="login">
          <div class="mb-3">
            <input type="text" class="form-control" v-model="username" placeholder="Username" required />
          </div>
          <div class="mb-3">
            <input type="password" class="form-control" v-model="password" placeholder="Password" required />
          </div>
          <button type="submit" class="btn btn-success w-100">Login as {{ role }}</button>
        </form>
        <p class="text-center mt-3">
          <router-link to="/forgot-password" class="text-primary">Forgot Password?</router-link>
            |
          <router-link to="/forgot-username" class="text-primary">Forgot Username?</router-link>
        </p>
        <p class="text-danger mt-3 text-center" v-if="error">{{ error }}</p>
        <p class="text-success mt-3 text-center" v-if="success">{{ success }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const role = ref('parent')
const error = ref('')
const success = ref('')
const router = useRouter()

const login = async () => {
  error.value = ''
  success.value = ''

  if (!username.value || !password.value) {
    error.value = 'Please enter both username and password'
    return
  }

  try {
    const response = await fetch('http://localhost:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value
      })
    })

    const result = await response.json()

    if (!response.ok) {
      error.value = result.error || 'Login failed'
      return
    }

    localStorage.setItem('access_token', result.access_token)
    localStorage.setItem('userRole', result.role)
    localStorage.setItem('username', username.value)

    success.value = 'Login successful! Redirecting...'

    if (result.role === 'parent') {
      localStorage.setItem('parent', JSON.stringify({
        username: username.value,
        name: username.value
      }))
    } else if (result.role === 'child') {
      localStorage.setItem('child', JSON.stringify({
        username: username.value,
        name: username.value
      }))
    }

    setTimeout(() => {
      router.push(result.redirect_to || '/')
    }, 2000)

  } catch (err) {
    console.error(err)
    error.value = 'Network error. Please try again.'
  }
}
</script>

<style scoped>
.navbar {
  background-color: #be6dbe !important;
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

.login-container {
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

.background-wrapper-default {
  background-image: url('/src/public/parent.jpg');
  opacity: 0.9;
  height: 100vh;
  width: 100vw;
  background-size:  100% 100%;
  background-position: center;
  background-repeat: no-repeat;
  overflow: hidden;
}

.background-wrapper-child {
  background-image: url('/src/public/child2.jpg'); 
  height: 100vh;
  width: 100vw;
  opacity: 80%;
  background-size: 100% 100%;
  background-position: center;
  background-repeat: no-repeat;
  overflow: hidden;
}
</style>
