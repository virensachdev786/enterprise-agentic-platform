# ServiceNow APIs

Curl to `Query User` via email addr.

```jsx
curl "https://dev249455.service-now.com/api/now/table/sys_user?sysparm_query=email=viren.sachdev@veeren.co" \
  --request GET \
  --header "Accept:application/json" \
  --user 'admin:[password]'
  
Response:
{"result":[{"calendar_integration":"1","country":"","user_password":"$s$GtM4Z116SsRtuPsMv0rD2d9PoWkM+TY227uzkiDPyZ0=$nozWRgHBg4+bkXYte63AXY7a/o9Jgj+CzIh2/ZGwl2I=","last_login_time":"2025-12-29 04:30:06","source":"","sys_updated_on":"2025-12-29 04:30:42","building":"","web_service_access_only":"false","notification":"2","enable_multifactor_authn":"false","sys_updated_by":"viren.sachdev_test","sys_created_on":"2025-12-29 03:03:56","sys_domain":{"link":"https://dev249455.service-now.com/api/now/table/sys_user_group/global","value":"global"},"state":"","fax":"","identity_type":"human","vip":"false","sys_created_by":"admin","zip":"","home_phone":"","time_format":"","last_login":"2025-12-29","default_perspective":"","active":"true","sys_domain_path":"/","cost_center":"","phone":"","name":"Viren Test","employee_number":"","password_needs_reset":"false","gender":"","city":"","failed_attempts":"0","user_name":"viren.sachdev_test","roles":"","manager_hp1":"/H]02<","title":"TEST-Account","sys_class_name":"sys_user","sys_id":"811c456e83463a105454f2a6feaad360","federated_id":"RsJBUHKOsZV16LeD0d+njZapJis9VPPw6ejMca7zvFA=","internal_integration_user":"false","ldap_server":"","mobile_phone":"(484) 364-8529","street":"","company":"","department":"","first_name":"Viren","email":"viren.sachdev@veeren.co","introduction":"","preferred_language":"en","manager":"","locked_out":"false","sys_mod_count":"5","last_name":"Test","photo":"","avatar":"","middle_name":"","sys_tags":"","time_zone":"","schedule":"","date_format":"","location":""}]}
```

Curl to `Password Reset (cutom REST Resource in Service Now)`

Once, Login After Success - user is forced to reset password after `temp_password`

```jsx
  curl "https://dev249455.service-now.com/api/1743979/agentic_pw_helper/reset" \
  --request POST \
  --header "Accept:application/json" \
  --header "Content-Type:application/json" \
  --user 'admin:[password]' \
  --data '{"email": "viren.sachdev@veeren.co"}'
  
  Response:
  {"result":{"status":"success","temp_pw":"tw4aziyccp","user_name":"viren.sachdev_test"}
  
  Thought:
	  "Send the temp_pw to phone_number instead of Email itslef for Enhanced Security.
	  In Case Email is comporomised."
```

---

Curl to `create an incident`

```jsx
curl "https://dev249455.service-now.com/api/now/table/incident" \
  --request POST \
  --header "Accept:application/json" \
  --header "Content-Type:application/json" \
  --user 'admin:[password]' \
  --data '{
    "short_description": "Password Reset via Agentic AI",
    "caller_id": "811c456e83463a105454f2a6feaad360",
    "state": "2",
    "work_notes": "Automatic reset performed by AI Agent. User issued temporary password."
  }'
  
  RESPONSE:
  {"result":{"parent":"","made_sla":"true","caused_by":"","watch_list":"","upon_reject":"cancel","sys_updated_on":"2025-12-29 19:01:49","child_incidents":"0","hold_reason":"","origin_table":"","task_effective_number":"INC0010010","approval_history":"","number":"INC0010010","resolved_by":"","sys_updated_by":"admin","opened_by":{"link":"https://dev249455.service-now.com/api/now/table/sys_user/6816f79cc0a8016401c5a33be04be441","value":"6816f79cc0a8016401c5a33be04be441"},"user_input":"","sys_created_on":"2025-12-29 19:01:49","sys_domain":{"link":"https://dev249455.service-now.com/api/now/table/sys_user_group/global","value":"global"},"state":"2","route_reason":"","sys_created_by":"admin","knowledge":"false","order":"","calendar_stc":"","closed_at":"","cmdb_ci":"","delivery_plan":"","contract":"","impact":"3","active":"true","work_notes_list":"","business_service":"","business_impact":"","priority":"5","sys_domain_path":"/","rfc":"","time_worked":"","expected_start":"","opened_at":"2025-12-29 19:01:49","business_duration":"","group_list":"","work_end":"","caller_id":{"link":"https://dev249455.service-now.com/api/now/table/sys_user/811c456e83463a105454f2a6feaad360","value":"811c456e83463a105454f2a6feaad360"},"reopened_time":"","resolved_at":"","approval_set":"","subcategory":"","work_notes":"","universal_request":"","short_description":"Password Reset via Agentic AI","close_code":"","correlation_display":"","delivery_task":"","work_start":"","assignment_group":"","additional_assignee_list":"","business_stc":"","cause":"","description":"","origin_id":"","calendar_duration":"","close_notes":"","notify":"1","service_offering":"","sys_class_name":"incident","closed_by":"","follow_up":"","parent_incident":"","sys_id":"2c5728ba8302ba105454f2a6feaad33a","contact_type":"","reopened_by":"","incident_state":"2","urgency":"3","problem_id":"","company":"","reassignment_count":"0","activity_due":"","assigned_to":"","severity":"3","comments":"","approval":"not requested","sla_due":"","comments_and_work_notes":"","due_date":"","sys_mod_count":"0","reopen_count":"0","sys_tags":"","escalation":"0","upon_approval":"proceed","correlation_id":"","location":"","category":"inquiry"}}
```

