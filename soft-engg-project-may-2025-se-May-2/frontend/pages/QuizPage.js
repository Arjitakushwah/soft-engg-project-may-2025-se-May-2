export default {
  name: 'QuizPage',
  template: `
    <div>
      <!-- Header -->
      <div class="d-flex justify-content-between align-items-center px-3 py-2" style="background-color: #171616; color: white; height: 50px;">
        <div><strong>Quiz Time!</strong></div>
        <div>
          <button class="btn btn-primary btn-sm" @click="$router.push('/')">Home</button>
        </div>
      </div>

      <!-- Quiz Content -->
      <div class="container mt-4">
        <h4 class="mb-4 text-center">Answer these questions based on your story</h4>
        <div v-for="(q, index) in questions" :key="index" class="mb-3">
          <label><strong>Q{{ index + 1 }}: {{ q }}</strong></label>
          <input type="text" class="form-control mt-1" v-model="answers[index]" placeholder="Your answer" />
        </div>
        <div class="text-center mt-4">
          <button class="btn btn-success px-4" @click="submitQuiz">Submit Answers</button>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      questions: [
        "What is the name of the main character in your story?",
        "What did they find or do?",
        "How did the character feel during the story?",
        "Who else was in the story?",
        "What was the final outcome?"
      ],
      answers: ['', '', '', '', '']
    };
  },
  methods: {
    submitQuiz() {
      if (this.answers.every(ans => ans.trim() !== '')) {
        alert('Quiz submitted! Great job.');
        this.$router.push('/');
      } else {
        alert('Please answer all questions before submitting.');
      }
    }
  }
};
