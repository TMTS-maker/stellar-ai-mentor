# Stellar AI - Admin UI Guide

**Version:** 1.0
**Last Updated:** November 14, 2025
**For:** Administrators, Teachers, Demo Presenters

---

## Quick Start

### 1. Setup (One-Time)

```bash
# Start from project root
cd /home/user/stellar-ai-mentor

# Install frontend dependencies (if not done)
npm install

# Seed demo data
cd backend
./scripts/run_demo_seed.sh
```

### 2. Run the Demo

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd /home/user/stellar-ai-mentor
npm run dev
```

### 3. Access Admin UI

**URL:** http://localhost:5173/admin

**Demo Admin Credentials:**
- Email: `admin@stellar-demo.school`
- Password: `StellarDemo123!`

---

## Admin UI Overview

The admin interface provides comprehensive school management capabilities across 4 main sections:

1. **Dashboard** - Overview statistics
2. **Students** - Student roster and LVO profiles
3. **Resources** - Curriculum content library
4. **Skills** - Skill definitions (future)

---

## 1. Admin Dashboard (`/admin`)

### What You See

**8 Stat Cards:**
- Total Students
- Total Skills
- Learning Paths
- Resources
- Credentials Issued
- Total XP Earned
- Active Students (7 days)
- Teachers

**Quick Action Cards:**
- Students Management
- Resources Library
- Skills Management
- Learning Paths

### Demo Script

> "This is the admin dashboard for Dubai Future Academy. You can see we have:
> - 1 student (Amira) currently enrolled
> - 5 skills defined across reading and math
> - 2 learning paths (English A1 and Math Basics)
> - 4 curriculum resources in our library
> - 1 blockchain-verified credential already issued
> - 85 total XP earned by our students
>
> Let's click into Students to see Amira's progress..."

---

## 2. Student Management (`/admin/students`)

### What You See

**Student Roster Table:**
| Column | Description |
|--------|-------------|
| Name | Student full name |
| Email | Student email address |
| Grade | Grade level badge |
| Level | Current XP level with icon |
| XP | Total XP earned |
| Weak Skills | Count of skills scoring < 60 (red alert) |
| Credentials | Count of credentials earned (gold) |
| Action | "View Profile" button |

**Summary Cards:**
- Students with weak skills
- Students with credentials
- Average XP

### Demo Script

> "Here's our student roster. Notice that Amira has:
> - Grade 3
> - Level 0 (85 XP - close to leveling up!)
> - 1 weak skill flagged in red
> - 1 credential already earned
>
> The system automatically identifies students who need support. Let's click on Amira to see her complete LVO profile..."

---

## 3. Student Detail View (`/admin/students/{id}`)

### What You See

**Student Info Header:**
- Student name and email
- Grade level
- Current level and total XP

**Skills Profile Card:**
- **Needs Support** (red section):
  - Skills scoring < 60
  - Example: "Reading A1 – Main Idea" at 45
- **Strong Skills** (green section):
  - Skills scoring >= 80
  - Example: "Simple Sentences" at 72
- **All Skills Progress Bars**:
  - Red bar: < 60
  - Yellow bar: 60-79
  - Green bar: >= 80
  - Shows confidence percentage and assessment count

**Learning Paths Card:**
- Path name and status (in_progress, completed)
- Progress percentage with visual bar
- Active modules list with task completion

**Credentials Card:**
- Badges earned (e.g., "Reading Rookie 🏅")
- Recent credentials with:
  - Title
  - Credential type
  - Status (draft, issued, minted)
  - Issue date
  - Blockchain status

**Verifications Card:**
- Verification history
- Skill name
- Status (verified, pending, rejected)
- Score
- Verification date

**Recommended Resources Card:**
- AI-powered recommendations
- Resources matched to weak skills
- Resource type (video, worksheet, game)
- Estimated time

### Demo Script (This is the WOW moment!)

> "This is Amira's complete Learn-Verify-Own profile. Let's break it down:
>
> **LEARN (Skills):**
> - Amira has been assessed on 3 skills
> - She's strong in 'Simple Sentences' with a 72 - great progress!
> - But she's struggling with 'Main Idea' at only 45 - needs support
> - The system automatically flagged this
>
> **LEARN (Learning Paths):**
> - She's enrolled in 2 learning paths
> - English A1 is 35% complete - she finished Module 1 (Simple Sentences) with 78%
> - Now working on Module 2 (Short Stories) - only 45%, which makes sense given her weak skill
>
> **VERIFY (Verifications):**
> - The AI verified her completion of 'Simple Sentences'
> - Score: 78%, Status: Verified ✅
> - This verification is backed by evidence from 2 completed tasks
>
> **OWN (Credentials):**
> - Amira earned the 'English A1 – Simple Sentences (Bronze)' credential
> - Status: Issued and Minted on blockchain ✅
> - She also earned a 'Reading Rookie' badge
> - These credentials are portable and verifiable for life
>
> **AI RECOMMENDATIONS:**
> - The system automatically recommended resources to help with her weak skill
> - 'Finding the Main Idea - Animated Story' - 8 minutes
> - Perfect match for what she needs to practice
>
> This is personalized learning at scale - the platform knows exactly where each student needs help and what resources will work best."

---

## 4. Resource Management (`/admin/resources`)

### What You See

**Resource Library Statistics:**
- Total Views
- Total Completions
- Average Quality Score
- Active Resources count

**Resource Table:**
| Column | Description |
|--------|-------------|
| Title | Resource name |
| Type | video, pdf, interactive, quiz, etc. |
| Subject | reading, math, etc. |
| Grade | Grade range (e.g., 2-4) |
| Quality | Badge (Excellent, Good, Fair, Needs Review) |
| Skills | Number of linked skills |
| Views | View count with eye icon |
| Status | Active/Inactive |
| Actions | Delete button (trash icon) |

**Quality Score Badges:**
- **Excellent** (green): 85-100
- **Good** (blue): 70-84
- **Fair** (yellow): 50-69
- **Needs Review** (red): < 50

### Demo Script

> "Here's our curriculum library with 4 resources:
>
> - 'Finding the Main Idea - Animated Story' - Quality: 85 (Excellent)
>   - This is the video we recommended to Amira
>   - 8 minutes long, targets her weak skill
>   - Open educational resource, CC BY-SA license
>
> - 'Simple Sentences Practice Worksheet' - Quality: 90 (Excellent)
>   - Teacher-uploaded content
>   - PDF format for practice
>
> - 'Add to 20 – Number Line Game' - Quality: 88 (Excellent)
>   - Interactive game for math practice
>
> - 'Word Problems for Beginners' - Quality: 82 (Good)
>   - AI-generated content from Stellar AI
>
> Each resource is:
> - Mapped to specific skills
> - Rated for quality based on student outcomes
> - Tagged with grade level and subject
> - Available for AI-powered recommendations
>
> Teachers and admins can delete resources that aren't working (soft delete - just deactivates them)."

---

## Features Deep Dive

### Authentication & Permissions

**Role-Based Access:**
- Only `school_admin` and `teacher` roles can access `/admin`
- Student and parent roles are redirected to login
- Uses existing JWT token management from main app

**Auth Flow:**
1. User logs in at `/login` (or goes to `/admin` directly)
2. Token stored in localStorage
3. Admin pages check user role on mount
4. Invalid role → redirect to `/login`
5. Token expired → auto-refresh or logout

### Data Loading

**Loading States:**
- Spinner animation while fetching
- "Loading..." text
- Prevents user interaction

**Error States:**
- Red error card with message
- "Try Again" button to retry
- Console error logging for debugging

**Empty States:**
- Friendly message when no data
- Instructions to run demo seed script
- Helpful code snippet

### UI Components

**Used from shadcn/ui:**
- Card, CardHeader, CardTitle, CardDescription, CardContent
- Button (variants: default, outline, ghost, destructive)
- Badge (variants: default, outline, secondary, destructive)

**Icons from lucide-react:**
- Users, Target, TrendingUp, Award, FileText, etc.
- Consistent sizing (h-4 w-4 for small, h-5 w-5 for medium)

**Tailwind Classes:**
- `bg-gradient-to-br from-purple-50 to-blue-50` - Brand background
- `hover:shadow-lg transition-shadow` - Card hover effects
- `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6` - Responsive grid
- Color coding: red (weak), yellow (medium), green (strong)

---

## API Integration

### Endpoints Used

| Endpoint | Method | Used By | Purpose |
|----------|--------|---------|---------|
| `/admin/stats` | GET | AdminDashboard | Get overview statistics |
| `/admin/students` | GET | AdminStudentList | List all students |
| `/admin/students/{id}/lvo-profile` | GET | AdminStudentDetail | Get student LVO profile |
| `/admin/resources` | GET | AdminResourceList | List all resources |
| `/admin/resources/{id}` | DELETE | AdminResourceList | Soft delete resource |

### TypeScript Types

All API responses are fully typed:

```typescript
interface AdminStatsResponse {
  total_students: number;
  total_skills: number;
  total_learning_paths: number;
  total_resources: number;
  total_credentials_issued: number;
  total_xp_earned: number;
  active_students_last_week: number;
  total_teachers: number;
}

