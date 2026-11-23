-- Unified AI Capability Registry, schema 0.1.0
-- Discovery store. A row is not permission to execute an action.
-- Join on id columns only. Display names are attributes.

PRAGMA foreign_keys = ON;

CREATE TABLE providers (
  id TEXT PRIMARY KEY,
  display_name TEXT NOT NULL
);

CREATE TABLE products (
  id TEXT PRIMARY KEY,
  provider_id TEXT NOT NULL REFERENCES providers(id),
  display_name TEXT NOT NULL,
  vendor_product_id TEXT
);

CREATE TABLE product_variants (
  id TEXT PRIMARY KEY,
  product_id TEXT NOT NULL REFERENCES products(id),
  display_name TEXT NOT NULL,
  vendor_variant_id TEXT
);

CREATE TABLE surfaces (
  id TEXT PRIMARY KEY,
  provider_id TEXT NOT NULL REFERENCES providers(id),
  display_name TEXT NOT NULL
);

CREATE TABLE runtimes (
  id TEXT PRIMARY KEY,
  display_name TEXT NOT NULL
);

CREATE TABLE processes (
  id TEXT PRIMARY KEY,
  display_name TEXT NOT NULL,
  model_status TEXT NOT NULL CHECK (model_status IN ('PILOT_BRIEF', 'CUSTOMER_CONFIRMED'))
);

CREATE TABLE process_steps (
  id TEXT PRIMARY KEY,
  process_id TEXT NOT NULL REFERENCES processes(id),
  step_order INTEGER NOT NULL,
  display_name TEXT NOT NULL,
  UNIQUE (process_id, step_order)
);

CREATE TABLE business_capabilities (
  id TEXT PRIMARY KEY,
  display_name TEXT NOT NULL
);

CREATE TABLE process_step_capabilities (
  id TEXT PRIMARY KEY,
  process_step_id TEXT NOT NULL REFERENCES process_steps(id),
  capability_id TEXT NOT NULL REFERENCES business_capabilities(id),
  UNIQUE (process_step_id, capability_id)
);

CREATE TABLE skill_definitions (
  id TEXT PRIMARY KEY,
  provider_id TEXT NOT NULL REFERENCES providers(id),
  vendor_skill_id TEXT NOT NULL,
  classification TEXT NOT NULL CHECK (classification IN (
    'BUSINESS_FUNCTIONAL', 'DEVELOPER_DELIVERY', 'AGENT_ORCHESTRATION',
    'ANALYTICAL', 'WORKFLOW', 'CUSTOM'
  )),
  UNIQUE (provider_id, vendor_skill_id)
);

CREATE TABLE skill_versions (
  id TEXT PRIMARY KEY,
  skill_id TEXT NOT NULL REFERENCES skill_definitions(id),
  version_label TEXT NOT NULL,
  published TEXT NOT NULL CHECK (published IN ('YES', 'NO', 'UNKNOWN')),
  product_available TEXT NOT NULL CHECK (product_available IN ('YES', 'NO', 'UNKNOWN')),
  installed TEXT NOT NULL CHECK (installed IN ('YES', 'NO', 'UNKNOWN')),
  configured TEXT NOT NULL CHECK (configured IN ('YES', 'NO', 'UNKNOWN')),
  authorized TEXT NOT NULL CHECK (authorized IN ('YES', 'NO', 'UNKNOWN')),
  executable TEXT NOT NULL CHECK (executable IN ('YES', 'NO', 'UNKNOWN')),
  entitled TEXT NOT NULL CHECK (entitled IN ('YES', 'NO', 'UNKNOWN')),
  UNIQUE (skill_id, version_label)
);

CREATE TABLE skill_capabilities (
  id TEXT PRIMARY KEY,
  skill_version_id TEXT NOT NULL REFERENCES skill_versions(id),
  capability_id TEXT NOT NULL REFERENCES business_capabilities(id),
  relationship_claim_id TEXT NOT NULL,
  UNIQUE (skill_version_id, capability_id, relationship_claim_id)
);

