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
        <form @submit.prevent="registerParent" novalidate>
          
          <div class="mb-3">
            <input
              type="text"
              class="form-control"
              :class="{ 'is-invalid': errors.name }"
              v-model.trim="form.name"
              placeholder="Full Name"
              @input="handleInput('name')" 
            />
            <div v-if="errors.name" class="invalid-feedback">{{ errors.name }}</div>
          </div>

          <div class="mb-3 position-relative">
            <input
              type="text"
              class="form-control"
              :class="{ 'is-invalid': errors.username }"
              v-model.trim="form.username"
              placeholder="Username"
              @input="handleInput('username')"
            />
            <div v-if="isCheckingUsername" class="spinner-border spinner-border-sm text-secondary position-absolute" style="top: 12px; right: 12px;" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <div v-if="errors.username" class="invalid-feedback">{{ errors.username }}</div>
          </div>

          <div class="mb-3">
            <input
              type="email"
              class="form-control"
              :class="{ 'is-invalid': errors.email }"
              v-model.trim="form.email"
              placeholder="Email"
              @input="handleInput('email')"
            />
            <div v-if="errors.email" class="invalid-feedback">{{ errors.email }}</div>
          </div>

          <div class="mb-3">
            <input
              type="password"
              class="form-control"
              :class="{ 'is-invalid': errors.password }"
              v-model="form.password"
              placeholder="Password"
              @input="handleInput('password')"
            />
            <div v-if="errors.password" class="invalid-feedback">{{ errors.password }}</div>
          </div>

          <div class="mb-3">
            <input
              type="password"
              class="form-control"
              :class="{ 'is-invalid': errors.passwordConfirm }"
              v-model="form.passwordConfirm"
              placeholder="Confirm Password"
              @input="handleInput('passwordConfirm')"
            />
            <div v-if="errors.passwordConfirm" class="invalid-feedback">{{ errors.passwordConfirm }}</div>
          </div>

          <button type="submit" class="btn btn-success w-100">Register</button>
        </form>

        <p v-if="serverError" class="text-danger mt-3 text-center">{{ serverError }}</p>
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
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const form = ref({
  name: '',
  username: '',
  email: '',
  password: '',
  passwordConfirm: '',
});

const errors = ref({});
const serverError = ref('');
const success = ref('');
const router = useRouter();

const isCheckingUsername = ref(false);
// Use a single object to manage timers for each field
const debounceTimers = {};

const handleInput = (fieldName) => {
  // Clear the previous timer for this specific field
  clearTimeout(debounceTimers[fieldName]);
  
  // Set a new timer
  debounceTimers[fieldName] = setTimeout(() => {
    validateField(fieldName);
  }, 500); // Wait for 500ms of inactivity before validating
};


// --- REFINED: Function to validate a single field ---
const validateField = async (fieldName) => {
  // CORRECTLY clear the error only when we are about to re-validate
  errors.value[fieldName] = '';

  switch (fieldName) {
    case 'name':
      const nameRegex = /^[a-zA-Z\s'-]+$/;
      if (!form.value.name) {
        errors.value.name = 'Full Name is required.';
      } else if (form.value.name.length < 4) { // <-- ADD THIS CHECK
        errors.value.name = 'Full Name must be at least 4 characters long.';
      } else if (!nameRegex.test(form.value.name)) {
        errors.value.name = 'Name can only contain valid characters.';
      }
      break;

    case 'username':
      const usernameRegex = /^[a-zA-Z0-9_]+$/;
      if (!form.value.username) {
          errors.value.username = 'Username is required.';
          break;
      }
      if (form.value.username.length < 4) {
          errors.value.username = 'Username must be at least 4 characters long.';
          break;
      }
      if (!usernameRegex.test(form.value.username)) {
          errors.value.username = 'Username can only contain letters, numbers, and underscores.';
          break;
      }
      
      // If client-side checks pass, then check availability via API
      isCheckingUsername.value = true;
      try {
        const response = await fetch(`http://localhost:5000/check-username?username=${form.value.username}`);
        const result = await response.json();
        if (response.ok && !result.available) {
          errors.value.username = 'This username is already taken.';
        }
      } catch (err) {
        console.error("Username check failed:", err);
      } finally {
        isCheckingUsername.value = false;
      }
      break;

    case 'email':
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!form.value.email) errors.value.email = 'Email is required.';
      else if (!emailRegex.test(form.value.email)) errors.value.email = 'Please enter a valid email address.';
      break;

    case 'password':
      const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/;
      if (!form.value.password) errors.value.password = 'Password is required.';
      else if (form.value.password.length < 8) errors.value.password = 'Password must be at least 8 characters long.';
      else if (!passwordRegex.test(form.value.password)) errors.value.password = 'Password must include uppercase, lowercase, and a number.';
      
      // Also re-validate the confirmation field if it has a value
      if(form.value.passwordConfirm) validateField('passwordConfirm');
      break;

    case 'passwordConfirm':
      if (!form.value.passwordConfirm) errors.value.passwordConfirm = 'Please confirm your password.';
      else if (form.value.password !== form.value.passwordConfirm) errors.value.passwordConfirm = 'Passwords do not match.';
      break;
  }
};

// --- Function to validate the entire form on final submit ---
const validateFormOnSubmit = async () => {
    // Run all validations and wait for them to complete
    await Promise.all([
        validateField('name'),
        validateField('username'),
        validateField('email'),
        validateField('password'),
        validateField('passwordConfirm')
    ]);

    // Return true if no error messages exist
    return Object.values(errors.value).every(error => !error);
};



const registerParent = async () => {
  serverError.value = '';
  success.value = '';

  // Run a final, full validation before submitting
  const isFormValid = await validateFormOnSubmit();
  if (!isFormValid) {
    return;
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
/* No changes to CSS are needed. */
.invalid-feedback { display: block; text-align: left; margin-top: 0.25rem; }
.navbar { background-color: #f0eae9 !important; }
.app-title { font-family: 'Fredoka One', cursive; font-size: 1.6rem; color: #ff6a88 !important; text-decoration: none; }
.btn-outline-primary { background-color: white; border-color: #3b82f6; color: #ff6a88; border: none; margin-left: 10px; padding: 10px 20px; font-family: 'Fredoka One', cursive; border-radius: 30px; cursor: pointer; transition: transform 0.3s, background-color 0.3s; }
.btn-outline-primary:hover { transform: scale(1.05); background-color: #faf2f4; }
.btn-primary { background-color: white; border-color: #3b82f6; color: #ff6a88; border: none; margin-left: 10px; padding: 10px 20px; font-family: 'Fredoka One', cursive; border-radius: 30px; cursor: pointer; transition: transform 0.3s, background-color 0.3s; }
.btn-primary:hover { transform: scale(1.05); background-color: #faf2f4; }
.register-container { font-family: 'Comic Neue', cursive; }
.card { background: linear-gradient(135deg, #fff0f5, #f0f8ff); border-radius: 20px; }
.btn-success { background-color: #ff6a88; font-family: 'Fredoka One', cursive; border: none; }
.btn-success:hover { background-color: #ff6a88; }
.login-link { color: #007bff; text-decoration: none; font-weight: bold; }
.login-link:hover { text-decoration: underline; }
</style>