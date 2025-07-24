<template>
    <div>
      <h3>Select Activity</h3>
      <select v-model="selectedActivity">
        <option value="journal">Journal</option>
        <option value="Daily tasks">Daily Tasks</option>
        <option value="stories">Stories</option>
        <option value="infotaiment">Infotainment</option>
      </select>
  
      <JournalInsight v-if="selectedActivity === 'journal'" />
      <TaskInsight v-if="selectedActivity === 'Daily tasks'" />
      <StoryInsight v-if="selectedActivity === 'stories'" />
      <InfoInsight v-if="selectedActivity === 'Infotainment'" />
    </div>
  </template>
  
  <script>
  import JournalInsight from '../components/ParentJournalAnalysis.vue'
  import TaskInsight from '../components/ParentToDoInsight.vue'
  import StoryInsight from '../components/ParentStoryInsight.vue'
  import InfoInsight from '../components/ParentInfotainmentInsight.vue'
  
  export default {
    components: {
      JournalInsight,
      TaskInsight,
      StoryInsight,
      InfoInsight
    },
    data() {
      return {
        selectedActivity: 'journal'
      }
    }
  }
  </script>
  
  