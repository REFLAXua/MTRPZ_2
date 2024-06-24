import unittest
import tempfile
import os
from app import parse_markdown_to_html, parse_markdown_to_ansi, convert_markdown

class TestMarkdownConverter(unittest.TestCase):
    
    def setUp(self):
        self.test_markdown = "# Заголовок 1\n\nЦе **жирний текст** і це _курсив_.\n\n- Пункт 1\n- Пункт 2\n\n```python\nprint(\"Це код Python\")\n```"
        self.expected_html = "<h1>Заголовок 1</h1>\n\n<p>Це <b>жирний текст</b> і це <i>курсив</i>.</p>\n\n<ul><li>Пункт 1</li><li>Пункт 2</li></ul>\n\n<pre><code>python\nprint(\"Це код Python\")\n</code></pre>"
        self.expected_ansi = "\033[1m\033[4mЗаголовок 1\033[0m\n\nЦе \033[1mжирний текст\033[0m і це \033[3mкурсив\033[0m.\n\n• Пункт 1\n• Пункт 2\n\n\033[7mpython\nprint(\"Це код Python\")\033[0m"

    def test_parse_markdown_to_html(self):
        html_output = parse_markdown_to_html(self.test_markdown)
        self.assertEqual(html_output.strip(), self.expected_html.strip())

    def test_parse_markdown_to_ansi(self):
        ansi_output = parse_markdown_to_ansi(self.test_markdown)
        self.assertEqual(ansi_output.strip(), self.expected_ansi.strip())

    def test_convert_markdown_to_html_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            convert_markdown(self.test_markdown, tmp_file.name, 'html', is_text=True)
            with open(tmp_file.name, 'r') as file:
                html_output = file.read()
                self.assertEqual(html_output.strip(), self.expected_html.strip())
            os.remove(tmp_file.name)

    def test_convert_markdown_to_ansi_stdout(self):
        from io import StringIO
        import sys
        sys.stdout = StringIO()
        convert_markdown(self.test_markdown, format='ansi', is_text=True)
        ansi_output = sys.stdout.getvalue().strip()
        sys.stdout = sys.__stdout__
        self.assertEqual(ansi_output, self.expected_ansi.strip())

if __name__ == '__main__':
    unittest.main()
