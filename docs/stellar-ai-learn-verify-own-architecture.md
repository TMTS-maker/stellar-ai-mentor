# Stellar AI: Learn - Verify - Own (LVO) Architecture

> **Version**: 1.0
> **Date**: November 2025
> **Status**: MVP Implementation

---

## 🌟 Executive Summary

Stellar AI is built on the revolutionary **Learn - Verify - Own** (LVO) principle, transforming traditional education into a competency-based system where students don't just earn points—they earn **verified, owned credentials** that represent real knowledge and skills.

**The LVO Promise:**
- **Students** own proof of their competencies, not just grades
- **Parents** see verified progress, not just completion percentages
- **Teachers** validate real understanding, not just task completion
- **Schools** issue blockchain-ready credentials that students carry for life

---

## 📚 Part 1: LEARN - AI-Powered Personalized Learning

### What is LEARN?

LEARN is the foundation of student growth in Stellar AI. It represents the entire journey from discovery to mastery, guided by AI mentors and structured learning paths.

### Core Concepts

#### 1. **Skills** - The Building Blocks of Knowledge

A **Skill** is a specific, measurable competency that a student can develop and demonstrate.

**Examples:**
- "Reading Comprehension - Level A1"
- "Present Simple Tense - English Grammar"
- "Basic Arithmetic - Addition and Subtraction"
- "Conversational French - Greetings"

**Database Model**: `Skill`
- Fields: `id`, `name`, `description`, `category`, `level`, `age_group`
- Categories: "Reading", "Writing", "Math", "Science", "Language", "Social Skills"
- Levels: Beginner → Intermediate → Advanced → Expert

**Why Skills Matter:**
- Skills are universal and transferable
- They map to real-world competencies
- They can be verified and certified
- They transcend traditional grades

#### 2. **Learning Paths** - Structured Growth Journeys

A **Learning Path** is a curated sequence of learning experiences designed to help students master related skills progressively.

**Examples:**
- "English A1 for Young Learners" (12 weeks)
- "Math Foundations - Grade 3"
- "Introduction to Science"

**Database Model**: `LearningPath`
- Fields: `id`, `name`, `description`, `recommended_age_min`, `recommended_age_max`
- Contains multiple **Modules** (steps in the path)

**Key Features:**
- Adaptive progression based on student performance
- AI-recommended based on student's current skill levels
- Tracks overall completion and mastery percentage

#### 3. **Modules** - Learning Milestones

A **Module** is a logical grouping of tasks within a Learning Path, representing a milestone or sub-topic.

**Examples:**
- Module 1: "Alphabet and Phonics" (in "English A1 for Young Learners")
- Module 2: "Basic Sentence Structure"
- Module 3: "Simple Conversations"

**Database Model**: `LearningModule`
- Fields: `id`, `learning_path_id`, `name`, `description`, `order_index`
- Contains multiple **Tasks**

**Module Completion = Verification Trigger:**
When a student completes all tasks in a module with sufficient quality, this triggers the VERIFY phase.

#### 4. **Tasks** - Learning Activities (Existing Model)

Tasks are the existing interactive activities that students complete:
- AI conversations
- Quizzes
- Pronunciation practice
- Writing exercises
- Problem-solving challenges

**Enhanced with Skills:**
- Each task is now linked to one or more **Skills**
- Completing tasks updates **SkillScore** for the student
- Task difficulty adapts based on current skill levels

#### 5. **AI-Powered Recommendations**

**Service**: `LearningPathService`

**How It Works:**
1. Analyzes student's current **SkillScores**
2. Identifies gaps or areas for growth
3. Recommends the **next best task** based on:
   - Learning path progression
   - Skill levels that need practice
   - Task difficulty matching student ability
   - Engagement history

**Endpoint**: `GET /api/v1/students/me/next-task`

**Student Dashboard Feature:**
- "Let Stellar choose my next mission" button
- Shows recommended task with AI-generated explanation
- Example: *"Great work on present tense! This task will help you practice past tense, which is the natural next step."*

### LEARN Data Flow

```
Student → Enrolls in Learning Path
        → Progresses through Modules
        → Completes Tasks (guided by AI recommendations)
        → Skills improve (tracked via SkillScore)
        → Module completion triggers VERIFY
```

### Technical Implementation - LEARN

