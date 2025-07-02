<template>
  <div class="bg-light">
    <div class="container d-flex justify-content-center align-items-center min-vh-100">
      <div class="card shadow p-4" style="width: 100%; max-width: 350px;">
        <h2 class="text-center mb-4">Parent Sign Up</h2>
        <form >
          <div class="mb-3">
            <label for="name" class="form-label">Name</label>
            <input
              type="text"
              class="form-control"
              id="name"
              placeholder="Enter your name"
              v-model="cred.name"
              required
            />
          </div>

          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input
              type="text"
              class="form-control"
              id="username"
              placeholder="Choose a username"
              v-model="cred.username"
              required
            />
          </div>
          <div class="mb-3">
            <label for="email" class="form-label">Email address</label>
            <input
              type="email"
              class="form-control"
              id="email"
              placeholder="Enter your email"
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
              placeholder="Create a password"
              v-model="cred.password"
              required
            />
          </div>

          <div class="d-grid gap-2 d-md-flex justify-content-md-end">
            <button class="btn btn-primary me-md-2" type="submit" @click="signup">Sign Up</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Parent_signup",
  data() {
    return {
      cred: {
        name: null,
        username: null,
        email: null,
        password: null,
      },
    };
  },
  methods: {
    async signup() {
      try {
        console.log(this.cred)
        const res = await fetch('http://127.0.0.1:5000/register', {
          method: 'POST',
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.cred),
        });

        if (res.ok) {
          const data = await res.json();
          this.$router.push({ path: "/login" });
        } else {
          const errorData = await res.json();
          console.error("Signup failed:", errorData.message);
        }
      } catch (err) {
        console.error("Network or server error:", err);
      }
    },
  },
};
</script>

<style scoped>
/* Add optional component-specific styles here */
</style>
