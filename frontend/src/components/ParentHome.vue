<template>
    <div class="parent-home-container">
      <h2 class="title">Welcome, {{ parentName }} </h2>
      <p class="subtitle">Use the sidebar to manage your child’s learning activities.</p>
  
      <!-- Children List -->
      <div class="child-list mt-5">
        <h3>Your Children</h3>
        <ul v-if="children.length">
          <li v-for="child in children" :key="child.id" class="child-item">
            👶 {{ child.name }} ({{ child.age }} yrs, {{ child.gender }})
          </li>
        </ul>
        <p v-else>No children added yet.</p>
      </div>
    </div>
  </template>
  
  <script setup>
import { ref, onMounted } from 'vue'

const parentName = ref('Parent')
const children = ref([])

onMounted(() => {
  const parent = JSON.parse(localStorage.getItem('parent'))

  if (!parent) return

  parentName.value = parent.name

  const dummyChildren = [
    { id: 2, name: 'Ravi', age: 10, gender: 'Male', parentUsername: parent.username },
    { id: 3, name: 'Meera', age: 9, gender: 'Female', parentUsername: parent.username }
  ]

  const allChildren = JSON.parse(localStorage.getItem('childList'))

  if (!allChildren || allChildren.length === 0) {
    // Set dummy children only if no children in localStorage
    localStorage.setItem('childList', JSON.stringify(dummyChildren))
    children.value = dummyChildren
  } else {
    // Filter by current parent
    children.value = allChildren.filter(
      (child) => child.parentUsername === parent.username
    )
  }
})
</script>

  
  <style scoped>
  .parent-home-container {
    font-family: 'Comic Neue', cursive;
    padding: 2rem;
    background-color: #fff;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
    text-align: center;
  }
  
  .title {
    font-size: 2.2rem;
    color: #ff6a88;
    margin-bottom: 1rem;
    font-family: 'Fredoka One', cursive;
  }
  
  .subtitle {
    font-size: 1.1rem;
    color: #666;
    margin-bottom: 2rem;
  }
  
  .quick-actions {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    align-items: center;
  }
  
  .quick-link {
    background-color: #ffe6ec;
    padding: 12px 24px;
    color: #ff6a88;
    font-weight: bold;
    border-radius: 10px;
    text-decoration: none;
    transition: all 0.2s ease-in-out;
    font-size: 1rem;
  }
  
  .quick-link:hover {
    background-color: #ff6a88;
    color: white;
  }
  
  .child-list {
    text-align: left;
    margin-top: 30px;
    max-width: 500px;
    margin-inline: auto;
  }
  
  .child-list h3 {
    font-family: 'Fredoka One', cursive;
    color: #333;
    margin-bottom: 10px;
  }
  
  .child-item {
    padding: 10px;
    background-color: #fef3f7;
    border-radius: 8px;
    margin-bottom: 10px;
    font-size: 1rem;
    color: #444;
  }
  </style>
  