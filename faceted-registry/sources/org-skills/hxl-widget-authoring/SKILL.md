---
name: hxl-widget-authoring
description: Create, edit, or troubleshoot HXL and UEM widget JSON using released UI components, allowed child-component rules, and GA expressions. Use for HXL widgets, UEM component trees, Agentforce widget JSON, cards, and rich UI responses. Not for deployment, CLT association, MCP tool registration, Agentforce actions, or Core integration.
---

# HXL Widget Authoring

Create a widget bundle: define its input contract in `uiWidgets/{widgetName}/schema.json`, then create its template in `uiWidgets/{widgetName}/{widgetName}.json`.

**Current API version:** `v68.0`

This toolkit is a snapshot of the currently released HXL schemas. Re-download the ZIP periodically to stay up to date.

## Fast path

Follow this path:

1. This file.
2. [Widget schema meta-schema](api/v68.0/schemas/widget-schema.meta.schema.json) when defining or checking the input contract.
3. [Common components](references/common-components.md).
4. The selected component reference or schema under `api/v68.0/`.
5. Before composing a widget template, read [Expressions](references/expressions.md) for bindings and formulas, conditional rendering with `meta.if`, and iteration with `meta.forEach`, `meta.forItem`, and `meta.forIndex`.

[release.json](release.json) is bundle metadata; it is not needed to author a default-version widget. Read [api/versions.json](api/versions.json) only when the user or project explicitly requires a different supported API version.

## Scope

This downloadable skill covers standalone widget authoring using the bundled component schemas and capability references. The public [Platform Widget Generate sf-skill](https://github.com/forcedotcom/sf-skills/tree/main/skills/platform-widget-generate) remains the source for end-to-end Salesforce development and deployment, CLT association, MCP tools, and Agentforce actions. This skill does not depend on or reproduce that workflow.

## Define the input schema first

Before composing the template, decide which content and options a caller can provide across different uses of this widget. Put those fields under `properties.attributes.properties` in `uiWidgets/{widgetName}/schema.json`. Use required fields only when every use needs them; leave variable content in the contract instead of hardcoding it in the template.

For example, `uiWidgets/support-case/schema.json` can describe the input for a support-case widget:

```json
{
    "title": "Support case",
    "description": "A support case and an independently supplied account-health flag.",
    "type": "object",
    "properties": {
        "attributes": {
            "lightning:type": "lightning__objectType",
            "properties": {
                "caseNumber": {
                    "title": "Case number",
                    "lightning:type": "lightning__textType"
                },
                "subject": {
                    "title": "Subject",
                    "lightning:type": "lightning__textType"
                },
                "status": {
                    "title": "Status",
                    "lightning:type": "lightning__textType"
                },
                "priority": {
                    "title": "Priority",
                    "lightning:type": "lightning__textType"
                },
                "isRedAccount": {
                    "title": "Red account",
                    "description": "Account-health flag supplied independently of this case's fields.",
                    "lightning:type": "lightning__booleanType"
                }
            },
            "required": ["caseNumber", "subject", "status", "priority", "isRedAccount"],
            "additionalProperties": false
        }
    },
    "required": ["attributes"],
    "additionalProperties": false
}
```

Prefer `lightning:type` for fields because Lightning types provide input editors. `lightning__textType` is short text (255 characters by default); `lightning__multilineTextType` is for longer text. Also available: `lightning__numberType`, `lightning__booleanType`, `lightning__objectType`, and `lightning__listType`. These resolve to ordinary JSON Schema value types; do not repeat `type` on a field that declares `lightning:type`. A list needs `items` with its own `lightning:type`. An object needs named child fields in `properties` and `additionalProperties: false`; do not define open objects. See the [widget schema meta-schema](api/v68.0/schemas/widget-schema.meta.schema.json) for the public authoring shape and recursive field constraints. It contains no private meta-schema references.

Then create `uiWidgets/support-case/support-case.json`, binding template values to the schema fields with `$attrs` (for example, `{!$attrs.caseNumber}`). Keep both files together in the same widget bundle.

## Widget shape

The file is a standalone widget envelope. Its `widgetBody` is a tile tree rooted at `tile/widget`; every child has a `definition`, optional `attributes`, and optional `children`.

The caller supplies an input matching that schema. It is not part of the widget file:

```json
{
    "caseNumber": "00001042",
    "subject": "Unable to sign in",
    "status": "New",
    "priority": "High",
    "isRedAccount": true
}
```

Save the template as `uiWidgets/support-case/support-case.json`. It displays the case fields and shows an account-health callout when the caller supplies `isRedAccount: true`; this flag is independent of the case's priority.

```json
{
    "type": "lightning__agentforceWidget",
    "contentBody": {
        "widgetBody": {
            "definition": "tile/widget",
            "children": [
                {
                    "definition": "tile/container",
                    "children": [
                        {
                            "definition": "tile/text",
                            "attributes": {
                                "text": "Case {!$attrs.caseNumber}",
                                "variant": "h2"
                            }
                        },
                        {
                            "definition": "tile/text",
                            "attributes": {
                                "text": "Subject: {!$attrs.subject}"
                            }
                        },
                        {
                            "definition": "tile/text",
                            "attributes": {
                                "text": "Status: {!$attrs.status}"
                            }
                        },
                        {
                            "definition": "tile/text",
                            "attributes": {
                                "text": "Priority: {!$attrs.priority}"
                            }
                        },
                        {
                            "definition": "tile/callout",
                            "meta": {
                                "if": "{!$attrs.isRedAccount}"
                            },
                            "attributes": {
                                "title": "Red account",
                                "description": "This account has been flagged for attention.",
                                "variant": "warning"
                            }
                        }
                    ]
                }
            ]
        }
    }
}
```

The machine-readable widget contract is [api/v68.0/schemas/widget-payload.schema.json](api/v68.0/schemas/widget-payload.schema.json).

## References

- Start with [references/common-components.md](references/common-components.md).
- Use [api/v68.0/references/component-index.md](api/v68.0/references/component-index.md) to find released components.
- Open the selected component reference or JSON schema before using it; these define its attributes and allowed children.
- Read [references/expressions.md](references/expressions.md) before composing a widget template; it covers bindings, formulas, conditional rendering, and iteration.

For a non-default version, confirm it in [api/versions.json](api/versions.json), then use the matching `api/{version}/` paths. Expressions and icons in `references/` are shared current references.

Only use components and capabilities in these references.
