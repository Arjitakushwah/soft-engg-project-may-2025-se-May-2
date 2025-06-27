<template>
  <!--<header class="custom-navbar">
    <div class="left-section">
      <h2>Hi, <span class="highlight">Child</span></h2>
    </div>
    <div class="center-section">
      <p class="welcome-text">Welcome to your Dashboard</p>
    </div>
    <div class="right-section">
      <button class="logout-button">Logout</button>
    </div>
  </header>-->

</template>

<script>

export default {
    name: 'Navbar',
  };
</script>

<style scoped>
.custom-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #1d1d2e; /* matches your image */
  padding: 20px 30px;
  color: white;
}

.left-section h2 {
  margin: 0;
  font-size: 24px;
}

.left-section .highlight {
  color: #00f8ff;
}

.center-section .welcome-text {
  margin: 0;
  font-size: 22px;
  text-align: center;
}

.right-section .logout-button {
  background-color: #ff4d5a;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 10px 20px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-button:hover {
  background-color: #e03a46;
}
</style>