**Backend Models:**
- `Skill` (`backend/app/models/skill.py`)
- `LearningPath` (`backend/app/models/learning_path.py`)
- `LearningModule` (`backend/app/models/learning_path.py`)
- `SkillScore` (`backend/app/models/skill.py`)

**Backend Services:**
- `LearningPathService` (`backend/app/services/learning_paths.py`)
  - `get_next_best_task_for_student()`
  - `calculate_module_completion()`
  - `update_skill_scores_from_task()`

**Backend Endpoints:**
- `GET /api/v1/learning-paths` - List available paths
- `GET /api/v1/students/me/learning-paths` - Student's enrolled paths
- `GET /api/v1/students/me/next-task` - AI-recommended next task
- `GET /api/v1/students/me/skills` - Student's skill profile

**Frontend Components:**
- Student Dashboard: "My Skills" section
- Student Dashboard: "Next Mission" recommendation card
- Learning Paths explorer page

---

## ✅ Part 2: VERIFY - Competency Validation

### What is VERIFY?

VERIFY is the process of confirming that a student has genuinely mastered a skill or completed a learning milestone with understanding, not just completion.

**Key Principle:** *Completion ≠ Understanding. Verification = Proof of Competency.*

### Types of Verification

#### 1. **AI Verification** (Automated)

The AI mentor evaluates student performance in real-time during conversations, quizzes, and tasks.

**Criteria:**
- Response quality (accuracy, depth)
- Consistency across multiple interactions
- Progress over time
- Engagement level

**Example:**
- Student completes 5 conversation tasks practicing past tense
- AI analyzes transcripts, correctness, fluency
- If score ≥ 80% across all 5 tasks, AI issues a verification

#### 2. **Teacher Verification** (Human Review)

Teachers can review student work and manually verify competencies.

**Use Cases:**
- Final assessment for sensitive skills
- Project-based work requiring subjective evaluation
- Parent-requested verification

**Teacher Dashboard Feature:**
- View pending verifications
- Review student submissions
- Approve or request revision

#### 3. **System Verification** (Rule-Based)

Automated verification based on objective criteria:
- Module completion (all tasks done with ≥ X score)
- XP thresholds reached
- Streak achievements

### SkillScore - The Verification Metric

**Database Model**: `SkillScore`

Fields:
- `student_id`, `skill_id`
- `score` (0-100, representing mastery level)
- `last_assessed_at`
- `source` (ai/teacher/system)
- `notes` (optional context)

**How Scores Update:**
- Task completion → Small incremental update
- Module completion → Significant update
- Teacher verification → Authoritative update (can override)

**Score Ranges:**
- 0-20: Novice
- 21-40: Developing
- 41-60: Competent
- 61-80: Proficient
- 81-100: Expert

### Verification Events

**Database Model**: `Verification`

Fields:
- `student_id`
- `skill_id` or `module_id` (what was verified)
- `verifier_type` (ai/teacher/system)
- `verifier_id` (optional, e.g., teacher user ID)
- `method` (quiz/conversation/assignment/exam)
- `result` (pass/fail/score)
- `created_at`
- `metadata` (JSON with evidence, scores, notes)

**Purpose:**
- Creates an audit trail of verification
- Required evidence for credential issuance
- Parents can review verification history

### VERIFY Workflow Example

```
1. Student completes Module 1: "Basic Sentence Structure"
2. System checks:
   - All 8 tasks in module completed? ✓
   - Average task score ≥ 70%? ✓
   - At least 3 AI conversation sessions? ✓
3. System creates Verification:
   - Type: "system"
   - Method: "module_completion"
   - Result: "pass"
   - Updates SkillScore for related skills
4. Triggers credential issuance (→ OWN phase)
```

### Technical Implementation - VERIFY

**Backend Models:**
- `SkillScore` (`backend/app/models/skill.py`)
- `Verification` (`backend/app/models/verification.py`)

**Backend Services:**
- `VerificationService` (`backend/app/services/verification.py`)
  - `check_module_completion_verification()`
  - `create_verification_event()`
  - `update_skill_scores()`

**Backend Endpoints:**
- `GET /api/v1/students/me/verifications` - Student's verification history
- `POST /api/v1/verifications/module/{module_id}` - Trigger verification check
- `GET /api/v1/teachers/verifications/pending` - Teacher pending reviews

**Frontend Components:**
- Student Dashboard: "Verification Progress" indicator
- Teacher Dashboard: "Pending Verifications" queue
- Parent Dashboard: "Verification History" timeline

