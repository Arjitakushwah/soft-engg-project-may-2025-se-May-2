<template>
<div v-if="role === 'parent'">
  <div style="display: flex; height: 100vh;">
    <div style="width: 250px; background-color: #1e3a8a; color: white; padding: 20px;">
      <p><button @click="currentPage = 'add_child'" class="nav-btn">Add Child</button></p>
      <p><button @click="currentPage = 'calender_report_parent'" class="nav-btn">calender report</button></p>
      <p><button @click="currentPage = 'Journal_Insight'" class="nav-btn">Journal Insight</button></p>
    </div>

    <div style="flex-grow: 1; padding: 20px; background-color: #f3f4f6;">
      <dashboard_parent v-if="currentPage === 'dashboard_parent'" />
      <journal_insight v-if="currentPage === 'Journal_Insight'" />
      <addchild v-if="currentPage === 'add_child'" />
      <calender_report_parent v-if="currentPage === 'calender_report_parent'" />
    </div>
  </div>
</div>
<div v-else>
  <div style="display: flex; height: 100vh;">
    <div style="width: 250px; background-color: #1e3a8a; color: white; padding: 20px;">
      <p><button @click="currentPage = 'calender_report_child'" class="nav-btn">calender report</button></p>
      <p><button @click="currentPage = 'to_do_list'" class="nav-btn">to do list</button></p>
      <p><button @click="currentPage = 'story'" class="nav-btn">Story</button></p>
      <p><button @click="currentPage = 'journaling'" class="nav-btn">Journaling</button></p>
      <p><button @click="currentPage = 'infotainment'" class="nav-btn">infotainment</button></p>
    </div>

    <div style="flex-grow: 1; padding: 20px; background-color: #f3f4f6;">
      <dashboard_child v-if="currentPage === 'dashboard_child'" />
      <calender_report_child v-if="currentPage === 'calender_report_child'" />
      <to_do_list v-if="currentPage === 'to_do_list'" />
      <story v-if="currentPage === 'story'" />
      <journaling v-if="currentPage === 'journaling'" />
      <infotainment v-if="currentPage === 'infotainment'" />
    </div>
  </div>
</div>
</template>

<script>
import dashboard_parent from '../components/Dashboard_parent.vue'
import journal_insight from '../components/Journal_Insight.vue'
import addchild from '../components/addchild.vue'
import calender_report_parent from '../components/calender_report_parent.vue'

import dashboard_child from '../components/Dashboard_child.vue'
import calender_report_child from '../components/calender_report_child.vue'
import to_do_list from '../components/to_do_list.vue'
import story from '../components/story.vue'
import journaling from '../components/journaling.vue'
import infotainment from '../components/infotainment.vue'

export default {
  name: 'Side_Panel',
  components: {
    dashboard_parent,
    addchild,
    calender_report_parent,
    journal_insight,
    dashboard_child,
    calender_report_child,
    to_do_list,
    story,
    journaling,
    infotainment,
  },
  data() {
  const role = 'child'; // hardcoded in real time it ll be fetch from localStorage

  return {
    role,
    currentPage: role === 'child' ? 'dashboard_child' : 'dashboard_parent',
  };
  },
}
</script>

<style scoped>
.nav-btn {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  font-weight: bold;
  background-color: #60a5fa;
  color: black;
  border: none;
  cursor: pointer;
}
.nav-btn:hover {
  background-color: #3b82f6;
  color: white;
}
</style>
