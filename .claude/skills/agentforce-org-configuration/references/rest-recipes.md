# REST recipes

From the Agentforce Labs LabBox page. Placeholders: `$INSTANCE_URL`, `$ACCESS_TOKEN`. Every call sends `Authorization: Bearer $ACCESS_TOKEN`; POSTs also send `Content-Type: application/json`. API version v65.0. Only use when the CLI is not available; **WRITE** marks calls that change the org.

```bash
H=(-H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json")
API="$INSTANCE_URL/services/data/v65.0"
q() { curl -s -G "$API/query" "${H[@]}" --data-urlencode "q=$1"; }
```

## 1. Core Platform — verify
```bash
q "SELECT Id, Name, DurableId FROM Organization LIMIT 1"
curl -s "$API/limits" "${H[@]}" | jq '.EinsteinGenAiStandard'   # limit key per the page; unverified
```

## 5. Permissions
```bash
# WRITE
curl -s -X POST "$API/sobjects/PermissionSet" "${H[@]}" \
  -d '{"Name":"AiAdmin","Label":"AiAdmin","Description":"Admin permissions for Agentforce","IsOwnedByProfile":false}'
```
System permissions (`ManageAgentforceGrids`, `ManageAgentforceTesting`, `ManageAiAgents`, `ApiEnabled`) cannot be set this way — the page says use Metadata API (see `cli-recipes.md` §5) or the UI.
```bash
ADMIN_ID=$(q "SELECT Id FROM User WHERE Profile.Name='System Administrator' AND IsActive=true ORDER BY CreatedDate ASC LIMIT 1" | jq -r '.records[0].Id')
PS_ID=$(q "SELECT Id FROM PermissionSet WHERE Name='AiAdmin'" | jq -r '.records[0].Id')
# WRITE
curl -s -X POST "$API/sobjects/PermissionSetAssignment" "${H[@]}" \
  -d "{\"PermissionSetId\":\"$PS_ID\",\"AssigneeId\":\"$ADMIN_ID\"}"
```
Repeat the assignment for `Data Cloud User` (by Label) and, after §6 UI steps, `Access Agentforce Optimization`.

## 8. Routing (after Omni-Channel is enabled in Setup)
```bash
# WRITE
curl -s -X POST "$API/sobjects/ServiceChannel" "${H[@]}" \
  -d '{"DeveloperName":"Agentforce_Service_configuration","MasterLabel":"Agentforce Service configuration","RoutingModel":"MostAvailable","SecondaryRoutingPriority":1}'
curl -s -X POST "$API/sobjects/Group" "${H[@]}" \
  -d '{"Name":"Agentforce Service Queue","DeveloperName":"Agentforce_Service_Queue","Type":"Queue"}'
QUEUE_ID=$(q "SELECT Id FROM Group WHERE Type='Queue' AND DeveloperName='Agentforce_Service_Queue'" | jq -r '.records[0].Id')
curl -s -X POST "$API/sobjects/QueueSobject" "${H[@]}" \
  -d "{\"QueueId\":\"$QUEUE_ID\",\"SobjectType\":\"MessagingSession\"}"
```
The REST path builds the queue from `Group` + `QueueSobject`; the CLI path deploys `Queue` metadata. The page does not say which is preferred.

## 9. Agent Deployment
The page gives no REST request details beyond the four endpoints used in `cli-recipes.md` §9 (bootstrap JWT, `authoring/scripts`, `authoring/agents`, `connect/bot-versions/{id}/activation`) and says metadata goes in as a ZIP through the SOAP Metadata API.

## 10. Messaging channel (after agent + queue exist)
```bash
BOT_ID=$(q "SELECT Id FROM BotDefinition WHERE DeveloperName='<AGENT_NAME>'" | jq -r '.records[0].Id')
# WRITE
curl -s -X POST "$API/sobjects/MessagingChannel" "${H[@]}" -d "{
  \"DeveloperName\":\"Salesforce_Agent\",\"MasterLabel\":\"Salesforce Agent Channel\",
  \"MessageType\":\"EmbeddedMessaging\",\"MessagingPlatformKey\":\"Salesforce_Agent-$(date +%s)\",
  \"IsActive\":true,\"SessionHandlerId\":\"$BOT_ID\",\"FallbackQueueId\":\"$QUEUE_ID\"}"
```

## 12–13. Experience Site publish, trusted domain
Site creation has no REST equivalent on the page.
```bash
NETWORK_ID=$(q "SELECT Id FROM Network WHERE Name='Salesforce Agent'" | jq -r '.records[0].Id')
# WRITE
curl -s -X POST "$API/sobjects/CorsWhitelistEntry" "${H[@]}" -d '{"UrlPattern":"https://*.my.site.com"}'
curl -s -X POST "$API/connect/communities/$NETWORK_ID/publish" "${H[@]}"
```

## 15–16. Coworker / Voice — verify
```bash
q "SELECT DeveloperName, MasterLabel FROM PermissionSetLicense WHERE DeveloperName IN ('AISearchUserPsl','AISearchAdminPsl')"
curl -s -G "$API/tooling/query" "${H[@]}" --data-urlencode "q=SELECT IsServiceCloudVoiceEnabled FROM ServiceCloudVoiceSettings"
```
