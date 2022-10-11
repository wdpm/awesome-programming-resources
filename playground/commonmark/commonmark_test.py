import commonmark
parser = commonmark.Parser()

with open('todo.md','r',encoding='utf-8') as f:
    content = f.read()
ast = parser.parse(content)

renderer = commonmark.HtmlRenderer()
html = renderer.render(ast)
# print(html) # <p>Hello <em>World</em><p/>

# inspecting the abstract syntax tree
json = commonmark.dumpJSON(ast)
print(json)
# commonmark.dumpAST(ast) # pretty print generated AST structure