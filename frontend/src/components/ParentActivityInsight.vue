<template>
  <div class="container py-4">
    <h2 class="mb-4 fw-bold">Activity Insight</h2>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2 text-muted">Loading activity data...</p>
    </div>

    <!-- No Children Found State -->
    <div v-else-if="noChildrenFound" class="text-center bg-light p-4 p-md-5 rounded-3">
        <i class="bi bi-person-plus-fill display-4 text-primary mb-3"></i>
        <h4 class="fw-semibold">No Child Profile Found</h4>
        <p class="text-muted">Please add a child profile first to view their activity insights.</p>
        <router-link to="/parent/add_child" class="btn btn-primary-custom mt-2">
            <i class="bi bi-plus-circle me-2"></i>Add Child Profile
        </router-link>
    </div>

    <!-- Main Content State -->
    <div v-else>
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
    const isLoading = ref(true)
    const noChildrenFound = ref(false)

    const tabs = [
      { name: 'Journal', route: 'journal' },
      { name: 'To-Do List', route: 'to-do-list' },
      { name: 'Story', route: 'story' },
      { name: 'Infotainment', route: 'infotainment' }
    ]

    const fetchChildren = async () => {
      isLoading.value = true;
      try {
        const token = localStorage.getItem('access_token')
        const res = await fetch('http://localhost:5000/parent/children', {
          headers: { Authorization: `Bearer ${token}` }
        })
        if (!res.ok) {
            // If the response is not OK (e.g., 404), assume no children
            throw new Error('No children found or failed to fetch.');
        }
        const data = await res.json()
        const childList = data.children || data; // Adjust based on your API response structure
        
        if (Array.isArray(childList) && childList.length > 0) {
            children.value = childList;
            selectedChildId.value = childList[0].id;
            noChildrenFound.value = false;
        } else {
            noChildrenFound.value = true;
        }
      } catch (err) {
        console.error('Failed to load children', err)
        noChildrenFound.value = true; // Set to true on error as well
      } finally {
          isLoading.value = false;
      }
    }

    onMounted(fetchChildren)

    return {
      tabs,
      children,
      selectedChildId,
      selectedDate,
      isLoading,
      noChildrenFound
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 1100px;
}

h2 {
  color: #0d6efd;
  font-size: 26px;
  border-left: 6px solid #0d6efd;
  padding-left: 12px;
  letter-spacing: 0.5px;
}

.form-label {
  font-size: 15px;
  color: #495057;
}

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

.btn-primary-custom {
    background-color: #0d6efd;
    color: white;
    border-radius: 25px;
    padding: 10px 25px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.btn-primary-custom:hover {
    background-color: #0b5ed7;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
}

.d-flex.gap-3 {
  flex-wrap: wrap;
  justify-content: flex-start;
}

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
