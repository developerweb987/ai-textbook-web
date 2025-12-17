# Physical AI & Humanoid Robotics Textbook - Full Stack Application

This repository contains a complete AI-Native textbook on Physical AI and Humanoid Robotics with a full-stack implementation. The project includes both a frontend Docusaurus-based textbook and a backend FastAPI RAG chatbot that provides AI-powered assistance for learning.

## 🌟 Features

- **Interactive Textbook**: Docusaurus-based textbook with 20 comprehensive chapters on Physical AI and Humanoid Robotics
- **AI-Powered Chatbot**: RAG (Retrieval-Augmented Generation) chatbot that can answer questions about textbook content
- **Text Selection**: Highlight text and ask questions about specific content sections
- **Session Management**: Chat sessions persist during browsing
- **Responsive Design**: Works on all device sizes

## 📚 Textbook Content

The textbook includes 20 comprehensive chapters:

### Part I: Physical AI Fundamentals
1. **Physical AI Fundamentals** - Core concepts of Physical AI vs. traditional AI
2. **Robotics Fundamentals and Kinematics** - Kinematic chains and mathematical representation
3. **Sensor Systems and Perception** - Various sensors and sensor fusion techniques
4. **Control Theory for Physical AI** - Control systems for robotic applications

### Part II: Locomotion and Manipulation
5. **Locomotion and Mobility** - Different locomotion principles in robotics
6. **Manipulation and Grasping** - Robotic manipulation and grasping techniques

### Part III: Human-Robot Interaction
7. **Human-Robot Interaction** - Principles of effective HRI

### Part IV: Learning and Adaptation
8. **Learning in Physical Systems** - Machine learning techniques for physical systems

### Part V: Safety and Ethics
9. **Safety and Ethics in Physical AI** - Safety principles and ethical considerations

### Part VI: Multi-Robot Systems
10. **Multi-Robot Systems** - Coordination and communication in multi-robot systems

### Part VII: Embodied Intelligence
11. **Embodied AI and Cognition** - Principles of embodied cognition in AI systems

### Part VIII: Hardware Design
12. **Hardware Design for Humanoid Robots** - Mechanical design principles for humanoid robots

### Part IX: Simulation and Transfer
13. **Simulation and Real-World Transfer** - Sim-to-real transfer challenges and solutions

### Part X: Efficiency and Optimization
14. **Energy Management and Efficiency** - Power optimization strategies for robots

### Part XI: Advanced Control
15. **Advanced Control Strategies** - Nonlinear, adaptive, and robust control methods

### Part XII: Applications and Future
16. **Applications and Case Studies** - Real-world applications and implementations
17. **Future Directions in Physical AI** - Emerging trends and technologies

### Part XIII: System Development
18. **Troubleshooting and Debugging** - Systematic approaches to troubleshooting
19. **Performance Optimization** - Performance optimization techniques
20. **Integration and System Design** - Complete system design and integration

## 🛠️ Tech Stack

### Frontend
- **Framework**: Docusaurus v3.9.2
- **Language**: React/TypeScript
- **Content Format**: Markdown with frontmatter metadata
- **Navigation**: Organized sidebar with logical grouping
- **Features**: Learning outcomes, diagrams, code examples, exercises for each chapter

### Backend
- **Framework**: FastAPI
- **Database**: SQLite (with option for PostgreSQL)
- **Vector Store**: Qdrant for document embeddings
- **AI Models**: Google Gemini and Cohere for RAG functionality
- **Architecture**: RESTful API with async processing

## 🚀 Quick Start

### Prerequisites
- Node.js (v18 or higher)
- Python (v3.9 or higher)
- pip package manager

### Environment Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/developerweb987/ai-textbook-web.git
   cd ai-textbook-web
   ```

2. **Setup Backend**:
   ```bash
   # Navigate to backend directory
   cd backend

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install Python dependencies
   pip install -r requirements.txt
   ```

3. **Setup Frontend**:
   ```bash
   # Navigate to frontend directory
   cd ai-textbook-web

   # Install npm dependencies
   npm install
   ```

### Running the Application

1. **Start the Backend**:
   ```bash
   cd backend
   python start_server.py
   # or: uvicorn main:app --reload --port 8000
   ```

2. **Start the Frontend**:
   ```bash
   cd ai-textbook-web
   npm start
   ```

3. **Access the Application**:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`
   - Backend API Docs: `http://localhost:8000/docs`

