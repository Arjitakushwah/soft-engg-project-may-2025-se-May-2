export default {
  template: `
  <div class="bg-light">
  <div class="container d-flex justify-content-center align-items-center min-vh-100">
    <div class="card shadow p-4" style="width: 100%; max-width: 300px;">
      <h3 class="text-decoration-underline text-center mb-4">Log In</h3>
      <form>
        <div class="mb-3">
          <div class='text-danger'>*{{error}}</div>
          <label for="email" class="form-label">Username</label>
          <input type="email" class="form-control" id="email" placeholder="name@example.com" v-model="cred.email">
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" class="form-control" id="password" placeholder="Password" v-model="cred.password">
        </div>
        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
            <router-link to="/parent_signup" class="text-decoration-underline me-md-auto mb-2 mb-md-0">Sign Up</router-link>
            <button class="btn btn-primary me-md-2" type="button" @click='login'>Log In</button>
        </div>
      </form>
    </div>
  </div>
</div>`,
  data() {
    return {
      cred: {
        email: '',                
        password: '',
      },
      error: null,
    }
  },
  methods: {
    async login() {
      const res = await fetch('/user-login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.cred),
      });
      const data = await res.json();
      if (res.ok) {
        localStorage.setItem('auth-token', data.token);
        localStorage.setItem('role', data.role);
        localStorage.setItem('user', JSON.stringify(data.user)); // Save user info
        this.$router.push({ path: '/' });
      } else {
        this.error = data.message;
      }
    }
  }
}
