<template>
  <div class="parent-home-container">
    <!-- Loading State -->
    <div v-if="isLoading" class="centered-message">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2 text-muted">Loading dashboard...</p>
    </div>

    <!-- No Children Found State -->
    <div v-else-if="noChildrenFound" class="centered-message bg-light p-4 p-md-5 rounded-3">
        <i class="bi bi-person-plus-fill display-4 text-primary mb-3"></i>
        <h4 class="fw-semibold">Welcome, {{ parentName }}!</h4>
        <p class="text-muted">To get started, please add a child profile to your account.</p>
        <router-link to="/parent/add_child" class="btn btn-primary-custom mt-2">
            <i class="bi bi-plus-circle me-2"></i>Add Child Profile
        </router-link>
    </div>

    <!-- Main Content -->
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
              <!-- Action Buttons -->
              <div class="btn-group mt-2">
                <button class="btn btn-info btn-sm" @click="fetchChildProfile(child.id)">
                  View Profile
                </button>
                <button class="btn btn-secondary btn-sm" @click="openEditModal(child)">
                  Edit Profile
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- View Profile Modal -->
        <transition name="modal-fade">
          <div v-if="showModal" class="modal-backdrop" @click.self="showModal = false">
            <div class="modal-content">
              <span class="modal-close" @click="showModal = false">×</span>
              <h4 class="modal-title">{{ profile.name }}'s Profile</h4>
              <p><strong>Age:</strong> {{ profile.age }}</p>
              <p><strong>Gender:</strong> {{ profile.gender }}</p>
              <p><strong>Streak:</strong> {{ profile.streak }}</p>
              <p><strong>Longest Streak:</strong> {{ profile.longest_streak }}</p>
              <p><strong>Badges:</strong> {{ profile.badges }}</p>
              <button class="btn btn-success mt-3" @click="downloadChildReport(profile.id)" :disabled="isDownloading">
                <span v-if="isDownloading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                <span v-else>Download Weekly Report</span>
              </button>
            </div>
          </div>
        </transition>

        <!-- Edit Profile Modal -->
        <transition name="modal-fade">
            <div v-if="showEditModal" class="modal-backdrop" @click.self="showEditModal = false">
                <div class="modal-content">
                    <span class="modal-close" @click="showEditModal = false">×</span>
                    <h4 class="modal-title">Edit {{ editingChild.name }}'s Profile</h4>
                    <form @submit.prevent="updateChildProfile">
                        <div class="form-group">
                            <label>Name</label>
                            <input v-model="editingChild.name" type="text" class="form-control" required />
                        </div>
                        <div class="form-group">
                            <label>Age</label>
                            <input v-model="editingChild.age" type="number" min="1" class="form-control" required />
                        </div>
                        <div class="form-group">
                            <label>Gender</label>
                            <select v-model="editingChild.gender" class="form-control" required>
                                <option value="male">Male</option>
                                <option value="female">Female</option>
                                <option value="other">Other</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary mt-3 w-100" :disabled="isUpdating">
                            <span v-if="isUpdating" class="spinner-border spinner-border-sm"></span>
                            <span v-else>Save Changes</span>
                        </button>
                    </form>
                </div>
            </div>
        </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const parentName = ref('Parent')
const children = ref([])
const profile = ref({})
const isLoading = ref(true)
const noChildrenFound = ref(false)
const isDownloading = ref(false)

// State for modals
const showModal = ref(false)
const showEditModal = ref(false)
const editingChild = ref(null)
const isUpdating = ref(false)

const fetchChildrenData = async () => {
    isLoading.value = true;
    noChildrenFound.value = false;
    try {
        const token = localStorage.getItem('access_token')
        if (!token) {
            router.push('/login');
            return;
        };

        const res = await fetch('http://localhost:5000/parent/children', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (res.ok) {
            const data = await res.json();
            const childList = data.children || data;
            if (Array.isArray(childList) && childList.length > 0) {
                children.value = childList;
            } else {
                noChildrenFound.value = true;
            }
        } else {
            console.error("Failed to fetch children:", await res.text());
            noChildrenFound.value = true;
        }
    } catch (error) {
        console.error("Error fetching children:", error);
        noChildrenFound.value = true;
    } finally {
        isLoading.value = false;
    }

    try {
        const parentData = JSON.parse(localStorage.getItem('parent'));
        if (parentData?.name) parentName.value = parentData.name;
    } catch (e) {
        console.error("Could not parse parent data from localStorage", e);
    }
};

onMounted(fetchChildrenData);

const fetchChildProfile = async (childId) => {
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(`http://localhost:5000/parent/child/${childId}/profile`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await res.json()
    if (res.ok) {
      profile.value = data.profile
      showModal.value = true
    } else {
      alert(data.error || 'Failed to fetch profile')
    }
  } catch (err) {
    alert('Network error')
  }
}

const openEditModal = (child) => {
    // Create a copy to avoid mutating the original object until save
    editingChild.value = { ...child };
    showEditModal.value = true;
};

const updateChildProfile = async () => {
    if (!editingChild.value) return;
    isUpdating.value = true;
    const token = localStorage.getItem('access_token');
    try {
        // Assuming an endpoint structure like this. You may need to create it.
        const res = await fetch(`http://localhost:5000/child/profile/update`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                // The API expects the child ID to be identified by the token
                name: editingChild.value.name,
                age: editingChild.value.age,
                gender: editingChild.value.gender
            })
        });
        const data = await res.json();
        if (!res.ok) {
            throw new Error(data.error || 'Failed to update profile');
        }
        // Success
        showEditModal.value = false;
        await fetchChildrenData(); // Refresh the list to show updated data
        alert('Profile updated successfully!');
    } catch (err) {
        console.error('Update error:', err);
        alert(err.message || 'Could not update profile.');
    } finally {
        isUpdating.value = false;
    }
};

const downloadChildReport = async (childId) => {
  isDownloading.value = true;
  const token = localStorage.getItem('access_token');
  const summaryRange = 'weekly';

  try {
    const url = `http://localhost:5000/parent/child-analysis?child_id=${childId}&summary_range=${summaryRange}`;

    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`Error: ${response.status} - ${errText}`);
    }

    const blob = await response.blob();
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
    color: #ff6a88 !important;
}

.btn-primary-custom {
    background-color: #ff6a88;
    color: white;
    border-radius: 25px;
    padding: 10px 25px;
    font-weight: 500;
    transition: all 0.3s ease;
    border: none;
    text-decoration: none;
}

.btn-primary-custom:hover {
    background-color: #e65c7a;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(255, 106, 136, 0.3);
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
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
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
  max-width: 400px;
  text-align: left;
  font-family: 'Comic Neue', cursive;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
  animation: pop-in 0.3s ease;
}

.modal-title {
  font-size: 1.4rem;
  color: #ff6a88;
  margin-bottom: 1rem;
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
  padding: 8px 16px;
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
  color: #ff6a88;
}
</style>
