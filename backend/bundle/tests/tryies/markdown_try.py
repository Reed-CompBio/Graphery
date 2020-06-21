import markdown


def read_markdown_and_write():
    with open('./markdowns/test1.md', 'r') as file, open('./markdowns/test1.html', 'w') as output:
        html = markdown.markdown(file.read())
        output.write(html)


if __name__ == '__main__':
    read_markdown_and_write()
