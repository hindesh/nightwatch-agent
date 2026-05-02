# Nightwatch 🛡️

Nightwatch is a dead-simple **Agentic Reasoning Engine** for DevOps and SRE teams. I built this to help automate the "scouting" phase of an investigation—turning standard Python functions into a smart, iterative agent that can find the root cause of a system issue.

It uses a classic **Observe → Think → Act** loop. You give it an alert, and it uses your tools to figure out what's actually going on in your infra.

---

## 🛠️ Why use this?

Most agents just "guess" based on context. Nightwatch is built to **investigate**. 

- **Stateful Reasoning**: It doesn't just call a tool; it looks at the result, thinks about it, and decides the next best action.
- **Universal LLM Support**: Built-in connectors for Gemini, Claude, OpenAI, and Groq. It also works with local models via Ollama.
- **No Heavy Frameworks**: It's just plain Python. Under 100 lines of core logic. No complex DSLs to learn.
- **Audit Trace**: Every run generates a `trace.json`, giving you a perfect timeline of the agent's reasoning and tool output.

---

## 🚀 Quick Start

### 1. Get it running
```bash
# Clone and setup
git clone https://github.com/hindesh/nightwatch-agent.git
cd nightwatch-agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Demo
No API keys required. This uses a local "mock" brain to show you how a typical SRE investigation flows:
```bash
python main.py "Alert: api-prod is feeling slow"
```

### 3. Power it with an LLM
To see real reasoning in action, set your provider and key:
```bash
# Example for Gemini
export LLM_PROVIDER=gemini
export LLM_API_KEY=your_gemini_key
python main.py "Alert: Why is api-prod latency spiking?"
```

---

## 🏗️ Build Your Own Autonomous SRE

Nightwatch is a foundation. To build a custom investigator for your own infrastructure:

1.  **Define your tools**: Open `tools.py` and wrap your cloud APIs (AWS, GCP, K8s) into simple Python functions.
2.  **Register them**: Add your functions to the `TOOL_REGISTRY` at the bottom of the file.
3.  **Run**: The agent will now see your tools and use them to solve alerts.

---

## 📂 Project Structure

- `agent.py`: The core reasoning loop logic.
- `llm_factory.py`: Swapping model backends.
- `llm_providers/`: Modular connectors for different LLMs.
- `tools.py`: Your infrastructure capability sandbox.
- `mock_llm.py`: A simple reasoning script for the demo.
- `main.py`: The CLI entry point.

## 📄 License
MIT