---

## 🏆 Part 3: OWN - Student-Owned Credentials

### What is OWN?

OWN represents the revolutionary concept that students **truly own** their verified competencies as **portable, blockchain-ready credentials** that belong to them for life.

**The Vision:**
- Traditional education: School owns your transcript, locked in their database
- **Stellar AI**: You own your competencies as verifiable credentials
- Future: These credentials are blockchain-anchored, globally portable, tamper-proof

### Credentials - Digital Proof of Competency

**Database Model**: `Credential`

A credential is an official, verifiable statement that a student has mastered a skill or completed a learning milestone.

Fields:
- `id`, `student_id`
- `skill_id` or `module_id` (what this credential proves)
- `title` (e.g., "English A1 - Basic Conversation")
- `description` (what the student can do)
- `issued_at`
- `issuer_type` (ai/teacher/school/system)
- `issuer_id` (optional reference)
- `status` (draft/issued/revoked)
- `metadata` (JSON: evidence, verification references)

**Credential Types:**
1. **Skill Credentials**: Prove mastery of a specific skill
2. **Module Credentials**: Prove completion of a learning module
3. **Path Credentials**: Prove completion of entire learning path

**Example Credential:**
```json
{
  "title": "English Grammar - Present Tense Mastery",
  "description": "Student demonstrates proficient use of present simple and present continuous tenses in written and spoken English",
  "issued_at": "2025-11-14",
  "issuer_type": "ai",
  "evidence": {
    "tasks_completed": 12,
    "average_score": 87,
    "verification_count": 3,
    "teacher_confirmed": true
  }
}
```

### Blockchain Integration - Future-Proof Ownership

**Why Blockchain?**
- **Immutability**: Once issued, cannot be altered or deleted
- **Portability**: Student carries credentials across schools, platforms, countries
- **Verifiability**: Anyone can verify authenticity without contacting the school
- **Student Control**: Student decides who can view their credentials

**Database Model**: `OnChainCredential`

Fields:
- `credential_id` (links to Credential)
- `chain_name` (e.g., "polygon-mainnet", "ethereum-sepolia")
- `contract_address` (smart contract)
- `token_id` or `transaction_hash`
- `created_at`
- `is_simulated` (true for MVP, false when real blockchain)

**MVP Implementation: Simulated Blockchain**

For the MVP, blockchain minting is **simulated**:
- No real transaction costs
- Instant "minting"
- Full credential functionality
- Same API/UX as real blockchain

**When ready for production:**
- Add `BLOCKCHAIN_PROVIDER_URL` to `.env`
- Add `BLOCKCHAIN_PRIVATE_KEY` (or use wallet integration)
- Update `BlockchainService` internals (same API signature)
- Flip `is_simulated` to `false`

### BlockchainService - Abstraction Layer

**Service**: `BlockchainService` (`backend/app/services/blockchain.py`)

**Key Method:**
```python
@staticmethod
async def mint_credential(
    credential: Credential,
    db: AsyncSession
) -> OnChainCredential:
    """
    Mint a credential on-chain (or simulate for MVP)

    MVP: Creates simulated on-chain record
    Production: Deploys real NFT/SBT on blockchain
    """
```

**Supported (Future):**
- Polygon (low-cost, fast)
- Ethereum Layer 2s (Arbitrum, Optimism)
- Soulbound Tokens (SBTs) - non-transferable credentials

### Credential Issuance Workflow

```
1. Student completes Module X with verification
2. VerificationService checks if credential criteria met:
   - All verifications passed? ✓
   - Skill scores ≥ threshold? ✓
3. CredentialService.create_credential():
   - Creates Credential record
   - Status: "issued"
4. (Optional) Student or system triggers minting:
   - POST /api/v1/credentials/mint/{credential_id}
5. BlockchainService.mint_credential():
   - MVP: Simulated on-chain record
   - Production: Real blockchain transaction
6. Student sees:
   - "You earned: English A1 - Basic Conversation"
   - Badge: "On-chain (simulated)" or "On-chain ✓"
```

### Student Credential Portfolio

**Student Dashboard Features:**

**"My Credentials" Section:**
- Lists all issued credentials
- Shows:
  - Title & description
  - Issue date
  - Issuer (AI/Teacher/School)
  - Status badge ("Issued", "On-chain")
  - Share button (future: generate verifiable link)

