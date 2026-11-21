#!/usr/bin/env bash
# Read-only audit of a Salesforce org against the Agentforce Labs "LabBox" baseline.
# Runs SOQL queries only; changes nothing. Usage: verify-org.sh <org-alias> [agent-developer-name]
set -uo pipefail

ALIAS="${1:?usage: verify-org.sh <org-alias> [agent-developer-name]}"
AGENT="${2:-}"
command -v sf >/dev/null || { echo "sf CLI not found"; exit 1; }
command -v jq >/dev/null || { echo "jq not found"; exit 1; }

count() {  # $1 = label, $2 = SOQL, $3 = optional --use-tooling-api
  local out n
  out=$(sf data query --target-org "$ALIAS" ${3:-} --json --query "$2" 2>/dev/null)
  if [ "$(echo "$out" | jq -r '.status // 1')" != "0" ]; then
    printf '%-42s %s\n' "$1" "CANNOT CHECK ($(echo "$out" | jq -r '.name // "query failed"'))"
    return
  fi
  n=$(echo "$out" | jq -r '.result.totalSize')
  if [ "$n" -gt 0 ]; then printf '%-42s %s\n' "$1" "OK ($n)"; else printf '%-42s %s\n' "$1" "MISSING"; fi
}

echo "== Org =="
sf data query --target-org "$ALIAS" --json --query "SELECT Id, Name, IsSandbox, OrganizationType FROM Organization" \
  | jq -r '.result.records[0] | "\(.Name)  \(.Id)  sandbox=\(.IsSandbox)  edition=\(.OrganizationType)"'

echo; echo "== Permissions =="
count "AiAdmin permission set"            "SELECT Id FROM PermissionSet WHERE Name='AiAdmin'"
count "AiAdmin assigned to a sysadmin"    "SELECT Id FROM PermissionSetAssignment WHERE PermissionSet.Name='AiAdmin' AND Assignee.Profile.Name='System Administrator'"
count "Data Cloud User assigned"          "SELECT Id FROM PermissionSetAssignment WHERE PermissionSet.Label='Data Cloud User'"
count "Access Agentforce Optimization assigned" "SELECT Id FROM PermissionSetAssignment WHERE PermissionSet.Label='Access Agentforce Optimization'"

echo; echo "== Routing & Messaging =="
count "ServiceChannel Agentforce_Service_configuration" "SELECT Id FROM ServiceChannel WHERE DeveloperName='Agentforce_Service_configuration'"
count "Queue Agentforce_Service_Queue"    "SELECT Id FROM Group WHERE Type='Queue' AND DeveloperName='Agentforce_Service_Queue'"
count "MessagingChannel Salesforce_Agent" "SELECT Id FROM MessagingChannel WHERE DeveloperName='Salesforce_Agent'"

echo; echo "== Agent =="
if [ -n "$AGENT" ]; then
  count "BotDefinition $AGENT"            "SELECT Id FROM BotDefinition WHERE DeveloperName='$AGENT'"
  # BotVersion check is an addition, not from the Labs page
  count "Active version of $AGENT"        "SELECT Id FROM BotVersion WHERE BotDefinition.DeveloperName='$AGENT' AND Status='Active'"
else
  echo "(pass an agent DeveloperName as 2nd argument to check it)"
fi

echo; echo "== Experience Site & domains =="
count "Network 'Salesforce Agent'"        "SELECT Id FROM Network WHERE Name='Salesforce Agent'"
count "Network 'Salesforce Agent' Live"   "SELECT Id FROM Network WHERE Name='Salesforce Agent' AND Status='Live'"
count "CORS entry https://*.my.site.com"  "SELECT Id FROM CorsWhitelistEntry WHERE UrlPattern='https://*.my.site.com'"

echo; echo "== Optional =="
count "Coworker PSLs (AISearch*)"         "SELECT Id FROM PermissionSetLicense WHERE DeveloperName IN ('AISearchUserPsl','AISearchAdminPsl')"
count "Service Cloud Voice enabled"       "SELECT Id FROM ServiceCloudVoiceSettings WHERE IsServiceCloudVoiceEnabled=true" "--use-tooling-api"

cat <<'EOF'

== Not checkable by API — confirm in Setup ==
- Einstein on, Agentforce Agents on, Data Cloud provisioned
- Enable SOAP API Login
- Einstein Trust Layer: LLM Data Masking off
- Identity verification for email changes off
- Audit & Feedback, RAG quality, Agent Analytics, Session Tracing, Service Agent Analytics app
- Digital Experiences enabled; Omni-Channel skills/secondary routing; Messaging enabled
- Embedded Service Deployment Salesforce_Agent (V2, published)
- Site domain registered; *.my.site.com in Trusted Domains for Inline Frames
- MCP Service (Beta) enabled and servers activated
EOF
