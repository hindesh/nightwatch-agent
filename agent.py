import json
from tools import TOOL_REGISTRY

# Keep it simple: Just a few lines to handle the agent loop.
class Agent:
    def __init__(self, llm, max_steps=5):
        self.llm = llm
        self.max_steps = max_steps

    def run(self, alert: str):
        """The main loop: Observe -> Think -> Act"""
        # Starting history with the user's alert
        messages = [{"role": "user", "content": alert}]
        trace = []

        print(f"\n⚡ Starting investigation for: '{alert}'")

        for step in range(1, self.max_steps + 1):
            # 1. Ask the LLM what to do
            try:
                response = self.llm.get_response(messages)
            except Exception as e:
                print(f"❌ Error from LLM provider: {e}")
                return

            # 2. Handle a tool call (Thinking/Acting)
            if response["type"] == "tool_call":
                thought = response.get("thought", "Investigating...")
                tool_name = response["tool"]
                params = response.get("parameters", {})

                print(f"\n[Step {step}] {thought}")
                print(f"       Action: {tool_name}({params})")

                # Actually execute the tool
                result = self.execute_action(tool_name, params)
                print(f"       Result: {result}")

                # Save to our audit log
                trace.append({
                    "step": step,
                    "thought": thought,
                    "action": {"tool": tool_name, "parameters": params},
                    "result": result
                })

                # Update the LLM's memory
                messages.append({"role": "assistant", "content": f"Thought: {thought}\nAction: {tool_name}({params})"})
                messages.append({"role": "tool", "content": str(result)})

            # 3. Handle a final answer (Conclusion)
            elif response["type"] == "final_answer":
                thought = response.get("thought", "Done.")
                answer = response["answer"]

                print(f"\n✨ Success! Found the cause in {step} steps.")
                print(f"   Thought: {thought}")
                print(f"   Final Answer: {answer}")

                trace.append({
                    "step": step,
                    "thought": thought,
                    "final_answer": answer
                })
                
                self.dump_trace(trace)
                return answer

        print(f"\n⚠️ Hit the max limit of {self.max_steps} steps. Stopping here.")
        self.dump_trace(trace)

    def execute_action(self, tool_name, params):
        if tool_name not in TOOL_REGISTRY:
            return f"Error: Tool '{tool_name}' doesn't exist."
        
        func = TOOL_REGISTRY[tool_name]["function"]
        try:
            return func(**params)
        except Exception as e:
            return f"Crash while running {tool_name}: {e}"

    def dump_trace(self, trace):
        """Save the session so we can debug it later."""
        with open("trace.json", "w") as f:
            json.dump(trace, f, indent=2)
        print("\n📄 Full reasoning trace saved to trace.json")
