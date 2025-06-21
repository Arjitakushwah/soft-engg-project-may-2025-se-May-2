export default {
  template: `
    <div>
      <!-- Header -->
      <div style="display: flex; justify-content: space-between; padding: 10px 20px; background-color: #171616; border-bottom: 2px solid black; font-weight: bold;">
        <div style="color: white;">Hi Riyansh</div>
        <div style="margin-left: auto;">
          <button style="background-color:#007bff; color:white; border:none; padding:5px 10px; border-radius:5px;">Logout</button>
        </div>
      </div>

      <!-- Container -->
      <div style="display: flex; height: calc(100vh - 50px);">
        <!-- Sidebar -->
        <div style="width: 200px; background-color: #f2f2f2; color: black; display: flex; flex-direction: column; padding: 10px; border-right: 1px solid #ccc;">
          <a href="#" 
             v-for="(item, index) in sidebarItems" 
             :key="index"
             :style="getSidebarStyle(index)">
             {{ item }}
          </a>
        </div>

        <!-- Main Content -->
        <div style="padding: 20px; flex-grow: 1; background-color: white;">
          <div style="display: inline-block; border: 1px solid black; padding: 5px 10px; background-color: #fef3b8; margin-bottom: 20px;">
            Your Profile
          </div>

          <p><strong>Streak</strong><br>6 days</p>

          <p><strong>Badges</strong></p>
          <div style="font-size: 30px;">
            <span style="color: gold;">★</span>
            <span style="color: gold;">★</span>
            <span style="color: gold;">★</span>
            <span style="color: lightgray;">★</span>
            <span style="color: lightgray;">★</span>
          </div>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      sidebarItems: [
        'Calendar Report',
        'To-Do List',
        'Story',
        'Journaling',
        'Infotainment'
      ],
      activeIndex: null // or set default active like 0
    };
  },
  methods: {
    getSidebarStyle(index) {
      const isActive = index === this.activeIndex;
      return {
        padding: '10px 15px',
        textDecoration: 'none',
        color: isActive ? 'white' : 'black',
        fontWeight: isActive ? 'bold' : 'normal',
        margin: '5px 0',
        borderRadius: '8px',
        backgroundColor: isActive ? '#007bff' : 'transparent',
        cursor: 'pointer'
      };
    }
  }
};
