<template>
  <div class="container py-4">
    <h2 class="mb-4 fw-bold">Activity Insight</h2>

    <!-- Selectors -->
    <div class="row g-4 mb-4">
      <div class="col-md-6">
        <label class="form-label fw-semibold">Select Child</label>
        <select v-model="selectedChildId" class="form-select">
          <option v-for="child in children" :key="child.id" :value="child.id">
            {{ child.name }}
          </option>
        </select>
      </div>
      <div class="col-md-6">
        <label class="form-label fw-semibold">Select Date</label>
        <input type="date" v-model="selectedDate" class="form-control" />
      </div>
    </div>

    <!-- Tabs as Buttons -->
    <div class="mb-4 d-flex flex-wrap gap-3">
      <router-link
        v-for="tab in tabs"
        :key="tab.name"
        :to="`/parent/activity_analysis/${tab.route}`"
        class="tab-btn btn"
        :class="{ active: $route.path.includes(tab.route) }"
      >
        {{ tab.name }}
      </router-link>
    </div>

    <!-- Router View for Tab Content -->
    <router-view :selectedChildId="selectedChildId" :selectedDate="selectedDate" />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'ParentActivityInsight',
  setup() {
    const children = ref([])
    const selectedChildId = ref(null)
    const selectedDate = ref(new Date().toISOString().split('T')[0])

    const tabs = [
      { name: 'Journal', route: 'journal' },
      { name: 'To-Do List', route: 'to-do-list' },
      { name: 'Story', route: 'story' },
      { name: 'Infotainment', route: 'infotainment' }
    ]

    const fetchChildren = async () => {
      try {
        const token = localStorage.getItem('access_token')
        const res = await fetch('http://localhost:5000/parent/children', {
          headers: { Authorization: `Bearer ${token}` }
        })
        const data = await res.json()
        children.value = data.children || []
        if (children.value.length) {
          selectedChildId.value = children.value[0].id
        }
      } catch (err) {
        console.error('Failed to load children', err)
      }
    }

    onMounted(fetchChildren)

    return {
      tabs,
      children,
      selectedChildId,
      selectedDate
    }
  }
}
</script>

<style scoped>
.tab-btn {
  background-color: #f8f9fa;
  color: #0d6efd;
  border: 2px solid #0d6efd;
  border-radius: 30px;
  padding: 8px 20px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.tab-btn:hover {
  background-color: #0d6efd;
  color: white;
  text-decoration: none;
}

.tab-btn.active {
  background-color: #0d6efd;
  color: white;
  box-shadow: 0 4px 10px rgba(0, 123, 255, 0.2);
}
.container {
  max-width: 1100px;
}

/* Page Heading */
h2 {
  color: #0d6efd;
  font-size: 26px;
  border-left: 6px solid #0d6efd;
  padding-left: 12px;
  letter-spacing: 0.5px;
}

/* Form Labels */
.form-label {
  font-size: 15px;
  color: #495057;
}

/* Form Controls */
.form-select,
.form-control {
  border-radius: 12px;
  border: 1px solid #ced4da;
  padding: 10px 14px;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.form-select:focus,
.form-control:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 6px rgba(13, 110, 253, 0.3);
}

/* Tab Buttons */
.tab-btn {
  background-color: #f8f9fa;
  color: #0d6efd;
  border: 2px solid #0d6efd;
  border-radius: 25px;
  padding: 8px 22px;
  transition: all 0.3s ease;
  font-weight: 500;
  font-size: 15px;
}

.tab-btn:hover {
  background-color: #0d6efd;
  color: white;
  text-decoration: none;
  transform: translateY(-2px);
}

.tab-btn.active {
  background-color: #0d6efd;
  color: white;
  box-shadow: 0 4px 12px rgba(13, 110, 253, 0.25);
}

/* Tabs Layout */
.d-flex.gap-3 {
  flex-wrap: wrap;
  justify-content: flex-start;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  h2 {
    font-size: 22px;
  }
  .tab-btn {
    padding: 7px 16px;
    font-size: 14px;
  }
  .form-label {
    font-size: 14px;
  }
}

</style>