## 📋 Features

- **Comprehensive Coverage**: 20 detailed chapters covering all aspects of Physical AI
- **Learning Outcomes**: Clear objectives for each chapter
- **Code Examples**: Practical implementations in Python
- **Exercises**: Analysis, design, and implementation exercises
- **Diagrams**: Visual representations for complex concepts
- **Responsive Design**: Works on all device sizes
- **Search Functionality**: Built-in search across all content

## 🎯 Target Audience

- University-level engineering, computer science, and robotics students
- Professionals entering Physical AI or humanoid robotics fields
- Panaversity learners using AI-native textbooks with integrated agents
- Educators teaching robotics, AI agents, and control systems

## 🏗️ Project Structure

```
physical-ai-textbook/
├── ai-textbook-web/          # Docusaurus website
│   ├── docs/                # Textbook content (20 chapters)
│   ├── src/                 # Custom components
│   │   ├── components/      # React components (including BookChatbot)
│   │   └── css/             # Custom styles
│   ├── static/              # Static assets
│   ├── docusaurus.config.ts # Site configuration
│   └── sidebars.ts          # Navigation structure
├── backend/                 # FastAPI backend services
│   ├── api/                 # API routes and controllers
│   │   ├── routers/         # API route definitions
│   │   ├── services/        # Business logic
│   │   └── rag/             # RAG implementation
│   ├── db/                  # Database models and configuration
│   ├── config.py            # Configuration settings
│   ├── main.py              # FastAPI application entry point
│   └── requirements.txt     # Python dependencies
├── specs/                   # Specification documents
└── history/                 # Prompt history records
```

## 🔐 Environment Variables

### Backend (.env)
Create a `.env` file in the `backend/` directory with the following variables:

```env
# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
COHERE_API_KEY=your_cohere_api_key_here

# Qdrant Configuration (optional)
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here

# Database Configuration
DATABASE_URL=sqlite+aiosqlite:///./physical_ai_textbook.db

# Qdrant Collection Name
COLLECTION_NAME=documents

# Frontend docs path
DOCS_PATH=../ai-textbook-web/docs

# Chunking settings
CHUNK_SIZE_TOKENS=700

# CORS settings - comma-separated list of allowed origins
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001,http://localhost:4000,http://127.0.0.1:8000,http://localhost:5173,http://127.0.0.1:5173,http://localhost:8080,http://127.0.0.1:8080,http://localhost:3002,http://127.0.0.1:3002

# Logging
LOG_LEVEL=INFO
```

### Frontend (Environment)
For local development and production, you can create a `.env` file in the `ai-textbook-web/` directory:

```env
# Backend URL for development
REACT_APP_BACKEND_URL=http://localhost:8000

# For Vercel deployment, set this to your deployed backend URL
# REACT_APP_BACKEND_URL=https://your-backend-project-name.vercel.app
```

## 🚀 Deployment

### GitHub Pages (Frontend Only)
The textbook can be deployed to GitHub Pages. Update the `docusaurus.config.ts` file with your repository details:

```ts
{
  url: 'https://your-username.github.io',
  baseUrl: '/physical-ai-textbook/',
  organizationName: 'your-username',
  projectName: 'physical-ai-textbook',
}
```

### Vercel Deployment (Recommended)

For full-stack deployment with both frontend and backend, follow the detailed instructions in [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md).

#### Quick Deployment Steps:

1. **Deploy Backend**:
   - Import the `/backend` directory as a separate Vercel project
   - Use the provided `vercel.json` configuration
   - Set required environment variables (API keys, database URL, CORS settings)

2. **Deploy Frontend**:
   - Import the `/ai-textbook-web` directory as a separate Vercel project
   - Use the provided `vercel.json` configuration
   - Set `REACT_APP_BACKEND_URL` to your deployed backend URL

3. **Configure CORS**:
   - Update `CORS_ORIGINS` in backend environment variables to include your frontend's Vercel URL

For complete step-by-step instructions, see [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md).

## 🤝 Contributing

This textbook was developed using Spec-Kit Plus methodology following the requirements → specify → plan → task → implement workflow. Contributions are welcome to expand or improve the content.

## 📄 License

This textbook is available for educational and research purposes. Please attribute appropriately when using the content.# physical-ai-textbook
