export default {
  name: 'StoryPage',
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
      <div class="d-flex" style="height: calc(100vh - 50px); overflow: hidden; background-color: white;">
        
        <!-- Sidebar -->
        <div class="bg-light p-3 border-right" style="width: 200px;">
          <a
            v-for="(item, index) in sidebarItems"
            :key="index"
            href="#"
            class="btn btn-block text-left mb-2"
            :style="activeIndex === index ? activeStyle : inactiveStyle"
            @click.prevent="activeIndex = index"
          >
            {{ item }}
          </a>
        </div>

        <!-- Main Content -->
        <div class="flex-grow-1 d-flex flex-column align-items-center justify-content-center p-4">
          <div style="background-color: #d9d9d9; padding: 20px; max-width: 500px; border-radius: 8px; width: 100%;">
            <h5 class="text-center font-weight-bold">Write Your Story</h5>
            <textarea
              v-model="storyText"
              class="form-control mt-3"
              rows="10"
              placeholder="Story will be added..."
              style="resize: none;"
            ></textarea>
          </div>
          <button class="btn btn-outline-primary mt-4 px-4" @click="submitStory">Quiz</button>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      sidebarItems: ['Calendar Report', 'To-Do List', 'Story', 'Journaling', 'Infotainment'],
      activeIndex: 2,
      storyText: '',
      activeStyle: {
        backgroundColor: '#0084ff',
        color: 'white',
        fontWeight: 'bold',
        borderRadius: '6px'
      },
      inactiveStyle: {
        backgroundColor: '#f8f9fa',
        color: '#000'
      }
    };
  },
  methods: {
    submitStory() {
      if (this.storyText.trim() !== '') {
        alert('Story saved! You can now take the quiz.');
        this.$router.push('/quiz'); // Change path if needed
      } else {
        alert('Please write a story before proceeding to the quiz.');
      }
    }
  }
};
