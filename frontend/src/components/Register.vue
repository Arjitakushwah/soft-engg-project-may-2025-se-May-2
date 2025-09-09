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

        <div class="mb-3">
            <button @click="registerWithGoogle" class="btn btn-google w-100" :disabled="isGoogleLoading">
                <span v-if="isGoogleLoading" class="spinner-border spinner-border-sm text-purple me-2" role="status" aria-hidden="true"></span>
                <svg v-else class="google-icon me-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                  <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                  <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                  <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                </svg>
                Register with Google
            </button>
        </div>

        <div class="separator">
            <span>OR</span>
        </div>
        
        <form @submit.prevent="handleSendOtp" v-if="step === 1" novalidate>
          <p class="text-center text-muted small">Register with your email to receive a verification code.</p>
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
            <span v-if="isLoading" class="spinner-border spinner-border-sm text-purple" role="status" aria-hidden="true"></span>
            <span v-else>Send OTP</span>
          </button>
        </form>

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
                <span v-if="isLoading" class="spinner-border spinner-border-sm text-purple" role="status" aria-hidden="true"></span>
                <span v-else>Verify OTP</span>
            </button>
             <button @click="step = 1; serverError=''" class="btn btn-link w-100 mt-2">Change Email</button>
        </form>

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
            <div v-if="isCheckingUsername" class="spinner-border spinner-border-sm text-purple position-absolute" style="top: 12px; right: 12px;" role="status">
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
          <div class="mb-3 form-check">
            <input type="checkbox" class="form-check-input" :class="{'is-invalid': errors.terms}" id="termsCheck" v-model="termsAccepted" @change="validateField('terms')">
            <label class="form-check-label" for="termsCheck">
              I agree to the <a href="#" target="_blank">Terms of Service</a> and <a href="#" target="_blank">Privacy Policy</a>.
            </label>
            <div v-if="errors.terms" class="invalid-feedback">{{ errors.terms }}</div>
          </div>

          <button type="submit" class="btn btn-success w-100" :disabled="isLoading">
            <span v-if="isLoading" class="spinner-border spinner-border-sm text-purple" role="status" aria-hidden="true"></span>
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
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const form = ref({
  name: '',
  username: '',
  email: '',
  password: '',
  passwordConfirm: '',
});
const otp = ref('');
const termsAccepted = ref(false);
const step = ref(1);
const errors = ref({});
const serverError = ref('');
const success = ref('');
const isLoading = ref(false);
const isCheckingUsername = ref(false);
const isGoogleLoading = ref(false);
const router = useRouter();
const route = useRoute();

const debounceTimers = {};
onMounted(() => {
    const error = route.query.error;
    if (error) {
        if (error === 'google_auth_failed') {
            serverError.value = "Google registration failed. Please try again or use email.";
        } else if (error === 'google_email_missing') {
            serverError.value = "Could not retrieve email from Google. Please ensure permissions are granted.";
        } else {
            serverError.value = "An unknown error occurred during Google registration.";
        }
    }
});

const registerWithGoogle = () => {
    isGoogleLoading.value = true;
    window.location.href = 'https://slice-abcd.onrender.com/auth/google/login';
};


const handleSendOtp = async () => {
  serverError.value = '';
  success.value = '';
  validateField('email');
  if (errors.value.email) return;

  isLoading.value = true;
  try {
    const response = await fetch('https://slice-abcd.onrender.com/register/send-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: form.value.email })
    });
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.error || 'Failed to send OTP.');
    }
    success.value = result.message;
    step.value = 2;
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
    const response = await fetch('https://slice-abcd.onrender.com/register/verify-otp', {
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
    const response = await fetch('https://slice-abcd.onrender.com/register', {
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

const handleInput = (fieldName) => {
  clearTimeout(debounceTimers[fieldName]);
  debounceTimers[fieldName] = setTimeout(() => {
    validateField(fieldName);
  }, 500);
};

const validateField = async (fieldName) => {
  errors.value[fieldName] = '';
  serverError.value = '';

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
        const response = await fetch(`https://slice-abcd.onrender.com/check-username?username=${form.value.username}`);
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
      
    case 'terms':
        if (!termsAccepted.value) {
            errors.value.terms = 'You must accept the terms and conditions to register.';
        }
        break;
  }
};

const validateFormOnSubmit = async () => {
    await Promise.all([
        validateField('name'),
        validateField('username'),
        validateField('password'),
        validateField('passwordConfirm'),
        validateField('terms')
    ]);
    return Object.values(errors.value).every(error => !error);
};
</script>

<style scoped>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css");

.invalid-feedback { display: block; text-align: left; margin-top: 0.25rem; }
.navbar { background-color: #756bdb !important; }
.app-title { font-family: 'Fredoka One', cursive; font-size: 1.6rem; color: #f3ebec !important; text-decoration: none; }
.btn-outline-primary { background-color: white; border-color: #3b82f6; color: #756bdb; border: none; margin-left: 10px; padding: 10px 20px; font-family: 'Fredoka One', cursive; border-radius: 30px; cursor: pointer; transition: transform 0.3s, background-color 0.3s; }
.btn-outline-primary:hover { transform: scale(1.05); background-color: #faf2f4; }
.btn-primary { background-color: white; border-color: #3b82f6; color: #756bdb; border: none; margin-left: 10px; padding: 10px 20px; font-family: 'Fredoka One', cursive; border-radius: 30px; cursor: pointer; transition: transform 0.3s, background-color 0.3s; }
.btn-primary:hover { transform: scale(1.05); background-color: #faf2f4; }
.register-container { font-family: 'Comic Neue', cursive; }
.card { background: linear-gradient(135deg, #fff0f5, #f0f8ff); border-radius: 20px; }
.btn-success { background-color: #756bdb; font-family: 'Fredoka One', cursive; border: none; color: white; }
.btn-success:hover { background-color: #F7D96F; color: black; }
.btn-link { color: #6c757d; text-decoration: none; }
.btn-link:hover { color: #0056b3; }
.login-link { color: #007bff; text-decoration: none; font-weight: bold; }
.login-link:hover { text-decoration: underline; }

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

.form-check-label a {
    color: #007bff;
    text-decoration: none;
}
.form-check-label a:hover {
    text-decoration: underline;
}

.text-purple {
    color: #756bdb !important;
}
</style>
