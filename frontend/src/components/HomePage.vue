<template>
  <div class="homepage">
    <header class="hero">
      <h1>Your Adventure in Learning Begins!</h1>
      <p>Unlock new skills, explore your creativity, and have fun every day.</p>
      <button class="cta-button">Let's Go!</button>
      <p class="login-prompt">Already have an account? <a href="#">Log In</a></p>
    </header>

    <main class="features-showcase">
      <h2>What will you discover today?</h2>
      <div class="features-grid">

        <div class="feature-card">
          <div class="feature-icon">✏️</div>
          <h3>Chart Your Quests</h3>
          <p>Keep track of your daily adventures and tasks.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">📖</div>
          <h3>Write Your Own Stories</h3>
          <p>Create magical tales and become a master storyteller.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">🧠</div>
          <h3>Discover Wow Facts</h3>
          <p>Learn amazing new things about the world around you.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">📅</div>
          <h3>See Your Progress</h3>
          <p>Watch your skills grow and celebrate your achievements.</p>
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
  name: 'HomePage',
}
</script>

<style scoped>
@import '../assets/styles/HomePage.css';
</style> <template>
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
    </header>

    <main class="features-showcase">
      <h2>What will you discover today?</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">🧭</div>
          <h3>Interactive Quests</h3>
          <p>Go on learning journeys and complete creative challenges!</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🎨</div>
          <h3>Creative Studio</h3>
          <p>Draw, paint, and build stories with your imagination.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🧩</div>
          <h3>Fun Facts & Puzzles</h3>
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