import mistletoe

# https://github.com/miyuchina/mistletoe
from mistletoe.ast_renderer import ASTRenderer

with open('../readme_sample.md', 'r', encoding='utf-8') as fin:
    rendered = mistletoe.markdown(fin, ASTRenderer)
    print(rendered)
