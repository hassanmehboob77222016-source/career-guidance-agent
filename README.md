# 🎓 Career Guidance Agent for Pakistani Students

An AI-powered Student Hub designed to help students confidently navigate their career paths after completing their FSC. Built with a modern, calm aesthetic, the agent analyzes a student's marks and interests to generate a personalized roadmap.

## 🚀 Features
- **Intelligent Career Path Suggestions**: Uses Llama 3 (via Groq) to suggest local market-focused career paths based on FSC group, marks, and interests.
- **University Recommender**: Integrates with Tavily Search to find top Pakistani universities, fee estimates, and merit cutoffs based on the student's preferred city.
- **Scholarship Finder**: Discovers both local and international scholarships available for the student's specific background.
- **Free Course Suggester**: Recommends free online courses to help students start building necessary skills immediately.
- **Premium UI**: A distraction-free, beautifully designed web interface with soft gradients and glassmorphism styling.

## 🛠️ Tech Stack
- **Backend**: Python, FastAPI
- **AI / Agent Framework**: LangChain, LangGraph, Groq (Llama 3.1)
- **Web Search**: Tavily API
- **Frontend**: Vanilla HTML, CSS, JavaScript (Premium Custom UI)

## ⚙️ How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/career-guidance-agent.git
cd career-guidance-agent
```

### 2. Set up API Keys
Create a `.env` file in the root directory based on `.env.example`:
```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 3. Run the Backend
Navigate to the backend folder, install dependencies, and start the FastAPI server:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 4. Run the Frontend
Simply open the `frontend/index.html` file in your preferred web browser or use a Live Server extension to start interacting with the agent!

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!

---
*Built to simplify campus life and empower the next generation of students.*