Curl to `Resolve Incident`

```jsx
virensachdev@Mac enterprise-agentic-platform %  curl -X PATCH \
  https://dev249455.service-now.com/api/now/table/incident/2c5728ba8302ba105454f2a6feaad33a \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -u 'admin:[password]' \
  -d '{
    "state": "6",
    "close_code": "Solution provided",
    "close_notes": "Resolved via API using a verified valid closure code."
  }'
{"result":{"parent":"","made_sla":"true","caused_by":"","watch_list":"","upon_reject":"cancel","sys_updated_on":"2025-12-29 21:32:05","child_incidents":"0","hold_reason":"","origin_table":"","task_effective_number":"INC0010010","approval_history":"","number":"INC0010010","resolved_by":{"link":"https://dev249455.service-now.com/api/now/table/sys_user/6816f79cc0a8016401c5a33be04be441","value":"6816f79cc0a8016401c5a33be04be441"},"sys_updated_by":"admin","opened_by":{"link":"https://dev249455.service-now.com/api/now/table/sys_user/6816f79cc0a8016401c5a33be04be441","value":"6816f79cc0a8016401c5a33be04be441"},"user_input":"","sys_created_on":"2025-12-29 19:01:49","sys_domain":{"link":"https://dev249455.service-now.com/api/now/table/sys_user_group/global","value":"global"},"state":"6","route_reason":"","sys_created_by":"admin","knowledge":"false","order":"","calendar_stc":"9016","closed_at":"","cmdb_ci":"","delivery_plan":"","contract":"","impact":"3","active":"true","work_notes_list":"","business_service":"","business_impact":"","priority":"5","sys_domain_path":"/","rfc":"","time_worked":"","expected_start":"","opened_at":"2025-12-29 19:01:49","business_duration":"1970-01-01 02:30:16","group_list":"","work_end":"","caller_id":{"link":"https://dev249455.service-now.com/api/now/table/sys_user/811c456e83463a105454f2a6feaad360","value":"811c456e83463a105454f2a6feaad360"},"reopened_time":"","resolved_at":"2025-12-29 21:32:05","approval_set":"","subcategory":"","work_notes":"","universal_request":"","short_description":"Password Reset via Agentic AI","close_code":"Solution provided","correlation_display":"","delivery_task":"","work_start":"","assignment_group":"","additional_assignee_list":"","business_stc":"9016","cause":"","description":"","origin_id":"","calendar_duration":"1970-01-01 02:30:16","close_notes":"Resolved via API using a verified valid closure code.","notify":"1","service_offering":"","sys_class_name":"incident","closed_by":"","follow_up":"","parent_incident":"","sys_id":"2c5728ba8302ba105454f2a6feaad33a","contact_type":"","reopened_by":"","incident_state":"6","urgency":"3","problem_id":"","company":"","reassignment_count":"0","activity_due":"","assigned_to":"","severity":"3","comments":"","approval":"not requested","sla_due":"","comments_and_work_notes":"","due_date":"","sys_mod_count":"1","reopen_count":"0","sys_tags":"","escalation":"0","upon_approval":"proceed","correlation_id":"","location":"","category":"inquiry"}}
```