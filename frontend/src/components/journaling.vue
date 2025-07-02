<template>
  <div class="search-container">
    <input type="text" placeholder="Search journal by date" v-model="search_Text">
    <button @click="performSearch">Search</button>
  </div>
  
  <div class="emoji-selector">
    <label>How are you feeling?</label>
    <div class="emoji-options">
      <span v-for="emoji in emojis" :key="emoji" :class="['emoji',selectedEmoji === emoji ? 'selected' : '']" 
        @click="selectedEmoji = emoji" >
        {{ emoji }}
      </span>
    </div>
  </div>

  <form>
    <div class="text-container">
    <label for="message">Write your journal here:</label><br>
    <textarea id="message" name="message" placeholder="How are you feeling today?"></textarea><br>
    </div>
    <div class="button-container">
    <button type="submit">Submit</button>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const search_Text = ref('')
const emojis = ['😄', '🙂', '😐', '😢', '😡']
const selectedEmoji = ref('')
</script>
<style scoped>
    .search-container {
      display: flex;
      gap: 10px;
      margin-bottom: 20px;
    }
    input[type='text'] {
      flex: 1;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 6px;
      font-size: 16px;
    }
    
    textarea {
      width: 90%;
      height: 120px;
      padding: 8px;
      font-size: 18px;
      border: 1px solid #ccc;
      border-radius: 6px;
    }
    .button-container {
      width: 90%;
      display: flex;
      justify-content: flex-end;
      margin-top: 10px;
    }
    button {
      padding: 10px 20px;
      background-color: #1e3a8a;
      color: white;
      border: none;
      border-radius: 6px;
    }
    .emoji-selector {
      margin-bottom: 10px;
      font-size: 16px;
      font-weight: 500;
    }

    .emoji-options {
      display: flex;
      gap: 10px;
      margin-top: 5px;
      margin-bottom: 10px;
    }

    .emoji {
      font-size: 28px;
      cursor: pointer;
      transition: transform 0.2s;
    }

    .emoji:hover {
      transform: scale(1.2);
    }

    .selected {
      border: 2px solid #1e3a8a;
      border-radius: 50%;
      padding: 2px;
    }

</style>