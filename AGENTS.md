# Working with the documentation catalog

- Read `SEARCH.md` before searching this catalog or answering from its results.
- Treat `index.md` as page-title/URL discovery and `content.md` as a synthesis.
  Read the linked official page before asserting implementation details.
- Rewrite natural-language requests into short, scoped connector searches;
  use exact identifiers and synonyms as separate queries where helpful.
- Preserve product distinctions, especially HXL versus Headless 360 and
  Communications Cloud Managed Package versus on Core.
- Preserve complete canonical `*/index.md` files. After changing one, run
  `python3 scripts/build_search_index.py` and commit the resulting search copies.
- Do not edit `search-index/` by hand. Check it with
  `python3 scripts/build_search_index.py --check`.
- Run `python3 -m unittest discover -s scripts -p 'test_*.py'` when changing the
  builder, and check that no original source lines are lost.
- A zero-result connector search is a coverage gap, not evidence of absence.
  Use direct file/blob reads or live official documentation as needed.
