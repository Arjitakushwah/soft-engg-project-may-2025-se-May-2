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
        
        <!-- Step 1: Email Input and Send OTP -->
        <form @submit.prevent="handleSendOtp" v-if="step === 1" novalidate>
          <p class="text-center text-muted">Start by entering your email to receive a verification code.</p>
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
          <button type="submit" class="btn btn-success w-100" :disabled="isLoading">
            <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            <span v-else>Send OTP</span>
          </button>
        </form>

        <!-- Step 2: OTP Verification -->
        <form @submit.prevent="handleVerifyOtp" v-if="step === 2" novalidate>
            <p class="text-center text-muted">An OTP has been sent to <strong>{{ form.email }}</strong>. Please enter it below.</p>
            <div class="mb-3">
                <input
                    type="text"
                    class="form-control"
                    :class="{ 'is-invalid': errors.otp }"
                    v-model.trim="otp"
                    placeholder="Enter OTP"
                    maxlength="6"
                />
                <div v-if="errors.otp" class="invalid-feedback">{{ errors.otp }}</div>
            </div>
            <button type="submit" class="btn btn-success w-100" :disabled="isLoading">
                <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                <span v-else>Verify OTP</span>
            </button>
             <button @click="step = 1; serverError=''" class="btn btn-link w-100 mt-2">Change Email</button>
        </form>

        <!-- Step 3: Full Registration Form -->
        <form @submit.prevent="registerParent" v-if="step === 3" novalidate>
          <p class="text-center text-success">✓ Email Verified!</p>
          <div class="mb-3">
            <input type="email" class="form-control" v-model="form.email" disabled readonly />
          </div>
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
          <button type="submit" class="btn btn-success w-100" :disabled="isLoading">
            <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            <span v-else>Register</span>
          </button>
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

// --- STATE MANAGEMENT ---
const form = ref({
  name: '',
  username: '',
  email: '',
  password: '',
  passwordConfirm: '',
});
const otp = ref('');
const step = ref(1); // 1: Email, 2: OTP, 3: Details
const errors = ref({});
const serverError = ref('');
const success = ref('');
const isLoading = ref(false);
const isCheckingUsername = ref(false);
const router = useRouter();

const debounceTimers = {};

// --- API CALLS ---

const handleSendOtp = async () => {
  serverError.value = '';
  success.value = '';
  validateField('email');
  if (errors.value.email) return;

  isLoading.value = true;
  try {
    const response = await fetch('http://localhost:5000/register/send-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: form.value.email })
    });
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.error || 'Failed to send OTP.');
    }
    success.value = result.message;
    step.value = 2; // Move to OTP verification step
  } catch (err) {
    serverError.value = err.message;
  } finally {
    isLoading.value = false;
  }
};

const handleVerifyOtp = async () => {
  serverError.value = '';
  success.value = '';
  errors.value.otp = !otp.value ? 'OTP is required.' : '';
  if (errors.value.otp) return;

  isLoading.value = true;
  try {
    const response = await fetch('http://localhost:5000/register/verify-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: form.value.email, otp: otp.value })
    });
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.error || 'OTP verification failed.');
    }
    success.value = result.message;
    step.value = 3; // Move to final registration details
  } catch (err) {
    serverError.value = err.message;
    errors.value.otp = err.message;
  } finally {
    isLoading.value = false;
  }
};

const registerParent = async () => {
  serverError.value = '';
  success.value = '';

  const isFormValid = await validateFormOnSubmit();
  if (!isFormValid) return;

  isLoading.value = true;
  try {
    const response = await fetch('http://localhost:5000/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: form.value.name,
        username: form.value.username,
        email: form.value.email,
        password: form.value.password
      })
    });
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.error || 'Registration failed.');
    }
    success.value = 'Registration successful! Redirecting to login...';
    localStorage.setItem('userRole', 'parent');
    localStorage.setItem('username', form.value.username);
    setTimeout(() => {
      router.push('/login');
    }, 2000);
  } catch (err) {
    serverError.value = err.message;
  } finally {
    isLoading.value = false;
  }
};


// --- VALIDATION LOGIC ---

const handleInput = (fieldName) => {
  clearTimeout(debounceTimers[fieldName]);
  debounceTimers[fieldName] = setTimeout(() => {
    validateField(fieldName);
  }, 500);
};

const validateField = async (fieldName) => {
  errors.value[fieldName] = '';
  serverError.value = ''; // Clear server error on new input

  switch (fieldName) {
    case 'name':
      const nameRegex = /^[a-zA-Z\s'-]+$/;
      if (!form.value.name) errors.value.name = 'Full Name is required.';
      else if (form.value.name.length < 4) errors.value.name = 'Full Name must be at least 4 characters long.';
      else if (!nameRegex.test(form.value.name)) errors.value.name = 'Name can only contain valid characters.';
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
      
      if(form.value.passwordConfirm) validateField('passwordConfirm');
      break;

    case 'passwordConfirm':
      if (!form.value.passwordConfirm) errors.value.passwordConfirm = 'Please confirm your password.';
      else if (form.value.password !== form.value.passwordConfirm) errors.value.passwordConfirm = 'Passwords do not match.';
      break;
  }
};

const validateFormOnSubmit = async () => {
    await Promise.all([
        validateField('name'),
        validateField('username'),
        validateField('password'),
        validateField('passwordConfirm')
    ]);
    return Object.values(errors.value).every(error => !error);
};
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
.btn-link { color: #6c757d; text-decoration: none; }
.btn-link:hover { color: #0056b3; }
.login-link { color: #007bff; text-decoration: none; font-weight: bold; }
.login-link:hover { text-decoration: underline; }
</style>
