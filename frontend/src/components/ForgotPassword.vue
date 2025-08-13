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

    <div class="container mt-5">
      <div class="card p-4 shadow-lg mx-auto position-relative" style="max-width: 500px;">
        <button @click="goBack" class="back-icon-btn" aria-label="Go Back">
          <i class="bi bi-arrow-left"></i>
        </button>

        <h3 class="text-center mb-4">Forgot Password</h3>

        <!-- Role Selector -->
        <div class="mb-4 d-flex justify-content-center gap-3">
            <div class="form-check">
                <input class="form-check-input" type="radio" value="parent" v-model="role" id="roleParent" />
                <label class="form-check-label" for="roleParent">I am a Parent</label>
            </div>
            <div class="form-check">
                <input class="form-check-input" type="radio" value="child" v-model="role" id="roleChild" />
                <label class="form-check-label" for="roleChild">I am a Child</label>
            </div>
        </div>
        
        <!-- Parent Logic -->
        <div v-if="role === 'parent'">
            <!-- Step 1: Email Input -->
            <form @submit.prevent="handleSendOtp" v-if="step === 1">
              <p class="text-center text-muted">Enter your registered email to receive a verification code.</p>
              <div class="mb-3">
                <input
                  type="email"
                  class="form-control"
                  :class="{ 'is-invalid': errors.email }"
                  v-model="form.email"
                  placeholder="Enter your registered email"
                  required
                />
                <div v-if="errors.email" class="invalid-feedback">{{ errors.email }}</div>
              </div>
              <button type="submit" class="btn btn-success w-100" :disabled="isLoading">
                <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                <span v-else>Send OTP</span>
              </button>
            </form>

            <!-- Step 2: OTP Verification -->
            <form @submit.prevent="handleVerifyOtp" v-if="step === 2">
              <p class="text-center text-muted">An OTP has been sent to <strong>{{ form.email }}</strong>. Please enter it below.</p>
              <div class="mb-3">
                <input
                  type="text"
                  class="form-control"
                  :class="{ 'is-invalid': errors.otp }"
                  v-model="form.otp"
                  placeholder="Enter OTP"
                  maxlength="6"
                  required
                />
                <div v-if="errors.otp" class="invalid-feedback">{{ errors.otp }}</div>
              </div>
               <button type="submit" class="btn btn-success w-100" :disabled="isLoading">
                <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                <span v-else>Verify OTP</span>
              </button>
              <button @click="step = 1; serverError=''" class="btn btn-link w-100 mt-2">Change Email</button>
            </form>

            <!-- Step 3: Set New Password -->
            <form @submit.prevent="handleSetPassword" v-if="step === 3">
              <p class="text-center text-success">✓ OTP Verified! Set a new password.</p>
              <div class="mb-3">
                <input
                  type="password"
                  class="form-control"
                  :class="{ 'is-invalid': errors.newPassword }"
                  v-model="form.newPassword"
                  placeholder="New Password"
                  required
                />
                <div v-if="errors.newPassword" class="invalid-feedback">{{ errors.newPassword }}</div>
              </div>
              <div class="mb-3">
                <input
                  type="password"
                  class="form-control"
                  :class="{ 'is-invalid': errors.confirmPassword }"
                  v-model="form.confirmPassword"
                  placeholder="Confirm New Password"
                  required
                />
                <div v-if="errors.confirmPassword" class="invalid-feedback">{{ errors.confirmPassword }}</div>
              </div>
              <button type="submit" class="btn btn-success w-100" :disabled="isLoading">
                <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                <span v-else>Reset Password</span>
              </button>
            </form>
        </div>

        <!-- Child Logic -->
        <div v-else class="text-center alert alert-info">
            <i class="bi bi-info-circle-fill h4"></i>
            <p class="mt-2 mb-0">Child accounts cannot reset passwords directly.</p>
            <p class="small text-muted">Please ask your parent for help to reset your password from their dashboard.</p>
        </div>

        <p v-if="serverError" class="mt-3 text-danger text-center">{{ serverError }}</p>
        <p v-if="success" class="mt-3 text-success text-center">{{ success }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const role = ref('parent'); // Default role
const form = ref({
  email: '',
  otp: '',
  newPassword: '',
  confirmPassword: '',
});
const step = ref(1); // 1: Email, 2: OTP, 3: Set Password
const isLoading = ref(false);
const serverError = ref('');
const success = ref('');
const errors = ref({});

const goBack = () => {
  router.back();
};

const validateField = (fieldName) => {
    errors.value[fieldName] = '';
    switch(fieldName) {
        case 'email':
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!form.value.email) errors.value.email = 'Email is required.';
            else if (!emailRegex.test(form.value.email)) errors.value.email = 'Please enter a valid email address.';
            break;
        case 'otp':
            if (!form.value.otp) errors.value.otp = 'OTP is required.';
            else if (form.value.otp.length !== 6) errors.value.otp = 'OTP must be 6 digits.';
            break;
        case 'newPassword':
            const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/;
            if (!form.value.newPassword) errors.value.newPassword = 'New password is required.';
            else if (form.value.newPassword.length < 8) errors.value.newPassword = 'Password must be at least 8 characters long.';
            else if (!passwordRegex.test(form.value.newPassword)) errors.value.newPassword = 'Password must include uppercase, lowercase, and a number.';
            break;
        case 'confirmPassword':
            if (!form.value.confirmPassword) errors.value.confirmPassword = 'Please confirm your new password.';
            else if (form.value.newPassword !== form.value.confirmPassword) errors.value.confirmPassword = 'Passwords do not match.';
            break;
    }
    return !errors.value[fieldName];
}

