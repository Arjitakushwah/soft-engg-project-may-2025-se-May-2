<template>
  <div class="activity-insight-container">
    <div class="header-section">
      <h2 class="page-title">Progress Tracker</h2>
      <p class="page-subtitle">Track and analyze your child's learning activities and progress</p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <div class="spinner-border text-purple" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="loading-text">Loading activity data...</p>
    </div>

    <!-- No Children Found State -->
    <div v-else-if="noChildrenFound" class="no-children-container">
        <div class="no-children-card">
          <i class="bi bi-person-plus-fill no-children-icon"></i>
          <h4 class="no-children-title">No Child Profile Found</h4>
          <p class="no-children-text">Please add a child profile first to view their activity insights.</p>
          <router-link to="/parent/add_child" class="btn btn-primary-custom">
              <i class="bi bi-plus-circle me-2"></i>Add Child Profile
          </router-link>
        </div>
    </div>

    <!-- Main Content State -->
    <div v-else class="main-content">
      <!-- Selectors Card -->
      <div class="selectors-card">
        <div class="row g-4">
          <div class="col-md-6">
            <label class="form-label">Select Child</label>
            <select v-model="selectedChildId" class="form-select custom-select">
              <option v-for="child in children" :key="child.id" :value="child.id">
                {{ child.name }}
              </option>
            </select>
          </div>
          <div class="col-md-6">
            <label class="form-label">Select Date</label>
            <input type="date" v-model="selectedDate" class="form-control custom-input" />
          </div>
        </div>
      </div>

      <!-- Tabs Navigation -->
      <div class="tabs-container">
        <router-link
          v-for="tab in tabs"
          :key="tab.name"
          :to="`/parent/activity_analysis/${tab.route}`"
          class="tab-btn"
          :class="{ active: $route.path.includes(tab.route) }"
        >
          <i :class="getTabIcon(tab.route)" class="tab-icon"></i>
          {{ tab.name }}
        </router-link>
      </div>

      <!-- Router View for Tab Content -->
      <div class="tab-content-container">
        <router-view :selectedChildId="selectedChildId" :selectedDate="selectedDate" />
      </div>
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

    const getTabIcon = (route) => {
      const icons = {
        'journal': 'bi bi-journal-text',
        'to-do-list': 'bi bi-check2-square',
        'story': 'bi bi-book',
        'infotainment': 'bi bi-lightbulb'
      }
      return icons[route] || 'bi bi-activity'
    }

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
        const childList = data.children || data; 
        
        if (Array.isArray(childList) && childList.length > 0) {
            children.value = childList;
            selectedChildId.value = childList[0].id;
            noChildrenFound.value = false;
        } else {
            noChildrenFound.value = true;
        }
      } catch (err) {
        console.error('Error fetching children:', err);
        noChildrenFound.value = true;
      } finally {
        isLoading.value = false;
      }
    }

    onMounted(() => {
      fetchChildren()
    })

    return {
      tabs,
      children,
      selectedChildId,
      selectedDate,
      isLoading,
      noChildrenFound,
      getTabIcon
    }
  }
}
</script>

<style scoped>
.activity-insight-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Comic Neue', cursive;
  /* background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%); */
  background:white;
  min-height: 100vh;
}

.header-section {
  text-align: center;
  margin-bottom: 3rem;
  padding: 2rem 0;
}


.page-title {
  font-size: 2.2rem;
  color: #5A4FCF;
  margin-bottom: 1rem;
  font-family: 'Fredoka One', cursive;
}

.page-subtitle {
  color: #666;
  font-size: 1.1rem;
  margin: 0;
  opacity: 0.8;
}

/* Loading State */
.loading-container {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(117, 107, 219, 0.1);
  margin: 2rem 0;
}

.loading-text {
  color: #6c757d;
  font-size: 1.1rem;
  margin-top: 1rem;
  font-weight: 500;
}

/* No Children State */
.no-children-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.no-children-card {
  background: white;
  padding: 3rem;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 8px 32px rgba(117, 107, 219, 0.1);
  max-width: 500px;
  width: 100%;
}

.no-children-icon {
  font-size: 4rem;
  color: #756bdb;
  margin-bottom: 1.5rem;
  opacity: 0.8;
}

.no-children-title {
  color: #756bdb;
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
  font-family: 'Fredoka One', cursive;
}

.no-children-text {
  color: #6c757d;
  font-size: 1rem;
  margin-bottom: 2rem;
  line-height: 1.6;
}

/* Main Content */
.main-content {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(117, 107, 219, 0.1);
}

/* Selectors Card */
.selectors-card {
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
  padding: 1.5rem;
  border-radius: 15px;
  margin-bottom: 2rem;
  border: 1px solid rgba(117, 107, 219, 0.1);
}

.form-label {
  font-size: 1rem;
  color: #756bdb;
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-family: 'Fredoka One', cursive;
}

.custom-select,
.custom-input {
  border-radius: 12px;
  border: 2px solid #e9ecef;
  padding: 12px 16px;
  transition: all 0.3s ease;
  background: white;
  font-size: 1rem;
}

.custom-select:focus,
.custom-input:focus {
  border-color: #756bdb;
  box-shadow: 0 0 0 3px rgba(117, 107, 219, 0.1);
  outline: none;
}

/* Tabs Navigation */
.tabs-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
  justify-content: center;
}

.tab-btn {
  background: white;
  color: #756bdb;
  border: 2px solid #756bdb;
  border-radius: 25px;
  padding: 12px 24px;
  transition: all 0.3s ease;
  font-weight: 600;
  font-size: 1rem;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 12px rgba(117, 107, 219, 0.1);
}

.tab-btn:hover {
  background: #756bdb;
  color: white;
  text-decoration: none;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(117, 107, 219, 0.2);
}

.tab-btn.active {
  background: #756bdb;
  color: white;
  box-shadow: 0 6px 20px rgba(117, 107, 219, 0.3);
}

.tab-icon {
  font-size: 1.1rem;
}

/* Tab Content */
.tab-content-container {
  background: #f8f9ff;
  border-radius: 15px;
  padding: 2rem;
  min-height: 400px;
}

/* Button Styling */
.btn-primary-custom {
  background: linear-gradient(135deg, #756bdb 0%, #6155b1 100%);
  color: white;
  border: none;
  border-radius: 25px;
  padding: 12px 30px;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  box-shadow: 0 4px 12px rgba(117, 107, 219, 0.2);
}

.btn-primary-custom:hover {
  background: linear-gradient(135deg, #6155b1 0%, #4a3f8a 100%);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(117, 107, 219, 0.3);
  text-decoration: none;
}

/* Purple Color Class */
.text-purple {
  color: #756bdb !important;
}

/* Responsive Design */
@media (max-width: 768px) {
  .activity-insight-container {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .page-subtitle {
    font-size: 1rem;
  }
  
  .main-content {
    padding: 1.5rem;
  }
  
  .tabs-container {
    justify-content: flex-start;
    gap: 0.5rem;
  }
  
  .tab-btn {
    padding: 10px 16px;
    font-size: 0.9rem;
  }
  
  .no-children-card {
    padding: 2rem;
    margin: 1rem;
  }
  
  .no-children-icon {
    font-size: 3rem;
  }
}

@media (max-width: 480px) {
  .tabs-container {
    flex-direction: column;
  }
  
  .tab-btn {
    justify-content: center;
  }
}
</style>
