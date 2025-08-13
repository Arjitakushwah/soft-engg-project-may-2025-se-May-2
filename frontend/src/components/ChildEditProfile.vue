<template>
  <div class="edit-profile-wrapper">
    <div class="edit-profile">
      <h2 class="form-title">Edit Child Profile</h2>
      <!-- Replaced the loading text with the Loader component -->
      <Loader v-if="loading" />
      
      <form v-else @submit.prevent="updateProfile">
        <!-- Name -->
        <div class="form-group">
          <label for="name">Name</label>
          <input id="name" v-model="form.name" type="text" placeholder="Enter name" required />
        </div>

        <!-- Age -->
        <div class="form-group">
          <label for="age">Age</label>
          <input id="age" v-model="form.age" type="number" min="1" placeholder="Enter age" required />
        </div>

        <!-- Gender -->
        <div class="form-group">
          <label for="gender">Gender</label>
          <select id="gender" v-model="form.gender" required>
            <option value="" disabled>Select gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
            <option value="prefer_not_to_say">Prefer not to say</option>
          </select>
        </div>

        <!-- Feedback Message -->
        <div v-if="message" :class="['message', messageType]">
          {{ message }}
        </div>

        <!-- Submit Button -->
        <button type="submit" :disabled="isSubmitting">
          <span v-if="isSubmitting">Saving...</span>
          <span v-else>Save Changes</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Loader from './Loader.vue'; // Import the Loader component

const router = useRouter();

// --- STATE MANAGEMENT ---
const form = ref({
  name: '',
  age: '',
  gender: ''
});

const loading = ref(true); // For initial data fetch
const isSubmitting = ref(false); // For form submission
const message = ref(''); // For user feedback
const messageType = ref(''); // 'success' or 'error'

// --- API & LOGIC ---

// 1. Fetch existing profile data when the component loads
async function fetchProfile() {
  loading.value = true;
  message.value = ''; // Clear previous messages
  try {
    const token = localStorage.getItem("access_token");
    // IMPORTANT: You need to create this GET endpoint in your Flask API
    const res = await fetch('http://localhost:5000/child_dashboard', {
      headers: { "Authorization": `Bearer ${token}` }
    });

    if (!res.ok) {
      throw new Error('Failed to fetch profile data.');
    }

    const data = await res.json();
    form.value.name = data.name;
    form.value.age = data.age;
    form.value.gender = data.gender;

  } catch (err) {
    message.value = err.message || 'Could not load profile. Please try again later.';
    messageType.value = 'error';
    console.error("Error fetching profile:", err);
  } finally {
    loading.value = false;
  }
}

// 2. Update the profile on form submission
async function updateProfile() {
  isSubmitting.value = true;
  message.value = ''; // Clear previous messages
  try {
    const token = localStorage.getItem("access_token");
    const res = await fetch('http://localhost:5000/child/profile-update', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        name: form.value.name,
        age: parseInt(form.value.age, 10), // Ensure age is an integer
        gender: form.value.gender
      })
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || 'Failed to update profile.');
    }

    // Show success message and redirect after a short delay
    message.value = 'Profile updated successfully!';
    messageType.value = 'success';
    setTimeout(() => {
      router.push('/child/home');
    }, 1500);

  } catch (err) {
    message.value = err.message;
    messageType.value = 'error';
    console.error("Error updating profile:", err);
  } finally {
    isSubmitting.value = false;
  }
}

// --- LIFECYCLE HOOK ---
onMounted(() => {
  fetchProfile();
});
</script>

<style scoped>
.edit-profile-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  background-color: #f9fafb;
  font-family: 'Poppins', sans-serif;
}

.edit-profile {
  max-width: 500px;
  width: 100%;
  margin: 2rem;
  background: #ffffff;
  padding: 2rem 2.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
}

.form-title {
  text-align: center;
  font-size: 1.75rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #374151;
  font-size: 0.9rem;
}

input, select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  box-sizing: border-box;
  transition: border-color 0.2s, box-shadow 0.2s;
}

input:focus, select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

button {
  width: 100%;
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.85rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #2563eb;
}

button:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.message {
  padding: 0.75rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  text-align: center;
  font-weight: 500;
}

.message.success {
  background-color: #d1fae5;
  color: #065f46;
}

.message.error {
  background-color: #fee2e2;
  color: #991b1b;
}
</style>
