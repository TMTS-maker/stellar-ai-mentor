export interface Agent {
  id: string;
  name: string;
  subject: string;
  personality: string[];
  expertise: string[];
  teachingStyle: string;
  targetAge: string;
  voice: string;
  gradient: string;
  icon: string;
  description: string;
}

export const agents: Agent[] = [
  {
    id: "stella",
    name: "Stella",
    subject: "Mathematics",
    personality: ["Analytical", "Patient", "Encouraging"],
    expertise: ["Algebra", "Geometry", "Calculus", "Statistics"],
    teachingStyle: "Step-by-step problem solving with visual demonstrations",
    targetAge: "12-18 years",
    voice: "Warm, clear, methodical",
    gradient: "gradient-stella",
    icon: "📐",
    description: "Your mathematical guide who makes complex concepts crystal clear through 3D visualizations"
  },
  {
    id: "max",
    name: "Max",
    subject: "Physics",
    personality: ["Curious", "Experimental", "Inspiring"],
    expertise: ["Mechanics", "Quantum Physics", "Electromagnetism", "Astrophysics"],
    teachingStyle: "Hands-on experiments and real-world applications",
    targetAge: "14-18 years",
    voice: "Enthusiastic, clear, wonder-filled",
    gradient: "gradient-max",
    icon: "⚛️",
    description: "Explore the universe's mysteries with AR/VR physics simulations and interactive experiments"
  },
  {
    id: "nova",
    name: "Nova",
    subject: "Chemistry",
    personality: ["Energetic", "Precise", "Safety-conscious"],
    expertise: ["Organic Chemistry", "Inorganic", "Biochemistry", "Lab Techniques"],
    teachingStyle: "Interactive lab simulations and molecular visualization",
    targetAge: "11-17 years",
    voice: "Upbeat, precise, encouraging",
    gradient: "gradient-nova",
    icon: "🧪",
    description: "Discover chemistry through safe virtual experiments and stunning molecular visualizations"
  },
  {
    id: "darwin",
    name: "Darwin",
    subject: "Biology",
    personality: ["Observant", "Nurturing", "Holistic"],
    expertise: ["Cell Biology", "Genetics", "Evolution", "Ecology"],
    teachingStyle: "Nature observation and systems thinking",
    targetAge: "10-17 years",
    voice: "Calm, nurturing, knowledgeable",
    gradient: "gradient-darwin",
    icon: "🧬",
    description: "Journey through life sciences with virtual microscopes and ecosystem simulations"
  },
  {
    id: "lexis",
    name: "Lexis",
    subject: "English & Literature",
    personality: ["Articulate", "Creative", "Empathetic"],
    expertise: ["Grammar", "Literature", "Creative Writing", "Rhetoric"],
    teachingStyle: "Story-based learning and writing workshops",
    targetAge: "8-18 years",
    voice: "Eloquent, warm, inspiring",
    gradient: "gradient-lexis",
    icon: "📚",
    description: "Master language and literature through storytelling and AI-powered writing assistance"
  },
  {
    id: "neo",
    name: "Neo",
    subject: "AI & Technology",
    personality: ["Forward-thinking", "Analytical", "Ethical"],
    expertise: ["Machine Learning", "Neural Networks", "Python", "AI Ethics"],
    teachingStyle: "Project-based coding and ethical discussions",
    targetAge: "13-18 years",
    voice: "Precise, futuristic, encouraging",
    gradient: "gradient-neo",
    icon: "🤖",
    description: "Build the future with hands-on AI projects and interactive code playgrounds"
  },
  {
    id: "luna",
    name: "Luna",
    subject: "Arts & Music",
    personality: ["Expressive", "Playful", "Inspiring"],
    expertise: ["Visual Arts", "Music Theory", "Digital Creation", "Composition"],
    teachingStyle: "Creative expression and technique mastery",
    targetAge: "6-18 years",
    voice: "Melodic, encouraging, passionate",
    gradient: "gradient-luna",
    icon: "🎨",
    description: "Unleash your creativity with AI-powered art and music generation tools"
  },
  {
    id: "atlas",
    name: "Atlas",
    subject: "History & Geography",
    personality: ["Worldly", "Storyteller", "Culturally aware"],
    expertise: ["World History", "Geography", "Cultural Studies", "Map Skills"],
    teachingStyle: "Story-driven learning and time-travel narratives",
    targetAge: "9-17 years",
    voice: "Adventurous, engaging, wise",
    gradient: "gradient-atlas",
    icon: "🗺️",
    description: "Travel through time with interactive timelines and immersive 3D historical maps"
  }
];

export const getAgentById = (id: string) => agents.find(agent => agent.id === id);
