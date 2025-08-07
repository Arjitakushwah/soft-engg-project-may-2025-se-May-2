<template>
  <div class="edit-profile">
    <h2>Edit Child Profile</h2>
    <form @submit.prevent="updateProfile">
      <div class="form-group">
        <label>Name</label>
        <input v-model="form.name" type="text" placeholder="Enter name" required />
      </div>

      <div class="form-group">
        <label>Age</label>
        <input v-model="form.age" type="number" min="1" required />
      </div>

      <button type="submit">Save Changes</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = ref({
  name: '',
  age: ''
})

// Load existing data from localStorage on mount
onMounted(() => {
  form.value.name = localStorage.getItem('child_name') || ''
  form.value.age = localStorage.getItem('child_age') || ''
})

// Save new data and navigate to dashboard
const updateProfile = () => {
  localStorage.setItem('child_name', form.value.name)
  localStorage.setItem('child_age', form.value.age)

  alert('Profile updated successfully!')
  router.push('/child/home')
}
</script>

<style scoped>
.edit-profile {
  max-width: 500px;
  margin: 40px auto;
  background: #f3f4f6;
  padding: 25px;
  border-radius: 10px;
}
.form-group {
  margin-bottom: 16px;
}
label {
  display: block;
  font-weight: bold;
  margin-bottom: 6px;
}
input {
  width: 100%;
  padding: 10px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
}
button {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 6px;
  cursor: pointer;
}
</style>
