import sys
import os
import re

def parse_markdown(markdown_text):
    markdown_text = re.sub(r'(?m)^# (.*?)$', r'<h1>\1</h1>', markdown_text)
    markdown_text = re.sub(r'(?m)^## (.*?)$', r'<h2>\1</h2>', markdown_text)
    markdown_text = re.sub(r'(?m)^### (.*?)$', r'<h3>\1</h3>', markdown_text)

    markdown_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', markdown_text)
    markdown_text = re.sub(r'_(.*?)_', r'<i>\1</i>', markdown_text)

    markdown_text = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', markdown_text, flags=re.DOTALL)
    markdown_text = re.sub(r'`(.*?)`', r'<code>\1</code>', markdown_text)

    markdown_text = re.sub(r'(?m)^- (.*?)$', r'<li>\1</li>', markdown_text)
    markdown_text = re.sub(r'(?s)(<li>.*?</li>)', r'<ul>\1</ul>', markdown_text)
    markdown_text = re.sub(r'(?s)(</ul>\s*<ul>)', '', markdown_text)

    markdown_text = re.sub(r'(?s)(<h\d>.*?</h\d>)', r'\1\n\n', markdown_text)
    markdown_text = re.sub(r'(?s)(<pre>.*?</pre>)', r'\1\n\n', markdown_text)
    markdown_text = re.sub(r'(?s)(<ul>.*?</ul>)', r'\1\n\n', markdown_text)
    paragraphs = markdown_text.split('\n\n')
    paragraphs = [f'<p>{p}</p>' if not re.match(r'<(h\d|ul|pre|li|b|i|code)', p) else p for p in paragraphs]
    markdown_text = '\n\n'.join(paragraphs)

    return markdown_text

def convert_markdown_to_html(input_path, output_path=None):
    if not os.path.isfile(input_path):
        print(f"error: file '{input_path}' does not exist", file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_path, 'r') as file:
            markdown_content = file.read()
    except Exception as e:
        print(f"error with reading file '{input_path}': {e}", file=sys.stderr)
        sys.exit(1)

    try:
        html_content = parse_markdown(markdown_content)
    except Exception as e:
        print(f"error: invalid markdown <{e}>", file=sys.stderr)
        sys.exit(1)

    if output_path:
        try:
            with open(output_path, 'w') as file:
                file.write(html_content)
        except Exception as e:
            print(f"error writing to file '{output_path}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(html_content)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("using: ./app /path/to/markdown [--out /path/to/output.html]", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = None

    if len(sys.argv) == 4 and sys.argv[2] == '--out':
        output_path = sys.argv[3]

    convert_markdown_to_html(input_path, output_path)