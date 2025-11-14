# 🚀 Stellar AI - Complete Setup Guide for Non-Developers

This guide will help you get Stellar AI running on your computer **without any coding knowledge**. Just follow these steps exactly as written, and copy-paste the commands.

---

## ✅ What You Need Before Starting

Make sure you have these installed on your computer:

1. **Git** - [Download here](https://git-scm.com/downloads)
2. **Node.js** (version 18 or higher) - [Download here](https://nodejs.org/)
3. **Python** (version 3.11 or higher) - [Download here](https://www.python.org/downloads/)
4. **PostgreSQL** (version 15 or higher) - [Download here](https://www.postgresql.org/download/)

**How to check if they're installed:**
- Open Terminal (Mac) or Command Prompt (Windows)
- Type these commands one by one:
  ```bash
  git --version
  node --version
  python3 --version
  psql --version
  ```
- If any show "command not found", you need to install that program.

---

## 📥 STEP 1: Get the Code

### 1.1 Open Terminal / Command Prompt
- **Mac**: Press `Cmd + Space`, type "Terminal", press Enter
- **Windows**: Press `Win + R`, type "cmd", press Enter

### 1.2 Clone the Repository
Copy and paste this command exactly (press Enter after pasting):

```bash
git clone https://github.com/TMTS-maker/stellar-ai-mentor.git
```

### 1.3 Enter the Project Folder
```bash
cd stellar-ai-mentor
```

### 1.4 Switch to the Correct Branch
```bash
git checkout claude/stellar-ai-backend-mvp-01VfkPYYMnbksUgdLVXeA2at
```

You should see: `Switched to branch 'claude/stellar-ai-backend-mvp-01VfkPYYMnbksUgdLVXeA2at'`

---

## 🗄️ STEP 2: Set Up the Database

### 2.1 Start PostgreSQL
- **Mac**: PostgreSQL should start automatically. If not, run:
  ```bash
  brew services start postgresql
  ```
- **Windows**: PostgreSQL runs as a service. It should already be running.

### 2.2 Create the Database
Copy and paste this command:

```bash
createdb stellar_ai
```

If you get an error about "role does not exist", you need to create a PostgreSQL user first:

```bash
psql postgres
CREATE USER postgres WITH PASSWORD 'postgres';
ALTER USER postgres WITH SUPERUSER;
\q
```

Then try creating the database again:
```bash
createdb stellar_ai
```

### 2.3 Verify the Database Exists
```bash
psql -l
```

You should see `stellar_ai` in the list of databases.

---

## 🔧 STEP 3: Set Up the Backend

### 3.1 Navigate to the Backend Folder
```bash
cd backend
```

### 3.2 Install Python Dependencies
This will install all the backend libraries. It might take 2-3 minutes:

```bash
pip3 install -r requirements.txt
```

If you get a permissions error, try:
```bash
pip3 install --user -r requirements.txt
```

### 3.3 The Environment File is Already Created!
The `.env` file with all necessary settings has already been created for you in `backend/.env`.

**OPTIONAL - Add AI API Keys (if you want real AI features):**

If you want the AI conversation features to work, you need to add your API keys:

1. Open `backend/.env` in a text editor (Notepad, TextEdit, VS Code, etc.)
2. Find these lines and remove the `#` symbol, then add your key:
   ```
   # OPENAI_API_KEY=your-openai-api-key-here
   ```
   Should become:
   ```
   OPENAI_API_KEY=sk-your-actual-openai-key
   ```

**Where to get API keys:**
- OpenAI: https://platform.openai.com/api-keys
- ElevenLabs (optional): https://elevenlabs.io/
- Anthropic Claude (optional): https://console.anthropic.com/

**Without API keys:** The AI features will return placeholder responses. Everything else will work fine!

### 3.4 Run Database Migrations
This creates all the tables in the database:

```bash
alembic upgrade head
```

You should see something like:
```
INFO [alembic.runtime.migration] Running upgrade -> ..., Initial migration
```

### 3.5 Start the Backend Server
```bash
python3 -m uvicorn app.main:app --reload
```

**What you should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
Starting Stellar AI Backend...
INFO:     Application startup complete.
```

**✅ Success!** The backend is now running.

**IMPORTANT:** Keep this terminal window open! The backend needs to stay running.

---

## 💻 STEP 4: Set Up the Frontend

### 4.1 Open a NEW Terminal Window
Don't close the backend terminal! Open a **new** one:
- **Mac**: Press `Cmd + N` in Terminal
- **Windows**: Open a new Command Prompt window

### 4.2 Navigate to the Project (in the new terminal)
```bash
cd stellar-ai-mentor
```

(If you closed the terminal, use the full path to where you cloned the repo)

### 4.3 Install Frontend Dependencies
This will install all the React libraries. It might take 3-5 minutes:

```bash
npm install
```

You'll see a lot of text scrolling. This is normal! Wait for it to finish.

### 4.4 The Frontend .env is Already Created!
The `.env` file has already been created for you in the root folder.

It contains:
```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

This tells the frontend where to find the backend. You don't need to change anything!

### 4.5 Start the Frontend
```bash
npm run dev
```

**What you should see:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**✅ Success!** The frontend is now running.

---

## 🎉 STEP 5: Open Stellar AI in Your Browser

### 5.1 Open Your Web Browser
Open Chrome, Firefox, Safari, or Edge.

### 5.2 Go to These URLs:

**Frontend (Main Application):**
```
http://localhost:5173
```

**Backend API Documentation:**
```
http://localhost:8000/docs
```

**Backend Health Check:**
```
http://localhost:8000/health
```

If you see the Stellar AI homepage, **congratulations!** Everything is working!

---

## 🧪 STEP 6: Test the System

Now let's make sure everything works by going through some test flows.

### TEST 1: Sign Up as a Student

1. Go to http://localhost:5173
2. Look for a "Sign Up" or "Get Started" button and click it
3. Fill in:
   - **Email**: test-student@stellar.ai
   - **Password**: password123
   - **Full Name**: Test Student
   - **Role**: Select "Student"
   - **School ID**: (This might be optional for MVP - leave blank if not required)
4. Click "Sign Up"
5. You should be redirected to a login page or dashboard

### TEST 2: Log In and View Dashboard

1. If not already logged in, go to http://localhost:5173/login
2. Enter:
   - **Email**: test-student@stellar.ai
   - **Password**: password123
3. Click "Log In"
4. You should see the **Student Dashboard** with:
   - Your name displayed
   - XP Progress (might show 0 to start)
   - Tasks section
   - Gamification elements (rings, plant, etc.)

### TEST 3: Check Gamification Data

While on the Student Dashboard:

1. Look for:
   - **XP Progress** bar or counter
   - **Level** indicator (should start at level 0 or 1)
   - **Ring Progress** (3 rings: engagement, mastery, curiosity)
   - **Plant Growth** or similar gamification element

2. This data comes from the backend! If you see it, the frontend-backend integration is working.

### TEST 4: Start a Task (if available)

1. On the Student Dashboard, look for "Open Tasks" or "Available Tasks"
2. If you see any tasks:
   - Click "Start Task" or similar button
   - The task status should update

3. If no tasks are shown (normal for fresh database), you can:
   - Create a test task via the API (advanced)
   - Or skip this test for now

### TEST 5: AI Conversation (Text)

**Note:** This test depends on whether you've added an OpenAI API key.

1. Look for a "Chat with AI" or "Ask Stellar" button/section
2. Type a simple message like: "Hello, can you help me with math?"
3. Click Send

**Expected Results:**
- **With API Key**: You should get an actual AI response from GPT-4
- **Without API Key**: You'll get a message like:
  ```
  [LLM stub response - Please configure LLM_PROVIDER and API key in .env]
  ```

**Both are correct!** The system is working - it's just using a placeholder when no API key is present.

### TEST 6: Check Backend API

1. Go to http://localhost:8000/docs
2. You should see an interactive API documentation page (Swagger UI)
3. Try expanding some endpoints:
   - Click on `/auth/me` → Try it out → Execute
   - You might get a 401 error (that's normal - you need to be logged in via the API)

4. Go to http://localhost:8000/health
5. You should see:
   ```json
   {"status": "healthy"}
   ```

---

## ✅ You're Done!

If you completed all the tests above, **Stellar AI is fully working!**

You now have:
- ✅ Backend running on http://localhost:8000
- ✅ Frontend running on http://localhost:5173
- ✅ Database connected and working
- ✅ Authentication system functional
- ✅ Student dashboard with gamification
- ✅ AI conversation endpoints (with or without real AI)

---

## 🔄 How to Start/Stop the System

### To Stop Everything:
1. Go to each terminal window (backend and frontend)
2. Press `Ctrl + C` (or `Cmd + C` on Mac)
3. Type `y` if asked to confirm

### To Start Again Later:
1. **Terminal 1 - Start Backend:**
   ```bash
   cd stellar-ai-mentor/backend
   python3 -m uvicorn app.main:app --reload
   ```

2. **Terminal 2 - Start Frontend:**
   ```bash
   cd stellar-ai-mentor
   npm run dev
   ```

3. Open http://localhost:5173 in your browser

---

## ❓ Troubleshooting

### Problem: "createdb: command not found"
**Solution:** PostgreSQL is not installed or not in your PATH.
- Mac: Install with `brew install postgresql`
- Windows: Reinstall PostgreSQL and ensure "Add to PATH" is checked

### Problem: "Port 8000 is already in use"
**Solution:** Another program is using port 8000.
- Close any other applications that might be using port 8000
- Or change the port in `backend/.env`:
  ```
  PORT=8001
  ```
  Then update the frontend `.env`:
  ```
  VITE_API_BASE_URL=http://localhost:8001/api/v1
  ```

### Problem: "Cannot connect to database"
**Solution:** PostgreSQL is not running.
- Mac: `brew services start postgresql`
- Windows: Open Services and start "PostgreSQL"
- Or check that `DATABASE_URL` in `backend/.env` is correct

### Problem: Frontend shows errors in browser console
**Solution:** Backend might not be running.
- Make sure the backend terminal is still open and showing "Application startup complete"
- Check http://localhost:8000/health - should return `{"status": "healthy"}`

### Problem: "Module not found" errors when starting backend
**Solution:** Python dependencies not installed properly.
```bash
cd backend
pip3 install --user -r requirements.txt
```

### Problem: Login doesn't work
**Solution:**
1. Check backend terminal for error messages
2. Check browser console (F12) for errors
3. Verify you can access http://localhost:8000/docs
4. Try signing up a new user first

---

## 📞 Getting Help

If you're stuck:

1. Check the terminal output for error messages
2. Look in the browser console (Press F12 → Console tab)
3. Review the troubleshooting section above
4. Check the full README.md for technical details
5. Create an issue on GitHub with:
   - What step you were on
   - The exact error message
   - Screenshots if helpful

---

## 🎯 Next Steps

Once everything is running, you can:

1. **Explore Different Roles:**
   - Sign up as a Teacher, Parent, or School Admin
   - See how each dashboard looks different

2. **Add Real AI:**
   - Get an OpenAI API key
   - Add it to `backend/.env`
   - Restart the backend
   - Try the AI conversation feature!

3. **Customize:**
   - Add more tasks via the API
   - Create schools and classrooms
   - Invite other users

4. **Deploy:**
   - Follow the deployment section in README.md
   - Put it online so others can use it!

---

**Congratulations on setting up Stellar AI! 🎉**

You now have a fully functional AI-powered learning platform running locally on your computer.
