from services.servicenow.client import ServiceNowClient


def get_user_by_email(email: str) -> dict | None:
    client = ServiceNowClient()

    resp = client.get(
        "/api/now/table/sys_user",
        params={"sysparm_query": f"email={email}"}
    )

    data = resp.json().get("result", [])
    return data[0] if data else None
