# Salesforce docs catalog

This folder is a link catalog. It is not the Salesforce Docs service that SF Pi calls through `sf_docs`.

SF Pi does not see a page by reading an index whole. `product-docs/index.md` is about 1.87 MB and 12,977 links (6,533 unique pages). Loading it returns a file that is too large to use, so the page looks missing.

Find one page like this:

1. Start at `salesforce-platform-docs-content-list.md` and open that product's `content.md`.
2. Search that product's `index.md` for the page title or object name. Read the matching line only.
3. Open the `developer.salesforce.com` URL on that line for fields and behavior. The index line is not the field list.

`sf_docs` inside SF Pi is a separate login. It stays empty until `/login sf-docs` or `SF_DOCS_MCP_ENDPOINT` and `SF_DOCS_MCP_TOKEN` are set. This catalog does not fill that login.
