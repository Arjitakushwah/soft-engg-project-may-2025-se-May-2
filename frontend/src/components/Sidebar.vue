<template>
  <div class="sidebar">
    <template v-if="role === 'parent'">
      <button class="nav-btn" @click="navigateTo('AddChild')">Add Child</button>
      <button class="nav-btn" @click="navigateTo('ParentCalendar')">Calendar Report</button>
      <button class="nav-btn" @click="navigateTo('ParentJournalAnalysis')">Journal Insight</button>
    </template>
    <template v-else-if="role === 'child'">
      <button class="nav-btn" @click="navigateTo('ChildCalender')">Calendar Report</button>
      <button class="nav-btn" @click="navigateTo('ChildToDoList')">To Do List</button>
      <button class="nav-btn" @click="navigateTo('ChildStory')">Story</button>
      <button class="nav-btn" @click="navigateTo('ChildJournal')">Journaling</button>
      <button class="nav-btn" @click="navigateTo('ChildInfotainment')">Infotainment</button>
    </template>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const props = defineProps(['role'])
const router = useRouter()

const navigateTo = (routeName) => {
  router.push({ name: routeName })
}
</script>

<style scoped>
.sidebar {
  width: 280px;
  background: linear-gradient(135deg, #ff9a8b 0%, #ff6a88 100%);
  color: #333;
  padding: 30px;
  font-family: 'Comic Neue', cursive;
}

.nav-btn {
  width: 90%;
  padding: 15px;
  margin-bottom: 20px;
  font-weight: bold;
  font-size: large;
  background-color: #ebbeb3;
  color: rgb(40, 36, 36);
  border: none;
  cursor: pointer;
  border-radius: 10px;
  transition: background-color 0.3s ease;
}

.nav-btn:hover {
  background-color: #ff4870;
}
</style>