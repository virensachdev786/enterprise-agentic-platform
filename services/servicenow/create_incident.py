from services.servicenow.client import ServiceNowClient

def create_incident(short_description: str, description: str, caller_id: str = None) -> dict:
    """
    Creates a ServiceNow incident and returns both the Number and Sys_ID.
    """
    client = ServiceNowClient()

    # Start with your verified fields
    payload = {
        "short_description": short_description,
        "description": description,
        "category": "IT Support",
        "impact": "2",
        "urgency": "2",
        "state": "2", 
        "work_notes": "Automatic incident created by Agentic AI Platform."
    }

    # ONLY add caller_id if we actually have one from the lookup
    if caller_id:
        payload["caller_id"] = caller_id
    resp = client.post("/api/now/table/incident", payload)
    
    # Check if request was successful before accessing JSON
    if resp.status_code != 201:
        raise Exception(f"ServiceNow Incident Creation Failed: {resp.text}")

    data = resp.json()
    result = data.get("result", {})

    # Return as a dictionary so the Dispatcher can store both
    return {
        "number": result.get("number"),
        "sys_id": result.get("sys_id")
    }

def update_incident_state(incident_sys_id: str, state: str = "6", close_notes: str = "Resolved by AI Agent") -> bool:
    """
    Updates the state of an incident (default 6 is 'Resolved').
    Requires the 32-character sys_id.
    """
    client = ServiceNowClient()
    
    payload = {
        "state": state,
        "close_code": "Solution provided",
        "close_notes": close_notes
    }

    # We use the sys_id in the URL for the PATCH request
    resp = client.patch(f"/api/now/table/incident/{incident_sys_id}", payload)
    
    return resp.status_code == 200