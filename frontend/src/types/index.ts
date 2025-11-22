/**
 * TypeScript Type Definitions for Stellecta Platform
 */

// ============================================================================
// User & Authentication Types
// ============================================================================

export type UserType = 'student' | 'teacher' | 'parent' | 'admin';

export interface User {
  id: string;
  email: string;
  fullName: string;
  userType: UserType;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface Student extends User {
  schoolId: string;
  gradeLevel: number;
  age?: number;
  parentId?: string;
  hPemLevel: number;
  totalXp: number;
  currentLevel: number;
  stellarWalletAddress?: string;
}

export interface Teacher extends User {
  schoolId: string;
  subjects: string[];
}

export interface AuthTokens {
  accessToken: string;
  refreshToken?: string;
  tokenType: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  fullName: string;
  userType: UserType;
  schoolId?: string;
  gradeLevel?: number;
  age?: number;
}

// ============================================================================
// Agent & Chat Types
// ============================================================================

export type MentorId = 'stella' | 'max' | 'nova' | 'darwin' | 'lexis' | 'neo' | 'luna' | 'atlas';

export interface Mentor {
  id: MentorId;
  name: string;
  subject: string;
  description: string;
  avatar: string;
  personality: string;
}

export interface Message {
  id: string;
  sessionId: string;
  userId: string;
  mentorId: MentorId;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  xpEarned?: number;
  objectiveId?: string;
}

export interface ChatSession {
  id: string;
  studentId: string;
  mentorId: MentorId;
  subject: string;
  startTime: string;
  endTime?: string;
  messageCount: number;
  totalXpEarned: number;
}

export interface SendMessageRequest {
  message: string;
  sessionId?: string;
  mentorId?: MentorId;
}

export interface SendMessageResponse {
  text: string;
  mentorId: MentorId;
  llmProvider: string;
  tokensUsed: number;
  xpEarned: number;
  objectiveId?: string;
}

// ============================================================================
// Curriculum Types
// ============================================================================

export type CurriculumType = 'INDIAN_CBSE' | 'INDIAN_ICSE' | 'UK_NATIONAL' | 'UK_IGCSE' | 'US_COMMON_CORE';
export type Subject = 'MATH' | 'PHYSICS' | 'CHEMISTRY' | 'BIOLOGY' | 'LANGUAGE' | 'HISTORY' | 'TECH' | 'ARTS';

export interface Curriculum {
  id: string;
  curriculumType: CurriculumType;
  curriculumName: string;
  country: string;
  board?: string;
  description: string;
}

export interface CurriculumObjective {
  id: string;
  curriculumId: string;
  objectiveCode: string;
  objectiveText: string;
  subject: Subject;
  gradeLevel: number;
  difficultyLevel: number;
  parentObjectiveId?: string;
  prerequisites: string[];
}

export interface StudentSkillProgress {
  id: string;
  studentId: string;
  skillId: string;
  objectiveId: string;
  learnProgress: number;
  verifyProgress: number;
  ownProgress: number;
  masteryScore: number;
  lastPracticed: string;
}

// ============================================================================
// Gamification Types
// ============================================================================

export interface Badge {
  id: string;
  name: string;
  description: string;
  iconUrl: string;
  category: string;
  xpRequired: number;
  rarity: 'common' | 'rare' | 'epic' | 'legendary';
}

export interface StudentBadge {
  id: string;
  studentId: string;
  badgeId: string;
  earnedAt: string;
  badge: Badge;
}

export interface XPLog {
  id: string;
  studentId: string;
  xpAmount: number;
  source: string;
  description: string;
  timestamp: string;
}

export interface Streak {
  id: string;
  studentId: string;
  currentStreak: number;
  longestStreak: number;
  lastActiveDate: string;
}

export interface LeaderboardEntry {
  rank: number;
  studentId: string;
  studentName: string;
  totalXp: number;
  currentLevel: number;
  badgeCount: number;
}

// ============================================================================
// School & Classroom Types
// ============================================================================

export interface School {
  id: string;
  name: string;
  country: string;
  curriculumType: CurriculumType;
  address?: string;
  contactEmail?: string;
}

export interface Classroom {
  id: string;
  schoolId: string;
  teacherId: string;
  name: string;
  gradeLevel: number;
  subject: Subject;
  studentIds: string[];
}

// ============================================================================
// H-PEM Blockchain Types
// ============================================================================

export interface HPEMCredential {
  id: string;
  studentId: string;
  objectiveId: string;
  hPemScore: number;
  stellarTxHash: string;
  issuedAt: string;
  metadata: Record<string, any>;
}
