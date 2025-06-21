export default {
  template: `
        <div class="bg-light">

        <div class="container d-flex justify-content-center align-items-center min-vh-100">
          <div class="card shadow p-4" style="width: 100%; max-width: 350px;">
            <h3 class="text-center mb-4"><h2>Parent Sign Up</h2></h3>
            <form>
              <div class="mb-3">
                <label for="name" class="form-label">Full Name</label>
                <input type="text" class="form-control" id="name" placeholder="Enter your full name" v-model="cred.full_name" required>
              </div>

              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input type="text" class="form-control" id="username" placeholder="Choose a username" v-model="cred.username" required>
              </div>

              <div class="mb-3">
                <label for="email" class="form-label">Email address</label>
                <input type="email" class="form-control" id="email" placeholder="Enter your email" v-model="cred.email" required>
              </div>

              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" placeholder="Create a password" v-model="cred.password" required>
              </div>
              <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                  <button class="btn btn-primary me-md-2" type="button" @click="signup">Sign Up</button>
              </div>
            </form>
          </div>
        </div>
      </div>`,
  data() {
    return {
      cred: {
        full_name: null,
        username: null,
        email: null,
        password: null,
      },
    };
  },
  methods: {
    async signup() {
      console.log(this.cred);
      const res = await fetch("/api/parent", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.cred),
      });
      if (res.ok) {
        const data = await res.json();
        this.$router.push({ path: "/login" });
      }
    },
  },
};