CREATE TABLE skill_installations (
  id TEXT PRIMARY KEY,
  skill_version_id TEXT NOT NULL REFERENCES skill_versions(id),
  location TEXT NOT NULL,
  observed_status TEXT NOT NULL
);

CREATE TABLE agent_definitions (
  id TEXT PRIMARY KEY,
  provider_id TEXT NOT NULL REFERENCES providers(id),
  classification TEXT NOT NULL CHECK (classification IN (
    'PREBUILT_OOTB', 'CONFIGURABLE_TEMPLATE', 'CUSTOM',
    'DEVELOPMENT_SUBAGENT', 'RUNTIME_SERVICE'
  )),
  display_name TEXT NOT NULL
);

CREATE TABLE agent_versions (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL REFERENCES agent_definitions(id),
  version_label TEXT NOT NULL,
  vendor_agent_ids_json TEXT NOT NULL,
  published TEXT NOT NULL CHECK (published IN ('YES', 'NO', 'UNKNOWN')),
  product_available TEXT NOT NULL CHECK (product_available IN ('YES', 'NO', 'UNKNOWN')),
  installed TEXT NOT NULL CHECK (installed IN ('YES', 'NO', 'UNKNOWN')),
  configured TEXT NOT NULL CHECK (configured IN ('YES', 'NO', 'UNKNOWN')),
  authorized TEXT NOT NULL CHECK (authorized IN ('YES', 'NO', 'UNKNOWN')),
  executable TEXT NOT NULL CHECK (executable IN ('YES', 'NO', 'UNKNOWN')),
  entitled TEXT NOT NULL CHECK (entitled IN ('YES', 'NO', 'UNKNOWN'))
);

CREATE TABLE agent_capabilities (
  id TEXT PRIMARY KEY,
  agent_version_id TEXT NOT NULL REFERENCES agent_versions(id),
  capability_id TEXT NOT NULL REFERENCES business_capabilities(id),
  relationship_claim_id TEXT NOT NULL
);

CREATE TABLE agent_skills (
  id TEXT PRIMARY KEY,
  agent_version_id TEXT NOT NULL REFERENCES agent_versions(id),
  skill_version_id TEXT NOT NULL REFERENCES skill_versions(id),
  relationship_claim_id TEXT NOT NULL
);

CREATE TABLE action_definitions (
  id TEXT PRIMARY KEY,
  canonical_action_id TEXT NOT NULL UNIQUE,
  display_name TEXT NOT NULL
);

CREATE TABLE action_versions (
  id TEXT PRIMARY KEY,
  action_id TEXT NOT NULL REFERENCES action_definitions(id),
  vendor_action_id TEXT,
  version_label TEXT NOT NULL
);

CREATE TABLE agent_actions (
  id TEXT PRIMARY KEY,
  agent_version_id TEXT NOT NULL REFERENCES agent_versions(id),
  action_version_id TEXT NOT NULL REFERENCES action_versions(id),
  relationship_claim_id TEXT NOT NULL
);

CREATE TABLE skill_actions (
  id TEXT PRIMARY KEY,
  skill_version_id TEXT NOT NULL REFERENCES skill_versions(id),
  action_version_id TEXT NOT NULL REFERENCES action_versions(id),
  relationship_claim_id TEXT NOT NULL
);

CREATE TABLE tools (
  id TEXT PRIMARY KEY,
  display_name TEXT NOT NULL,
  protocol TEXT
);

CREATE TABLE execution_bindings (
  id TEXT PRIMARY KEY,
  action_version_id TEXT NOT NULL REFERENCES action_versions(id),
  protocol TEXT NOT NULL,
  target_system TEXT NOT NULL,
  read_write TEXT NOT NULL CHECK (read_write IN ('READ', 'WRITE', 'UNKNOWN')),
  confirmation_required TEXT NOT NULL CHECK (confirmation_required IN ('YES', 'NO', 'UNKNOWN'))
);

