<template>
    <div class="spinner-container">
      <div class="spinner"></div>
      <p class="loading-text">Loading...</p>
    </div>
  </template>
  
  <style scoped>
  .spinner-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 3rem;
    gap: 1rem;
  }
  
  .spinner {
    width: 48px;
    height: 48px;
    border: 5px solid #f3f3f3;
    border-top: 5px solid #3498db;
    border-radius: 50%;
    animation: spin 1.2s linear infinite;
  }
  
  .loading-text {
    font-weight: 600;
    color: #2c3e50;
    font-size: 1rem;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  </style>