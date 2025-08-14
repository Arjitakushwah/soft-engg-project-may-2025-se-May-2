# soft-engg-project-may-2025-se-May-2

## Project Overview
A comprehensive AI-powered child and parent engagement platform built with a Python backend (Flask/FastAPI) and a Vue.js frontend .  
The system offers mood classification, news curation, storytelling, analytics, streak and badge tracking, email notifications, and an AI-driven analytics Report for children.

## Project Team
- **Arjita Singh Kushwaha**
- **Jyoti Singh**
- **Shruti Kumari**
- **Praveen**
- **Anand Ratna Maurya**
- **Akash Tyagi**
- **Shalini Chaudhary**

---

## Project Structure
```
soft-engg-project-may-2025-se-May-2/
├── backend/
│   ├── agents/                  # AI agents for mood, news, story, and reporting
│   │   ├── child_analysis_report.md
│   │   ├── mood_classifier.py
│   │   ├── news_agent.py
│   │   ├── report_agent.py
│   │   └── story_agent.py
│   ├── instance/
│   │   └── project.db            # SQLite database file
│   ├── migrations/               # Database migration files
│   ├── tests/                    # Backend test suite
│   ├── api.py                    # API route definitions
│   ├── api.yaml                  # OpenAPI/Swagger specification
│   ├── app.py                    # Backend application entry point
│   ├── client_secret.json        # Google API credentials
│   ├── config.py                 # Configuration settings
│   ├── conftest.py               # Pytest configuration file
│   ├── models.py                 # SQLAlchemy models
│   ├── prod.env                  # Production environment variables
│   ├── exaa.env                  # Example environment variables
│   ├── progressor.py             # Progress tracking logic
│   ├── report_pdf.py             # PDF generation logic
│   ├── requirements.txt          # Python dependencies
│   ├── send_email.py             # Email sending utility
│   ├── setup_db.py               # Database initialization script
│   ├── streak_badges_logic.py    # Streak and badge logic
│   └── utils.py                  # Utility/helper functions
│
├── frontend/
│   ├── public/                   # Public static assets
│   │   ├── U1.jpeg
│   │   ├── U2.jpeg
│   │   ├── U3.jpeg
│   │   ├── child.png
│   │   ├── child2.jpg
│   │   └── parent.jpg
│   ├── src/
│   │   ├── assets/
│   │   │   ├── styles/
│   │   │   │   ├── HomePage.css
│   │   │   │   ├── base.css
│   │   │   │   └── badges.js
│   │   ├── components/           # Vue single-file components
│   │   │   ├── AddChild.vue
│   │   │   ├── ChildCalender.vue
│   │   │   ├── ChildDashboard.vue
│   │   │   ├── ChildEditProfile.vue
│   │   │   ├── ChildHome.vue
│   │   │   ├── ChildInfotainment.vue
│   │   │   ├── ChildJournal.vue
│   │   │   ├── ChildStory.vue
│   │   │   ├── ChildToDoList.vue
│   │   │   ├── Error404.vue
│   │   │   ├── ForgotPassword.vue
│   │   │   ├── ForgotUsername.vue
│   │   │   ├── GoogleAuthCallBack.vue
│   │   │   ├── HomePage.vue
│   │   │   ├── InfoResult.vue
│   │   │   ├── Loader.vue
│   │   │   ├── Login.vue
│   │   │   ├── Nav.vue
│   │   │   ├── ParentActivityInsight.vue
│   │   │   ├── ParentCalendar.vue
│   │   │   ├── ParentDashboard.vue
│   │   │   ├── ParentEditProfile.vue
│   │   │   ├── ParentHome.vue
│   │   │   ├── ParentInfotainmentInsight.vue
│   │   │   ├── ParentJournalAnalysis.vue
│   │   │   ├── ParentStoryInsight.vue
│   │   │   ├── ParentToDoInsight.vue
│   │   │   ├── Register.vue
│   │   │   ├── ResetPassword.vue
│   │   │   ├── Sidebar.vue
│   │   │   └── checkotp.vue
│   │   ├── router/
│   │   │   └── index.js           # Vue Router configuration
│   │   ├── stores/
│   │   │   ├── counter.js
│   │   │   └── setup.js
│   │   ├── App.vue                # Root Vue component
│   │   └── main.js                # Vue app entry point
│   ├── index.html                 # HTML entry file
│   ├── package.json               # Frontend dependencies
│   ├── vite.config.js             # Vite configuration
│   └── vitest.config.js           # Vitest test configuration
```

