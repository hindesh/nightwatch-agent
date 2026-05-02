# tools.py — Infrastructure & SRE Capability Sandbox
# This is where you define the tools your agent can use to scout your infra.
# I've added a mock dataset to show a typical latency investigation.

MOCK_INFRA = {
    "endpoints": {
        "api-prod": {"status": "LIVE", "latency": "950ms", "load": "High"},
        "api-staging": {"status": "LIVE", "latency": "35ms", "load": "Normal"}
    },
    "system_events": {
        "api-prod": [
            "12:00:05 - WARN: High CPU on instance i-0af82",
            "12:15:30 - ERROR: DB connection timeout during session fetch",
            "12:15:40 - CRITICAL: Circuit breaker opened for primary-db"
        ],
        "api-staging": ["No alerts found."]
    }
}

def get_endpoint_metrics(endpoint_id: str):
    """Fetch current status and performance metrics for a service endpoint."""
    return MOCK_INFRA["endpoints"].get(endpoint_id, {"status": "UNKNOWN"})

def list_system_events(endpoint_id: str, pattern: str = ""):
    """Scout system alerts and event logs for a specific endpoint."""
    events = MOCK_INFRA["system_events"].get(endpoint_id, ["Endpoint not found."])
    if pattern:
        return [e for e in events if pattern.lower() in e.lower()]
    return events

# Registry: This defines the "API" your agent sees.
TOOL_REGISTRY = {
    "get_endpoint_metrics": {
        "function": get_endpoint_metrics,
        "description": "Check the health and performance (latency/load) of an endpoint.",
        "parameters": {"endpoint_id": "string (e.g. api-prod)"}
    },
    "list_system_events": {
        "function": list_system_events,
        "description": "Retrieve recent infrastructure alerts, errors, or logs.",
        "parameters": {"endpoint_id": "string", "pattern": "string (optional filter)"}
    }
}
