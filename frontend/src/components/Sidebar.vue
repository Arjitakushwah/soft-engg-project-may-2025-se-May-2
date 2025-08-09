<template>
  <div class="sidebar" :class="{ collapsed: isCollapsed }">
    <!-- Collapse Toggle Button -->
    <button class="collapse-toggle" @click="toggleCollapse">
      <i :class="isCollapsed ? 'bi bi-arrow-bar-right' : 'bi bi-arrow-bar-left'"></i>
    </button>

    <!-- Navigation Buttons -->
    <div class="nav-section">
      <button
        v-for="item in navItems"
        :key="item.name"
        class="btn nav-btn mb-2"
        :class="{ active: currentRoute === item.route }"
        @click="navigate(item.route)"
      >
        <i v-if="isCollapsed" :class="item.icon"></i>
        <span v-else>{{ item.name }}</span>
      </button>
    </div>
  </div>
</template>

<script>
import { useRoute, useRouter } from 'vue-router';
import { ref, computed } from 'vue';
  
  export default {
    props: ['role'],
    emits: ['navigate'],
    setup(props, { emit }) {
      const router = useRouter();
      const route = useRoute();
      const isCollapsed = ref(false);
  
      const parentNavItems = [
        { name: 'Home', route: 'ParentHome', icon: 'bi bi-house-door' },
        {name: 'Add Child', route: 'AddChild', icon: 'bi bi-person-plus'},
        { name: 'Calendar', route: 'ParentCalendar', icon: 'bi bi-calendar3' },
        { name: 'Activity Insights', route: 'ParentActivityInsight', icon: 'bi bi-graph-up' },

      ];
  
      const childNavItems = [
      { name: 'Home', route: 'ChildHome', icon: 'bi bi-house-door' },
        { name: 'Calendar', route: 'ChildCalender', icon: 'bi bi-calendar3' },
        { name: 'To Do List', route: 'ChildToDoList', icon: 'bi bi-list-check' },
        { name: 'Story', route: 'ChildStory', icon: 'bi bi-book' },
        { name: 'Journaling', route: 'ChildJournal', icon: 'bi bi-journal-text' },
        { name: 'Infotainment', route: 'ChildInfotainment', icon: 'bi bi-tv' },
      ];
  
      const navItems = computed(() => {
        return props.role === 'parent' ? parentNavItems : childNavItems;
      });
  
      const toggleCollapse = () => {
        isCollapsed.value = !isCollapsed.value;
      };
  
      const navigate = (routeName) => {
        router.push({ name: routeName });
        emit('navigate', routeName);
      };
  
      const currentRoute = computed(() => route.name);
  
      return {
        isCollapsed,
        navItems,
        toggleCollapse,
        navigate,
        currentRoute
      };
    }
  };
  </script>

<style scoped>
.sidebar {
  width: 160px;
  transition: width 0.3s ease;
  background:  #756bdb;
  font-family: 'Comic Neue', cursive;
  height: 100vh;
  padding: 10px;
  overflow: hidden;
}

.sidebar.collapsed {
  width: 70px;
}

.collapse-toggle {
  background: none;
  border: none;
  font-size: 1.5rem;
  margin-bottom: 10px;
  cursor: pointer;
  color: white;
  display: flex;
  justify-content: flex-end;
  width: 100%;
}

.nav-btn {
  width: 100%;
  text-align: left;
  font-size: 1.1rem;
  padding: 10px;
  border: none;
  background-color: transparent;
  color: white;
  font-weight: bold;
  display: flex;
  align-items: center;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.nav-btn:hover {
  background-color: #F7D96f;
  color: #4A4A4A;
  font-weight: bold;
}

.nav-btn.active {
  background-color: #F7D96f;
    color: #4A4A4A;
  font-weight: bold;
}

.nav-btn i {
  font-size: 1.2rem;
}
.sidebar.collapsed .nav-btn {
    justify-content: center;
  }
</style>
