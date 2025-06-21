export default {
  template: `
    <div class="home-wrapper">
      <!-- Hero Section -->
      <section class="hero-section">
        <div class="hero-content">
          <h1 class="home-title">Welcome to <span class="brand-gradient">Life Skills App</span></h1>
          <p class="home-slogan">Unlock your superpowers! Learn, play, and grow every day.</p>
          <div class="hero-illustration">
            <span class="emoji" role="img" aria-label="super kids">🦸🎨🤹‍♂️📚</span>
          </div>
          <div class="home-buttons">
            <button class="home-btn register-btn" @click="$router.push('/register')">
              <span class="btn-icon">📝</span> Register
            </button>
            <button class="home-btn login-btn" @click="$router.push('/login')">
              <span class="btn-icon">🚀</span> Login
            </button>
          </div>
        </div>
        <div class="wavy-divider">
          <svg viewBox="0 0 1440 80" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill="#a5b4fc" fill-opacity="0.25" d="M0,32 C360,80 1080,0 1440,48 L1440,80 L0,80 Z"></path></svg>
        </div>
      </section>

      <!-- Features/Skills Grid -->
      <section class="features-section">
        <h2 class="features-title">Explore Awesome Life Skills</h2>
        <div class="features-grid">
          <div class="feature-card card-blue">
            <span class="feature-emoji">🤝</span>
            <div class="feature-title">Daily Goals</div>
            <div class="feature-desc">Check off your tasks and feel awesome!</div>
          </div>
          <div class="feature-card card-pink">
            <span class="feature-emoji">🎨</span>
            <div class="feature-title">Creativity</div>
            <div class="feature-desc">Let your imagination fly!</div>
          </div>
          <div class="feature-card card-yellow">
            <span class="feature-emoji">💡</span>
            <div class="feature-title">Confidence</div>
            <div class="feature-desc">Believe in yourself every day.</div>
          </div>
          <div class="feature-card card-green">
            <span class="feature-emoji">🌱</span>
            <div class="feature-title">Growth</div>
            <div class="feature-desc">Learn new things, grow new skills.</div>
          </div>
          <div class="feature-card card-purple">
            <span class="feature-emoji">🧠</span>
            <div class="feature-title">Problem Solving</div>
            <div class="feature-desc">Crack puzzles, solve challenges!</div>
          </div>
          <div class="feature-card card-orange">
            <span class="feature-emoji">😊</span>
            <div class="feature-title">Kindness</div>
            <div class="feature-desc">Spread smiles and help others.</div>
          </div>
        </div>
      </section>

      <!-- Benefits Section -->
      <section class="benefits-section">
        <div class="benefit-banner banner-blue">
          <span class="benefit-icon">🔒</span>
          Safe & Fun Environment
        </div>
        <div class="benefit-banner banner-yellow">
          <span class="benefit-icon">🎲</span>
          Learn by Playing
        </div>
        <div class="benefit-banner banner-green">
          <span class="benefit-icon">🌍</span>
          For All Kids!
        </div>
      </section>

      <!-- Testimonials Section -->
      <section class="testimonials-section">
        <h2 class="testimonials-title">What Our Super Kids Say</h2>
        <div class="testimonials-grid">
          <div class="testimonial-card card-blue">
            <div class="testimonial-avatar">👦</div>
            <div class="testimonial-quote">“I love the games and learned so much!”</div>
            <div class="testimonial-name">- Aryan, 10</div>
          </div>
          <div class="testimonial-card card-pink">
            <div class="testimonial-avatar">👧</div>
            <div class="testimonial-quote">“The teamwork challenges are my favorite!”</div>
            <div class="testimonial-name">- Priya, 12</div>
          </div>
          <div class="testimonial-card card-yellow">
            <div class="testimonial-avatar">🧑‍🦱</div>
            <div class="testimonial-quote">“I feel more confident at school now.”</div>
            <div class="testimonial-name">- Kabir, 11</div>
          </div>
        </div>
      </section>

      <!-- Footer -->
      <footer class="footer-section">
        <div class="footer-content">
          <span>© 2025 Life Skills App</span>
          <span class="footer-links">
            <a href="#">About</a> | <a href="#">Contact</a>
          </span>
        </div>
      </footer>
    </div>
  `
};
