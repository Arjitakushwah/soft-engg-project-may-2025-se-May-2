export default {
  name: 'ToDoListPage',
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

      <!-- Main Layout -->
      <div class="d-flex" style="height: calc(100vh - 50px); overflow: hidden;">
        
        <!-- Sidebar -->
        <div class="bg-light p-3 border-right" style="width: 200px;">
          <a
            v-for="(item, index) in sidebarItems"
            :key="index"
            href="#"
            class="btn btn-block text-left mb-2"
            :class="activeIndex === index ? 'btn-primary text-white font-weight-bold' : 'btn-light'"
            @click.prevent="activeIndex = index"
          >
            {{ item }}
          </a>
        </div>

        <!-- Main Content Area -->
        <div class="flex-grow-1 p-4 bg-white d-flex flex-column">
          <div class="border px-3 py-1 mb-3" style="background-color: #fef3b8; width: fit-content;">
            19 June 2025
          </div>

          <!-- Add Task Button -->
          <button class="btn btn-outline-dark mb-3 ml-auto" @click="showForm = !showForm">
            Add New Task
          </button>

          <!-- New Task Form -->
          <div v-if="showForm" class="mb-3 d-flex">
            <input
              type="text"
              v-model="newTask"
              class="form-control mr-2"
              placeholder="Enter task name"
              style="max-width: 300px;"
            />
            <button class="btn btn-success" @click="addTask">Add</button>
          </div>

          <!-- Task List -->
          <h5><strong>Tasks for today</strong></h5>
          <div v-for="(task, index) in tasks" :key="index" class="d-flex justify-content-between align-items-center border-bottom py-2">
            <span>{{ task.name }}</span>
            <span
              class="badge px-3 py-1"
              :style="{
                backgroundColor: task.status === 'completed' ? 'green' : 'red',
                color: 'white',
                cursor: 'pointer',
                fontWeight: 'bold'
              }"
              @click="toggleStatus(task)"
            >
              {{ task.status === 'completed' ? 'Completed' : 'Pending' }}
            </span>
          </div>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      sidebarItems: ['Calendar Report', 'To-Do List', 'Story', 'Journaling', 'Infotainment'],
      activeIndex: 1,
      showForm: false,
      newTask: '',
      tasks: [
        { name: 'School', status: 'completed' },
        { name: 'Lunch', status: 'completed' },
        { name: 'Homework', status: 'pending' },
        { name: 'Tuition', status: 'pending' },
        { name: 'Football', status: 'pending' }
      ]
    };
  },
  methods: {
    toggleStatus(task) {
      task.status = task.status === 'pending' ? 'completed' : 'pending';
    },
    addTask() {
      if (this.newTask.trim() !== '') {
        this.tasks.push({ name: this.newTask.trim(), status: 'pending' });
        this.newTask = '';
        this.showForm = false;
      }
    }
  }
};
