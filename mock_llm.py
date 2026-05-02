class MockLLM:
    """
    A rule-based brain for the demo.
    It mimics an SRE agent investigating a performance spike.
    """

    def __init__(self):
        self.step = 0

    def get_response(self, messages: list) -> dict:
        self.step += 1
        
        # Scrappy target detection
        alert = messages[0]["content"].lower()
        target = "api-prod" # default
        if "staging" in alert: target = "api-staging"

        # Step 1: Metrics Check
        if self.step == 1:
            return {
                "type": "tool_call",
                "thought": f"I've received an alert for {target}. I'll start by checking the current latency and status metrics.",
                "tool": "get_endpoint_metrics",
                "parameters": {"endpoint_id": target}
            }

        # Look at the tool output
        last_result = str(messages[-1]["content"])

        # Step 2: Investigation or Early Exit
        if self.step == 2:
            if "950ms" in last_result or "High" in last_result:
                return {
                    "type": "tool_call",
                    "thought": f"Latency on {target} is definitely spiking. I need to check the system events to see if a DB timeout or resource limit was hit.",
                    "tool": "list_system_events",
                    "parameters": {"endpoint_id": target, "pattern": "ERROR"}
                }
            else:
                return {
                    "type": "final_answer",
                    "thought": f"The metrics for {target} look within normal operating range.",
                    "answer": f"Everything looks healthy on {target}. Closing investigation."
                }

        # Step 3: Final Cause
        if "timeout" in last_result.lower():
            return {
                "type": "final_answer",
                "thought": f"The event logs for {target} confirm a database timeout coincided with the latency spike.",
                "answer": f"CAUSE: {target} is experiencing high latency due to primary-db timeouts. RECOMMENDATION: Check database connection pool and scale up if necessary."
            }
        
        return {
            "type": "final_answer",
            "thought": "Investigation complete. No clear cause found in available event logs.",
            "answer": f"Concluded investigation of {target}. No critical failure patterns detected."
        }
