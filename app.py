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
    paragraphs = markdown_text.split('\n\n')
    paragraphs = [f'<p>{p}</p>' if not re.match(r'<(h\d|ul|pre|li|b|i|code)', p) else p for p in paragraphs]
    markdown_text = '\n'.join(paragraphs)

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

    markdown_text = re.sub(r'\n\s*\n', '\n', markdown_text).strip()

    return markdown_text

def convert_markdown(input_data, output_path=None, format='ansi', is_text=False):
    if not is_text:
        if not os.path.isfile(input_data):
            raise FileNotFoundError(f"error: file '{input_data}' does not exist")

        try:
            with open(input_data, 'r') as file:
                markdown_content = file.read()
        except Exception as e:
            raise IOError(f"error with reading file '{input_data}': {e}")
    else:
        markdown_content = input_data

    try:
        if format == 'html':
            output_content = parse_markdown_to_html(markdown_content)
        elif format == 'ansi':
            output_content = parse_markdown_to_ansi(markdown_content)
        else:
            raise ValueError("Unsupported format")
    except Exception as e:
        raise ValueError(f"error: invalid markdown <{e}>")

    if output_path:
        try:
            with open(output_path, 'w') as file:
                file.write(output_content)
        except Exception as e:
            raise IOError(f"error writing to file '{output_path}': {e}")
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
