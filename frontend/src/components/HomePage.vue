<template>
  <div class="homepage">
    <!-- ======================= NAVBAR ======================== -->
    <nav class="navbar">
      <h1 class="logo">Skill Explorers</h1>
      <div class="nav-links">
        <button @click="$router.push('/register')">Register as Parent</button>
        <button @click="$router.push('/login')">Login</button>
      </div>
    </nav>

    <!-- ======================= HERO SECTION ======================== -->
    <header class="hero">
      <h1>Your Adventure in Learning Begins!</h1>
      <p>Unlock new skills, explore your creativity, and have fun every day.</p>
      <!-- Hero Buttons Added to Match New CSS -->
      <div class="nav-links">
        <button class="btn-primary" @click="$router.push('/register')">Get Started Now</button>
        <button class="btn-secondary" @click="$router.push('/login')">I have an account</button>
      </div>
    </header>

    <!-- ======================= FEATURES SHOWCASE ======================== -->
    <main class="features-showcase">
      <h2>What’s Inside for You?</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">
            <i class="fas fa-book-open"></i>
          </div>
          <h3>Daily Journaling</h3>
          <p>Help children express their thoughts and emotions with engaging journal prompts.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <i class="fas fa-calendar-alt"></i>
          </div>
          <h3>Task Planner</h3>
          <p>Track daily learning tasks, set routines, and visualize progress on calendars.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <i class="fas fa-puzzle-piece"></i>
          </div>
          <h3>Fun Facts</h3>
          <p>Crack codes, learn amazing facts and sharpen your brain.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <i class="fas fa-trophy"></i>
          </div>
          <h3>Track Achievements</h3>
          <p>See badges, streaks, and celebrate learning milestones!</p>
        </div>
      </div>
    </main>

    <!-- ======================= 'HOW IT WORKS' SECTION (UPDATED STYLE) ======================== -->
    <section class="how-it-works-vertical">
      <div class="container">
        <h2 class="section-title">Getting Started is Easy</h2>

        <!-- Step 1: Parent Registration -->
        <div class="step-row">
          <div class="step-image">
            <img src="\src\public\opt-verify.png" alt="Parent registration screen showing email input field." onerror="this.onerror=null;this.src='https://placehold.co/600x400';">
          </div>
          <div class="step-content">
            <span class="step-number">Step 1</span>
            <h3>Register & Verify Your Account</h3>
            <p>Start by entering your email address. We'll send a secure one-time password (OTP) right to your inbox. Enter the OTP to verify your account and keep it safe.</p>
          </div>
        </div>

        <!-- Step 2: Parent Fills Details -->
        <div class="step-row">
          <div class="step-image">
            <img src="\src\public\parent-profile.png" alt="Parent profile details form." onerror="this.onerror=null;this.src='https://placehold.co/600x400';">
          </div>
          <div class="step-content">
            <span class="step-number">Step 2</span>
            <h3>Complete Your Parent Profile</h3>
            <p>Once your email is verified, fill in your details to create your parent account. This will be your central hub for managing your children's learning journey.</p>
          </div>
        </div>

        <!-- Step 3: Parent Adds Children -->
        <div class="step-row">
          <div class="step-image">
            <img src="\src\public\parent-add-children.png" alt="Parent dashboard with an 'Add Child' button." onerror="this.onerror=null;this.src='https://placehold.co/600x400';">
          </div>
          <div class="step-content">
            <span class="step-number">Step 3</span>
            <h3>Create Profiles for Your Explorers</h3>
            <p>From your parent dashboard, you can easily add your children. You'll create a unique username and password for each child to use for their own login.</p>
          </div>
        </div>

        <!-- Step 4: Child Logs In -->
        <div class="step-row">
          <div class="step-image">
            <img src="\src\public\child-login.png" alt="Child login screen with username and password fields." onerror="this.onerror=null;this.src='https://placehold.co/600x400';">
          </div>
          <div class="step-content">
            <span class="step-number">Step 4</span>
            <h3>Let the Adventure Begin!</h3>
            <p>Your children can now log in with their own credentials to access their personalized dashboard, complete fun tasks, and start their learning adventure.</p>
          </div>
        </div>

      </div>
    </section>
    <!-- ======================== 'HOW IT WORKS' SECTION END ========================= -->

    <!-- ======================= FOOTER ======================== -->
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
/* ================================================= */
/* ==         NEW STYLES YOU PROVIDED             == */
/* ================================================= */
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&family=Fredoka+One&display=swap');

.homepage {
  font-family: 'Comic Neue', cursive;
  background: #F8F8FF;
  min-height: 100vh;
  color: #333;
}

/* === NAVBAR === */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #F8F8FF;
  padding: 1rem 2rem;
  color: rgb(169, 208, 240);
  font-family: 'Fredoka One', cursive;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.navbar .logo {
  color: #5A4FCF;
  font-size: 1.8rem;
}

