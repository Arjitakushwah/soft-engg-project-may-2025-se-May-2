<template>
  <div class="profile-setup-container container py-4">
    <!-- Title changes based on profile status -->
    <h2 class="mb-4 fw-bold">{{ isProfileComplete ? 'Edit Your Profile' : 'Complete Your Profile' }}</h2>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary-custom" role="status">
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
              <div v-if="isCheckingUsername" class="spinner-border spinner-border-sm text-secondary position-absolute" style="top: 42px; right: 12px;" role="status">
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
              <span v-if="isUpdatingProfile" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              <span v-else>Save Changes</span>
            </button>
          </form>
        </div>
      </div>

      <!-- Section 2: Change Password -->
      <div class="col-lg-6">
        <div class="card shadow-sm p-4 h-100">
          <h4 class="card-title mb-4">Change Password</h4>
          <form @submit.prevent="changePassword" novalidate>
            <div class="mb-3">
              <label for="currentPassword" class="form-label">Current Password</label>
              <input type="password" id="currentPassword" class="form-control" v-model="passwordForm.current_password" @input="validateField('current_password')" />
               <div v-if="errors.current_password" class="invalid-feedback d-block">{{ errors.current_password }}</div>
            </div>
            <div class="mb-3">
              <label for="newPassword" class="form-label">New Password</label>
              <input type="password" id="newPassword" class="form-control" v-model="passwordForm.new_password" @input="validateField('new_password')" />
              <div v-if="errors.new_password" class="invalid-feedback d-block">{{ errors.new_password }}</div>
            </div>
            <div class="mb-3">
              <label for="confirmPassword" class="form-label">Confirm New Password</label>
              <input type="password" id="confirmPassword" class="form-control" v-model="passwordForm.confirm_password" @input="validateField('confirm_password')" />
              <div v-if="errors.confirm_password" class="invalid-feedback d-block">{{ errors.confirm_password }}</div>
            </div>
            <button type="submit" class="btn btn-secondary-custom w-100 mt-3" :disabled="isChangingPassword">
              <span v-if="isChangingPassword" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              <span v-else>Change Password</span>
            </button>
          </form>
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
           <div v-if="isCheckingUsername" class="spinner-border spinner-border-sm text-secondary position-absolute" style="top: 42px; right: 12px;" role="status">
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

    <!-- Success/Error Message -->
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
const passwordForm = ref({ current_password: '', new_password: '', confirm_password: '' });
const errors = ref({});
const message = ref('');
const messageType = ref('');
const isLoading = ref(true);
const isUpdatingProfile = ref(false);
const isChangingPassword = ref(false);
const isCheckingUsername = ref(false);
const isProfileComplete = ref(false);
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
        
        // Determine which view to show. If username and name are set, profile is complete.
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

    switch (fieldName) {
        case 'name':
            if (!profileForm.value.name) errors.value.name = 'Full Name is required.';
            break;

        case 'username':
            if (!profileForm.value.username) {
                errors.value.username = 'Username is required.';
                break;
            }
            if (profileForm.value.username !== originalUsername.value) {
                isCheckingUsername.value = true;
                try {
                    const response = await fetch(`http://localhost:5000/check-username?username=${profileForm.value.username}`);
                    const result = await response.json();
                    if (response.ok && !result.available) {
                        errors.value.username = 'This username is already taken.';
                    }
                } catch (err) {
                    console.error("Username check failed:", err);
                } finally {
                    isCheckingUsername.value = false;
                }
            }
            break;

        case 'current_password':
             if (!passwordForm.value.current_password) errors.value.current_password = 'Current password is required.';
            break;

        case 'new_password':
            const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
            if (!passwordForm.value.new_password) {
                errors.value.new_password = 'New password is required.';
            } else if (!passwordRegex.test(passwordForm.value.new_password)) {
                errors.value.new_password = 'Password must be 8+ characters with uppercase, lowercase, and a number.';
            }
            if (passwordForm.value.confirm_password) {
                validateField('confirm_password');
            }
            break;

        case 'confirm_password':
            if (!passwordForm.value.new_password) {
                // No validation needed if new password isn't entered
            } else if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
                errors.value.confirm_password = 'Passwords do not match.';
            }
            break;
    }
};

