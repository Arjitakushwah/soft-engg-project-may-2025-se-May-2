<template>
    <div class="home-wrapper">
      <!-- Hero Section -->
      <section class="hero-section">
        <div class="hero-content">
          <h1 class="home-title">
            Welcome to <span class="brand-gradient">Life Skills App</span>
          </h1>
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
          <svg viewBox="0 0 1440 80" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path
              fill="#a5b4fc"
              fill-opacity="0.25"
              d="M0,32 C360,80 1080,0 1440,48 L1440,80 L0,80 Z"
            />
          </svg>
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
  </template>
  
  <script>
  export default {
    name: 'Home',
  };
  </script>
  
  <style scoped>
  /* Home Wrapper */
.home-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #b39ddb 0%, #4dd0e1 100%);
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #b39ddb 0%, #4dd0e1 60%, #ffe0b2 100%);
  border-bottom-left-radius: 48px;
  border-bottom-right-radius: 48px;
  box-shadow: 0 8px 32px rgba(51, 51, 51, 0.10);
  padding: 56px 0 0 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: stretch;
  position: relative;
}
.hero-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 600px;
  width: 100%;
  margin: 0 auto;
  background: rgba(250, 249, 246, 0.85);
  border-radius: 32px;
  box-shadow: 0 4px 24px rgba(51, 51, 51, 0.10);
  padding: 32px 24px 24px 24px;
}
.home-title {
  font-size: 2.8rem;
  font-weight: bold;
  margin-bottom: 16px;
  letter-spacing: 1px;
  text-align: center;
  text-shadow: 0 2px 8px #b39ddb33, 0 1px 0 #fff;
}
.brand-gradient {
  color: #7c3aed; /* Bold purple */
  background: none;
  -webkit-background-clip: initial;
  -webkit-text-fill-color: initial;
  background-clip: initial;
  text-shadow: 0 2px 8px rgba(51,51,51,0.18), 0 1px 0 #fff;
  font-weight: 900;
}
.home-slogan {
  color: #333333;
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 28px;
  letter-spacing: 0.5px;
  text-align: center;
  text-shadow: 0 1px 0 #fff;
}
.hero-illustration {
  margin: 22px 0 28px 0;
  font-size: 3.2rem;
  text-shadow: 0 2px 8px #b39ddb33;
}
.emoji {
  display: inline-block;
  animation: bounce 1.2s infinite alternate;
}
@keyframes bounce {
  to {
    transform: translateY(-10px) scale(1.1);
  }
}
.home-buttons {
  display: flex;
  justify-content: center;
  gap: 28px;
  margin-bottom: 18px;
}
.home-btn {
  font-size: 1.2rem;
  font-weight: bold;
  padding: 16px 36px;
  border: none;
  border-radius: 28px;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
  box-shadow: 0 4px 12px rgba(51, 51, 51, 0.10);
  display: flex;
  align-items: center;
}
.register-btn {
  background: #ffe0b2;
  color: #333333;
}
.register-btn:hover {
  background: #b39ddb;
  color: #faf9f6;
  transform: scale(1.07);
}
.login-btn {
  background: #4dd0e1;
  color: #faf9f6;
}
.login-btn:hover {
  background: #b39ddb;
  color: #faf9f6;
  transform: scale(1.07);
}
.btn-icon {
  font-size: 1.3em;
  margin-right: 8px;
  vertical-align: middle;
}
.wavy-divider {
  width: 100%;
  margin-top: 24px;
  line-height: 0;
}

