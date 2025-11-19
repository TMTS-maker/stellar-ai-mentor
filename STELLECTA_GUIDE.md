# Stellecta - Interactive Landing Page

## 🌟 Overview

Stellecta is a next-generation EdTech platform that combines AI-powered personalized learning with blockchain-verified credentials. This interactive landing page showcases 8 specialized AI mentor agents, each with unique personalities and expertise.

## ✨ Features

### 🎨 Beautiful Design System
- **Custom Gradients**: Each AI agent has a unique gradient color scheme
- **Glass Morphism**: Modern frosted glass effects throughout
- **Smooth Animations**: Framer Motion powered transitions and micro-interactions
- **Responsive Design**: Fully optimized for mobile, tablet, and desktop

### 🤖 8 AI Super Agents

1. **Stella** - Mathematics Master (Purple/Pink gradient)
   - Analytical, Patient, Encouraging
   - Expertise: Algebra, Geometry, Calculus, Statistics

2. **Max** - Physics Genius (Blue/Cyan gradient)
   - Curious, Experimental, Inspiring
   - Expertise: Mechanics, Quantum Physics, Astrophysics

3. **Nova** - Chemistry Expert (Orange/Red gradient)
   - Energetic, Precise, Safety-conscious
   - Expertise: Organic Chemistry, Biochemistry

4. **Darwin** - Biology Guide (Green/Teal gradient)
   - Observant, Nurturing, Holistic
   - Expertise: Cell Biology, Genetics, Evolution

5. **Lexis** - English & Literature (Violet/Purple gradient)
   - Articulate, Creative, Empathetic
   - Expertise: Grammar, Literature, Creative Writing

6. **Neo** - AI & Technology (Slate/Gray gradient)
   - Forward-thinking, Analytical, Ethical
   - Expertise: Machine Learning, Python, AI Ethics

7. **Luna** - Arts & Music (Yellow/Orange gradient)
   - Expressive, Playful, Inspiring
   - Expertise: Visual Arts, Music Theory

8. **Atlas** - History & Geography (Amber/Orange gradient)
   - Worldly, Storyteller, Culturally aware
   - Expertise: World History, Geography

### 📱 Interactive Sections

#### Home
- Hero section with animated background
- Three Pillars: Learn, Verify, Own
- Agent showcase grid
- Blockchain credentials section
- Final CTA with stats

#### For Students
- Personalized learning benefits
- Interactive quiz example
- Gamification features
- Progress tracking

#### For Teachers
- Class management tools
- Real-time analytics dashboard
- Automated grading
- Time-saving features

#### For Parents
- Safety and compliance features
- Progress visibility dashboard
- Weekly reports
- Achievement tracking

### 💬 AI Chat Interface
- Click any agent card to open chat
- Simulated conversation interface
- Quick question shortcuts
- Agent personality in responses

## 🛠️ Technology Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Three.js** - 3D graphics (ready for integration)
- **React Three Fiber** - React renderer for Three.js
- **Shadcn UI** - Component library

## 🎨 Design System

### Colors (HSL)
```css
--stellar-purple: 262 83% 58%
--cosmic-blue: 239 84% 60%
--nebula-pink: 330 81% 60%
--stellar-cyan: 188 94% 43%
```

### Agent Gradients
Each agent has a unique gradient accessible via Tailwind classes:
- `gradient-stella` - Mathematics
- `gradient-max` - Physics
- `gradient-nova` - Chemistry
- `gradient-darwin` - Biology
- `gradient-lexis` - English
- `gradient-neo` - AI/Tech
- `gradient-luna` - Arts
- `gradient-atlas` - History

### Animations
- `animate-floating` - Gentle up/down motion
- `animate-glow` - Pulsing glow effect
- Custom hover and click interactions

## 🚀 Getting Started

1. **Install Dependencies**
```bash
npm install
```

2. **Run Development Server**
```bash
npm run dev
```

3. **Build for Production**
```bash
npm run build
```

## 📂 Project Structure

```
src/
├── assets/
│   ├── agents/          # AI character images
│   ├── hero-bg.jpg      # Hero background
│   └── stellar-logo.png # Logo
├── components/
│   ├── ui/              # Shadcn UI components
│   ├── sections/        # Page sections (Students, Teachers, Parents)
│   ├── Navigation.tsx
│   ├── HeroSection.tsx
│   ├── AgentCard.tsx
│   ├── AgentsShowcase.tsx
│   ├── AIChat.tsx
│   ├── ThreePillars.tsx
│   ├── BlockchainSection.tsx
│   ├── FinalCTA.tsx
│   └── Footer.tsx
├── data/
│   └── agents.ts        # Agent data structure
├── pages/
│   └── Index.tsx        # Main page component
└── index.css            # Design system & global styles
```

## 🎯 Next Steps

### Immediate Enhancements
1. **Real AI Integration**
   - Connect to OpenAI API or similar
   - Implement actual chat functionality
   - Add voice interaction

2. **3D Character Integration**
   - Use Ready Player Me for avatar generation
   - Implement Three.js scenes
   - Add interactive 3D elements

3. **Backend Integration**
   - Set up Supabase/Firebase
   - User authentication
   - Progress tracking
   - Blockchain credential minting

4. **Advanced Features**
   - Real-time learning analytics
   - Adaptive learning paths
   - Multi-language support (English/German)
   - Parent/Teacher dashboards

## 🌐 SEO Optimized

- Semantic HTML structure
- Meta tags configured
- Alt text on all images
- Mobile-responsive
- Fast loading times

## 📱 Mobile Optimized

- Hamburger menu on mobile
- Touch-friendly interactions
- Responsive grid layouts
- Optimized images

## 🔒 Privacy & Compliance

- GDPR compliant structure
- COPPA considerations
- Data privacy notices in footer
- Transparent data usage

## 💡 Tips for Customization

1. **Change Colors**: Edit `src/index.css` and update the CSS variables
2. **Add Agents**: Update `src/data/agents.ts` with new agent data
3. **Modify Sections**: Edit components in `src/components/sections/`
4. **Update Content**: All text is editable in the respective components

## 🤝 Contributing

This is a demo/prototype project showcasing modern web development practices for EdTech platforms.

## 📄 License

Educational demonstration project.

---


