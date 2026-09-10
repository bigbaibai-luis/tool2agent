import unittest

from tool2agent.generate import slugify
from tool2agent.template import build_user_prompt


class TestSlugify(unittest.TestCase):
    def test_lowercase(self):
        self.assertEqual(slugify("Scrapling"), "scrapling")

    def test_spaces_and_symbols(self):
        self.assertEqual(slugify("Some Cool Tool!"), "some-cool-tool")

    def test_empty_fallback(self):
        self.assertEqual(slugify("!!!"), "agent")


class TestPrompt(unittest.TestCase):
    def test_build_user_prompt(self):
        meta = {
            "name": "scrapling",
            "summary": "web scraping framework",
            "version": "1.0",
            "home_page": "https://example.com",
            "docs_url": "https://example.com/docs",
        }
        prompt = build_user_prompt(meta, "some docs text")
        self.assertIn("scrapling", prompt)
        self.assertIn("some docs text", prompt)
        self.assertIn("Compliance & Safety", prompt)


if __name__ == "__main__":
    unittest.main()
