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
              <input type="text" id="username" class="form-control" v-model.trim="profileForm.username" @input="handleInput('username')" />
              <div v-if="isCheckingUsername" class="spinner-border spinner-border-sm text-purple position-absolute" style="top: 42px; right: 12px;" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <div v-if="errors.username" class="invalid-feedback d-block">{{ errors.username }}</div>
            </div>
            <div class="mb-3">
              <label for="email" class="form-label">Email</label>
              <input type="email" id="email" class="form-control" v-model="profileForm.email" disabled readonly />
              <div class="form-text">Your email address cannot be changed.</div>
            </div>
            <button type="submit" class="btn btn-primary-custom w-100 mt-3" :disabled="isUpdatingProfile">
              <span v-if="isUpdatingProfile" class="spinner-border spinner-border-sm text-purple" role="status" aria-hidden="true"></span>
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
          <button class="btn btn-secondary-custom w-100" @click="showForgotPasswordModal = true">
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
          <span v-if="isUpdatingProfile" class="spinner-border spinner-border-sm text-purple" role="status" aria-hidden="true"></span>
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
                    <p class="text-muted text-center small">An OTP will be sent to your registered email: <strong>{{ profileForm.email }}</strong></p>
                    <button type="submit" class="btn btn-primary-custom w-100" :disabled="isChangingPassword">
                        <span v-if="isChangingPassword" class="spinner-border spinner-border-sm text-purple"></span>
                        <span v-else>Send OTP</span>
                    </button>
                </form>

                <!-- Step 2: Verify OTP -->
                <form v-if="forgotPasswordStep === 2" @submit.prevent="verifyResetOtp" class="mt-3">
                    <p class="text-muted text-center small">Enter the OTP sent to your email.</p>
                    <div class="form-group">
                        <label>OTP Code</label>
                        <input v-model="passwordForm.otp" type="text" class="form-control" required maxlength="6" />
                    </div>
                    <button type="submit" class="btn btn-primary-custom w-100" :disabled="isChangingPassword">
                        <span v-if="isChangingPassword" class="spinner-border spinner-border-sm text-purple"></span>
                        <span v-else>Verify OTP</span>
                    </button>
                </form>

                <!-- Step 3: Set New Password -->
                <form v-if="forgotPasswordStep === 3" @submit.prevent="setNewPassword" class="mt-3">
                    <p class="text-success text-center small">✓ OTP Verified!</p>
                    <div class="form-group">
                        <label>New Password</label>
                        <input v-model="passwordForm.new_password" type="password" class="form-control" required />
                    </div>
                    <div class="form-group">
                        <label>Confirm New Password</label>
                        <input v-model="passwordForm.confirm_password" type="password" class="form-control" required />
                    </div>
                    <button type="submit" class="btn btn-danger w-100" :disabled="isChangingPassword">
                        <span v-if="isChangingPassword" class="spinner-border spinner-border-sm text-purple"></span>
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
const passwordForm = ref({ otp: '', new_password: '', confirm_password: '' });
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

const fetchProfile = async () => {
    isLoading.value = true;
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('http://localhost:5000/parent_dashboard', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'Could not fetch profile.');

        profileForm.value = {
            name: result.name,
            username: result.username,
            email: result.email
        };
        originalUsername.value = result.username;
        
        if (result.username && result.name) {
            isProfileComplete.value = true;
        }

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
    // ... (validation logic for name, username, passwords remains the same)
};

// ... (completeProfile and updateExistingProfile logic remains the same)

const closeForgotPasswordModal = () => {
    showForgotPasswordModal.value = false;
    setTimeout(() => {
        forgotPasswordStep.value = 1;
        modalMessage.value = '';
        passwordForm.value = { otp: '', new_password: '', confirm_password: '' };
    }, 300);
};

const sendResetOtp = async () => {
    isChangingPassword.value = true;
    modalMessage.value = '';
    try {
        const res = await fetch('http://localhost:5000/forgot-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: profileForm.value.email })
        });
        const result = await res.json();
        if (!res.ok) throw new Error(result.error || 'Failed to send OTP.');
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
        const res = await fetch('http://localhost:5000/verify-otp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: profileForm.value.email, otp: passwordForm.value.otp })
        });
        const result = await res.json();
        if (!res.ok || !result.success) throw new Error(result.message || 'Invalid OTP.');
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
        const res = await fetch('http://localhost:5000/set-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: profileForm.value.email,
                new_password: passwordForm.value.new_password
            })
        });
        const result = await res.json();
        if (!res.ok) throw new Error(result.error || 'Failed to reset password.');
        
        modalMessage.value = 'Password reset successfully!';
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
/* ... (all existing styles remain the same) ... */

.text-purple {
    color: #756bdb !important;
}
.modal-content {
  position: relative;
  background: #fff;
  padding: 2rem;
  border-radius: 14px;
  width: 90%;
  max-width: 400px;
  text-align: left;
  font-family: 'Comic Neue', cursive;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
  animation: pop-in 0.3s ease;
}

.modal-title {
  font-size: 1.4rem;
  color: #756bdb;
  margin-bottom: 1rem;
}

.modal-close {
  position: absolute;
  top: 1px;
  right: 16px;
  font-size: 2.5rem;
  color: #888;
  cursor: pointer;
  font-weight: bold;
  transition: color 0.2s ease;
}

.modal-close:hover {
  color: #756bdb;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
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
