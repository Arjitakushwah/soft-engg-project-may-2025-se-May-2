import { createApp } from 'vue'
import { createPinia } from 'pinia'
import 'bootstrap-icons/font/bootstrap-icons.css'
import App from './App.vue'
import router from './router'
// import { initializeDummyData } from './stores/setup'
// initializeDummyData()
const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
