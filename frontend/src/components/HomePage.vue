<template>
  <div class="homepage">
    <nav class="navbar">
      <h1 class="logo">Skill Explorers</h1>
      <div class="nav-links">
        <button @click="$router.push('/register')">Register as Parent</button>
        <button @click="$router.push('/login')">Login</button>
      </div>
    </nav>
    <header class="hero">
      <h1>Your Adventure in Learning Begins!</h1>
      <p>Unlock new skills, explore your creativity, and have fun every day.</p>
      <div class="nav-links">
        <button class="btn-primary" @click="$router.push('/register')">Register as Parent</button>
        <button class="btn-secondary" @click="$router.push('/login')">Login</button>
      </div>
    </header>
    <main class="features-showcase">
      <h2>What’s Inside for You?</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">📖</div>
          <h3>Daily Journaling</h3>
          <p>Help children express their thoughts and emotions with engaging journal prompts.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📅</div>
          <h3>Task Planner</h3>
          <p>Track daily learning tasks, set routines, and visualize progress on calendars.</p>
        
        </div>
        <div class="feature-card">
          <div class="feature-icon">🧩</div>
          <h3>Fun Facts</h3>
          <p>Crack codes, learn amazing facts and sharpen your brain.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🌟</div>
          <h3>Track Achievements</h3>
          <p>See badges, streaks, and celebrate learning milestones!</p>
        </div>
      </div>
    </main>

    <footer class="footer">
      <p>&copy; 2025 Skill Explorers. Let's make learning fun!</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'HomePage'
}
</script>

<style scoped>
@import '../assets/styles/HomePage.css';
</style>