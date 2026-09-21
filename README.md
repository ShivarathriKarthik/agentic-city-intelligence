# 🌆 City Intelligence Agent

An **Agentic AI-powered City Intelligence Assistant** built with **LangChain, Google Gemini, OpenWeather API, Tavily, Runnable pipelines, and Streamlit**.

The application allows users to ask natural-language questions about a city and automatically decides which tools are required to answer the request.

For example:

- "What's the weather in Hyderabad?"
- "Give me the latest news about Hyderabad."
- "What's the weather and latest news in Mumbai?"
- "Tell me the current weather in Bangalore."

The agent automatically invokes the appropriate tools and combines their results into a final response.

---

## 🚀 Features

### 🤖 Agentic AI

Uses LangChain's modern agent architecture to automatically determine which tool should be called based on the user's request.

### 🌦️ Real-Time Weather

Uses the OpenWeather API to retrieve:

- Temperature
- Weather condition
- Humidity
- Wind speed

### 📰 Latest News

Uses Tavily Search to retrieve recent information and news related to a city.

### 🔧 Tool Calling

The agent has access to two tools:

```text
get_weather()
get_news()
```

The LLM decides when these tools are required.

### 🔄 Runnable Input Pipeline

User input is processed using LangChain's:

```python
RunnableLambda
```

The input is cleaned before being passed to the agent.

### 🧠 Gemini LLM

The application uses Google Gemini through:

```python
ChatGoogleGenerativeAI
```

### 🖥️ Streamlit UI

Provides a simple conversational web interface with:

- Chat history
- User messages
- AI responses
- Loading indicators
- Error handling

---

# 🏗️ Architecture

```text
                  ┌─────────────────────┐
                  │      User Input     │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Streamlit UI      │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  RunnableLambda     │
                  │ Input Preprocessing │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   LangChain Agent   │
                  │    Google Gemini    │
                  └──────────┬──────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
       ┌─────────────────┐       ┌─────────────────┐
       │  Weather Tool   │       │    News Tool    │
       │ OpenWeather API │       │  Tavily Search  │
       └────────┬────────┘       └────────┬────────┘
                │                         │
                └────────────┬────────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Final AI Answer   │
                  └─────────────────────┘
```

---

# 🧩 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangChain | Agent and tool orchestration |
| Google Gemini | Large Language Model |
| LangChain Google GenAI | Gemini integration |
| OpenWeather API | Weather information |
| Tavily | Web/news search |
| RunnableLambda | Input preprocessing |
| Streamlit | Web application UI |
| python-dotenv | Environment variable management |
| Requests | HTTP API requests |

---

# 📁 Project Structure

```text
city-intelligence-agent/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/city-intelligence-agent.git
```

Move into the project directory:

```bash
cd city-intelligence-agent
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

---

# 📦 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 4. Configure API Keys

Create a `.env` file in the project root.

```env
OPENWEATHER_API_KEY=your_openweather_api_key
TAVILY_API_KEY=your_tavily_api_key
GOOGLE_API_KEY=your_google_api_key
```

Never commit `.env` to GitHub.

---

# ▶️ 5. Run the application

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 💬 Example Queries

### Weather

```text
What's the weather in Hyderabad?
```

### News

```text
Give me the latest news in Hyderabad.
```

### Weather + News

```text
Give me today's weather and latest news in Hyderabad.
```

The agent automatically determines which tools are required.

---

# 🔧 Agent Tools

## Weather Tool

```python
@tool
def get_weather(city: str) -> str:
```

This tool communicates with the OpenWeather API.

It returns:

```text
Temperature
Weather condition
Humidity
Wind speed
```

---

## News Tool

```python
@tool
def get_news(city: str) -> str:
```

This tool uses Tavily to search for recent information related to the requested city.

---

# 🤖 Agent Configuration

The project uses LangChain's agent architecture:

```python
agent = create_agent(
    model=llm,
    tools=[get_weather, get_news],
    system_prompt="..."
)
```

The agent can select the appropriate tool based on the user's request.

For example:

```text
User
 ↓
"What is the weather in Hyderabad?"
 ↓
Gemini
 ↓
get_weather("Hyderabad")
 ↓
OpenWeather API
 ↓
Weather result
 ↓
Final response
```

For a combined request:

```text
User
 ↓
"Weather and latest news in Hyderabad"
 ↓
Gemini
 ↓
┌─────────────────┐
│ get_weather     │
│ get_news        │
└────────┬────────┘
         ↓
    Tool Results
         ↓
    Gemini Response
         ↓
    Final Answer
```

---

# 🔄 Runnable Pipeline

The project also demonstrates LangChain Runnable concepts.

```python
def prepare_input(user_input: str) -> str:
    return user_input.strip()

input_runnable = RunnableLambda(prepare_input)
```

The pipeline becomes:

```text
User Input
     ↓
RunnableLambda
     ↓
Cleaned Input
     ↓
Agent
```

This provides a simple example of preprocessing user input before sending it to an Agentic AI workflow.

---

# 🧠 Memory

The current version **does not implement persistent conversational memory**.

Streamlit maintains displayed chat messages using:

```python
st.session_state
```

However, those messages are not currently configured as persistent agent memory.

Future versions can add:

- Conversation memory
- LangGraph checkpointers
- Persistent sessions
- User-specific memory
- Redis/PostgreSQL-backed memory

---

# 🔐 Security

API keys are loaded from environment variables.

```python
os.getenv("OPENWEATHER_API_KEY")
os.getenv("TAVILY_API_KEY")
os.getenv("GOOGLE_API_KEY")
```

Do not hard-code API keys in Python files.

The `.env` file is excluded using `.gitignore`.

---

# 🚀 Future Improvements

Planned improvements include:

- [ ] Conversational memory
- [ ] LangGraph checkpointing
- [ ] Persistent chat sessions
- [ ] More city intelligence tools
- [ ] Air quality information
- [ ] Traffic information
- [ ] Flight information
- [ ] Local events
- [ ] Currency conversion
- [ ] Multi-agent architecture
- [ ] Tool execution tracing
- [ ] LangSmith observability
- [ ] Docker deployment
- [ ] Cloud deployment
- [ ] Authentication
- [ ] Production API layer

---

# 🎯 Learning Objectives

This project demonstrates practical implementation of:

- Agentic AI
- LLM tool calling
- LangChain Agents
- LangChain Tools
- RunnableLambda
- API integration
- Gemini integration
- Web search
- Streamlit
- Environment variables
- Error handling
- Agent orchestration

---

# 👨‍💻 Author

**Karthik Shivarathri**

AI / ML Engineer | Agentic AI Engineer

GitHub:

https://github.com/ShivarathriKarthik

---

# ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.