// For completing the profile for the first time
const completeProfile = async () => {
    validateField('name');
    validateField('username');
    validateField('new_password');
    validateField('confirm_password');
    if (Object.values(errors.value).some(err => err)) return;
    
    isUpdatingProfile.value = true;
    message.value = '';
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('http://localhost:5000/parent/update-profile', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify({
                name: profileForm.value.name,
                username: profileForm.value.username,
                password: passwordForm.value.new_password
            })
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'Failed to set up profile.');
        
        message.value = 'Profile setup successful! Redirecting...';
        messageType.value = 'success';
        localStorage.setItem('username', profileForm.value.username);
        setTimeout(() => router.push('/parent/home'), 2000);
    } catch (err) {
        message.value = err.message;
        messageType.value = 'error';
    } finally {
        isUpdatingProfile.value = false;
    }
};

// For updating an already existing profile
const updateExistingProfile = async () => {
    validateField('name');
    validateField('username');
    if (errors.value.name || errors.value.username) return;
    
    isUpdatingProfile.value = true;
    message.value = '';
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('http://localhost:5000/parent/profile-update', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify({
                name: profileForm.value.name,
                username: profileForm.value.username
            })
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'Failed to update profile.');
        
        message.value = 'Profile details updated successfully!';
        messageType.value = 'success';
        localStorage.setItem('username', profileForm.value.username);
        originalUsername.value = profileForm.value.username;
    } catch (err) {
        message.value = err.message;
        messageType.value = 'error';
    } finally {
        isUpdatingProfile.value = false;
    }
};

const changePassword = async () => {
    validateField('current_password');
    validateField('new_password');
    validateField('confirm_password');
    if (Object.values(errors.value).some(err => err)) return;

    isChangingPassword.value = true;
    message.value = '';
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('http://localhost:5000/parent/password/change', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify(passwordForm.value)
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'Failed to change password.');

        message.value = 'Password changed successfully!';
        messageType.value = 'success';
        passwordForm.value = { current_password: '', new_password: '', confirm_password: '' };
    } catch (err) {
        message.value = err.message;
        messageType.value = 'error';
    } finally {
        isChangingPassword.value = false;
    }
};
</script>

<style scoped>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css");

.profile-setup-container {
  max-width: 1100px;
  font-family: 'Comic Neue', cursive;
}

h2 {
  color: #756bdb;
  border-left: 6px solid #756bdb;
  padding-left: 12px;
}

.card {
  border: none;
  border-radius: 1rem;
  background-color: #f8f9fa;
}

.card-title {
    color: #343a40;
    font-family: 'Fredoka One', cursive;
}

.form-label {
    font-weight: 600;
    color: #495057;
}

.form-control {
    border-radius: 0.75rem;
}

.form-control:disabled {
    background-color: #e9ecef;
}

.btn-primary-custom, .text-primary-custom {
    background-color: #756bdb;
    border-color: #756bdb;
    color: white;
}

.btn-primary-custom {
    font-family: 'Fredoka One', cursive;
    border-radius: 30px;
    padding: 10px 20px;
    transition: all 0.3s ease;
}

.btn-primary-custom:hover {
    background-color: #756bdb;
    border-color: #756bdb;
    transform: translateY(-2px);
}

.btn-secondary-custom {
    background-color: #6c757d;
    border-color: #6c757d;
    color: white;
    font-family: 'Fredoka One', cursive;
    border-radius: 30px;
    padding: 10px 20px;
    transition: all 0.3s ease;
}

.btn-secondary-custom:hover {
    background-color: #5a6268;
    border-color: #545b62;
    transform: translateY(-2px);
}
</style>