.navbar .nav-links button {
  background: #5A4FCF;
  color: white;
  border: none;
  margin-left: 10px;
  padding: 10px 20px;
  font-family: 'Fredoka One', cursive;
  border-radius: 30px;
  cursor: pointer;
  transition: transform 0.3s, background-color 0.3s;
}

.navbar .nav-links button:hover {
  transform: scale(1.05);
  background-color: #F7D96f;
  color: #4A4A4A;
}

/* === HERO === */
.hero {
  text-align: center;
  background: #756bdb;
  color: white;
  padding: 80px 20px;
  border-bottom-left-radius: 50% 30px;
  border-bottom-right-radius: 50% 30px;
}

.hero h1 {
  font-family: 'Fredoka One', cursive;
  font-size: 4rem;
  margin-bottom: 20px;
  text-shadow: 3px 3px 0px rgba(0, 0, 0, 0.1);
}

.hero p {
  font-size: 1.5rem;
  max-width: 600px;
  margin: 0 auto;
}

/* === HERO BUTTONS === */
.hero .nav-links {
  margin-top: 30px; /* Adds some space above the buttons */
}

/* Shared styles for both buttons */
.hero .nav-links button {
  font-family: 'Fredoka One', cursive;
  padding: 12px 30px;
  border-radius: 50px; /* Creates the pill shape */
  border: 2px solid white;
  font-size: 1.1rem;
  cursor: pointer;
  margin: 0 10px;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

/* Primary Button Style (Register) */
.hero .nav-links .btn-primary {
  background-color: #F7D96F;
  color: #4A4A4A; /* Uses the hero background color for text */
}

/* Secondary Button Style (Login) */
.hero .nav-links .btn-secondary {
  background-color: transparent;
  color: white;
}

/* --- HOVER EFFECTS --- */

/* Primary button gets slightly darker on hover */
.hero .nav-links .btn-primary:hover {
  background-color: #fff0e9; /* A very light pink/orange */
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

/* Secondary button fills with color on hover */
.hero .nav-links .btn-secondary:hover {
  background-color: white;
  color: #756bdb;
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

/* === FEATURES SECTION === */
.features-showcase {
  padding: 60px 20px;
  text-align: center;
}

.features-showcase h2 {
  font-family: 'Fredoka One', cursive;
  font-size: 3rem;
  margin-bottom: 40px;
  color: #4A4A4A;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: #E6E6FA;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 15px;
  color: #5A4FCF;
}

.feature-icon i {
  transition: transform 0.3s ease, color 0.3s ease;
}

.feature-card:hover .feature-icon i {
  transform: scale(1.1);
  color: #F7D96F;
}

.feature-card h3 {
  font-family: 'Fredoka One', cursive;
  font-size: 1.5rem;
  margin-bottom: 10px;
}

/* === 'HOW IT WORKS' SECTION (ADAPTED STYLE) === */
.how-it-works-vertical {
  padding: 80px 20px;

}

.how-it-works-vertical .container {
  max-width: 1000px;
  margin: 0 auto;
}

.how-it-works-vertical .section-title {
  text-align: center;
  font-family: 'Fredoka One', cursive;
  font-size: 3rem;
  font-weight: 500;
  color: #4A4A4A;
  margin-bottom: 60px;
}

.step-row {
  display: flex;
  align-items: center;
  gap: 50px;
  margin-bottom: 60px;
}

.step-row:nth-child(even) {
  flex-direction: row-reverse;
}

.step-image {
  flex: 1;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.step-image:hover {
    transform: scale(1.03);
}

.step-image img {
  width: 100%;
  height: auto;
  display: block;
}

.step-content {
  flex: 1;
  padding: 20px;
}

.step-number {
  display: inline-block;
  background-color: #F7D96F;
  color: #4A4A4A;
  padding: 8px 16px;
  border-radius: 20px;
  font-family: 'Fredoka One', cursive;
  font-weight: 500;
  font-size: 1rem;
  margin-bottom: 16px;
}

.step-content h3 {
  font-family: 'Fredoka One', cursive;
  font-size: 2rem;
  font-weight: 500;
  color: #5A4FCF;
  margin-bottom: 12px;
}

.step-content p {
  font-family: 'Comic Neue', cursive;
  font-size: 1.1rem;
  line-height: 1.7;
  color: #4b5563;
}

/* === FOOTER === */
.footer {
  padding: 20px;
  background-color: #333;
  color: white;
  text-align: center;
  margin-top: 60px;
  font-family: 'Fredoka One', cursive;
}

/* === RESPONSIVE STYLES === */
@media (max-width: 768px) {
  .hero h1 {
    font-size: 3rem;
  }
  .hero .nav-links button {
    display: block;
    margin: 10px auto;
    width: 80%;
  }
  .step-row,
  .step-row:nth-child(even) {
    flex-direction: column;
    gap: 20px;
  }

  .step-content {
    text-align: center;
  }

  .how-it-works-vertical .section-title,
  .features-showcase h2 {
    font-size: 2.5rem;
  }

  .step-content h3 {
    font-size: 1.8rem;
  }
}
</style>