---

## Prerequisites

### Backend
- Python 3.9+
- Virtual environment tool (venv, pipenv, or conda)

### Frontend
- Node.js v18+
- npm v9+
- Modern browser (Chrome/Firefox/Edge)
- Internet connection (for Google Auth, external APIs)

---

## Setup Instructions

### Backend Setup
   1. Navigate to the backend directory:
   ```bash
    cd backend
   ```
   2. Create and activate a virtual environment:
   ```bash
    python -m venv venv
    source venv/scripts/activate  # Windows: venv\Scripts\activate
   ```
   3. Install dependencies:
   ```bash
    pip install -r requirements.txt
   ```
   4. Set up environment variables:
   ```
    cp exaa.env prod.env          # Copy and configure environment variables
   ```
   5. Create Database and Add initial data:
   ```
    python seed_data.py
   ```
   6. Initialize the database:
   ```
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
   ```
   8. Run Backend server:
   ```
    python app.py             
   ```

---
### Google API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project **or** select an existing one.
3. In the left menu, navigate to **"APIs & Services" → "Dashboard"**.
4. Click **"+ ENABLE APIS AND SERVICES"** and enable the required Google APIs for your project.
5. Go to **"APIs & Services" → "Credentials"**.
6. Click **"Create Credentials" → "OAuth client ID"** (or API key if needed).
7. For OAuth, download the generated JSON file — it will be named something like `client_secret.json`.
8. Place this file in the **`backend`** folder of the project (next to `app.py`).
9. Make sure `.gitignore` includes `client_secret.json` so it’s not uploaded to version control.

### Email Notifications (OTP, Credential, and Confirmation)

The backend includes email-based communication for account security and updates.

**Features:**
- **Send OTP** – When a user initiates signup, password reset, or sensitive profile changes, a One-Time Password is generated and sent to their registered email.
- **Send Credentials** – On successful account creation (for child or parent), login credentials or a Google OAuth link are sent via email.
- **Confirmation Emails** – After actions like password reset, account update, or report generation, a confirmation email is sent to notify the user.