**Credential Details Page:**
- Full description of what the credential proves
- Verification evidence (tasks completed, scores, etc.)
- Blockchain information (if minted)
- Download as PDF (future)
- Share on LinkedIn (future)

### OWN for Parents

Parents can view their child's credentials:
- `GET /api/v1/parents/me/children/{student_id}/credentials`
- Shows what their child has officially achieved
- More meaningful than XP or grades

### OWN for Schools/Teachers

Schools can:
- Issue official credentials
- Review credential requests
- Track how many credentials issued school-wide

### Technical Implementation - OWN

**Backend Models:**
- `Credential` (`backend/app/models/credential.py`)
- `OnChainCredential` (`backend/app/models/credential.py`)

**Backend Services:**
- `CredentialService` (`backend/app/services/credentials.py`)
  - `create_credential_from_verification()`
  - `issue_credential_to_student()`
- `BlockchainService` (`backend/app/services/blockchain.py`)
  - `mint_credential()` (simulated for MVP)

**Backend Endpoints:**
- `GET /api/v1/credentials/me` - Student's credentials
- `POST /api/v1/credentials/mint/{id}` - Mint on blockchain
- `GET /api/v1/parents/me/children/{id}/credentials` - Parent view

**Frontend Components:**
- Student Dashboard: "My Credentials" card
- Credential detail modal/page
- "Mint on blockchain" button (if not yet minted)

---

## 🔄 Complete LVO Flow: End-to-End Example

### Scenario: Maria Masters Basic English

**Phase 1: LEARN**
1. Maria (8 years old) logs into Stellar AI
2. System recommends Learning Path: "English A1 for Beginners"
3. Maria enrolls and starts Module 1: "Greetings and Introductions"
4. She clicks "Let Stellar choose my next mission"
5. AI recommends: Task "Practice Saying Hello" (conversation with AI avatar)
6. Maria completes the task, earns XP, updates SkillScore for "Basic Greetings"

**Phase 2: VERIFY**
7. After 6 tasks in Module 1, Maria completes the module
8. System checks verification criteria:
   - All tasks done: ✓
   - Average score: 85% ✓
   - AI conversation quality: Good ✓
9. System creates Verification event:
   - Type: "system"
   - Method: "module_completion"
   - Result: "pass"
10. SkillScore for "Basic Greetings" updated to 85

**Phase 3: OWN**
11. System triggers credential issuance
12. Credential created:
    - Title: "English A1 - Greetings and Basic Communication"
    - Description: "Can introduce herself and engage in simple greetings"
13. Notification: "🎉 You earned a new credential!"
14. Maria views in "My Credentials"
15. (Optional) Maria clicks "Mint on blockchain"
16. System creates simulated on-chain record
17. Badge shows: "On-chain (simulated)"

**Parent View:**
- Maria's mom receives weekly email: "Maria earned 1 new credential this week!"
- Views in Parent Dashboard: verified proof of Maria's English skills

**Future:**
- Maria transfers to new school in another country
- New school accepts her Stellar AI credentials (blockchain-verified)
- Maria doesn't have to retake placement tests

---

## 📊 Database Schema: LVO Models

### New Tables (Beyond MVP)

**Skills Management:**
```sql
skills (
  id, name, description, category, level, age_group
)

skill_scores (
  id, student_id, skill_id, score, last_assessed_at, source, notes
)
```

**Learning Paths:**
```sql
learning_paths (
  id, name, description, recommended_age_min, recommended_age_max
)

learning_modules (
  id, learning_path_id, name, description, order_index
)

module_tasks (many-to-many)
  module_id, task_id
```

**Verification:**
```sql
verifications (
  id, student_id, skill_id, module_id,
  verifier_type, verifier_id, method, result,
  created_at, metadata
)
```

**Credentials & Blockchain:**
```sql
credentials (
  id, student_id, skill_id, module_id,
  title, description, issued_at,
  issuer_type, issuer_id, status, metadata
)

on_chain_credentials (
  id, credential_id, chain_name,
  contract_address, token_id, transaction_hash,
  created_at, is_simulated
)
```

### Relationships

```
Student
  → has many SkillScores
  → has many Verifications
  → has many Credentials

Skill
  → has many SkillScores (across students)
  → linked to Tasks (many-to-many)

LearningPath
  → has many Modules

Module
  → has many Tasks (many-to-many)

Credential
  → may have one OnChainCredential (if minted)
```

