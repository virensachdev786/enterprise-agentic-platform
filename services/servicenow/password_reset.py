# services/servicenow/password_reset.py
from services.servicenow.client import ServiceNowClient

def reset_password(email: str) -> str | None:
    client = ServiceNowClient()

    # Using the Scripted REST API endpoint you provided earlier
    # NOTE: You mentioned your API takes 'email' as a key
    payload = {"email": email}

    resp = client.post("/api/1743979/agentic_pw_helper/reset", payload)
    
    if resp.status_code == 200:
        data = resp.json()
        # The JSON you showed earlier: {"result":{"status":"success","temp_pw":"..."}}
        result = data.get("result", {})
        return result.get("temp_pw")
    
    return None