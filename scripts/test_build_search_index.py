import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import build_search_index as builder


class SearchIndexTests(unittest.TestCase):
    def test_unicode_boundaries_and_lossless_source_ranges(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'example' / 'index.md'
            source.parent.mkdir()
            original = '# Example\n\n## CPQ\n' + ''.join(
                f'| Zażółć {i} | https://example.test/{i} |\n' for i in range(100)
            ) + 'Last line without newline'
            source.write_text(original, encoding='utf-8')
            chunks = builder.split_index(source, root, max_bytes=900)
            reconstructed = ''
            next_line = 1
            for _, text, info in chunks:
                self.assertLessEqual(len(text.encode('utf-8')), 900)
                self.assertEqual(info['start_line'], next_line)
                marker = f'Original source lines: {info["start_line"]}–{info["end_line"]}.\n\n'
                reconstructed += text.split(marker, 1)[1]
                next_line = info['end_line'] + 1
            self.assertEqual(reconstructed, original)
            self.assertGreater(len(chunks), 1)

    def test_stale_detection_cleanup_and_preserved_canonical_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'example' / 'index.md'
            source.parent.mkdir()
            original = b'# Example\n\n' + b'row\n' * 100
            source.write_bytes(original)
            with patch.object(builder, 'SOURCE_THRESHOLD', 100):
                self.assertTrue(builder.rebuild(root))
                self.assertEqual(builder.rebuild(root, check=True), [])
                self.assertEqual(source.read_bytes(), original)
                chunk = root / 'search-index/example/part-001.md'
                chunk.write_text('stale')
                self.assertIn('search-index/example/part-001.md', builder.rebuild(root, check=True))
                self.assertEqual(chunk.read_text(), 'stale')
                builder.rebuild(root)
                source.write_text('# Now small\n')
                self.assertIn('search-index/example/part-001.md', builder.rebuild(root))
                self.assertFalse(chunk.exists())
                self.assertEqual(builder.rebuild(root, check=True), [])

    def test_oversized_single_line_fails_without_silent_truncation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'example/index.md'
            source.parent.mkdir()
            source.write_text('# Example\n' + 'x' * 2000)
            with self.assertRaisesRegex(ValueError, 'line exceeds'):
                builder.split_index(source, root, max_bytes=900)


if __name__ == '__main__':
    unittest.main()