### Configuration (Gmail SMTP example)
1. Go to your [Google Account](https://myaccount.google.com/).
2. Navigate to **Security** → enable **2-Step Verification**.
3. In the search bar, type **"App Passwords"**.
4. Select the app (e.g., "Mail") and device name, then click **Generate**.
5. Copy the generated pass key (format: `XXXX XXXX XXXX XXXX`).
6. Set up your `prod.env` file with:
   ```env
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASSWORD=XXXX XXXX XXXX XXXX
   ```
 ### Adding EXA API Key

- Sign up for an account at EXA API (https://exa.ai/).

- Generate your API key.

- Add it to exaa.env:

  ```
    EXA_API_KEY=your_exa_api_key_here
  ```

### Adding Google Gemini Flash 2.0 API Key

- Go to Google AI Studio.

- Generate a Gemini Flash 2.0 API key.

- Add to prod.env:

  ```
    GEMINI_API_KEY=your_gemini_flash_2_api_key_here
  ```
### JWT Secret Keys
- Visit https://jwtsecret.com/generate
- Set the length parameter to 128
- Click "Generate Secret Key"
- Copy the generated key and add it to config.py file

   ```
     JWT_SECRET_KEY = "ENTER GENERATED KEY"
   ```
  ---

### Frontend Setup

   1. Navigate to the frontend directory:
      
     cd frontend
    
   2. Install dependencies:
      
     npm install
    
   3. Run frontend server:
      
     npm run dev

---

## Quickstart

**Start Backend**

   1. Navigate to the backend directory:
      
     cd backend
    
   2. Activate the virtual environment(if not activated):
      
     source venv/scripts/activate
    
   3. Start the Flask development server::
      
     python app.py
   Server runs at: (http://localhost:5000)

**Start Frontend**
   1. Navigate to the Frontend directory:

     cd frontend
     
   2. Start the Vue development server:
      
     npm run dev
  
   App runs at: (http://localhost:5173)

---

## Feature Walkthrough

1. **Authentication**
   
   - Navigate to http://localhost:8080/
   - Login as Parent with "parent1" and "Parent@123" as username and password respectively.
   - Login as Child with "child1" and "Child@123" as username and password respectively.
   - Register with new credentials or use Google OAuth SignIn as parent role then add child to get child credential.

3. **Child Dashboard**
   
   When logged in as a Child, the dashboard displays:
    Statistics:
    - Longest streak
    - Total badges earned
    - All milestones with corresponding badges
    
    Sidebar Features:
    - Calendar report
    - To-Do Task Manager
    - Story
    - Journaling
    - Infotainment
 4. **To-Do Task Manager Rules**

    Creating Tasks:
      - A child can create a task with a specific date and time.
    
    Updating Task Status:
      Not allowed:
       - Update past date/time tasks.
       - Mark as complete a task scheduled for a future day.

      Allowed:
       - Mark as complete only within 15 minutes before the scheduled time up to 1 hour after the scheduled time.

    Deleting Tasks:
      Not allowed:
      - Delete completed tasks.
      - Delete any past-date tasks (whether completed or not).
    
 6. **Story Reading**

    Generate a Story:
     - Child provides a prompt (topic or idea) for the story.
     - System generates a unique, AI-powered story based on the given prompt.

    Start a Quiz:
      - After reading, child can take a quiz related to the story content.
      - Options are shuffled after every wrong answer.

 7. **Journaling**

    Write Journal Entries:
      - Child can write short statements or reflections multiple times throughout the day.
      - Entries can express how they are feeling, what happened, or any personal thoughts.

    Mood Classification:
      - System uses a mood classifier to analyze the journal text.
      - Determines the child’s emotional state (e.g., happy, sad, Anaxious, excited).

    Parent Visibility:
      - Classified moods and journal summaries are visible to the parent account.
      - Helps parents track emotional well-being over time.
   
  8. **Infotainment**

     Topic Selection:
       - Child can choose from topics like Science, History, and more.

     Child-Friendly News Generation:
       - System generates a news article tailored for children simple language, age-appropriate, and engaging.

     Reading & Marking as Read:
       - Child reads the generated article.
       - "Mark as Read" button becomes available only after 3 minutes to encourage proper reading time.
  9. **Calendar Report**

     Availability:
       - Accessible in both Child Dashboard and Parent Dashboard.

     Purpose:
       - Allows both child and parent to view tasks for any selected date.
     Features:
       - Displays all tasks for that date with clear status indicators Completed or Not Completed.

  10. **Parent Dashboard**

      Child Management:
        - View all added children’s profiles and details.
        - Add new child accounts with credentials.

      Calendar Report:
        - Same as in the child dashboard, lets parent view tasks done/not done for any selected date.

      Reports:
        - Download Weekly AI-Generated Report for a particular child.

      Statistics & Insights:
        - View all performance stats of the child.
        - Access a real-time data graph showing all tasks completed by the child.

---
### Some important component

- **Mood Classification** - Detects child’s emotional state from journal entries or activities.  
- **News Agent** – Fetches curated child-friendly news.  
- **Story Agent** – Generates personalized bedtime or educational stories.  
- **Report Agent** – Compiles child’s activity report in PDF.  
- **Progress Tracker** – Visualizes child’s progress via streaks and badges.  
- **Parent Dashboard** – Parents get detailed insights on child’s activities, moods, and learning.  
- **Email Notifications** – Sends OTP, Credential, and Confirmation.  

---








