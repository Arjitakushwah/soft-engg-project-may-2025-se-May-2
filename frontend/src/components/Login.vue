<template>
  <div class="bg-light">
    <div class="d-flex justify-content-center align-items-center min-vh-100">
      <div class="card shadow p-4" style="width: 100%; max-width: 300px;">
        <h3 class="text-decoration-underline text-center mb-4">Log In</h3>
        <form @submit.prevent="login">
          <div class="mb-3">
            <div class="text-danger" v-if="error">*{{ error }}</div>
            <label for="email" class="form-label">Username</label>
            <input
              type="email"
              class="form-control"
              id="email"
              placeholder="name@example.com"
              v-model="cred.email"
              required
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input
              type="password"
              class="form-control"
              id="password"
              placeholder="Password"
              v-model="cred.password"
              required
            />
          </div>
          <div class="d-grid gap-2 d-md-flex justify-content-md-end">
            <router-link
              to="/register"
              class="text-decoration-underline me-md-auto mb-2 mb-md-0"
            >Sign Up</router-link>
            <button class="btn btn-primary me-md-2" type="submit">Log In</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      cred: {
        email: null,
        password: null,
      },
      error: null,
    };
  },
  methods: {
    async login() {
      try {
        const res = await fetch("/user-login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.cred),
        });

        const data = await res.json();

        if (res.ok) {
          localStorage.setItem("auth-token", data.token);
          localStorage.setItem("role", data.role);
          this.$router.push({ path: "/" });
        } else {
          this.error = data.message;
        }
      } catch (err) {
        this.error = "Something went wrong. Please try again.";
        console.error(err);
      }
    },
  },
};
</script>

<style scoped>
/* Optional: Add component-specific styles here */
</style>