---

## 🛠️ Technical Architecture

### Backend Structure

```
backend/app/
├── models/
│   ├── skill.py (Skill, SkillScore)
│   ├── learning_path.py (LearningPath, LearningModule)
│   ├── verification.py (Verification)
│   ├── credential.py (Credential, OnChainCredential)
├── schemas/
│   ├── skill.py
│   ├── learning_path.py
│   ├── verification.py
│   ├── credential.py
├── services/
│   ├── learning_paths.py (LearningPathService)
│   ├── verification.py (VerificationService)
│   ├── credentials.py (CredentialService)
│   ├── blockchain.py (BlockchainService)
├── routers/
│   ├── skills.py
│   ├── learning_paths.py
│   ├── verifications.py
│   ├── credentials.py
```

### Frontend Structure

```
src/
├── pages/
│   ├── StudentDashboard.tsx (enhanced with Skills, Credentials)
│   ├── LearningPathsPage.tsx (new)
│   ├── CredentialsPage.tsx (new)
├── components/
│   ├── learning/
│   │   ├── NextMissionCard.tsx
│   │   ├── SkillsProfile.tsx
│   │   ├── LearningPathProgress.tsx
│   ├── credentials/
│   │   ├── CredentialCard.tsx
│   │   ├── CredentialsList.tsx
│   │   ├── MintButton.tsx
```

---

## 🌍 Value Propositions by Stakeholder

### For Students
- ✅ Own your achievements forever
- ✅ Portable credentials across schools/platforms
- ✅ AI guides your learning journey
- ✅ Clear proof of what you know

### For Parents
- ✅ See verified competencies, not just grades
- ✅ Track real skill development
- ✅ Peace of mind: credentials are tamper-proof
- ✅ Child's portfolio follows them for life

### For Teachers
- ✅ Focus on verification, not data entry
- ✅ Issue meaningful credentials, not just grades
- ✅ AI handles routine assessments
- ✅ Track class-wide skill gaps

### For Schools
- ✅ Differentiate with blockchain-ready credentials
- ✅ Attract parents seeking modern education
- ✅ Reduce administrative burden
- ✅ Join the future of competency-based learning

### For Investors
- ✅ Clear monetization: Premium credential services
- ✅ Network effects: More students = more valuable credential network
- ✅ Blockchain integration: Positioned for Web3 education
- ✅ Scalable: AI automates verification

---

## 🚀 Roadmap: From MVP to Production

### Phase 1: MVP (Current)
- ✅ Simulated blockchain
- ✅ Basic recommendation engine
- ✅ System + AI verification
- ✅ Local credential storage

### Phase 2: Enhanced AI
- Advanced recommendation algorithms (ML-based)
- Personalized learning paths
- Predictive skill gap analysis
- Natural language skill assessments

### Phase 3: Real Blockchain
- Integration with Polygon/Ethereum L2
- Real NFT/SBT minting
- Wallet integration
- Credential marketplace

### Phase 4: Ecosystem
- Credential verification API for employers/schools
- Inter-school credential transfer protocol
- Credential-based learning communities
- Open credential standard (W3C Verifiable Credentials)

---

## 🔐 Security & Privacy

**Student Data:**
- Credentials stored encrypted
- Blockchain records are pseudonymous (no PII on-chain)
- Student controls credential visibility

**Verification Integrity:**
- All verifications logged with timestamps
- Teacher verifications require auth
- AI verifications include confidence scores
- Audit trail for all credential issuance

---

## 📖 Glossary

- **Credential**: Digital proof of a verified competency
- **LVO**: Learn - Verify - Own (Stellar AI's core principle)
- **Minting**: Creating an on-chain record of a credential
- **Module**: A step within a learning path
- **On-chain**: Stored on blockchain (immutable, decentralized)
- **SBT**: Soulbound Token (non-transferable blockchain credential)
- **Skill**: A specific, measurable competency
- **SkillScore**: A student's current assessed level for a skill
- **Verification**: The process of confirming skill mastery

---

## 📞 Questions?

**For Technical Implementation:**
- See: `backend/app/models/`, `backend/app/services/`
- API Docs: `http://localhost:8000/docs`

**For Business/Partnerships:**
- Contact: partnerships@stellar-ai.com

**For Investors:**
- Deck: Available on request

---

**Stellar AI: Learn - Verify - Own**
*Empowering students to own their learning journey.*
