# CLI recipes (Salesforce CLI `sf`)

From the Agentforce Labs LabBox page. Placeholders: `<alias>` (page: `{{ORG_ALIAS}}`), `<AGENT_NAME>` (page sample: `Reservation_Agent`). Needs `sf` and `jq`. Run only steps the user approved; every write is marked **WRITE**.

## 1. Core Platform — verify only

```bash
sf data query --target-org <alias> --query "SELECT Id, Name, DurableId FROM Organization LIMIT 1"
sf org display --target-org <alias> --verbose --json | jq '.result'
```
Enabling Einstein, Agentforce and Data Cloud is Setup UI only (`ui-steps.md` §1).

## 2–4. API Access, Trust Layer, Identity Verification
No CLI equivalent. See `ui-steps.md` §2–4.

## 5. Permissions — AiAdmin

```bash
# Create the permission set if missing — WRITE
EXISTING=$(sf data query --target-org <alias> --json \
  --query "SELECT Id FROM PermissionSet WHERE Name='AiAdmin'" | jq -r '.result.totalSize')
if [ "$EXISTING" = "0" ]; then
  sf data create record --target-org <alias> --sobject PermissionSet \
    --values "Name='AiAdmin' Label='AiAdmin' Description='Admin permissions for Agentforce'"
fi

# Set system permissions through Metadata API — WRITE
DIR=$(mktemp -d)   # the page uses /tmp/aiadmin-deploy
mkdir -p "$DIR/permissionsets"
cat > "$DIR/permissionsets/AiAdmin.permissionset-meta.xml" <<'XML'
<?xml version="1.0" encoding="UTF-8"?>
<PermissionSet xmlns="http://soap.sforce.com/2006/04/metadata">
    <label>AiAdmin</label>
    <description>Admin permissions for Agentforce</description>
    <userPermissions><enabled>true</enabled><name>ManageAgentforceGrids</name></userPermissions>
    <userPermissions><enabled>true</enabled><name>ManageAgentforceTesting</name></userPermissions>
    <userPermissions><enabled>true</enabled><name>ManageAiAgents</name></userPermissions>
    <userPermissions><enabled>true</enabled><name>ApiEnabled</name></userPermissions>
</PermissionSet>
XML
cat > "$DIR/package.xml" <<'XML'
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types><members>AiAdmin</members><name>PermissionSet</name></types>
    <version>65.0</version>
</Package>
XML
sf project deploy start --target-org <alias> --source-dir "$DIR"

# Assign AiAdmin and Data Cloud User to the first active System Administrator — WRITE
ADMIN_ID=$(sf data query --target-org <alias> --json --query \
  "SELECT Id FROM User WHERE Profile.Name='System Administrator' AND IsActive=true ORDER BY CreatedDate ASC LIMIT 1" \
  | jq -r '.result.records[0].Id')
PS_ID=$(sf data query --target-org <alias> --json \
  --query "SELECT Id FROM PermissionSet WHERE Name='AiAdmin'" | jq -r '.result.records[0].Id')
sf data create record --target-org <alias> --sobject PermissionSetAssignment \
  --values "PermissionSetId='$PS_ID' AssigneeId='$ADMIN_ID'"
DC_PS_ID=$(sf data query --target-org <alias> --json \
  --query "SELECT Id FROM PermissionSet WHERE Label='Data Cloud User' LIMIT 1" | jq -r '.result.records[0].Id')
sf data create record --target-org <alias> --sobject PermissionSetAssignment \
  --values "PermissionSetId='$DC_PS_ID' AssigneeId='$ADMIN_ID'"
```

Ask the user which user should get the assignments; "first active System Administrator" is the page's default and may be wrong in a real org.

Verify (expect 1 record):
```bash
sf data query --target-org <alias> --query "SELECT Id, Assignee.Name, PermissionSet.Name FROM PermissionSetAssignment WHERE PermissionSet.Name='AiAdmin' AND Assignee.Profile.Name='System Administrator'"
```