CREATE TABLE execution_policies (
  id TEXT PRIMARY KEY,
  binding_id TEXT NOT NULL REFERENCES execution_bindings(id),
  policy_text TEXT NOT NULL
);

CREATE TABLE implementation_options (
  id TEXT PRIMARY KEY,
  capability_id TEXT NOT NULL REFERENCES business_capabilities(id),
  display_name TEXT NOT NULL,
  verification TEXT NOT NULL
);

CREATE TABLE implementation_components (
  id TEXT PRIMARY KEY,
  option_id TEXT NOT NULL REFERENCES implementation_options(id),
  component_ref TEXT NOT NULL
);

CREATE TABLE capability_implementations (
  id TEXT PRIMARY KEY,
  capability_id TEXT NOT NULL REFERENCES business_capabilities(id),
  option_id TEXT NOT NULL REFERENCES implementation_options(id),
  relationship_claim_id TEXT NOT NULL
);

CREATE TABLE licensing_links (
  id TEXT PRIMARY KEY,
  subject_id TEXT NOT NULL,
  commercial_ref TEXT,
  price_status TEXT NOT NULL CHECK (price_status IN ('VERIFIED_POINTER', 'UNKNOWN')),
  entitlement_status TEXT NOT NULL CHECK (entitlement_status IN ('VERIFIED', 'UNKNOWN')),
  document_statement TEXT,
  relationship_claim_id TEXT NOT NULL
);

CREATE TABLE metering_links (
  id TEXT PRIMARY KEY,
  subject_id TEXT NOT NULL,
  meter_ref TEXT,
  status TEXT NOT NULL CHECK (status IN ('VERIFIED_POINTER', 'UNKNOWN'))
);

CREATE TABLE source_snapshots (
  id TEXT PRIMARY KEY,
  repository TEXT,
  resolved_commit TEXT,
  path TEXT,
  original_url TEXT,
  retrieved_at TEXT NOT NULL,
  retrieval_status TEXT NOT NULL
);

CREATE TABLE evidence_claims (
  id TEXT PRIMARY KEY,
  snapshot_id TEXT NOT NULL REFERENCES source_snapshots(id),
  locator TEXT NOT NULL,
  supported_fact TEXT NOT NULL,
  evidence_status TEXT NOT NULL CHECK (evidence_status IN ('VERIFIED', 'INFERRED', 'UNKNOWN', 'CONFLICTED'))
);

CREATE TABLE relationship_claims (
  id TEXT PRIMARY KEY,
  source_id TEXT NOT NULL,
  target_id TEXT NOT NULL,
  relationship_type TEXT NOT NULL,
  applicability TEXT NOT NULL,
  evidence_id TEXT NOT NULL REFERENCES evidence_claims(id),
  verification TEXT NOT NULL CHECK (verification IN ('VERIFIED', 'INFERRED', 'UNKNOWN', 'CONFLICTED', 'CANDIDATE')),
  observed_at TEXT NOT NULL
);

CREATE TABLE epics (
  id TEXT PRIMARY KEY,
  process_id TEXT NOT NULL REFERENCES processes(id),
  display_name TEXT NOT NULL
);

CREATE TABLE user_stories (
  id TEXT PRIMARY KEY,
  epic_id TEXT NOT NULL REFERENCES epics(id),
  capability_id TEXT NOT NULL REFERENCES business_capabilities(id),
  persona TEXT NOT NULL,
  statement TEXT NOT NULL,
  business_outcome TEXT NOT NULL
);

CREATE TABLE acceptance_criteria (
  id TEXT PRIMARY KEY,
  user_story_id TEXT NOT NULL REFERENCES user_stories(id),
  given_text TEXT NOT NULL,
  when_text TEXT NOT NULL,
  then_text TEXT NOT NULL
);

CREATE TABLE test_cases (
  id TEXT PRIMARY KEY,
  user_story_id TEXT NOT NULL REFERENCES user_stories(id),
  kind TEXT NOT NULL CHECK (kind IN ('FUNCTIONAL', 'SECURITY')),
  title TEXT NOT NULL
);
