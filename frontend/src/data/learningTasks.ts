export interface Question {
  question: string;
  type: 'multiple-choice' | 'input' | 'text-input' | 'sorting';
  options?: string[];
  correctAnswer: string | string[];
  explanation: string;
  hint?: string;
}

export interface LearningTask {
  id: string;
  title: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  description: string;
  questions: Question[];
  xp: number;
}

export interface ChatMessage {
  sender: 'user' | 'agent';
  message: string;
  timestamp: Date;
}

export const learningTasks: Record<string, LearningTask[]> = {
  stella: [
    {
      id: 'math-1',
      title: 'Pattern Recognition',
      difficulty: 'Easy',
      description: 'Find the next number in the sequence',
      questions: [
        {
          question: 'What comes next? 2, 4, 6, 8, ?',
          type: 'multiple-choice',
          options: ['9', '10', '12', '14'],
          correctAnswer: '10',
          explanation: 'Each number increases by 2, so 8 + 2 = 10',
          hint: 'Look at the difference between consecutive numbers'
        },
        {
          question: 'Now try this: 5, 10, 15, 20, ?',
          type: 'multiple-choice',
          options: ['22', '25', '30', '35'],
          correctAnswer: '25',
          explanation: 'Each number increases by 5, so 20 + 5 = 25',
          hint: 'What number is being added each time?'
        }
      ],
      xp: 50
    },
    {
      id: 'math-2',
      title: 'Basic Algebra',
      difficulty: 'Medium',
      description: 'Solve for x',
      questions: [
        {
          question: 'If 3x + 5 = 14, what is x?',
          type: 'input',
          correctAnswer: '3',
          explanation: '3x = 14 - 5 = 9, so x = 9 ÷ 3 = 3',
          hint: 'First subtract 5 from both sides'
        },
        {
          question: 'Now try: 2x - 3 = 7, what is x?',
          type: 'input',
          correctAnswer: '5',
          explanation: '2x = 7 + 3 = 10, so x = 10 ÷ 2 = 5',
          hint: 'Add 3 to both sides first'
        }
      ],
      xp: 75
    },
    {
      id: 'math-3',
      title: 'Geometry Challenge',
      difficulty: 'Medium',
      description: 'Calculate the area',
      questions: [
        {
          question: 'What is the area of a rectangle with length 8 and width 5?',
          type: 'multiple-choice',
          options: ['13', '26', '40', '80'],
          correctAnswer: '40',
          explanation: 'Area = length × width = 8 × 5 = 40',
          hint: 'Remember: Area = length × width'
        }
      ],
      xp: 60
    }
  ],
  max: [
    {
      id: 'phys-1',
      title: 'Force & Motion',
      difficulty: 'Easy',
      description: 'Understanding Newton\'s Laws',
      questions: [
        {
          question: 'What happens to an object in motion if no force acts on it?',
          type: 'multiple-choice',
          options: ['It stops immediately', 'It continues at constant velocity', 'It speeds up', 'It falls down'],
          correctAnswer: 'It continues at constant velocity',
          explanation: 'This is Newton\'s First Law - an object in motion stays in motion unless acted upon by an external force',
          hint: 'Think about Newton\'s First Law of Motion'
        }
      ],
      xp: 50
    },
    {
      id: 'phys-2',
      title: 'Energy Conservation',
      difficulty: 'Medium',
      description: 'Potential and Kinetic Energy',
      questions: [
        {
          question: 'A ball at the top of a hill has 100J of potential energy. How much kinetic energy will it have at the bottom (ignoring friction)?',
          type: 'input',
          correctAnswer: '100',
          explanation: 'Energy is conserved! Potential energy converts to kinetic energy: 100J',
          hint: 'Energy cannot be created or destroyed, only transformed'
        }
      ],
      xp: 75
    }
  ],
  lexis: [
    {
      id: 'eng-1',
      title: 'Word Association',
      difficulty: 'Easy',
      description: 'Choose the best synonym',
      questions: [
        {
          question: 'What is a synonym for "happy"?',
          type: 'multiple-choice',
          options: ['Sad', 'Joyful', 'Angry', 'Tired'],
          correctAnswer: 'Joyful',
          explanation: 'Joyful means feeling or expressing great happiness',
          hint: 'Think of words that describe positive emotions'
        }
      ],
      xp: 50
    },
    {
      id: 'eng-2',
      title: 'Creative Writing',
      difficulty: 'Medium',
      description: 'Complete the story',
      questions: [
        {
          question: 'Write the next sentence: "The spaceship landed on the mysterious planet, and..."',
          type: 'text-input',
          correctAnswer: '',
          explanation: 'Great creativity! Keep exploring your imagination!',
          hint: 'Imagine what the astronauts might discover'
        }
      ],
      xp: 100
    }
  ],
  neo: [
    {
      id: 'ai-1',
      title: 'What is AI?',
      difficulty: 'Easy',
      description: 'Understanding artificial intelligence',
      questions: [
        {
          question: 'Which of these is an example of AI?',
          type: 'multiple-choice',
          options: ['A calculator', 'Voice assistants like Siri', 'A bicycle', 'A pencil'],
          correctAnswer: 'Voice assistants like Siri',
          explanation: 'Voice assistants use machine learning to understand and respond to human speech',
          hint: 'Which one can learn and adapt to user behavior?'
        }
      ],
      xp: 50
    },
    {
      id: 'ai-2',
      title: 'Algorithm Thinking',
      difficulty: 'Medium',
      description: 'Create a simple algorithm',
      questions: [
        {
          question: 'Put these steps in order to make a sandwich: A) Add filling B) Get bread C) Close sandwich D) Add second slice',
          type: 'multiple-choice',
          options: ['B-A-D-C', 'A-B-C-D', 'B-D-A-C', 'D-B-A-C'],
          correctAnswer: 'B-A-D-C',
          explanation: 'This is algorithmic thinking - breaking down tasks into logical steps!',
          hint: 'Start with getting the bread first'
        }
      ],
      xp: 75
    }
  ],
  nova: [
    {
      id: 'chem-1',
      title: 'Elements Basics',
      difficulty: 'Easy',
      description: 'Understanding the periodic table',
      questions: [
        {
          question: 'What is the chemical symbol for water?',
          type: 'multiple-choice',
          options: ['H2O', 'O2', 'CO2', 'NaCl'],
          correctAnswer: 'H2O',
          explanation: 'Water is H2O - two hydrogen atoms bonded to one oxygen atom!',
          hint: 'Water contains hydrogen and oxygen'
        }
      ],
      xp: 50
    }
  ],
  darwin: [
    {
      id: 'bio-1',
      title: 'Cell Biology',
      difficulty: 'Easy',
      description: 'Understanding cells',
      questions: [
        {
          question: 'What is the powerhouse of the cell?',
          type: 'multiple-choice',
          options: ['Nucleus', 'Mitochondria', 'Ribosome', 'Cell membrane'],
          correctAnswer: 'Mitochondria',
          explanation: 'Mitochondria produce energy (ATP) for the cell through cellular respiration!',
          hint: 'This organelle produces energy for the cell'
        },
        {
          question: 'Which organelle controls what enters and exits the cell?',
          type: 'multiple-choice',
          options: ['Nucleus', 'Mitochondria', 'Cell membrane', 'Vacuole'],
          correctAnswer: 'Cell membrane',
          explanation: 'The cell membrane acts as a selective barrier, controlling the movement of substances in and out of the cell!',
          hint: 'Think about the outer boundary of the cell'
        }
      ],
      xp: 50
    }
  ],
  luna: [
    {
      id: 'art-1',
      title: 'Color Theory',
      difficulty: 'Easy',
      description: 'Understanding primary colors',
      questions: [
        {
          question: 'Which colors are the three primary colors?',
          type: 'multiple-choice',
          options: ['Red, Blue, Yellow', 'Red, Green, Blue', 'Orange, Purple, Green', 'Black, White, Gray'],
          correctAnswer: 'Red, Blue, Yellow',
          explanation: 'Primary colors cannot be created by mixing other colors - they are the foundation!',
          hint: 'These colors cannot be made by mixing other colors'
        }
      ],
      xp: 50
    }
  ],
  atlas: [
    {
      id: 'hist-1',
      title: 'Ancient Civilizations',
      difficulty: 'Easy',
      description: 'World History',
      questions: [
        {
          question: 'Which ancient civilization built the pyramids?',
          type: 'multiple-choice',
          options: ['Romans', 'Greeks', 'Egyptians', 'Mayans'],
          correctAnswer: 'Egyptians',
          explanation: 'The ancient Egyptians built the pyramids as tombs for their pharaohs!',
          hint: 'This civilization was located along the Nile River'
        }
      ],
      xp: 50
    }
  ]
};
