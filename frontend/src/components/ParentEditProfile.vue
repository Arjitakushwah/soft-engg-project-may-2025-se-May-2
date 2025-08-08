<template>
  <div class="edit-profile">
    <h2>Edit Profile</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="name">Name:</label>
        <input id="name" v-model="form.name" type="text" required />
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input id="email" v-model="form.email" type="email" required />
      </div>
      <button type="submit">Save</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = ref({
  name: '',
  email: ''
})

onMounted(() => {
  // Pre-fill form using localStorage
  form.value.name = localStorage.getItem('username') || ''
  form.value.email = localStorage.getItem('email') || ''
})

const submitForm = () => {
  // Save updated values to localStorage
  localStorage.setItem('username', form.value.name)
  localStorage.setItem('email', form.value.email)

  alert('Profile updated successfully!')
  router.push('/Parent/home')
}

</script>

<style scoped>
.edit-profile {
  max-width: 600px;
  margin: 0 auto;
  background: #f9fafb;
  padding: 20px;
  border-radius: 10px;
}
.form-group {
  margin-bottom: 15px;
}
label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}
input {
  width: 100%;
  padding: 8px;
  border: 1px solid #d1d5db;
  border-radius: 5px;
}
button {
  padding: 10px 20px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background: #2563eb;
}
</style>