const handleSendOtp = async () => {
  serverError.value = '';
  success.value = '';
  if (!validateField('email')) return;

  isLoading.value = true;
  try {
    const res = await fetch('http://localhost:5000/forgot-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: form.value.email })
    });
    const result = await res.json();
    if (!res.ok) throw new Error(result.error || 'Failed to send OTP.');
    
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
  if (!validateField('otp')) return;

  isLoading.value = true;
  try {
    const res = await fetch('http://localhost:5000/verify-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: form.value.email, otp: form.value.otp })
    });
    const result = await res.json();
    if (!res.ok || !result.success) throw new Error(result.message || 'Invalid OTP.');
    
    success.value = result.message;
    step.value = 3;
  } catch (err) {
    serverError.value = err.message;
  } finally {
    isLoading.value = false;
  }
};

const handleSetPassword = async () => {
  serverError.value = '';
  success.value = '';
  const isNewPasswordValid = validateField('newPassword');
  const isConfirmPasswordValid = validateField('confirmPassword');
  if (!isNewPasswordValid || !isConfirmPasswordValid) return;

  isLoading.value = true;
  try {
    const res = await fetch('http://localhost:5000/set-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: form.value.email,
        new_password: form.value.newPassword
      })
    });
    const result = await res.json();
    if (!res.ok) throw new Error(result.error || 'Failed to reset password.');
    
    success.value = 'Password reset successfully! Redirecting to login...';
    setTimeout(() => {
      router.push('/login');
    }, 2000);
  } catch (err) {
    serverError.value = err.message;
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css");

.btn-success {
  background-color: #756bdb;
  font-family: 'Fredoka One', cursive;
  border: none;
}
.btn-success:hover {
  background-color: #6155b1;
}
.navbar {
  background-color: #756bdb !important;
}
.app-title {
  font-family: 'Fredoka One', cursive;
  font-size: 1.6rem;
  color: white !important;
  text-decoration: none;
}
.btn-outline-primary {
  background-color: white;
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
  background-color: white;
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
.back-icon-btn {
  position: absolute;
  top: 15px;
  left: 15px;
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #756bdb;
  cursor: pointer;
  transition: transform 0.2s ease;
}
.back-icon-btn:hover {
  transform: scale(1.1);
}
.invalid-feedback {
    display: block;
}
.btn-link { 
    color: #6c757d; 
    text-decoration: none; 
}
.btn-link:hover { 
    color: #0056b3; 
}
.form-check-input:checked {
    background-color: #756bdb;
    border-color: #756bdb;
}
</style>
