#!/usr/bin/env python3
"""Build small, lossless search copies of oversized documentation indexes.

Uses only Python's standard library and the checked-in catalog; no network calls.
Run with --check to detect stale copies without writing files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_THRESHOLD = 320_000
MAX_CHUNK_BYTES = 200_000


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def split_index(source: Path, root: Path, max_bytes: int = MAX_CHUNK_BYTES):
    """Keep every source line, in order, with source ranges and section context."""
    raw = source.read_bytes()
    lines = raw.decode('utf-8').splitlines(keepends=True)
    relative = source.relative_to(root).as_posix()
    title = lines[0].strip().lstrip('# ').strip() if lines else source.parent.name
    source_hash = sha256(raw)
    start, section, part, outputs = 0, '', 1, []
    while start < len(lines):
        prefix = (
            f'# {title} — search part {part:03d}\n\n'
            f'Catalog source: [../../{relative}](../../{relative}).\n'
            f'Source SHA-256: `{source_hash}`.\n'
            'This is a page-link catalog, not the linked documentation text.\n'
            f'Section at start: {section or "Index introduction"}.\n\n'
        )
        # Reserve enough room for the source-range annotation.
        available = max_bytes - len(prefix.encode('utf-8')) - 100
        end, used = start, 0
        while end < len(lines):
            size = len(lines[end].encode('utf-8'))
            if used + size > available:
                break
            used += size
            end += 1
        if end == start:
            raise ValueError(f'{relative}:{start + 1}: line exceeds chunk byte budget')
        body = ''.join(lines[start:end])
        header = prefix + f'Original source lines: {start + 1}–{end}.\n\n'
        rendered = header + body
        if len(rendered.encode('utf-8')) > max_bytes:
            raise ValueError(f'{relative}: chunk exceeds byte budget')
        path = f'search-index/{source.parent.name}/part-{part:03d}.md'
        outputs.append((path, rendered, {
            'path': path, 'start_line': start + 1, 'end_line': end,
            'bytes': len(rendered.encode('utf-8')),
            'sha256': sha256(rendered.encode('utf-8')),
        }))
        for line in lines[start:end]:
            if line.startswith('## '):
                section = line[3:].strip()
        start, part = end, part + 1
    return outputs


def expected_files(root: Path) -> dict[str, str]:
    outputs: dict[str, str] = {}
    sources = []
    for source in sorted(root.glob('*/index.md')):
        raw = source.read_bytes()
        if len(raw) < SOURCE_THRESHOLD:
            continue
        chunks = split_index(source, root)
        outputs.update((path, text) for path, text, _ in chunks)
        sources.append({
            'path': source.relative_to(root).as_posix(),
            'bytes': len(raw), 'sha256': sha256(raw),
            'chunks': [entry for _, _, entry in chunks],
        })
    manifest = {
        'schema_version': 1,
        'source_threshold_bytes': SOURCE_THRESHOLD,
        'max_chunk_bytes': MAX_CHUNK_BYTES,
        'sources': sources,
    }
    outputs['search-index/manifest.json'] = json.dumps(manifest, indent=2) + '\n'
    readme = [
        '# Searchable catalog copies', '',
        'Small copies of oversized catalogs, produced by `scripts/build_search_index.py`.',
        'Original indexes remain the canonical complete link lists. These copies contain',
        'the same lines, with source ranges and hashes; they do not contain full page text.', '',
        'GitHub only searches the default branch. A draft PR does not change live search.',
        'File size alone does not guarantee indexing; validate search after merge.', '',
        '| Catalog | Source bytes | Search parts |', '|---|---:|---|',
    ]
    for source in sources:
        area = source['path'].split('/')[0]
        links = ', '.join(
            f'[{i}]({area}/part-{i:03d}.md)'
            for i in range(1, len(source['chunks']) + 1)
        )
        readme.append(f'| [{area}](../{source["path"]}) | {source["bytes"]:,} | {links} |')
    outputs['search-index/README.md'] = '\n'.join(readme) + '\n'
    return outputs


def rebuild(root: Path = ROOT, check: bool = False) -> list[str]:
    """Return changed paths; --check never writes or removes files."""
    expected = expected_files(root)
    existing = {
        p.relative_to(root).as_posix()
        for p in (root / 'search-index').glob('*/part-*.md')
    }
    changed = []
    for name, text in expected.items():
        path = root / name
        data = text.encode('utf-8')
        if not path.exists() or path.read_bytes() != data:
            changed.append(name)
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
    for name in sorted(existing - expected.keys()):
        changed.append(name)
        if not check:
            (root / name).unlink()
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    changed = rebuild(check=args.check)
    print(f'{len(changed)} search files {"out of date" if args.check else "updated"}')
    return int(args.check and bool(changed))


if __name__ == '__main__':
    raise SystemExit(main())
