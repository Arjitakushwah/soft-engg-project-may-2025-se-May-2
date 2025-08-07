<template>
  <div class="add-child-container container mt-5">
    <div class="card shadow-lg p-4 mx-auto" style="max-width: 500px;">
      <h2 class="text-center mb-4">Add Child Profile</h2>
      <form @submit.prevent="addChild" novalidate>
        <div class="mb-3">
          <input 
            v-model.trim="form.username" 
            type="text" 
            class="form-control" 
            :class="{ 'is-invalid': errors.username }"
            placeholder="Child Username" 
            @input="validateField('username')"
          />
          <div v-if="errors.username" class="invalid-feedback">{{ errors.username }}</div>
        </div>
        <div class="mb-3">
          <input 
            v-model="form.password" 
            type="password" 
            class="form-control" 
            :class="{ 'is-invalid': errors.password }"
            placeholder="Child Password" 
            @input="validateField('password')"
          />
          <div v-if="errors.password" class="invalid-feedback">{{ errors.password }}</div>
        </div>
        <div class="mb-3">
          <input 
            v-model.trim="form.name" 
            type="text" 
            class="form-control" 
            :class="{ 'is-invalid': errors.name }"
            placeholder="Child Name" 
            @input="validateField('name')"
          />
          <div v-if="errors.name" class="invalid-feedback">{{ errors.name }}</div>
        </div>
        <div class="mb-3">
          <input 
            v-model="form.age" 
            type="number" 
            class="form-control" 
            :class="{ 'is-invalid': errors.age }"
            placeholder="Child Age" 
            @input="validateField('age')"
          />
          <div v-if="errors.age" class="invalid-feedback">{{ errors.age }}</div>
        </div>
        <div class="mb-4">
          <select 
            v-model="form.gender" 
            class="form-select" 
            :class="{ 'is-invalid': errors.gender }"
            @change="validateField('gender')"
          >
            <option disabled value="">Select Gender</option>
            <option>Male</option>
            <option>Female</option>
            <option>Other</option>
          </select>
          <div v-if="errors.gender" class="invalid-feedback">{{ errors.gender }}</div>
        </div>
        <button type="submit" class="btn btn-info w-100 text-white fw-bold">Add Child</button>
      </form>
      <p v-if="serverMessage" class="mt-3 text-center" :class="messageClass">{{ serverMessage }}</p>
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

const errors = ref({});
const serverMessage = ref('')
const parentUsername = ref('')

onMounted(() => {
  const role = localStorage.getItem('userRole')
  // Assuming parent info is stored upon login
  const parentInfo = localStorage.getItem('parent');
  
  if (role !== 'parent' || !parentInfo) {
    router.push('/login')
    return;
  }
  
  try {
      const parent = JSON.parse(parentInfo);
      parentUsername.value = parent.username
  } catch(e) {
      console.error("Failed to parse parent info from localStorage", e);
      router.push('/login');
  }
})

const messageClass = computed(() => {
  if (serverMessage.value.includes('successfully')) return 'text-success'
  if (serverMessage.value) return 'text-danger'
  return ''
})

const validateField = (fieldName) => {
    errors.value[fieldName] = '';

    switch(fieldName) {
        case 'username':
            const usernameRegex = /^[a-zA-Z0-9_]+$/;
            if (!form.value.username) errors.value.username = 'Username is required.';
            else if (form.value.username.length < 4) errors.value.username = 'Username must be at least 4 characters.';
            else if (!usernameRegex.test(form.value.username)) errors.value.username = 'Username can only contain letters, numbers, and underscores.';
            break;
        case 'password':
            const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
            if (!form.value.password) errors.value.password = 'Password is required.';
            else if (!passwordRegex.test(form.value.password)) errors.value.password = 'Password must be 8+ characters with uppercase, lowercase, and a number.';
            break;
        case 'name':
            if (!form.value.name) errors.value.name = 'Child\'s name is required.';
            else if (form.value.name.length < 2) errors.value.name = 'Name seems too short.';
            break;
        case 'age':
            if (!form.value.age) errors.value.age = 'Child\'s age is required.';
            else if (form.value.age < 1 || form.value.age > 18) errors.value.age = 'Age must be between 1 and 18.';
            break;
        case 'gender':
            if (!form.value.gender) errors.value.gender = 'Please select a gender.';
            break;
    }
}

const validateForm = () => {
    validateField('username');
    validateField('password');
    validateField('name');
    validateField('age');
    validateField('gender');

    return Object.values(errors.value).every(error => !error);
}

const addChild = async () => {
  serverMessage.value = ''

  if (!validateForm()) {
    return;
  }

  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch('http://localhost:5000/add-child', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(form.value)
    })

    const result = await response.json()

    if (!response.ok) {
      serverMessage.value = result.error || 'Something went wrong.'
      return
    }

    serverMessage.value = 'Child profile added successfully!'

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
    serverMessage.value = 'Network error. Please try again.'
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

.invalid-feedback {
    display: block;
}
</style>
