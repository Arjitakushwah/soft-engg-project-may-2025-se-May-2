<template>
  <div class="parent-dashboard container mt-5">
    <div class="card shadow p-4 text-center">
      <h2 class="dashboard-title mb-4">Welcome to Parent Dashboard 👨‍👩‍👧‍👦</h2>

      <router-link to="/add-child" class="btn btn-primary fw-bold">
        ➕ Add Child Profile
      </router-link>
    </div>
  </div>
</template>

<script setup>
// No logic needed here for now
</script>

<style scoped>
.parent-dashboard {
  font-family: 'Comic Neue', cursive;
}

.card {
  background: linear-gradient(135deg, #f0fff0, #e0f7fa);
  border-radius: 20px;
}

.dashboard-title {
  font-family: 'Fredoka One', cursive;
  font-size: 2.2rem;
  color: #333;
}

.btn-primary {
  background-color: #ff6a88;
  border: none;
  font-family: 'Fredoka One', cursive;
}

.btn-primary:hover {
  background-color: #ff4870;
}
</style>
