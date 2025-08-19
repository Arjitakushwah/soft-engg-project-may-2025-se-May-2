<template>
    <div class="nf-hero-bg">
      <div class="nf-hero-container">
        <div class="nf-hero-left">
          <h1 class="nf-hero-title">Lost in the Digital Wilderness!</h1>
          <p class="nf-hero-desc">
            Our brave explorer seems to have wandered off the path, and so has the page you were looking for!
            Fear not, let's guide them back to the main adventure.
          </p>
          <button class="nf-hero-btn" @click="goHome">Return to Home</button>
        </div>
  
        <div class="nf-hero-right">
          <div class="nf-hero-svg">
            <svg viewBox="0 0 900 650" xmlns="http://www.w3.org/2000/svg">
              <rect x="0" y="0" width="900" height="650" fill="#E1F5FE" />
              <path d="M0 500 C300 400, 700 450, 900 350 L900 650 L0 650 Z" fill="#A5D6A7" />
  
              <circle cx="800" cy="120" r="70" fill="#FFCA28" class="sun-pulse" />
  
              <g class="cloud-group">
                <ellipse cx="150" cy="100" rx="90" ry="40" fill="#FFFFFF" class="cloud-float-1" />
                <ellipse cx="400" cy="80" rx="110" ry="45" fill="#FFFFFF" class="cloud-float-2" />
                <ellipse cx="700" cy="150" rx="80" ry="35" fill="#FFFFFF" class="cloud-float-3" />
              </g>
  
              <g class="explorer-group">
                <path d="M450 550 L430 500 Q400 450, 450 400 Q500 450, 470 500 L450 550 Z" fill="#795548" />
                <rect x="400" y="400" width="100" height="150" fill="#64B5F6" stroke="#424242" stroke-width="3" rx="10" />
                <circle cx="450" cy="350" r="60" fill="#FFC107" stroke="#424242" stroke-width="3" />
                <path d="M420 300 C400 280, 500 280, 480 300" fill="#F57C00" />
                <circle cx="435" cy="335" r="8" fill="#FFF" />
                <circle cx="465" cy="335" r="8" fill="#FFF" />
                <circle cx="435" cy="335" r="3" fill="#424242" />
                <circle cx="465" cy="335" r="3" fill="#424242" />
                <path d="M430 365 Q450 380, 470 365" stroke="#424242" stroke-width="2" fill="none" />
                <path d="M440 550 C430 580, 470 580, 460 550" stroke="#424242" stroke-width="5" fill="none" stroke-linecap="round" />
                <path d="M380 420 C350 400, 330 480, 360 500" stroke="#424242" stroke-width="5" fill="none" stroke-linecap="round" />
                <path d="M520 420 C550 400, 570 480, 540 500" stroke="#424242" stroke-width="5" fill="none" stroke-linecap="round" />
              </g>
  
              <g class="sign-group">
                <path d="M150 500 L200 250 L350 250 L300 500 Z" fill="#D7CCC8" stroke="#424242" stroke-width="4" stroke-linejoin="round" />
                <path d="M225 250 C210 200, 315 200, 285 250 Z" fill="#BCAAA4" stroke="#424242" stroke-width="4" stroke-linecap="round" />
                <text x="250" y="400" font-family="'Luckiest Guy', cursive" font-size="120" font-weight="bold" fill="#E65100" text-anchor="middle" class="shake-text">
                  404
                </text>
              </g>
            </svg>
          </div>
        </div>
      </div>
    </div>
</template>
  
  <script setup>
  import { useRouter } from 'vue-router';
  import { onMounted } from 'vue';
  
  const router = useRouter();
  const goHome = () => {
    router.push('/');
  };
  
  onMounted(() => {
    const explorerGroup = document.querySelector('.explorer-group');
    if (explorerGroup) {
      setTimeout(() => {
        explorerGroup.style.transformOrigin = 'center bottom';
        explorerGroup.style.animation = 'lookAround 2s ease-in-out';
        setTimeout(() => {
          explorerGroup.style.animation = '';
          explorerGroup.style.transformOrigin = '';
        }, 2000);
      }, 500);
    }
  });
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy:wght@400&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
  
  .nf-hero-bg {
    min-height: 100vh;
    width: 100vw;
    background-color: #E1F5FE;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Poppins', sans-serif;
    color: #424242;
    overflow: hidden;
  }
  
  .nf-hero-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    width: 100vw;
    max-width: 1600px;
    padding: 0 5vw;
    gap: 4vw;
  }
  
  .nf-hero-left {
    flex: 1 1 550px;
    max-width: 700px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
  }
  
  .nf-hero-title {
    font-family: 'Poppins', sans-serif;
    font-size: 4.5rem;
    font-weight: 700;
    color: #1976D2;
    margin-bottom: 0.7em;
    line-height: 1.1;
    text-shadow: 2px 2px #E3F2FD;
  }
  
  .nf-hero-desc {
    color: #546E7A;
    font-size: 1.3rem;
    margin-bottom: 2.5em;
    line-height: 1.7;
    max-width: 600px;
  }
  
  .nf-hero-btn {
    background: linear-gradient(135deg, #FFB300 30%, #F57C00 90%);
    color: #fff;
    font-weight: 600;
    font-size: 1.3rem;
    border: none;
    border-radius: 50px;
    padding: 20px 50px;
    box-shadow: 0 6px 25px rgba(255, 179, 0, 0.5);
    cursor: pointer;
    transition: transform 0.2s ease-in-out;
  }
  
  .nf-hero-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 30px rgba(255, 179, 0, 0.7);
  }
  
  .nf-hero-right {
    flex: 1 1 600px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .nf-hero-svg {
    width: 100%;
    max-width: 900px;
    height: auto;
  }
@keyframes cloud-float {
    0% { transform: translateX(20px); }
    50% { transform: translateX(-20px); }
    100% { transform: translateX(20px); }
  }
  .cloud-float-1 { animation: cloud-float 25s ease-in-out infinite; animation-delay: 2s; }
  .cloud-float-2 { animation: cloud-float 30s ease-in-out infinite; }
  .cloud-float-3 { animation: cloud-float 28s ease-in-out infinite; animation-delay: 5s; }
  
  @keyframes sun-pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.1); opacity: 0.8; }
  }
  .sun-pulse { animation: sun-pulse 10s ease-in-out infinite; }
  
  @keyframes lookAround {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(-10deg); }
    75% { transform: rotate(10deg); }
  }
  
  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    10%, 90% { transform: translateX(-5px); }
    30%, 70% { transform: translateX(5px); }
    50% { transform: translateX(-10px); }
  }
  .shake-text {
    animation: shake 1s cubic-bezier(.36,.07,.19,.97) infinite;
  }
  
  /* Responsive adjustments */
  @media (max-width: 1200px) {
    .nf-hero-container {
      flex-direction: column-reverse;
      text-align: center;
      gap: 5vw;
    }
    .nf-hero-left {
      align-items: center;
      max-width: 90vw;
    }
    .nf-hero-title {
      font-size: 3.5rem;
    }
    .nf-hero-svg {
      max-width: 95%;
    }
  }
  
  @media (max-width: 768px) {
    .nf-hero-title {
      font-size: 2.8rem;
    }
    .nf-hero-desc {
      font-size: 1.1rem;
    }
    .nf-hero-btn {
      padding: 15px 40px;
      font-size: 1.1rem;
    }
  }
  </style>