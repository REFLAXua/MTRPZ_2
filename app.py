import sys
import os
import re

def parse_markdown_to_html(markdown_text):
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

def parse_markdown_to_ansi(markdown_text):
    markdown_text = re.sub(r'(?m)^# (.*?)$', r'\033[1m\033[4m\1\033[0m', markdown_text)
    markdown_text = re.sub(r'(?m)^## (.*?)$', r'\033[1m\033[4m\1\033[0m', markdown_text)
    markdown_text = re.sub(r'(?m)^### (.*?)$', r'\033[1m\033[4m\1\033[0m', markdown_text)

    markdown_text = re.sub(r'\*\*(.*?)\*\*', r'\033[1m\1\033[0m', markdown_text)
    markdown_text = re.sub(r'_(.*?)_', r'\033[3m\1\033[0m', markdown_text)

    markdown_text = re.sub(r'```(.*?)```', r'\033[7m\1\033[0m', markdown_text, flags=re.DOTALL)
    markdown_text = re.sub(r'`(.*?)`', r'\033[7m\1\033[0m', markdown_text)

    markdown_text = re.sub(r'(?m)^- (.*?)$', r'• \1', markdown_text)

    return markdown_text

def convert_markdown(input_path, output_path=None, format='ansi'):
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
        if format == 'html':
            output_content = parse_markdown_to_html(markdown_content)
        elif format == 'ansi':
            output_content = parse_markdown_to_ansi(markdown_content)
        else:
            raise ValueError("Unsupported format")
    except Exception as e:
        print(f"error: invalid markdown <{e}>", file=sys.stderr)
        sys.exit(1)

    if output_path:
        try:
            with open(output_path, 'w') as file:
                file.write(output_content)
        except Exception as e:
            print(f"error writing to file '{output_path}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output_content)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("using: ./app /path/to/markdown [--out /path/to/output.html] [--format=value]", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = None
    format = 'ansi'

    if '--out' in sys.argv:
        output_path = sys.argv[sys.argv.index('--out') + 1]

    if '--format' in sys.argv:
        format = sys.argv[sys.argv.index('--format') + 1]

    convert_markdown(input_path, output_path, format)