/* Features Grid */
.features-section {
  background: #f8fafc;
  padding: 48px 0 32px 0;
  text-align: center;
}
.features-title {
  color: #6366f1;
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 32px;
  letter-spacing: 1px;
}
.features-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 28px;
}
.feature-card {
  width: 180px;
  min-height: 180px;
  border-radius: 24px;
  box-shadow: 0 4px 16px rgba(51, 51, 51, 0.10);
  padding: 24px 12px 18px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.22s, box-shadow 0.22s;
  cursor: pointer;
  font-size: 1rem;
}
.feature-card:hover {
  transform: translateY(-10px) scale(1.07);
  box-shadow: 0 12px 32px rgba(51, 51, 51, 0.18);
  z-index: 2;
}
.card-blue { background: linear-gradient(135deg, #a5b4fc 80%, #f8fafc 100%); color: #3730a3; }
.card-pink { background: linear-gradient(135deg, #fbc2eb 80%, #f8fafc 100%); color: #be185d; }
.card-yellow { background: linear-gradient(135deg, #fcd34d 80%, #f8fafc 100%); color: #b45309; }
.card-green { background: linear-gradient(135deg, #6ee7b7 80%, #f8fafc 100%); color: #047857; }
.card-purple { background: linear-gradient(135deg, #c4b5fd 80%, #f8fafc 100%); color: #6d28d9; }
.card-orange { background: linear-gradient(135deg, #fdba74 80%, #f8fafc 100%); color: #b45309; }
.feature-emoji { font-size: 2.2rem; margin-bottom: 8px; }
.feature-title { font-size: 1.1rem; font-weight: bold; margin-bottom: 4px; }
.feature-desc { font-size: 0.97rem; font-style: italic; text-align: center; }

/* Benefits Banners */
.benefits-section {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 18px;
  padding: 32px 0 24px 0;
  background: #fff;
}
.benefit-banner {
  display: flex;
  align-items: center;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 18px;
  padding: 16px 32px;
  box-shadow: 0 2px 12px rgba(51, 51, 51, 0.08);
  gap: 12px;
}
.banner-blue { background: #a5b4fc; color: #3730a3; }
.banner-yellow { background: #fcd34d; color: #b45309; }
.banner-green { background: #6ee7b7; color: #047857; }
.benefit-icon { font-size: 1.5rem; margin-right: 10px; }

/* Testimonials */
.testimonials-section {
  background: #f8fafc;
  padding: 48px 0 32px 0;
  text-align: center;
}
.testimonials-title {
  color: #6366f1;
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 32px;
  letter-spacing: 1px;
}
.testimonials-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 28px;
}
.testimonial-card {
  border-radius: 20px;
  box-shadow: 0 4px 16px rgba(51, 51, 51, 0.10);
  padding: 24px 18px 18px 18px;
  width: 240px;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 1rem;
}
.testimonial-card.card-blue    { background: linear-gradient(135deg, #a5b4fc 80%, #f8fafc 100%); color: #3730a3; }
.testimonial-card.card-pink    { background: linear-gradient(135deg, #fbc2eb 80%, #f8fafc 100%); color: #be185d; }
.testimonial-card.card-yellow  { background: linear-gradient(135deg, #fcd34d 80%, #f8fafc 100%); color: #b45309; }
.testimonial-avatar { font-size: 2.2rem; margin-bottom: 8px; }
.testimonial-quote { font-size: 1.05rem; font-style: italic; margin-bottom: 8px; color: #6366f1; }
.testimonial-name { font-size: 0.97rem; color: #6b7280; }

/* Footer */
.footer-section {
  background: #a5b4fc;
  color: #3730a3;
  padding: 18px 0;
  text-align: center;
  font-size: 1rem;
  border-top-left-radius: 24px;
  border-top-right-radius: 24px;
  margin-top: 32px;
}
.footer-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}
.footer-links a {
  color: #3730a3;
  text-decoration: underline;
  margin: 0 4px;
  font-weight: 500;
}
.footer-links a:hover {
  color: #be185d;
}

/* Responsive Tweaks */
@media (max-width: 900px) {
  .features-grid, .testimonials-grid, .benefits-section {
    flex-direction: column;
    align-items: center;
    gap: 18px;
  }
  .feature-card, .testimonial-card, .benefit-banner {
    width: 90vw;
    max-width: 340px;
  }
}
  </style>
  