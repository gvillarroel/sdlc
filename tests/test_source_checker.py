import unittest

from scripts.check_sources import collect_urls


class SourceCheckerTest(unittest.TestCase):
    def test_collect_urls_finds_core_sources(self):
        urls = collect_urls()
        self.assertIn("https://github.com/openai/codex", urls)
        self.assertIn("https://github.com/withastro/flue", urls)
        self.assertIn("https://docs.openhands.dev/sdk", urls)
        self.assertIn("https://arxiv.org/abs/2606.14796", urls)
        self.assertIn(
            "https://oecd.ai/en/ai-publications/the-effects-of-generative-ai-on-productivity-innovation-and-entrepreneurship",
            urls,
        )
        self.assertEqual(urls, sorted(set(urls)))


if __name__ == "__main__":
    unittest.main()