interface StudentLVOProfile {
  student_id: string;
  student_name: string;
  email: string;
  grade_level: number;
  total_xp: number;
  current_level: number;
  skill_scores: Array<{...}>;
  weak_skills: Array<{...}>;
  strong_skills: Array<{...}>;
  learning_paths: Array<{...}>;
  // ... full LVO data
}

interface ResourceManagementResponse {
  id: string;
  title: string;
  resource_type: string;
  source_type: string;
  quality_score: number | null;
  // ... metadata
}
```

---

## Demo Walkthrough (10 Minutes)

### Minute 0-2: Dashboard Overview

1. Open http://localhost:5173/admin
2. Log in (auto-filled credentials)
3. Point out 8 stat cards
4. Highlight: "1 credential issued, 85 XP earned"
5. Quick links to sub-pages

### Minute 2-5: Student Profile Deep Dive

1. Click "View Students"
2. Show student roster
3. Point out red alert (weak skills)
4. Click on Amira Hassan
5. **Walk through LVO architecture:**
   - LEARN: Skills profile, weak vs strong
   - LEARN: Learning paths, progress bars
   - VERIFY: Verifications (AI-verified)
   - OWN: Credentials + blockchain status
6. **Show AI recommendations**
7. Explain: "This is what makes Stellar AI different - every student gets personalized, verified, owned learning"

### Minute 5-7: Resource Library

1. Back to dashboard → Click "Resources"
2. Show 4 resources in library
3. Point out quality scores
4. Explain multi-source ingestion:
   - Teacher uploads
   - Public OER
   - AI-generated
   - School systems
5. Demo delete functionality (cancel confirmation)

### Minute 7-10: Business Value

1. Back to dashboard
2. "Imagine this scaled to 1,000 students"
3. Value propositions:
   - **For admins**: Data visibility, ROI tracking
   - **For teachers**: Identify struggling students instantly
   - **For schools**: Personalization at scale
   - **For students**: Verified, portable credentials
4. "This is the complete Learn-Verify-Own platform"
5. Close with: "Ready for pilot program"

---

## Troubleshooting

### Issue: "Failed to load stats"

**Cause:** Backend not running or database empty

**Fix:**
```bash
# Check backend is running
curl http://localhost:8000/health