## 6. Observability & Analytics
Enable the audit/analytics toggles in Setup first (`ui-steps.md` §6). Then — WRITE:
```bash
OPT_PS_ID=$(sf data query --target-org <alias> --json \
  --query "SELECT Id FROM PermissionSet WHERE Label='Access Agentforce Optimization' LIMIT 1" | jq -r '.result.records[0].Id')
sf data create record --target-org <alias> --sobject PermissionSetAssignment \
  --values "PermissionSetId='$OPT_PS_ID' AssigneeId='$ADMIN_ID'"
```

## 7. Digital Experiences
No CLI equivalent (`ui-steps.md` §7).

## 8. Routing
Prerequisite: Omni-Channel settings and Messaging enabled in Setup (`ui-steps.md` §8).
```bash
# Routing configuration — WRITE
sf data create record --target-org <alias> --sobject ServiceChannel \
  --values "DeveloperName='Agentforce_Service_configuration' MasterLabel='Agentforce Service configuration' RoutingModel='MostAvailable' SecondaryRoutingPriority=1"

# Queue via Metadata API — WRITE
QDIR=$(mktemp -d)   # the page uses /tmp/queue-deploy
mkdir -p "$QDIR/queues"
cat > "$QDIR/queues/Agentforce_Service_Queue.queue-meta.xml" <<'XML'
<?xml version="1.0" encoding="UTF-8"?>
<Queue xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Agentforce_Service_Queue</fullName>
    <name>Agentforce Service Queue</name>
    <queueSobject><sobjectType>MessagingSession</sobjectType></queueSobject>
</Queue>
XML
cat > "$QDIR/package.xml" <<'XML'
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types><members>Agentforce_Service_Queue</members><name>Queue</name></types>
    <version>65.0</version>
</Package>
XML
sf project deploy start --target-org <alias> --source-dir "$QDIR"
```
Note: the page's queue XML does not link the queue to the routing configuration or add members; the UI path does both (`ui-steps.md` §8). Check this after deploy.

Verify (each 1 record):
```bash
sf data query --target-org <alias> --query "SELECT Id, DeveloperName FROM ServiceChannel WHERE DeveloperName='Agentforce_Service_configuration'"
sf data query --target-org <alias> --query "SELECT Id, DeveloperName FROM Group WHERE Type='Queue' AND DeveloperName='Agentforce_Service_Queue'"
```

## 9. Agent Deployment — deploy, compile, publish, activate
Assumes the agent source is in `data/AgentforceDotCom` with an Agent Script bundle at `aiAuthoringBundles/<AGENT_NAME>/<AGENT_NAME>.agent`. All steps WRITE.

```bash
# 1. Deploy metadata
sf project deploy start --target-org <alias> --source-dir data/AgentforceDotCom

# 2. Session and instance (keep tokens out of output and logs)
ORG_JSON=$(sf org display --target-org <alias> --json)
SESSION_ID=$(echo "$ORG_JSON" | jq -r '.result.accessToken')
INSTANCE=$(echo "$ORG_JSON" | jq -r '.result.instanceUrl')

# 3. Named-user JWT
JWT=$(curl -s "$INSTANCE/agentforce/bootstrap/nameduser" \
  -H "Cookie: sid=$SESSION_ID" -H "Accept: application/json" | jq -r '.access_token')

# 4. Compile Agent Script
SCRIPT=$(jq -Rs . < "data/AgentforceDotCom/aiAuthoringBundles/<AGENT_NAME>/<AGENT_NAME>.agent")
COMPILED=$(curl -s -X POST "https://api.salesforce.com/einstein/ai-agent/v1.1/authoring/scripts" \
  -H "Authorization: Bearer $JWT" -H "Content-Type: application/json" -H "x-client-name: org-recipe" \
  -d "{\"assets\":[{\"type\":\"AFScript\",\"name\":\"AFScript\",\"content\":$SCRIPT}],\"afScriptVersion\":\"1.0.1\"}" \
  | jq '.compiledArtifact')

# 5. Publish version
BOT_VERSION_ID=$(curl -s -X POST "https://api.salesforce.com/einstein/ai-agent/v1.1/authoring/agents" \
  -H "Authorization: Bearer $JWT" -H "Content-Type: application/json" \
  -d "{\"agentDefinition\":$COMPILED,\"agentVersion\":\"1\",\"instanceConfig\":{\"endpoint\":\"$INSTANCE\"}}" \
  | jq -r '.botVersionId')

# 6. Activate
curl -s -X POST "$INSTANCE/services/data/v65.0/connect/bot-versions/$BOT_VERSION_ID/activation" \
  -H "Authorization: Bearer $SESSION_ID" -H "Content-Type: application/json" -d '{"status":"ACTIVE"}'
```
These endpoints are taken from the Labs page and are not in the official API references this repo indexes — unverified. If the `sf agent` commands in the installed CLI cover publish/activate (check `sf agent --help`), prefer them.

