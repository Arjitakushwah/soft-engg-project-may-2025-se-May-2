export default {
  name: 'CalendarReport',
  template: `
    <div>
      <!-- Header -->
      <div class="d-flex justify-content-between align-items-center px-3 py-2" style="background-color: #171616; color: white; height: 50px;">
        <div><strong>Hi Riyansh</strong></div>
        <div>
          <button class="btn btn-primary btn-sm mr-2" @click="$router.push('/')">Home</button>
          <button class="btn btn-primary btn-sm" @click="$router.push('/login')">Logout</button>
        </div>
      </div>

      <!-- Main Container -->
      <div class="d-flex" style="height: calc(100vh - 50px); overflow: hidden;">
        
        <!-- Sidebar -->
        <div class="bg-light p-2 border-right" style="width: 200px;">
          <a v-for="(item, index) in sidebarItems"
             :key="index"
             href="#"
             class="btn btn-block text-left mb-2"
             :class="activeIndex === index ? 'btn-primary text-white font-weight-bold' : 'btn-light'"
             @click="activeIndex = index">
            {{ item }}
          </a>
        </div>

        <!-- Content Area -->
        <div class="flex-grow-1 p-3 bg-white d-flex flex-column">
          <div class="border px-3 py-1 mb-3" style="background-color: #fef3b8; width: fit-content;">
            {{ sidebarItems[activeIndex] }}
          </div>
          <div id="calendar" style="flex-grow: 1;"></div>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      sidebarItems: ['Calendar Report', 'To-Do List', 'Story', 'Journaling', 'Infotainment'],
      activeIndex: 0
    };
  },
  mounted() {
    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      height: '100%',
      events: [
        { title: 'Event 1', start: '2025-06-20' },
        { title: 'Event 2', start: '2025-06-25' }
      ]
    });
    calendar.render();
  }
};