# Seed demo data
cd backend
./scripts/run_demo_seed.sh
```

### Issue: "Redirected to login"

**Cause:** Not logged in or wrong role

**Fix:**
- Use demo admin credentials
- Email: `admin@stellar-demo.school`
- Password: `StellarDemo123!`

### Issue: "No students found"

**Cause:** Database not seeded

**Fix:**
```bash
cd backend
./scripts/run_demo_seed.sh
```

### Issue: Components not rendering

**Cause:** Missing UI components

**Fix:**
```bash
npm install
# shadcn/ui components should already be installed
```

---

## Future Enhancements

### Short-Term (1-2 weeks)

**Resource Creation Form:**
```
/admin/resources/new
- Title, description fields
- Resource type dropdown
- Subject selection
- Grade range inputs
- Skill multi-select
- Upload file or enter URL
```

**Student Search & Filters:**
- Search by name or email
- Filter by grade level
- Filter by weak skills count
- Sort by XP, credentials, etc.

**Skills Management UI:**
```
/admin/skills
- List all skills
- Create new skill form
- Edit skill details
- Link skills to modules
```

### Medium-Term (1-2 months)

**Bulk Operations:**
- Import students from CSV
- Bulk assign learning paths
- Bulk upload resources

**Analytics Dashboard:**
- Engagement charts
- Content performance graphs
- Student cohort analysis
- Mentor usage statistics

**Learning Path Builder:**
- Visual path designer
- Drag-and-drop modules
- Prerequisite mapping
- Skill alignment tools

### Long-Term (2-3 months)

**Multi-School Management:**
- School switcher dropdown
- Cross-school analytics
- District-wide reporting

**Parent Communication:**
- Send messages to parents
- Progress report generator
- Auto-notifications

**Advanced Recommendations:**
- A/B testing resources
- Collaborative filtering
- Content effectiveness tracking

---

## Technical Notes

### File Structure

```
src/
├── lib/
│   └── api.ts (extended with admin methods)
├── pages/
│   ├── admin/
│   │   ├── AdminDashboard.tsx
│   │   ├── AdminStudentList.tsx
│   │   ├── AdminStudentDetail.tsx
│   │   └── AdminResourceList.tsx
│   ├── StudentDashboard.tsx (existing)
│   ├── TeacherDashboard.tsx (existing)
│   └── ...
└── App.tsx (admin routes added)
```

### Dependencies

- React 18+
- React Router 6+
- TanStack Query (for future caching)
- shadcn/ui components
- Tailwind CSS
- lucide-react icons

### Code Quality

- **TypeScript**: Full type safety
- **React Hooks**: Functional components
- **Error Handling**: Try-catch with user-friendly messages
- **Loading States**: Proper UX during async operations
- **Responsive**: Mobile-friendly (tablet+)
- **Accessible**: Semantic HTML, ARIA labels

---

## Keyboard Shortcuts (Future)

| Shortcut | Action |
|----------|--------|
| `Ctrl/Cmd + K` | Search students |
| `Ctrl/Cmd + N` | New resource |
| `Ctrl/Cmd + B` | Toggle sidebar |
| `/` | Focus search bar |

---

## Support

**For bugs or feature requests:**
- GitHub Issues: https://github.com/stellar-ai/issues

**For demo support:**
- Check `/docs/stellar-ai-demo-story.md`
- Review backend API docs at http://localhost:8000/docs

---

**Admin UI is production-ready for demos and investor presentations!** 🌟

---

## Quick Reference

### Demo Login
- **URL:** http://localhost:5173/admin
- **Email:** admin@stellar-demo.school
- **Password:** StellarDemo123!

### Student to Demo
- **Name:** Amira Hassan
- **Weak Skill:** Reading A1 – Main Idea (45)
- **Strong Skill:** Simple Sentences (72)
- **Credential:** English A1 – Simple Sentences (Bronze) ✅

### Key Selling Points
1. **Complete LVO Architecture** - Learn, Verify, Own in one platform
2. **AI-Powered Personalization** - Automatic recommendations
3. **Blockchain Credentials** - Portable, verifiable achievements
4. **Multi-Source Content** - Schools, teachers, OER, AI
5. **Data-Driven Insights** - Know exactly where students need help
6. **Scalable** - Works for 1 student or 10,000

---

**Ready to revolutionize education!** 🚀
