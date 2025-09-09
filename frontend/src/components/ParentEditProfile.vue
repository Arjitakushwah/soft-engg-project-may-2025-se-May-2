<template>
    <div class="profile-setup-container container py-4">
      <!-- Title changes based on profile status -->
      <h2 class="mb-4 fw-bold">{{ isProfileComplete ? 'Edit Your Profile' : 'Complete Your Profile' }}</h2>
  
      <!-- Loading State -->
      <div v-if="isLoading" class="text-center py-5">
        <div class="spinner-border text-purple" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2 text-muted">Loading your profile...</p>
      </div>
  
      <!-- View for COMPLETED Profiles (Edit Details) -->
      <div v-else-if="isProfileComplete" class="row g-5">
        <!-- Section 1: Update Profile Details -->
        <div class="col-lg-6">
          <div class="card shadow-sm p-4 h-100">
            <h4 class="card-title mb-4">Profile Information</h4>
            <form @submit.prevent="updateExistingProfile" novalidate>
              <div class="mb-3">
                <label for="name" class="form-label">Full Name</label>
                <input type="text" id="name" class="form-control" v-model.trim="profileForm.name" @input="validateField('name')" />
                <div v-if="errors.name" class="invalid-feedback d-block">{{ errors.name }}</div>
              </div>
              <div class="mb-3 position-relative">
                <label for="username" class="form-label">Username</label>
                <input type="text" id="username" class="form-control" v-model.trim="profileForm.username" disabled readonly />
                 <div class="form-text">Your username cannot be changed after setup.</div>
              </div>
              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" id="email" class="form-control" v-model="profileForm.email" disabled readonly />
                <div class="form-text">Your email address cannot be changed.</div>
              </div>
              <button type="submit" class="btn btn-primary-custom w-100 mt-3" :disabled="isUpdatingProfile">
                <span v-if="isUpdatingProfile" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                <span v-else>Save Changes</span>
              </button>
            </form>
          </div>
        </div>
  
        <!-- Section 2: Forgot Password -->
        <div class="col-lg-6">
          <div class="card shadow-sm p-4 h-100 d-flex flex-column justify-content-center text-center">
            <h4 class="card-title mb-3">Security</h4>
            <p class="text-muted">If you've forgotten your password, you can reset it here.</p>
            <button class="btn btn-secondary-custom w-100" @click="openForgotPasswordModal">
              Forgot Password
            </button>
          </div>
        </div>
      </div>
  
      <!-- View for INCOMPLETE Profiles (One-time Setup) -->
      <div v-else class="card shadow-sm p-4">
        <p class="text-muted text-center mb-4">
          Welcome! Please set up your profile details. This is a one-time setup.
        </p>
        <form @submit.prevent="completeProfile" novalidate>
          <div class="mb-3">
            <label for="setup-name" class="form-label">Full Name</label>
            <input type="text" id="setup-name" class="form-control" v-model.trim="profileForm.name" @input="validateField('name')" />
            <div v-if="errors.name" class="invalid-feedback d-block">{{ errors.name }}</div>
          </div>
          <div class="mb-3 position-relative">
            <label for="setup-username" class="form-label">Username</label>
            <input type="text" id="setup-username" class="form-control" v-model.trim="profileForm.username" @input="handleInput('username')" />
            <div v-if="isCheckingUsername" class="spinner-border spinner-border-sm text-purple position-absolute" style="top: 42px; right: 12px;" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <div v-if="errors.username" class="invalid-feedback d-block">{{ errors.username }}</div>
          </div>
          <div class="mb-3">
            <label for="setup-password" class="form-label">Password</label>
            <input type="password" id="setup-password" class="form-control" v-model="passwordForm.new_password" @input="validateField('new_password')" />
            <div v-if="errors.new_password" class="invalid-feedback d-block">{{ errors.new_password }}</div>
          </div>
          <div class="mb-3">
            <label for="setup-confirmPassword" class="form-label">Confirm Password</label>
            <input type="password" id="setup-confirmPassword" class="form-control" v-model="passwordForm.confirm_password" @input="validateField('confirm_password')" />
            <div v-if="errors.confirm_password" class="invalid-feedback d-block">{{ errors.confirm_password }}</div>
          </div>
          <button type="submit" class="btn btn-primary-custom w-100 mt-3" :disabled="isUpdatingProfile">
            <span v-if="isUpdatingProfile" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            <span v-else>Save Profile</span>
          </button>
        </form>
      </div>
  
      <!-- Forgot Password Modal -->
      <transition name="modal-fade">
          <div v-if="showForgotPasswordModal" class="modal-backdrop" @click.self="closeForgotPasswordModal">
              <div class="modal-content">
                  <span class="modal-close" @click="closeForgotPasswordModal">×</span>
                  <h4 class="modal-title text-center">Reset Password</h4>
  
                  <!-- Step 1: Send OTP -->
                  <form v-if="forgotPasswordStep === 1" @submit.prevent="sendResetOtp" class="mt-3">
                      <p class="text-muted text-center small mb-3">Enter your email address to receive a password reset code.</p>
                      <div class="form-group mb-3">
                          <label for="reset-email">Email</label>
                          <input id="reset-email" v-model="passwordForm.email" type="email" class="form-control" required />
                      </div>
                      <button type="submit" class="btn btn-primary-custom w-100" :disabled="isChangingPassword">
                          <span v-if="isChangingPassword" class="spinner-border spinner-border-sm"></span>
                          <span v-else>Send OTP</span>
                      </button>
                  </form>
  
                  <!-- Step 2: Verify OTP -->
                  <form v-if="forgotPasswordStep === 2" @submit.prevent="verifyResetOtp" class="mt-3">
                      <p class="text-muted text-center small">Enter the OTP sent to <strong>{{ passwordForm.email }}</strong>.</p>
                      <div class="form-group mb-3">
                          <label>OTP Code</label>
                          <input v-model="passwordForm.otp" type="text" class="form-control" required maxlength="6" />
                      </div>
                      <button type="submit" class="btn btn-primary-custom w-100" :disabled="isChangingPassword">
                          <span v-if="isChangingPassword" class="spinner-border spinner-border-sm"></span>
                          <span v-else>Verify OTP</span>
                      </button>
                  </form>
  
                  <!-- Step 3: Set New Password -->
                  <form v-if="forgotPasswordStep === 3" @submit.prevent="setNewPassword" class="mt-3">
                      <p class="text-success text-center small">✓ OTP Verified!</p>
                      <div class="form-group mb-2">
                          <label>New Password</label>
                          <input v-model="passwordForm.new_password" type="password" class="form-control" required />
                      </div>
                      <div class="form-group mb-3">
                          <label>Confirm New Password</label>
                          <input v-model="passwordForm.confirm_password" type="password" class="form-control" required />
                      </div>
                      <button type="submit" class="btn btn-danger w-100" :disabled="isChangingPassword">
                          <span v-if="isChangingPassword" class="spinner-border spinner-border-sm"></span>
                          <span v-else>Reset Password</span>
                      </button>
                  </form>
                  
                  <p v-if="modalMessage" :class="['mt-3', 'text-center', 'small', messageType === 'success' ? 'text-success' : 'text-danger']">{{ modalMessage }}</p>
              </div>
          </div>
      </transition>
  
      <!-- General Success/Error Message -->
      <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger', 'mt-4']" role="alert">
        {{ message }}
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  const profileForm = ref({ name: '', username: '', email: '' });
  const originalUsername = ref('');
  const passwordForm = ref({ email: '', otp: '', new_password: '', confirm_password: '' });
  const errors = ref({});
  const message = ref('');
  const messageType = ref('');
  const modalMessage = ref('');
  const isLoading = ref(true);
  const isUpdatingProfile = ref(false);
  const isChangingPassword = ref(false);
  const isCheckingUsername = ref(false);
  const isProfileComplete = ref(false);
  const showForgotPasswordModal = ref(false);
  const forgotPasswordStep = ref(1);
  const debounceTimers = {};
  
  // --- Utility Functions ---
  const getAuthToken = () => localStorage.getItem('access_token');
  
  const apiRequest = async (url, options) => {
      const token = getAuthToken();
      const headers = {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
      };
      const response = await fetch(url, { headers, ...options });
      const result = await response.json();
      if (!response.ok) {
          throw new Error(result.error || `Request failed with status ${response.status}`);
      }
      return result;
  };
  
  // --- Profile Data Fetching ---
  const fetchProfile = async () => {
      isLoading.value = true;
      try {
          const result = await apiRequest('https://slice-abcd.onrender.com/parent_dashboard', { method: 'GET' });
          profileForm.value = {
              name: result.name,
              username: result.username,
              email: result.email
          };
          originalUsername.value = result.username;
          isProfileComplete.value = !!(result.username && result.name);
      } catch (err) {
          message.value = err.message;
          messageType.value = 'error';
      } finally {
          isLoading.value = false;
      }
  };
  
  onMounted(fetchProfile);

  const handleInput = (fieldName) => {
      clearTimeout(debounceTimers[fieldName]);
      debounceTimers[fieldName] = setTimeout(() => {
          validateField(fieldName);
      }, 500);
  };
  
  const validateField = async (fieldName) => {
      errors.value[fieldName] = '';
      let hasError = false;
  
      switch (fieldName) {
          case 'name':
              if (!profileForm.value.name) {
                  errors.value.name = 'Full Name is required.';
                  hasError = true;
              }
              break;
          case 'username':
              const username = profileForm.value.username;
              if (!username) {
                  errors.value.username = 'Username is required.';
                  hasError = true;
              } else if (username.length < 3) {
                  errors.value.username = 'Username must be at least 3 characters.';
                  hasError = true;
              } else if (username.toLowerCase() !== originalUsername.value?.toLowerCase()) {
                  isCheckingUsername.value = true;
                  try {
                      await apiRequest(`https://slice-abcd.onrender.com/check-username?username=${username}`, { method: 'GET' });
                  } catch (err) {
                      errors.value.username = 'Username is already taken.';
                      hasError = true;
                  } finally {
                      isCheckingUsername.value = false;
                  }
              }
              break;
          case 'new_password':
              if (!passwordForm.value.new_password) {
                  errors.value.new_password = 'Password is required.';
                  hasError = true;
              } else if (passwordForm.value.new_password.length < 6) {
                  errors.value.new_password = 'Password must be at least 6 characters.';
                  hasError = true;
              }
              break;
          case 'confirm_password':
              if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
                  errors.value.confirm_password = 'Passwords do not match.';
                  hasError = true;
              }
              break;
      }
      return !hasError;
  };
  
  const validateAllFields = async (fields) => {
      let isFormValid = true;
      for (const field of fields) {
          const isValid = await validateField(field);
          if (!isValid) isFormValid = false;
      }
      return isFormValid;
  };

  const completeProfile = async () => {
      const isValid = await validateAllFields(['name', 'username', 'new_password', 'confirm_password']);
      if (!isValid) return;
  
      isUpdatingProfile.value = true;
      message.value = '';
      try {
          const payload = {
              name: profileForm.value.name,
              username: profileForm.value.username,
              password: passwordForm.value.new_password,
          };
          const result = await apiRequest('https://slice-abcd.onrender.com/parent/update-profile', {
              method: 'PUT',
              body: JSON.stringify(payload)
          });
          message.value = result.message || 'Profile completed successfully!';
          messageType.value = 'success';
          await fetchProfile();
      } catch (err) {
          message.value = err.message;
          messageType.value = 'error';
      } finally {
          isUpdatingProfile.value = false;
      }
  };
  
  const updateExistingProfile = async () => {
      const isValid = await validateAllFields(['name']);
      if (!isValid) return;
  
      isUpdatingProfile.value = true;
      message.value = '';
      try {
          const payload = {
              name: profileForm.value.name,
          };
          
          const result = await apiRequest('https://slice-abcd.onrender.com/parent/update-profile', {
              method: 'PUT',
              body: JSON.stringify(payload)
          });
          
          message.value = result.message || 'Profile updated successfully!';
          messageType.value = 'success';
      } catch (err) {
          message.value = err.message;
          messageType.value = 'error';
      } finally {
          isUpdatingProfile.value = false;
      }
  };

  const openForgotPasswordModal = () => {
      passwordForm.value.email = profileForm.value.email;
      showForgotPasswordModal.value = true;
  };
  
  const closeForgotPasswordModal = () => {
      showForgotPasswordModal.value = false;
      setTimeout(() => {
          forgotPasswordStep.value = 1;
          modalMessage.value = '';
          messageType.value = '';
          passwordForm.value = { email: '', otp: '', new_password: '', confirm_password: '' };
      }, 300);
  };
  
  const sendResetOtp = async () => {
      if (!passwordForm.value.email) {
          modalMessage.value = "Please enter your email address.";
          messageType.value = 'error';
          return;
      }
      isChangingPassword.value = true;
      modalMessage.value = '';
      try {
          await apiRequest('https://slice-abcd.onrender.com/forgot-password', {
              method: 'POST',
              body: JSON.stringify({ email: passwordForm.value.email })
          });
          forgotPasswordStep.value = 2;
          modalMessage.value = 'OTP sent to your email!';
          messageType.value = 'success';
      } catch (err) {
          modalMessage.value = err.message;
          messageType.value = 'error';
      } finally {
          isChangingPassword.value = false;
      }
  };
  
  const verifyResetOtp = async () => {
      isChangingPassword.value = true;
      modalMessage.value = '';
      try {
          await apiRequest('https://slice-abcd.onrender.com/verify-otp', {
              method: 'POST',
              body: JSON.stringify({ email: passwordForm.value.email, otp: passwordForm.value.otp })
          });
          forgotPasswordStep.value = 3;
          modalMessage.value = '';
      } catch (err) {
          modalMessage.value = err.message;
          messageType.value = 'error';
      } finally {
          isChangingPassword.value = false;
      }
  };
  
  const setNewPassword = async () => {
      if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
          modalMessage.value = "Passwords do not match.";
          messageType.value = 'error';
          return;
      }
      isChangingPassword.value = true;
      modalMessage.value = '';
      try {
          const result = await apiRequest('https://slice-abcd.onrender.com/set-password', {
              method: 'POST',
              body: JSON.stringify({
                  email: passwordForm.value.email,
                  new_password: passwordForm.value.new_password
              })
          });
          modalMessage.value = result.message || 'Password reset successfully!';
          messageType.value = 'success';
          setTimeout(closeForgotPasswordModal, 2000);
      } catch (err) {
          modalMessage.value = err.message;
          messageType.value = 'error';
      } finally {
          isChangingPassword.value = false;
      }
  };
  </script>
  
  <style scoped>
  .profile-setup-container {
      max-width: 900px;
      margin: auto;
  }
  
  .btn-primary-custom {
      background-color: #756bdb;
      border-color: #756bdb;
      color: #fff;
      transition: background-color 0.2s ease, border-color 0.2s ease;
  }
  
  .btn-primary-custom:hover {
      background-color: #5a50a3;
      border-color: #5a50a3;
  }
  
  .btn-secondary-custom {
      background-color: #6c757d;
      border-color: #6c757d;
      color: #fff;
  }
  
  .text-purple {
      color: #756bdb !important;
  }
  
  .invalid-feedback {
      font-size: 0.875em;
  }
  
.modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1050;
  }
  
.modal-content {
    position: relative;
    background: #fff;
    padding: 2rem;
    border-radius: 14px;
    width: 90%;
    max-width: 400px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
    animation: pop-in 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  }
  
  @keyframes pop-in {
    from {
      transform: scale(0.9);
      opacity: 0;
    }
    to {
      transform: scale(1);
      opacity: 1;
    }
  }
  
  .modal-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #756bdb;
    margin-bottom: 1rem;
  }
  
  .modal-close {
    position: absolute;
    top: 10px;
    right: 20px;
    font-size: 2rem;
    color: #aaa;
    cursor: pointer;
    font-weight: bold;
    transition: color 0.2s ease;
    line-height: 1;
  }
  
  .modal-close:hover {
    color: #756bdb;
  }
  
  .modal-fade-enter-active,
  .modal-fade-leave-active {
    transition: opacity 0.3s ease;
  }
  
  .modal-fade-enter-from,
  .modal-fade-leave-to {
    opacity: 0;
  }
  </style>
  