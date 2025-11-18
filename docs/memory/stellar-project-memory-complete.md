# STELLAR AI – Lovable Project Memory (Complete Technical Specification)

**Project:** Stellar AI Landing Page & Platform MVP  
**Platform:** Lovable.dev  
**Version:** 2.0 (Comprehensive Rebuild)  
**Date:** November 2025  
**Status:** Active Development  

---

## 📋 TABLE OF CONTENTS

1. [Project Overview](#project-overview)
2. [Core Architecture](#core-architecture)
3. [Database Schema (Supabase)](#database-schema-supabase)
4. [Authentication & Role-Based Access Control](#authentication--role-based-access-control)
5. [Landing Page Features](#landing-page-features)
6. [Interactive Features & Components](#interactive-features--components)
7. [Demo & Customer Journey](#demo--customer-journey)
8. [Design System & Styling](#design-system--styling)
9. [Constraints & Requirements](#constraints--requirements)
10. [Infrastructure & DevOps](#infrastructure--devops)

---

## PROJECT OVERVIEW

### Mission Statement
Build a production-ready landing page and MVP platform for Stellar AI that showcases our 8 AI mentors, gamification system, and Learn-Verify-Own (LVO) framework to multiple stakeholder groups (students, teachers, parents, schools).

### Tech Stack
- **Frontend:** React + TypeScript (Lovable.dev environment)
- **Backend:** Supabase (PostgreSQL + Auth + Storage + Realtime)
- **AI Integration:** Google Gemini 2.5 Flash (via Lovable AI integration)
- **Styling:** Tailwind CSS + Custom Design System
- **Deployment:** Lovable.dev hosting + Custom domain

### Target Audiences
1. **Students** – Interactive learning experience demo
2. **Teachers** – Admin dashboard preview
3. **Parents** – Progress tracking showcase
4. **Schools** – B2B offering and pilot inquiry

---

## CORE ARCHITECTURE

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    LANDING PAGE (Public)                     │
│  ┌────────────┬────────────┬────────────┬────────────┐     │
│  │ For Students│ For Teachers│ For Parents│ For Schools│     │
│  └────────────┴────────────┴────────────┴────────────┘     │
│           │              │              │              │      │
│           └──────────────┴──────────────┴──────────────┘     │
│                           │                                   │
│                    ┌──────▼──────┐                           │
│                    │ Stellar Chat│ (Floating Icon/Modal)     │
│                    └──────┬──────┘                           │
│                           │                                   │
└───────────────────────────┼───────────────────────────────────┘
                            │
                ┌───────────▼───────────┐
                │   Authentication      │
                │   (Supabase Auth)     │
                └───────────┬───────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼────┐       ┌─────▼─────┐      ┌─────▼─────┐
   │ Student │       │  Teacher  │      │  Parent   │
   │Dashboard│       │ Dashboard │      │ Dashboard │
   └─────────┘       └───────────┘      └───────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                   ┌────────▼────────┐
                   │ Supabase Backend│
                   │  (PostgreSQL +  │
                   │   Row-Level     │
                   │   Security)     │
                   └─────────────────┘
```

### Multi-Role Architecture

**Key Design Principle:** Separate login pages and role-based authentication flows for Students, Parents, and Teachers with explicit relationship linkages.

**Role Hierarchy:**
- **Students:** Linked to their Parents + Teachers
- **Parents:** Can access multiple Students (their children)
- **Teachers:** Can access multiple Students (their class members)

**Access Patterns:**
- Students can only see their own data
- Parents can see all data for their linked children
- Teachers can see all data for their linked students
- No cross-role data leakage

---

## DATABASE SCHEMA (SUPABASE)

### Complete Table Structure

**16 Core Tables:**

```sql
-- 1. USERS (extends Supabase auth.users)
CREATE TABLE users (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  role TEXT NOT NULL CHECK (role IN ('student', 'parent', 'teacher', 'admin')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. PROFILES (additional user metadata)
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES users(id),
  avatar_url TEXT,
  bio TEXT,
  preferences JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. ORGANIZATIONS (schools)
CREATE TABLE organizations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  type TEXT CHECK (type IN ('school', 'district', 'pilot')),
  location TEXT,
  contact_email TEXT,
  settings JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. AI_AGENTS (8 mentors: Stella, Max, Nova, Darwin, Lexis, Neo, Luna, Atlas)
CREATE TABLE ai_agents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE,
  personality_description TEXT,
  subject_area TEXT, -- Math, Physics, English, Science, Reading, Critical Thinking, Arts, History
  avatar_url TEXT,
  system_prompt TEXT, -- LLM instructions for this agent
  voice_id TEXT, -- TTS voice identifier
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. ACHIEVEMENTS (badges, milestones)
CREATE TABLE achievements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT,
  badge_icon_url TEXT,
  category TEXT, -- streak, skill_mastery, challenge_completion
  criteria JSONB, -- conditions for earning this achievement
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. LEARNING_PATHS (curriculum sequences)
CREATE TABLE learning_paths (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT,
  grade_level TEXT,
  subject TEXT,
  difficulty TEXT CHECK (difficulty IN ('beginner', 'intermediate', 'advanced')),
  sequence_order INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. CLASSES (teacher's classes)
CREATE TABLE classes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID REFERENCES organizations(id),
  teacher_id UUID REFERENCES users(id),
  name TEXT NOT NULL,
  grade_level TEXT,
  subject TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. CLASS_MEMBERS (student enrollment in classes)
CREATE TABLE class_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  class_id UUID REFERENCES classes(id) ON DELETE CASCADE,
  student_id UUID REFERENCES users(id) ON DELETE CASCADE,
  enrolled_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(class_id, student_id)
);

-- 9. TASKS (learning activities)
CREATE TABLE tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  learning_path_id UUID REFERENCES learning_paths(id),
  agent_id UUID REFERENCES ai_agents(id),
  title TEXT NOT NULL,
  description TEXT,
  content JSONB, -- task instructions, questions, resources
  difficulty TEXT,
  estimated_duration_minutes INTEGER,
  xp_reward INTEGER DEFAULT 10,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 10. USER_PROGRESS (student learning progress)
CREATE TABLE user_progress (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  task_id UUID REFERENCES tasks(id),
  status TEXT CHECK (status IN ('not_started', 'in_progress', 'completed', 'verified')),
  progress_percentage INTEGER DEFAULT 0,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, task_id)
);

-- 11. USER_ACHIEVEMENTS (earned badges)
CREATE TABLE user_achievements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  achievement_id UUID REFERENCES achievements(id),
  earned_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, achievement_id)
);

-- 12. AGENT_CONVERSATIONS (chat history)
CREATE TABLE agent_conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  agent_id UUID REFERENCES ai_agents(id),
  task_id UUID REFERENCES tasks(id),
  messages JSONB DEFAULT '[]', -- array of {role, content, timestamp}
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 13. NOTIFICATIONS (system notifications)
CREATE TABLE notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  type TEXT CHECK (type IN ('achievement', 'reminder', 'announcement', 'parent_alert')),
  title TEXT NOT NULL,
  message TEXT,
  read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 14. RESOURCES (learning materials)
CREATE TABLE resources (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id UUID REFERENCES tasks(id),
  type TEXT CHECK (type IN ('video', 'article', 'interactive', 'pdf')),
  title TEXT NOT NULL,
  url TEXT,
  content JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 15. CONTENT (static content: articles, videos, interactive modules)
CREATE TABLE content (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  type TEXT CHECK (type IN ('video', 'article', 'interactive', 'assessment')),
  title TEXT NOT NULL,
  description TEXT,
  url TEXT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 16. SETTINGS (global app settings)
CREATE TABLE settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key TEXT UNIQUE NOT NULL,
  value JSONB,
  category TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Row-Level Security (RLS) Policies

**Critical:** All tables must have RLS enabled with role-based policies.

**Example RLS Policies:**

```sql
-- Students can only see their own progress
CREATE POLICY "Students view own progress"
ON user_progress FOR SELECT
TO authenticated
USING (user_id = auth.uid() AND EXISTS (
  SELECT 1 FROM users WHERE id = auth.uid() AND role = 'student'
));

-- Parents can view their children's progress
CREATE POLICY "Parents view children progress"
ON user_progress FOR SELECT
TO authenticated
USING (EXISTS (
  SELECT 1 FROM users u
  JOIN profiles p ON p.id = u.id
  WHERE u.id = auth.uid() 
    AND u.role = 'parent'
    AND user_progress.user_id = ANY(
      SELECT jsonb_array_elements_text(p.preferences->'children')::UUID
    )
));

-- Teachers can view their students' progress
CREATE POLICY "Teachers view class progress"
ON user_progress FOR SELECT
TO authenticated
USING (EXISTS (
  SELECT 1 FROM users u
  JOIN class_members cm ON cm.student_id = user_progress.user_id
  JOIN classes c ON c.id = cm.class_id
  WHERE u.id = auth.uid() 
    AND u.role = 'teacher'
    AND c.teacher_id = auth.uid()
));
```

### Database Triggers

**Automatic Profile Creation:**

```sql
CREATE OR REPLACE FUNCTION create_user_profile()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO profiles (id, preferences)
  VALUES (NEW.id, '{}');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER on_user_created
AFTER INSERT ON users
FOR EACH ROW EXECUTE FUNCTION create_user_profile();
```

**Update Timestamps:**

```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables with updated_at
CREATE TRIGGER update_users_timestamp
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

---

## AUTHENTICATION & ROLE-BASED ACCESS CONTROL

### Multi-Role Authentication Design

**Separate Login Pages by Role:**

```
/login/student  → Student Login
/login/parent   → Parent Login
/login/teacher  → Teacher Login
/login/admin    → Admin Login (future)
```

**Authentication Flow:**

```
1. User navigates to role-specific login page
2. Supabase Auth validates credentials
3. Backend checks user.role matches URL role
4. If mismatch: Redirect to correct role page or show error
5. If match: Generate session token, redirect to role dashboard
```

**Implementation (React Router):**

```tsx
// Protected Route Component
const ProtectedRoute = ({ 
  children, 
  allowedRoles 
}: { 
  children: React.ReactNode; 
  allowedRoles: string[] 
}) => {
  const { user, loading } = useAuth();
  
  if (loading) return <LoadingSpinner />;
  
  if (!user) {
    return <Navigate to="/login" />;
  }
  
  if (!allowedRoles.includes(user.role)) {
    return <Navigate to="/unauthorized" />;
  }
  
  return <>{children}</>;
};

// Route Configuration
<Routes>
  <Route path="/login/student" element={<StudentLogin />} />
  <Route path="/login/parent" element={<ParentLogin />} />
  <Route path="/login/teacher" element={<TeacherLogin />} />
  
  <Route 
    path="/dashboard/student" 
    element={
      <ProtectedRoute allowedRoles={['student']}>
        <StudentDashboard />
      </ProtectedRoute>
    } 
  />
  
  <Route 
    path="/dashboard/parent" 
    element={
      <ProtectedRoute allowedRoles={['parent']}>
        <ParentDashboard />
      </ProtectedRoute>
    } 
  />
  
  <Route 
    path="/dashboard/teacher" 
    element={
      <ProtectedRoute allowedRoles={['teacher']}>
        <TeacherDashboard />
      </ProtectedRoute>
    } 
  />
</Routes>
```

### Relationship Linkages

**Parent-Student Linking:**

```sql
-- Store children IDs in parent's profile preferences
UPDATE profiles
SET preferences = jsonb_set(
  preferences,
  '{children}',
  '["child-uuid-1", "child-uuid-2"]'::jsonb
)
WHERE id = 'parent-uuid';
```

**Teacher-Student Linking:**

```sql
-- Insert into class_members table
INSERT INTO class_members (class_id, student_id)
VALUES ('class-uuid', 'student-uuid');
```

### Session Management

**Supabase Auth Configuration:**

```typescript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_ANON_KEY!,
  {
    auth: {
      autoRefreshToken: true,
      persistSession: true,
      detectSessionInUrl: true
    }
  }
);

// Auth helper hooks
export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
      setLoading(false);
    });

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setUser(session?.user ?? null);
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  return { user, loading };
};
```

---

## LANDING PAGE FEATURES

### 1. For Students Tab

**Purpose:** Showcase gamified learning experience.

**Key Elements:**
- Hero section with Stella avatar (animated)
- XP/Badges/Levels visual representation
- Interactive challenge preview (see below)
- CTA: "Start Learning Free"

**Content:**
```
Title: "Learn with AI Mentors Who Get You"
Subtitle: "Earn XP, unlock badges, level up your skills"

Features:
✅ 8 AI mentors (pick your favorite)
✅ Learn at your own pace
✅ Earn points, badges, and achievements
✅ Track progress in real-time
✅ Fun challenges and games

CTA Button: "Try Stella Now" → Opens interactive challenge
```

### 2. For Teachers Tab

**Purpose:** Highlight teacher time savings and admin tools.

**Key Elements:**
- Dashboard preview screenshot
- Key stats (10+ hours saved/week)
- Class management features
- CTA: "Request Demo"

**Content:**
```
Title: "Empower Your Teaching with AI"
Subtitle: "Save 10+ hours per week on grading and tracking"

Features:
✅ Class dashboard with real-time insights
✅ Automated grading and progress tracking
✅ Early intervention alerts
✅ Parent communication tools
✅ Exportable analytics

CTA Button: "Schedule Demo" → Opens contact form
```

### 3. For Parents Tab

**Purpose:** Show transparency and progress visibility.

**Key Elements:**
- Parent app mockup
- Real-time progress visualization
- Skill breakdown examples
- CTA: "See Your Child's Progress"

**Content:**
```
Title: "See Your Child's Real Progress"
Subtitle: "Not just grades—real skills, real-time"

Features:
✅ Daily progress updates
✅ Skill-by-skill breakdown
✅ Recommended home activities
✅ Achievement notifications
✅ Chat with AI mentors

CTA Button: "Try Parent App" → Demo login
```

### 4. For Schools Tab (NEW)

**Purpose:** B2B offering for pilot schools and institutional sales.

**Key Elements:**
- Institutional value proposition
- Pricing tiers (pilot vs. paid)
- Contact form for school inquiries
- Case study highlights (when available)

**Content:**
```
Title: "Transform Your School with Stellar AI"
Subtitle: "Scalable personalization without hiring tutors"

Features:
✅ Whole-school deployment
✅ Teacher training included
✅ Real-time admin analytics
✅ Pilot programs available
✅ ROI tracking and reporting

Pricing:
- Pilot: Free for 3 months (50-100 students)
- Paid: $6-15/student/month

CTA Button: "Contact Us" → School inquiry form
```

---

## INTERACTIVE FEATURES & COMPONENTS

### 1. Stellar AI Chat Feature (Floating Icon + Modal)

**Location:** Floating bottom-right on all landing page sections.

**Design:**
- Floating Stella icon/button (animated pulse effect)
- Clicks opens full-screen or large modal
- Chat interface with Gemini AI integration

**Functionality:**
- Users can ask Stella about:
  - Stellar AI's vision ("Learn • Verify • Own")
  - Mission (blockchain credentials, 8 agents, UAE-first strategy)
  - Detailed information about all 8 specialized agents
  - Gamification features (XP, levels, achievements)
  - Learn-Verify-Own blockchain credential flow
- Real AI responses with token-by-token streaming
- Quick question suggestions (chips below input)
- Welcome message on first open
- Error handling for API failures

**Implementation:**

```tsx
// Floating Chat Button
<button 
  onClick={() => setIsChatOpen(true)}
  className="fixed bottom-6 right-6 w-16 h-16 bg-gradient-to-r from-teal-500 to-blue-500 rounded-full shadow-lg hover:shadow-xl transition-all animate-pulse"
>
  <img src="/stella-avatar.png" alt="Chat with Stella" />
</button>

// Chat Modal
{isChatOpen && (
  <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
    <div className="bg-white rounded-2xl w-full max-w-2xl h-[600px] flex flex-col">
      <ChatHeader onClose={() => setIsChatOpen(false)} />
      <ChatMessages messages={messages} />
      <ChatInput onSend={handleSendMessage} />
    </div>
  </div>
)}

// Gemini AI Integration
const sendMessageToStella = async (userMessage: string) => {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      message: userMessage,
      context: 'landing_page_chat' 
    })
  });
  
  const reader = response.body?.getReader();
  // Stream response token-by-token
};
```

**Chat Styling Requirements:**
- Same avatar design as landing page hero section (visual consistency)
- Markdown formatting where asterisks (*text*) display as **bold text** in UI (not literal asterisks)
- Clean, modern chat bubbles
- Smooth scroll behavior

### 2. Landing Page Interactive Challenge

**Location:** "For Students" tab.

**Purpose:** Live demonstration feature to showcase gamified learning experience directly on landing page.

**Design:**
- Hint button (matching main webapp design/functionality)
- Multiple simple questions (minimum: 1 AI-focused, 1 English-focused)
- Next button to progress through questions
- Ability to answer each question before moving forward
- Immediate feedback on answers

**Implementation:**

```tsx
// Challenge Component
const InteractiveChallenge = () => {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<string[]>([]);
  const [showHint, setShowHint] = useState(false);
  
  const questions = [
    {
      id: 1,
      type: 'ai',
      question: 'What is an AI mentor?',
      options: ['A robot', 'A smart tutor', 'A video game', 'A book'],
      correct: 'A smart tutor',
      hint: 'Think about how a teacher helps you learn...'
    },
    {
      id: 2,
      type: 'english',
      question: 'Which word means "happy"?',
      options: ['Sad', 'Joyful', 'Angry', 'Tired'],
      correct: 'Joyful',
      hint: 'Think of a synonym for happy...'
    }
  ];
  
  return (
    <div className="challenge-container">
      <Question 
        data={questions[currentQuestion]}
        onAnswer={(answer) => setAnswers([...answers, answer])}
      />
      {showHint && <Hint text={questions[currentQuestion].hint} />}
      <button onClick={() => setShowHint(true)}>Show Hint</button>
      <button onClick={() => setCurrentQuestion(prev => prev + 1)}>Next</button>
    </div>
  );
};
```

### 3. Agent Interaction Popup

**Location:** Landing page, triggered by clicking on any of the 8 AI agent cards.

**Purpose:** Users can experience core app functionality (task solving, AI chat) directly on landing page.

**Popup Contains:**
1. Brief explanation/description of the agent
2. Ability to solve tasks associated with that specific agent
3. Chat functionality with the agent

**Implementation:**

```tsx
// Agent Card (clickable)
<div 
  onClick={() => setSelectedAgent(agent)}
  className="agent-card cursor-pointer hover:scale-105 transition"
>
  <img src={agent.avatar_url} alt={agent.name} />
  <h3>{agent.name}</h3>
  <p>{agent.subject_area}</p>
</div>

// Agent Popup Modal
{selectedAgent && (
  <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
    <div className="bg-white rounded-2xl w-full max-w-4xl h-[80vh] overflow-y-auto">
      <AgentHeader agent={selectedAgent} onClose={() => setSelectedAgent(null)} />
      
      <div className="p-6">
        <h2>{selectedAgent.name}</h2>
        <p>{selectedAgent.personality_description}</p>
        
        <Tabs>
          <Tab label="Tasks">
            <TaskList agentId={selectedAgent.id} />
          </Tab>
          <Tab label="Chat">
            <ChatInterface agentId={selectedAgent.id} />
          </Tab>
        </Tabs>
      </div>
    </div>
  </div>
)}
```

### 4. Footer Navigation Links

**Purpose:** Quick navigation from footer to each market segment section on landing page.

**Links:**
- "For Students" → links to students tab
- "For Teachers" → links to teacher tab
- "For Parents" → links to parents tab
- "For Schools" → links to new schools tab

**Implementation:**

```tsx
// Footer Component
<footer className="bg-gray-900 text-white py-8">
  <div className="container mx-auto px-4">
    <div className="grid grid-cols-4 gap-8">
      <div>
        <h3 className="font-bold mb-4">For Students</h3>
        <a href="#students" className="hover:text-teal-400">
          Learn with AI
        </a>
      </div>
      
      <div>
        <h3 className="font-bold mb-4">For Teachers</h3>
        <a href="#teachers" className="hover:text-teal-400">
          Save Time
        </a>
      </div>
      
      <div>
        <h3 className="font-bold mb-4">For Parents</h3>
        <a href="#parents" className="hover:text-teal-400">
          Track Progress
        </a>
      </div>
      
      <div>
        <h3 className="font-bold mb-4">For Schools</h3>
        <a href="#schools" className="hover:text-teal-400">
          Contact Us
        </a>
      </div>
    </div>
  </div>
</footer>
```

### 5. Contact Form Popup Modal

**Location:** "For Schools" tab (triggered by sign-up CTA button).

**Purpose:** Schools can submit inquiries for pilots or paid contracts.

**Form Fields:**
- School Name
- Contact Name
- Email
- Phone (optional)
- Number of Students
- Grade Level
- Message / Special Requirements
- Inquiry Type (Pilot / Paid / General Inquiry)

**Integration:**
- Form connects to backend (Supabase table: `school_inquiries`)
- Email notification sent to Stellar AI team
- Auto-response email to school contact

**Implementation:**

```tsx
// Contact Form Modal
const SchoolContactForm = ({ onClose }: { onClose: () => void }) => {
  const [formData, setFormData] = useState({
    school_name: '',
    contact_name: '',
    email: '',
    phone: '',
    num_students: '',
    grade_level: '',
    message: '',
    inquiry_type: 'pilot'
  });
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Submit to Supabase
    const { error } = await supabase
      .from('school_inquiries')
      .insert([formData]);
    
    if (!error) {
      // Send email notification
      await sendNotificationEmail(formData);
      // Show success message
      toast.success('Inquiry submitted! We\'ll contact you within 24 hours.');
      onClose();
    }
  };
  
  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
      <div className="bg-white rounded-2xl w-full max-w-2xl p-8">
        <h2 className="text-2xl font-bold mb-6">Contact Us - School Inquiry</h2>
        <form onSubmit={handleSubmit}>
          {/* Form fields */}
          <button type="submit" className="btn-primary">
            Submit Inquiry
          </button>
        </form>
      </div>
    </div>
  );
};
```

---

## DEMO & CUSTOMER JOURNEY

### Customer Journey Demo: Familie Sass

**Purpose:** Complete demo customer journey implemented for "Familie Sass" with realistic 30-day progression data.

**Participants:**
- **Parent:** Kisaya Sass
- **Children (Students):** Amy, Lyon, Noah (3 students)
- **Teachers:** Mr. Smith, Mrs. Paris, Mrs. Padington (3 teachers)
- **Classes:** Math (Max agent), English (Lexis agent), Art/Music (Nova agent)
- **Total Tasks:** 28 sample tasks across all subjects
- **Progress Records:** 90 user_progress records (30 per student)
- **Credentials:** Test credentials established for all roles (parent, students, teachers)

**Demo Data Structure:**

```sql
-- Parent Account
INSERT INTO users (id, email, full_name, role)
VALUES (
  'kisaya-sass-uuid',
  'kisaya@sass-family.com',
  'Kisaya Sass',
  'parent'
);

-- Student Accounts (3 children)
INSERT INTO users (id, email, full_name, role) VALUES
  ('amy-uuid', 'amy@sass-family.com', 'Amy Sass', 'student'),
  ('lyon-uuid', 'lyon@sass-family.com', 'Lyon Sass', 'student'),
  ('noah-uuid', 'noah@sass-family.com', 'Noah Sass', 'student');

-- Parent-Children Linking
UPDATE profiles
SET preferences = jsonb_set(
  preferences,
  '{children}',
  '["amy-uuid", "lyon-uuid", "noah-uuid"]'::jsonb
)
WHERE id = 'kisaya-sass-uuid';

-- Teacher Accounts
INSERT INTO users (id, email, full_name, role) VALUES
  ('mr-smith-uuid', 'mr.smith@school.com', 'Mr. Smith', 'teacher'),
  ('mrs-paris-uuid', 'mrs.paris@school.com', 'Mrs. Paris', 'teacher'),
  ('mrs-padington-uuid', 'mrs.padington@school.com', 'Mrs. Padington', 'teacher');

-- Classes
INSERT INTO classes (id, teacher_id, name, subject) VALUES
  ('math-class-uuid', 'mr-smith-uuid', 'Math 101', 'Math'),
  ('english-class-uuid', 'mrs-paris-uuid', 'English Literature', 'English'),
  ('art-class-uuid', 'mrs-padington-uuid', 'Art & Music', 'Arts');

-- Class Enrollments (all 3 students in all 3 classes)
INSERT INTO class_members (class_id, student_id) VALUES
  ('math-class-uuid', 'amy-uuid'),
  ('math-class-uuid', 'lyon-uuid'),
  ('math-class-uuid', 'noah-uuid'),
  ('english-class-uuid', 'amy-uuid'),
  ('english-class-uuid', 'lyon-uuid'),
  ('english-class-uuid', 'noah-uuid'),
  ('art-class-uuid', 'amy-uuid'),
  ('art-class-uuid', 'lyon-uuid'),
  ('art-class-uuid', 'noah-uuid');
```

**30-Day Progression Data:**

Each student has realistic progress over 30 days:
- Tasks completed at varying rates (some fast, some slow)
- XP earned accumulates
- Achievements unlocked at milestones
- Streaks tracked
- AI conversations logged

**Demo Use Cases:**

1. **Parent Dashboard:** Kisaya logs in, sees all 3 children's progress side-by-side
2. **Teacher Dashboard:** Mr. Smith sees entire Math class, identifies Lyon needs help
3. **Student Dashboard:** Amy logs in, continues Math task, earns XP, unlocks badge
4. **Cross-Role Verification:** Parent sees what teacher sees (same student data)

---

## DESIGN SYSTEM & STYLING

### Tailwind CSS Configuration

**Custom Colors (Brand Palette):**

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'stellar-teal': {
          50: '#E6F7F7',
          100: '#CCEFEF',
          200: '#99DFDF',
          300: '#66CFCF',
          400: '#33BFBF',
          500: '#00AFAF', // Primary teal
          600: '#008C8C',
          700: '#006969',
          800: '#004646',
          900: '#002323'
        },
        'stellar-blue': {
          500: '#3B82F6',
          600: '#2563EB'
        },
        'stellar-purple': {
          500: '#8B5CF6',
          600: '#7C3AED'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Poppins', 'system-ui', 'sans-serif']
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 3s ease-in-out infinite'
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' }
        }
      }
    }
  }
};
```

### Component Design Patterns

**Button Styles:**

```tsx
// Primary Button
className="bg-stellar-teal-500 hover:bg-stellar-teal-600 text-white font-semibold py-3 px-6 rounded-lg shadow-md hover:shadow-lg transition-all duration-200"

// Secondary Button
className="bg-white hover:bg-gray-50 text-stellar-teal-500 font-semibold py-3 px-6 rounded-lg border-2 border-stellar-teal-500 transition-all duration-200"

// Outline Button
className="border-2 border-stellar-teal-500 text-stellar-teal-500 hover:bg-stellar-teal-50 font-semibold py-3 px-6 rounded-lg transition-all duration-200"
```

**Card Styles:**

```tsx
// Standard Card
className="bg-white rounded-xl shadow-md hover:shadow-xl transition-shadow duration-300 p-6"

// Elevated Card
className="bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 p-8 border border-gray-100"

// Interactive Card (Agent cards, feature cards)
className="bg-gradient-to-br from-white to-gray-50 rounded-xl shadow-md hover:shadow-xl hover:scale-105 transition-all duration-300 p-6 cursor-pointer"
```

### Responsive Design

**Breakpoints:**

```css
/* Mobile-first approach */
sm: 640px   // Small devices
md: 768px   // Tablets
lg: 1024px  // Laptops
xl: 1280px  // Desktops
2xl: 1536px // Large screens
```

**Layout Patterns:**

```tsx
// Landing Page Sections
<section className="py-16 md:py-24 lg:py-32">
  <div className="container mx-auto px-4 md:px-6 lg:px-8">
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {/* Content */}
    </div>
  </div>
</section>
```

---

## CONSTRAINTS & REQUIREMENTS

### 1. English Language Requirement

**Constraint:** All UI text, content, and messaging throughout the application must be in **English**.

**Applies to:**
- All landing page content
- Feature descriptions
- Agent information
- Chat responses
- Form labels
- System prompts for AI agents
- User-facing copy

**Why:** Application is being built with English as the primary language. The application is designed for international schools in UAE + Saudi Arabia where English is common. Arabic localization is planned for future iterations.

**Implementation Note:**

```typescript
// Language validation in AI prompts
const SYSTEM_PROMPT = `
You are Stella, an AI learning mentor for Stellar AI.
CRITICAL: All responses must be in English.
Do not respond in Arabic, French, German, or any other language.
If user asks in another language, politely respond in English.
`;
```

### 2. Stellar Chat Styling Requirements

**Constraint:** The Stellar chat modal must use the **same avatar design** as the landing page hero section for visual consistency.

**Requirements:**
- Avatar image matches hero section avatar
- Markdown formatting where asterisks (`*text*`) display as **bold text** in actual UI (not literal asterisks shown to user)
- Clean, modern chat bubbles
- Smooth scroll behavior
- Consistent color scheme with landing page

**Implementation:**

```tsx
// Message Rendering with Markdown
const renderMessage = (content: string) => {
  // Replace *text* with <strong>text</strong>
  const formattedContent = content.replace(
    /\*(.*?)\*/g, 
    '<strong>$1</strong>'
  );
  
  return (
    <div 
      className="message-content prose"
      dangerouslySetInnerHTML={{ __html: formattedContent }}
    />
  );
};
```

### 3. Production Readiness

**Requirements:**
- Error handling on all API calls
- Loading states for all async operations
- Responsive design (mobile, tablet, desktop)
- Accessibility (ARIA labels, keyboard navigation)
- Performance (lazy loading, code splitting)
- SEO optimization (meta tags, semantic HTML)

---

## INFRASTRUCTURE & DEVOPS

### Supabase Infrastructure Reset

**Context:** User deleted old Supabase organization and created fresh one from scratch. Project now uses fresh Supabase organization disconnected from previous setup.

**Goal:** Rebuild all database tables, RLS policies, functions, and demo data from scratch in new organization to prepare for live Stellar AI presentation.

**Reset Checklist:**

- [ ] Create all 16 database tables
- [ ] Enable RLS on all tables
- [ ] Create RLS policies for each role (student, parent, teacher)
- [ ] Create database triggers (profile creation, timestamp updates)
- [ ] Seed 8 AI agents (Stella, Max, Nova, Darwin, Lexis, Neo, Luna, Atlas)
- [ ] Seed demo data (Familie Sass: parent, 3 students, 3 teachers, 3 classes, 28 tasks, 90 progress records)
- [ ] Test authentication flows for all roles
- [ ] Verify RLS policies work correctly
- [ ] Test parent-student and teacher-student linkages
- [ ] Deploy to production

### Environment Variables

```bash
# .env.local
SUPABASE_URL=https://[project-id].supabase.co
SUPABASE_ANON_KEY=[anon-key]
SUPABASE_SERVICE_ROLE_KEY=[service-role-key]
GEMINI_API_KEY=[google-ai-api-key]
```

### Deployment

**Lovable.dev Deployment:**
- Automatic deployment on git push
- Custom domain configuration: stellar-ai.com (or stellarlearning.ai)
- HTTPS enabled by default
- CDN caching for static assets

**Supabase Configuration:**
- Production database URL
- Connection pooling enabled
- Realtime subscriptions configured
- Storage buckets for user avatars, agent images

---

## NEXT STEPS & ROADMAP

### Immediate Priorities (Week 1-2)

1. ✅ Complete Supabase infrastructure reset
2. ✅ Implement multi-role authentication
3. ✅ Build landing page with all 4 tabs
4. ✅ Implement Stellar Chat feature
5. ✅ Build interactive challenge component
6. ✅ Create agent interaction popups
7. ✅ Implement school contact form

### Short-Term (Month 1)

- Deploy to production with custom domain
- Test with Familie Sass demo data
- Gather feedback from pilot users
- Iterate on UX based on feedback
- Prepare investor demo materials

### Medium-Term (Months 2-3)

- Add Arabic language support
- Expand agent personalities and tasks
- Build full student/teacher/parent dashboards
- Implement blockchain credential issuance (LVO)
- Launch first pilot school

### Long-Term (Months 4-6)

- Scale to 5-10 pilot schools
- Build mobile apps (React Native)
- Integrate advanced analytics
- Implement social features (leaderboards, peer collaboration)
- Prepare for Seed fundraising

---

## TECHNICAL DECISIONS LOG

### Why Supabase?
- PostgreSQL-based (mature, reliable)
- Built-in authentication (row-level security)
- Real-time subscriptions (live updates)
- Generous free tier (perfect for MVP)
- Easy migration to self-hosted if needed

### Why Google Gemini 2.5 Flash?
- Lovable.dev has native integration
- Fast inference (token streaming)
- Cost-effective for MVP
- Strong multilingual support (future Arabic)
- Good instruction-following capability

### Why Single-Page Architecture?
- Faster initial load
- Smooth transitions between sections
- Better for landing page experience
- Easy to add animations/interactions
- SEO handled via meta tags + SSR (future)

### Why Row-Level Security?
- Centralized access control (database-level)
- No business logic in frontend for auth
- Prevents data leakage bugs
- Easy to audit and test
- Industry best practice for multi-tenant apps

---

## GLOSSARY

**RLS (Row-Level Security):** PostgreSQL feature that restricts database row access based on user identity.

**RBAC (Role-Based Access Control):** Access control paradigm where permissions are assigned to roles (student, parent, teacher) rather than individual users.

**Supabase Auth:** Built-in authentication system in Supabase (email/password, OAuth, magic links).

**LVO (Learn-Verify-Own):** Stellar AI's proprietary framework where students Learn (AI mentoring), Verify (multi-source validation), Own (blockchain credentials).

**Agent:** AI mentor personality (Stella, Max, Nova, etc.) with specialized subject expertise and unique interaction style.

**Task:** Learning activity assigned by an agent (question, challenge, project, assessment).

**XP (Experience Points):** Gamification currency earned by completing tasks and engaging with content.

**Achievement:** Badge or milestone earned by meeting specific criteria (streak, skill mastery, challenge completion).

**Credential:** Blockchain-backed proof of skill ownership issued when student completes verified learning milestone.

---

## CONTACT & SUPPORT

**Project Owner:** Lars Philip Sass  
**Email:** lars@stellar-ai.com  
**Platform:** Lovable.dev  
**Repository:** [GitHub URL]  
**Documentation:** This file (lovable-project-memory.md)  

---

**END OF DOCUMENT**

This memory file should be uploaded to Lovable.dev project "Memories" to provide complete context for AI-assisted development.

Last Updated: November 2025  
Version: 2.0 (Complete Rebuild Specification)
