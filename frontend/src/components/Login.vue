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

        <!-- Google Sign-In Button (Visible only for parents) -->
        <div v-if="role === 'parent'" class="mb-3">
            <button @click="loginWithGoogle" class="btn btn-google w-100" :disabled="isGoogleLoading">
                <span v-if="isGoogleLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                <svg v-else class="google-icon me-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                  <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                  <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                  <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                </svg>
                Login with Google
            </button>
        </div>

        <!-- Separator (Visible only for parents) -->
        <div v-if="role === 'parent'" class="separator">
            <span>OR</span>
        </div>

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
          <button type="submit" class="btn btn-success w-100" :disabled="isLoading">
             <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
             <span v-else>Login as {{ role }}</span>
          </button>
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
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const username = ref('')
const password = ref('')
const role = ref('parent')
const error = ref('')
const success = ref('')
const isLoading = ref(false)
const isGoogleLoading = ref(false)
const router = useRouter()
const route = useRoute()

onMounted(() => {
    const queryError = route.query.error;
    if (queryError) {
        if (queryError === 'google_auth_failed' || queryError === 'google_fetch_failed') {
            error.value = "Google login failed. Please try again.";
        } else if (queryError === 'google_email_missing') {
             error.value = "Could not retrieve email from Google. Please ensure permissions are granted.";
        }
    }
});

const loginWithGoogle = () => {
    isGoogleLoading.value = true;
    // Redirect to the backend which handles the Google OAuth flow
    window.location.href = 'http://localhost:5000/auth/google/login';
};

const login = async () => {
  error.value = ''
  success.value = ''
  isLoading.value = true;

  if (!username.value || !password.value) {
    error.value = 'Please enter both username and password'
    isLoading.value = false;
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
        password: password.value,
        role: role.value // Send the selected role to the backend
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
    
    // Store parent/child specific info if needed
    if (result.role === 'parent') {
      localStorage.setItem('parent', JSON.stringify({
        username: username.value,
        name: username.value // Assuming name is same as username for now
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
  } finally {
      isLoading.value = false;
  }
}
</script>

<style scoped>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css");

.navbar {
  background-color: #756bdb !important;
}

.app-title {
  font-family: 'Fredoka One', cursive;
  font-size: 1.6rem;
  color: #f0f8ff !important;
  text-decoration: none;
}

.btn-outline-primary {
  background-color: #f0f8ff;
  border-color: #3b82f6;
  color: #756bdb;
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
  background-color: #f0f8ff;
  border-color: #3b82f6;
  color: #756bdb;
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
  background-color: #756bdb;
  font-family: 'Fredoka One', cursive;
  border: none;
  color: white;
}

.btn-success:hover {
  background-color: #F7D96F;
  color: black;
}

.background-wrapper-default {
  background-image: url('/src/public/parent.jpg');
  opacity: 0.9;
  height: 100vh;
  width: 100vw;
  background-size:   100% 100%;
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

.btn-google {
    background-color: #ffffff;
    color: #5f6368;
    border: 1px solid #dadce0;
    font-weight: 600;
    font-size: 14px;
    padding: 12px 16px;
    border-radius: 4px;
    transition: all 0.3s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    position: relative;
    overflow: hidden;
}

.btn-google:hover {
    background-color: #f8f9fa;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    border-color: #c6c6c6;
    transform: translateY(-1px);
}

.btn-google:active {
    background-color: #f1f3f4;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    transform: translateY(0);
}

.google-icon {
    width: 18px;
    height: 18px;
    margin-right: 8px;
}

.separator {
    display: flex;
    align-items: center;
    text-align: center;
    color: #aaa;
    margin: 1.5rem 0;
}
.separator::before,
.separator::after {
    content: '';
    flex: 1;
    border-bottom: 1px solid #ddd;
}
.separator:not(:empty)::before {
    margin-right: .5em;
}
.separator:not(:empty)::after {
    margin-left: .5em;
}
</style>
