import Navbar from '../components/navbar.js';
import router from '../utils/router.js';
import store from '../utils/store.js';

new Vue({
    el: '#app',
    template: `
        <div class="app-container">
            <Navbar v-if="!isAuthRoute" />
            <div class="content-container">
                <router-view></router-view>
            </div>
        </div>
    `,
    components: {
        Navbar
    },
    computed: {
        isAuthRoute() {
            return ['/login', '/register'].includes(this.$route.path)
        }
    },
    created() {
        const user = JSON.parse(localStorage.getItem('user'));
        if (user) {
            this.$store.commit('setUser', user);
        }
    },
    router,
    store
})