with open('foo.md', 'w', encoding='utf-8') as fd:
    str = ""
    str += "123" + "\r\n"
    fd.write(str)
