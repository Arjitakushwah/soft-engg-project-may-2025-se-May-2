<template>
    <div class="parent-home-container">
      <div v-if="isLoading" class="centered-message">
        <div class="spinner-border text-purple" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2 text-muted">Loading dashboard...</p>
      </div>
  
      <div v-else-if="isProfileIncomplete" class="centered-message bg-light p-4 p-md-5 rounded-3">
          <i class="bi bi-person-badge display-4 text-warning mb-3"></i>
          <h4 class="fw-semibold">Welcome!</h4>
          <p class="text-muted">Your profile is not yet complete. Please set up your details to continue.</p>
          <router-link to="/parent/edit-profile" class="btn btn-warning mt-2">
              <i class="bi bi-pencil-square me-2"></i>Complete Profile
          </router-link>
      </div>
  
      <div v-else-if="noChildrenFound" class="centered-message bg-light p-4 p-md-5 rounded-3">
          <i class="bi bi-person-plus-fill display-4 text-primary mb-3"></i>
          <h4 class="fw-semibold">Welcome, {{ parentName }}!</h4>
          <p class="text-muted">To get started, please add a child profile to your account.</p>
          <router-link to="/parent/add-child" class="btn btn-primary-custom mt-2">
              <i class="bi bi-plus-circle me-2"></i>Add Child Profile
          </router-link>
      </div>
  
      <div v-else>
        <h2 class="title">Welcome, {{ parentName }}</h2>
        <p class="subtitle">Use the sidebar to manage your child’s learning activities.</p>
  
        <div class="child-cards">
          <h3 class="section-title">Your Children</h3>
          <div class="card-grid">
            <div v-for="child in children" :key="child.id" class="child-card">
              <h4>{{ child.name }}</h4>
              <p><strong>Age:</strong> {{ child.age }}</p>
              <p><strong>Gender:</strong> {{ child.gender }}</p>
              <div class="btn-group mt-2">
                <button class="btn btn-info btn-sm" @click="viewChildProfile(child.id)">
                  View
                </button>
                <button class="btn btn-primary btn-sm" @click="openEditModal(child)">
                  Update
                </button>
                <button class="btn btn-warning btn-sm" @click="openForgotCredentialsModal(child)">
                  Credentials
                </button>
              </div>
            </div>
          </div>
        </div>
  
        <transition name="modal-fade">
          <div v-if="showModal" class="modal-backdrop" @click.self="showModal = false">
            <div class="modal-content">
              <span class="modal-close" @click="showModal = false">×</span>
              <h4 class="modal-title">{{ profile.name }}'s Dashboard</h4>
              <div>
                <div class="profile-stats-grid">
                  <div class="stat-item">
                    <span class="stat-label">Current Streak</span>
                    <span class="stat-value streak">{{ profile.current_streak ?? 'N/A' }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Journals Written</span>
                    <span class="stat-value journals">{{ profile.total_journals_written ?? 'N/A' }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Stories Read</span>
                    <span class="stat-value stories">{{ profile.total_stories_read ?? 'N/A' }}</span>
                  </div>
                </div>
                <div class="badges-section">
                  <h5 class="badges-title">Badges Earned</h5>
                  <div v-if="profile.badges && profile.badges.length > 0" class="badge-list">
                    <span v-for="badge in profile.badges" :key="badge.name" class="badge-pill">{{ badge.name }}</span>
                  </div>
                  <p v-else class="text-muted small text-center">No badges earned yet.</p>
                </div>
                <button class="btn btn-success mt-4 w-100" @click="downloadChildReport(profile.id)" :disabled="isDownloading">
                  <span v-if="isDownloading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                  <span v-else><i class="bi bi-download me-2"></i>Download Weekly Report</span>
                </button>
              </div>
            </div>
          </div>
        </transition>
        
        <transition name="modal-fade">
          <div v-if="showEditModal" class="modal-backdrop" @click.self="showEditModal = false">
            <div class="modal-content">
              <span class="modal-close" @click="showEditModal = false">×</span>
              <h4 class="modal-title">Update {{ editingChild.name }}'s Profile</h4>
              <form @submit.prevent="updateChildProfile" class="mt-3">
                <div class="form-group">
                  <label>Name</label>
                  <input v-model="editingChild.name" type="text" class="form-control" required />
                </div>
                <div class="form-group">
                  <label>Age</label>
                  <input v-model="editingChild.age" type="number" class="form-control" required min="1" />
                </div>
                <div class="form-group">
                  <label>Gender</label>
                  <select v-model="editingChild.gender" class="form-control" required>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
                <p v-if="editErrorMessage" class="text-danger mt-2 small">{{ editErrorMessage }}</p>
                <button type="submit" class="btn btn-primary-custom mt-3 w-100" :disabled="isUpdating">
                  <span v-if="isUpdating" class="spinner-border spinner-border-sm"></span>
                  <span v-else>Save Changes</span>
                </button>
              </form>
            </div>
          </div>
        </transition>
  
        <transition name="modal-fade">
          <div v-if="showForgotCredentialsModal" class="modal-backdrop" @click.self="closeForgotCredentialsModal">
            <div class="modal-content text-center">
              <span class="modal-close" @click="closeForgotCredentialsModal">×</span>
              <h4 class="modal-title">{{ selectedChildForCredentials.name }}'s Credentials</h4>
              <div v-if="credentialStep === 1">
                <div class="alert alert-light mt-3">
                  <p class="mb-1"><strong>Username:</strong></p>
                  <p class="h5">{{ selectedChildForCredentials.username }}</p>
                </div>
                <p class="text-muted small mt-3">Click below to send a password reset OTP to your registered email.</p>
                <button class="btn btn-danger mt-2 w-100" @click="sendChildResetOtp" :disabled="isResettingPassword">
                  <span v-if="isResettingPassword" class="spinner-border spinner-border-sm"></span>
                  <span v-else>Send Reset OTP</span>
                </button>
              </div>
              <form v-if="credentialStep === 2" @submit.prevent="verifyChildResetOtp" class="text-start mt-3">
                <p class="text-muted text-center small">An OTP has been sent to your parent email.</p>
                <div class="form-group">
                  <label>OTP Code</label>
                  <input v-model="otp" type="text" class="form-control" required maxlength="6" />
                </div>
                <p v-if="resetErrorMessage" class="text-danger mt-2 small">{{ resetErrorMessage }}</p>
                <button type="submit" class="btn btn-primary-custom mt-3 w-100" :disabled="isResettingPassword">
                  <span v-if="isResettingPassword" class="spinner-border spinner-border-sm"></span>
                  <span v-else>Verify OTP</span>
                </button>
              </form>
              <form v-if="credentialStep === 3" @submit.prevent="resetChildPassword" class="text-start mt-3">
                <p class="text-success text-center small">✓ OTP Verified! Set a new password for your child.</p>
                <div class="form-group">
                  <label>New Password</label>
                  <input v-model="newPassword" type="password" class="form-control" required />
                </div>
                <div class="form-group">
                  <label>Confirm New Password</label>
                  <input v-model="confirmNewPassword" type="password" class="form-control" required />
                </div>
                <p v-if="resetErrorMessage" class="text-danger mt-2 small">{{ resetErrorMessage }}</p>
                <button type="submit" class="btn btn-danger mt-3 w-100" :disabled="isResettingPassword">
                  <span v-if="isResettingPassword" class="spinner-border spinner-border-sm"></span>
                  <span v-else>Confirm Reset</span>
                </button>
              </form>
              <div v-if="credentialStep === 4" class="alert alert-success mt-3">
                <i class="bi bi-check-circle-fill h4"></i>
                <p class="mt-2 mb-0">{{ resetSuccessMessage }}</p>
              </div>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  const parentName = ref('Parent');
  const children = ref([]);
  const profile = ref({});
  const isLoading = ref(true);
  const noChildrenFound = ref(false);
  const isProfileIncomplete = ref(false);
  const isDownloading = ref(false);
  const showModal = ref(false);
  const showEditModal = ref(false);
  const editingChild = ref(null);
  const isUpdating = ref(false);
  const editErrorMessage = ref('');
  const showForgotCredentialsModal = ref(false);
  const selectedChildForCredentials = ref(null);
  const isResettingPassword = ref(false);
  const resetSuccessMessage = ref('');
  const resetErrorMessage = ref('');
  const credentialStep = ref(1);
  const otp = ref('');
  const newPassword = ref('');
  const confirmNewPassword = ref('');
  
  const apiRequest = async (url, options) => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      router.push('/login');
      throw new Error('No authentication token found.');
    }
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers,
    };
    const response = await fetch(url, { ...options, headers });
    if (!response.ok) {
      // Handle the 404 for 'no children' gracefully without throwing a fatal error
      if (response.status === 404 && url.includes('/parent/children')) {
        return { children: [] }; // Return a default empty state
      }
      const errorData = await response.json().catch(() => ({ error: 'An unknown error occurred' }));
      throw new Error(errorData.error || `Request failed with status ${response.status}`);
    }
    if (response.headers.get('Content-Type')?.includes('application/pdf')) {
      return response.blob();
    }
    return response.json();
  };
  
  const fetchDashboardData = async () => {
    isLoading.value = true;
    noChildrenFound.value = false;
    isProfileIncomplete.value = false;
  
    try {
      const parentData = await apiRequest('http://localhost:5000/parent_dashboard', { method: 'GET' });
  
      if (!parentData || !parentData.name) {
        console.log("Parent profile is incomplete. Displaying setup message.");
        isProfileIncomplete.value = true;
        isLoading.value = false;
        return;
      }
  
      parentName.value = parentData.name;
  
      const childrenData = await apiRequest('http://localhost:5000/parent/children', { method: 'GET' });
      const childList = childrenData.children || [];
  
      if (Array.isArray(childList) && childList.length > 0) {
        children.value = childList;
      } else {
        noChildrenFound.value = true;
      }
  
    } catch (error) {
      console.error("Error fetching dashboard data:", error);
      isProfileIncomplete.value = true; // Fallback to profile incomplete on critical errors
    } finally {
      isLoading.value = false;
    }
  };
  
  onMounted(fetchDashboardData);
  
  const confirmDeleteChild = (child) => {
    if (window.confirm(`Are you sure you want to delete the profile for ${child.name}? This action cannot be undone.`)) {
      deleteChildProfile(child.id);
    }
  };
  
  
  const viewChildProfile = (childId) => {
    const selectedChild = children.value.find(child => child.id === childId);
    if (!selectedChild) {
      alert('Error: Could not find child details.');
      return;
    }
    profile.value = selectedChild;
    showModal.value = true;
  };
  
  const openEditModal = (child) => {
    editingChild.value = { ...child };
    showEditModal.value = true;
  };
  
  const updateChildProfile = async () => {
    if (!editingChild.value) return;
    isUpdating.value = true;
    editErrorMessage.value = '';
    try {
      const payload = {
        child_id: editingChild.value.id,
        name: editingChild.value.name,
        age: parseInt(editingChild.value.age, 10),
        gender: editingChild.value.gender
      };
      await apiRequest('http://localhost:5000/parent/child/profile/update', {
        method: 'PUT',
        body: JSON.stringify(payload)
      });
      showEditModal.value = false;
      await fetchDashboardData();
      alert('Profile updated successfully!');
    } catch (err) {
      editErrorMessage.value = err.message;
    } finally {
      isUpdating.value = false;
    }
  };
  
  const openForgotCredentialsModal = (child) => {
    selectedChildForCredentials.value = child;
    showForgotCredentialsModal.value = true;
  };
  
  const closeForgotCredentialsModal = () => {
    showForgotCredentialsModal.value = false;
    setTimeout(() => {
      credentialStep.value = 1;
      resetSuccessMessage.value = '';
      resetErrorMessage.value = '';
      otp.value = '';
      newPassword.value = '';
      confirmNewPassword.value = '';
    }, 500);
  };
  
  const sendChildResetOtp = async () => {
    isResettingPassword.value = true;
    resetErrorMessage.value = '';
    try {
      await apiRequest('http://localhost:5000/forgot-password-child', {
        method: 'POST',
        body: JSON.stringify({ username: selectedChildForCredentials.value.username })
      });
      credentialStep.value = 2;
    } catch (err) {
      resetErrorMessage.value = err.message;
    } finally {
      isResettingPassword.value = false;
    }
  };
  
  const verifyChildResetOtp = async () => {
    if (!otp.value) {
      resetErrorMessage.value = "Please enter the OTP.";
      return;
    }
    isResettingPassword.value = true;
    resetErrorMessage.value = '';
    try {
      await apiRequest('http://localhost:5000/verify-otp-child', {
        method: 'POST',
        body: JSON.stringify({
          username: selectedChildForCredentials.value.username,
          otp: otp.value
        })
      });
      credentialStep.value = 3;
    } catch (err) {
      resetErrorMessage.value = err.message;
    } finally {
      isResettingPassword.value = false;
    }
  };
  
  const resetChildPassword = async () => {
    resetErrorMessage.value = '';
    if (newPassword.value !== confirmNewPassword.value) {
      resetErrorMessage.value = "Passwords do not match.";
      return;
    }
    if (newPassword.value.length < 6) {
      resetErrorMessage.value = "Password must be at least 6 characters.";
      return;
    }
  
    isResettingPassword.value = true;
    try {
      const data = await apiRequest(`http://localhost:5000/set-password-child`, {
        method: 'POST',
        body: JSON.stringify({
          new_password: newPassword.value,
          username: selectedChildForCredentials.value.username
        })
      });
      resetSuccessMessage.value = data.message;
      credentialStep.value = 4;
    } catch (err) {
      console.error('Password reset error:', err);
      resetErrorMessage.value = err.message || 'Could not reset password.';
    } finally {
      isResettingPassword.value = false;
    }
  };
  
  const downloadChildReport = async (childId) => {
    isDownloading.value = true;
    const summaryRange = 'weekly';
    try {
      const url = `http://localhost:5000/parent/child-analysis?child_id=${childId}&summary_range=${summaryRange}`;
      const blob = await apiRequest(url, { method: 'POST' });
  
      const fileUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = fileUrl;
      a.download = `child_analysis_report_${childId}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(fileUrl);
    } catch (error) {
      console.error('Download error:', error);
      alert(error.message || 'Error downloading report');
    } finally {
      isDownloading.value = false;
    }
  };
  </script>
  
  <style scoped>
  @import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css");
  
  .parent-home-container {
    font-family: 'Comic Neue', cursive;
    padding: 2rem;
    background-color: #fff;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
    text-align: center;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
  }
  
  .centered-message {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      flex-grow: 1;
  }
  
  .bg-light {
      background-color: #f8f9fa !important;
  }
  
  .rounded-3 {
      border-radius: 1rem !important;
  }
  
  .text-primary {
      color: #756bdb !important;
  }
  
  .text-purple {
      color: #756bdb !important;
  }
  
  .btn-primary-custom {
      background-color: #756bdb;
      color: white;
      border-radius: 25px;
      padding: 10px 25px;
      font-weight: 500;
      transition: all 0.3s ease;
      border: none;
      text-decoration: none;
  }
  
  .btn-primary-custom:hover {
      background-color: #5145ce;
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(117, 107, 219, 0.3);
  }
  
  .title {
    font-size: 2.2rem;
    color: #5A4FCF;
    margin-bottom: 1rem;
    font-family: 'Fredoka One', cursive;
  }
  
  .subtitle {
    font-size: 1.1rem;
    color: #666;
    margin-bottom: 2rem;
  }
  
  .child-cards {
    text-align: left;
    margin-top: 2rem;
  }
  
  .section-title {
    font-weight: bold;
    margin-bottom: 1rem;
    color: #333;
  }
  
  .card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.5rem;
    margin-top: 1rem;
  }
  
  .child-card {
    background-color: #E6E6FA;
    padding: 1.2rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    text-align: center;
  }
  
  .child-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
  }
  
  .child-card h4 {
    color: #5A4FCF;
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }
  
  .child-card p {
    margin: 0.3rem 0;
    font-size: 1rem;
    color: #555;
  }
  
  .btn-group {
      display: flex;
      gap: 0.5rem;
      justify-content: center;
      flex-wrap: wrap;
  }
  
  /* Modal Styles */
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
  
  .modal-content {
    position: relative;
    background: #fff;
    padding: 2rem;
    border-radius: 14px;
    width: 90%;
    max-width: 450px;
    text-align: left;
    font-family: 'Comic Neue', cursive;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
    animation: pop-in 0.3s ease;
  }
  
  .modal-title {
    font-size: 1.4rem;
    color: #756bdb;
    margin-bottom: 1.5rem;
    text-align: center;
  }
  
  .modal-content .form-group {
      margin-bottom: 1rem;
  }
  
  .modal-content .form-control {
      width: 100%;
      padding: 0.5rem;
      border-radius: 6px;
      border: 1px solid #ccc;
  }
  
  /* Profile Modal Specific Styles */
  .profile-stats-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1rem;
      text-align: center;
      margin-bottom: 1.5rem;
  }
  .stat-item {
      background-color: #f8f9fa;
      padding: 1rem;
      border-radius: 8px;
  }
  .stat-label {
      display: block;
      font-size: 0.85rem;
      color: #6c757d;
      margin-bottom: 0.25rem;
  }
  .stat-value {
      font-size: 2rem;
      font-weight: bold;
      line-height: 1;
  }
  .stat-value.streak { color: #f59e0b; }
  .stat-value.journals { color: #f65c7d; }
  .stat-value.stories { color: #10b981; }
  
  .badges-section {
      margin-top: 1.5rem;
      padding-top: 1.5rem;
      border-top: 1px solid #e9ecef;
  }
  .badges-title {
      text-align: center;
      font-size: 1.1rem;
      color: #495057;
      margin-bottom: 1rem;
  }
  .badge-list {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      justify-content: center;
  }
  .badge-pill {
      background-color: #e9ecef;
      color: #495057;
      padding: 0.4rem 0.8rem;
      border-radius: 20px;
      font-size: 0.9rem;
  }
  
  
  /* Animations */
  @keyframes pop-in {
    from {
      opacity: 0;
      transform: scale(0.85);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
  
  .modal-fade-enter-active,
  .modal-fade-leave-active {
    transition: opacity 0.3s ease;
  }
  
  .modal-fade-enter-from,
  .modal-fade-leave-to {
    opacity: 0;
  }
  
  .btn-success {
    background-color: #28a745;
    border: none;
    color: white;
    padding: 10px 16px;
    font-size: 0.95rem;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }
  
  .btn-success:hover {
    background-color: #218838;
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
  </style>