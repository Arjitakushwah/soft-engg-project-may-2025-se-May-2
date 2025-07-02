<template>
  <div class="add-child-container container mt-5">
    <div class="card shadow-lg p-4 mx-auto" style="max-width: 500px;">
      <h2 class="text-center mb-4">Add Child Profile</h2>

      <form @submit.prevent="addChild">
        <div class="mb-3">
          <input
            v-model="form.username"
            type="text"
            class="form-control"
            placeholder="Child Username"
            required
          />
        </div>

        <div class="mb-3">
          <input
            v-model="form.password"
            type="password"
            class="form-control"
            placeholder="Child Password"
            required
          />
        </div>

        <div class="mb-3">
          <input
            v-model="form.name"
            type="text"
            class="form-control"
            placeholder="Child Name"
            required
          />
        </div>

        <div class="mb-3">
          <input
            v-model="form.age"
            type="number"
            class="form-control"
            placeholder="Child Age"
            required
          />
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = ref({
  username: '',
  password: '',
  name: '',
  age: '',
  gender: 'Male'
})
const message = ref('')

const messageClass = computed(() => {
  if (message.value.includes('successfully')) return 'text-success'
  if (message.value) return 'text-danger'
  return ''
})

const addChild = async () => {
  const token = localStorage.getItem('token')
  const res = await fetch('http://127.0.0.1:5000/add-child', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}` 
    },
    body: JSON.stringify(form.value)
  })

  const data = await res.json()
  if (res.ok) {
    message.value = data.message
    setTimeout(() => {
      router.push('/login')  
    }, 2000)
  } else {
    message.value = data.error
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