## 10. Messaging channel
Prerequisite: Messaging enabled (UI), agent deployed (§9), queue exists (§8). WRITE:
```bash
BOT_ID=$(sf data query --target-org <alias> --json \
  --query "SELECT Id FROM BotDefinition WHERE DeveloperName='<AGENT_NAME>'" | jq -r '.result.records[0].Id')
QUEUE_ID=$(sf data query --target-org <alias> --json \
  --query "SELECT Id FROM Group WHERE Type='Queue' AND DeveloperName='Agentforce_Service_Queue'" | jq -r '.result.records[0].Id')
sf apex run --target-org <alias> <<APEX
MessagingChannel mc = new MessagingChannel();
mc.DeveloperName = 'Salesforce_Agent';
mc.MasterLabel = 'Salesforce Agent Channel';
mc.MessageType = 'EmbeddedMessaging';
mc.MessagingPlatformKey = 'Salesforce_Agent-' + String.valueOf(Crypto.getRandomLong());
mc.IsActive = true;
mc.SessionHandlerId = '$BOT_ID';
mc.FallbackQueueId = '$QUEUE_ID';
insert mc;
System.debug(mc.Id);
APEX
```

## 11. Embedded Service Deployment
No CLI equivalent (`ui-steps.md` §11).

## 12. Experience Site
```bash
# WRITE
sf community create --target-org <alias> --name "Salesforce Agent" \
  --template-name "Build Your Own (LWR)" --url-path-prefix "salesforceagent"
# Add the Enhanced Chat component in Experience Builder (UI), then — WRITE
sf community publish --target-org <alias> --name "Salesforce Agent"
```
Verify (expect Status `Live`):
```bash
sf data query --target-org <alias> --query "SELECT Id, Name, Status FROM Network WHERE Name='Salesforce Agent'"
```

## 13. Site Domain & Trusted Domains
Site domain registration is UI only (`ui-steps.md` §13).
```bash
sf data query --target-org <alias> --query "SELECT Id, Domain FROM Domain WHERE DomainType='DNS' LIMIT 1"
# WRITE
sf data create record --target-org <alias> --sobject CorsWhitelistEntry --values "UrlPattern='https://*.my.site.com'"
sf community publish --target-org <alias> --name "Salesforce Agent"
```
Note: `CorsWhitelistEntry` is the CORS allowlist. The UI step instead adds the domain to the deployment site's "Trusted Domains for Inline Frames". They are different settings; if the widget still shows nothing, do the UI step too.

## 15–16. Coworker / Voice — verify only
```bash
sf data query --target-org <alias> --query "SELECT DeveloperName, MasterLabel FROM PermissionSetLicense WHERE DeveloperName IN ('AISearchUserPsl','AISearchAdminPsl')"
sf data query --use-tooling-api --target-org <alias> --query "SELECT IsServiceCloudVoiceEnabled FROM ServiceCloudVoiceSettings"
```
