# services/servicenow/context_processor.py

def prepare_ai_user_state(raw_user: any) -> dict:
    """
    Safely transforms ServiceNow data into AI context.
    Ensures no data-type mismatches crash the orchestration flow.
    """
    # 1. Guard against non-dictionary inputs (e.g., if user lookup returned a string)
    if not isinstance(raw_user, dict):
        print(f"WARNING: Expected dict for user, got {type(raw_user)}: {raw_user}")
        return {
            "full_name": "Unknown",
            "account_status": "not_found",
            "vip_status": False,
            "department": "Unknown",
            "failed_login_attempts": 0
        }

    # 2. Status Logic Transformation
    is_active = str(raw_user.get("active", "false")).lower() == "true"
    is_locked = str(raw_user.get("locked_out", "false")).lower() == "true"
    
    status = "active" if is_active else "terminated"
    if is_locked: 
        status = "locked"

    # 3. Robust Integer Conversion for Failed Attempts
    # This prevents the "invalid literal for int() with base 10: ''" error
    raw_attempts = raw_user.get("failed_attempts")
    
    # Handle empty strings or None before attempting conversion
    if raw_attempts is None or str(raw_attempts).strip() == "":
        failed_attempts_clean = 0
    else:
        try:
            failed_attempts_clean = int(raw_attempts)
        except (ValueError, TypeError):
            # If data is non-numeric (e.g. "three"), default to 0
            failed_attempts_clean = 0

    return {
        "full_name": raw_user.get("name", "Unknown"),
        "vip_status": str(raw_user.get("vip", "false")).lower() == "true",
        "account_status": status,
        "department": raw_user.get("department", "Unknown"),
        "failed_login_attempts": failed_attempts_clean
    }