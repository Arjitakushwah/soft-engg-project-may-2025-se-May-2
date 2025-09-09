<template>
  <div class="edit-profile-wrapper">
    <div class="edit-profile">
      <h2 class="form-title">Edit Your Profile</h2>
      
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-purple" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      
      <form v-else @submit.prevent="updateProfile">
        <h3 class="section-title">Your Details</h3>
        <div class="form-group">
          <label for="name">Name</label>
          <input id="name" v-model="form.name" type="text" placeholder="Enter name" required />
        </div>
        <div class="form-group">
          <label for="age">Age</label>
          <input id="age" v-model="form.age" type="number" min="1" placeholder="Enter age" required />
        </div>
        <div class="form-group">
          <label for="gender">Gender</label>
          <select id="gender" v-model="form.gender" required>
            <option value="" disabled>Select gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
            <option value="prefer_not_to_say">Prefer not to say</option>
          </select>
        </div>

        <div v-if="message" :class="['message', messageType, 'mt-3']">
          {{ message }}
        </div>

        <button type="submit" :disabled="isSubmitting" class="mt-4">
          <span v-if="isSubmitting" class="spinner-border spinner-border-sm"></span>
          <span v-else>Save Changes</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const form = ref({
  name: '',
  age: '',
  gender: ''
});
const loading = ref(true);
const isSubmitting = ref(false);
const message = ref('');
const messageType = ref('');

async function fetchProfile() {
  loading.value = true;
  message.value = '';
  try {
    const token = localStorage.getItem("access_token");
    const res = await fetch('https://slice-abcd.onrender.com/child_dashboard', {
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


async function updateProfile() {
  isSubmitting.value = true;
  message.value = '';
  try {
    const token = localStorage.getItem("access_token");
    
    const payload = {
      name: form.value.name,
      age: parseInt(form.value.age, 10),
      gender: form.value.gender
    };

    const res = await fetch('https://slice-abcd.onrender.com/child/profile/update', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || 'Failed to update profile.');
    }

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
  background: #F8F8FF;
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
  color: #5A4FCF;
  margin-bottom: 1.5rem;
}

.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #5A4FCF;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #e5e7eb;
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
  border-color: #5A4FCF;
  
}

button {
  width: 100%;
  background-color: #5A4FCF;
  color: #ffffff;
  border: none;
  padding: 0.85rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #493dcc;
}

button:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.message {
  padding: 0.75rem;
  border-radius: 6px;
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

.invalid-feedback {
    font-size: 0.8rem;
    color: #ef4444;
}

.text-purple {
    color: #756bdb !important;
}
</style>
