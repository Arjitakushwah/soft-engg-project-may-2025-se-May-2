<template>
    <div class="add-child-container container mt-5">
      <div class="card shadow-lg p-4 mx-auto" style="max-width: 500px;">
        <h2 class="text-center mb-4">Add Child Profile</h2>
        <form @submit.prevent="addChild">
          <div class="mb-3">
            <input v-model="form.username" type="text" class="form-control" placeholder="Child Username" required />
          </div>
          <div class="mb-3">
            <input v-model="form.password" type="password" class="form-control" placeholder="Child Password" required />
          </div>
          <div class="mb-3">
            <input v-model="form.name" type="text" class="form-control" placeholder="Child Name" required />
          </div>
          <div class="mb-3">
            <input v-model="form.age" type="number" class="form-control" placeholder="Child Age" required />
          </div>
          <div class="mb-4">
            <select v-model="form.gender" class="form-select" required>
              <option disabled value="">Select Gender</option>
              <option>Male</option>
              <option>Female</option>
              <option>Other</option>
            </select>
          </div>
          <button type="submit" class="btn btn-info w-100 text-white fw-bold">Add Child</button>
        </form>
        <p class="mt-3 text-center" :class="messageClass">{{ message }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
  const form = ref({
    username: '',
    password: '',
    name: '',
    age: '',
    gender: ''
  })
  
  const message = ref('')
  const parentUsername = ref('')
  
  onMounted(() => {
    const role = localStorage.getItem('userRole')
    const parent = JSON.parse(localStorage.getItem('parent'))
  
    if (role !== 'parent' || !parent) {
      router.push('/login')
    }
  
    parentUsername.value = parent.username
  })
  
  const messageClass = computed(() => {
    if (message.value.includes('successfully')) return 'text-success'
    if (message.value) return 'text-danger'
    return ''
  })
  
  const addChild = async () => {
  message.value = ''

  const { username, password, name, age, gender } = form.value

  if (!username || !password || !name || !age || !gender) {
    message.value = 'Please fill all the fields.'
    return
  }

  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch('http://localhost:5000/add-child', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ username, password, name, age, gender })
    })

    const result = await response.json()

    if (!response.ok) {
      message.value = result.error || 'Something went wrong.'
      return
    }

    message.value = 'Child profile added successfully!'

    // Reset form
    form.value = {
      username: '',
      password: '',
      name: '',
      age: '',
      gender: ''
    }

    // Redirect after short delay
    setTimeout(() => {
      router.push('/parent/home')
    }, 2000)

  } catch (err) {
    console.error(err)
    message.value = 'Network error. Please try again.'
  }
}

  </script>
  
  <style scoped>
  .add-child-container {
    font-family: 'Comic Neue', cursive;
  }
  
  .card {
    background: linear-gradient(135deg, #fff8dc, #e0f7fa);
    border-radius: 20px;
  }
  
  .btn-info {
    background-color: #17a2b8;
    border: none;
    font-family: 'Fredoka One', cursive;
  }
  
  .btn-info:hover {
    background-color: #148a9e;
  }
  </style>
  