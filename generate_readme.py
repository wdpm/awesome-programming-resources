import json
import textwrap

import mistletoe
from jinja2 import Template
from mistletoe.ast_renderer import ASTRenderer


# use built-in open module
class MarkdownReader:

    @staticmethod
    def read(url: str) -> str:
        with open(url, 'r', encoding='utf-8') as fd:
            content = fd.read()
        return content


class ListItem(object):
    """
    Base class for the list items in README.
    """

    def __init__(self, title: str = "", link: str = "", description: str = "", tags: list = None):
        self._type = "ListItem"
        self.title = title
        self.link = link
        self.description = description
        if tags is None:
            self.tags = []
        else:
            self.tags = tags

    def get_type(self):
        return self._type

    def get_title(self):
        return self.title

    def set_title(self, title: str = ""):
        self.title = title

    def get_link(self):
        return self.link

    def set_link(self, link: str = ""):
        self.link = link

    def get_description(self):
        return self.description

    def set_description(self, description: str = ""):
        self.description = description

    def get_tags(self):
        return self.tags

    def set_tags(self, tags: list = None):
        if tags:
            self.tags = tags

    def __repr__(self):
        return f"<ListItem: {self.title}:{self.link}:{self.description}:{self.tags}>"


class ParsedSummary:

    def __init__(self):
        self.state = "UNRESOLVED"
        self.ast_item_size = None
        self.markdown_item_size = None

    def __repr__(self):
        return f'<ParsedSummary: state={self.state};ast_item_size={self.ast_item_size};' \
               f'markdown_item_size={self.markdown_item_size}>'


# use mistletoe to get markdown AST
class MarkdownParser:

    def __init__(self):
        pass

    @staticmethod
    def _parse_to_ast(text: str) -> str:
        parsed = mistletoe.markdown(text, ASTRenderer)
        return parsed

    def parse(self, text: str) -> tuple:
        ast_str = self._parse_to_ast(text)
        # print(ast_str)

        # statistics for ast list
        ast_item_size = 0

        # ast str(as json) -> dict object
        ast_dict = json.loads(ast_str)

        # item & link: find 'type': 'Paragraph' and only has one child and child type is link.
        # description & tags: refer docs/implementation.md
        root_children = None
        try:
            root_children = ast_dict['children']
        except (TypeError, KeyError,) as e:
            print(f'Parsing ast_dict failed with error: ${e}')

        result_array = []
        new_list_item = ListItem()

        # collect ast item sequentially
        for item in root_children:

            if item['type'] == 'Paragraph':

                # normal paragraph
                if item['children'] and len(item['children']) == 1 and item['children'][0]['type'] == 'RawText':
                    result_array.append(item)

                # link
                if item['children'] and len(item['children']) == 1 and item['children'][0]['type'] == 'Link':
                    ast_item_size += 1

                    children_ = item['children'][0]
                    item_title = children_['children'][0]['content']
                    item_link = children_['target']
                    new_list_item.set_title(item_title)
                    new_list_item.set_link(item_link)

                # description and tags
                if item['children'] and len(item['children']) > 1:
                    description_line = item['children']
                    item_tags = []
                    item_description = None

                    for line_item in description_line:
                        item_type = line_item['type']
                        if item_type == 'RawText' and line_item['content'].strip():
                            item_description = line_item["content"]
                        if item_type == 'InlineCode':
                            item_tag = line_item['children'][0]['content']
                            item_tags.append(item_tag)

                    new_list_item.set_description(item_description)
                    new_list_item.set_tags(item_tags)
                    result_array.append({
                        "type": new_list_item.get_type(),
                        "title": new_list_item.get_title(),
                        "link": new_list_item.get_link(),
                        "description": new_list_item.get_description(),
                        "tags": new_list_item.get_tags()
                    })

                    # MUST reset ListItem when one ListItem traverses done
                    new_list_item = ListItem()
            else:
                # is not paragraph
                result_array.append(item)

        markdown_item_size = self._compute_markdown_item_size(result_array)

        summary = ParsedSummary()
        summary.state = "RESOLVED"
        summary.ast_item_size = ast_item_size
        summary.markdown_item_size = markdown_item_size

        return result_array, summary

    @staticmethod
    def _compute_markdown_item_size(md_list: list = None):
        count = 0
        for md_list_item in md_list:
            if md_list_item['type'] == 'ListItem':
                count += 1
        return count


# use jinja2 to write markdown back
class MarkdownWriter:

    @staticmethod
    def _transform(markdown_list: list = None) -> str:

        markdown_content = ""
        line_break = "\r\n"

        # only handle heading, quote, and ListItem type for now.
        for item in markdown_list:
            item_type = item['type']
            if item_type == 'Heading':
                heading = item['children'][0]['content']
                level = int(item['level'])
                markdown_content += "#" * level + " " + heading + line_break
            elif item_type == 'Quote':
                quote = ""
                quote_children = item['children'][0]['children']
                if quote_children:
                    for quote_child in quote_children:
                        quote_child_type = quote_child['type']
                        if quote_child_type == 'RawText':
                            quote += quote_child['content']
                        elif quote_child_type == 'Strikethrough':
                            strikethrough_text = "~~"
                            for inner in quote_child['children']:
                                if inner['type'] == 'RawText':
                                    strikethrough_text += inner['content'].strip()
                            strikethrough_text += "~~"
                            quote += strikethrough_text

                markdown_content += "> " + quote + line_break
            elif item_type == 'ListItem':
                data = {
                    'title': item['title'],
                    'link': item['link'],
                    'description': item['description'],
                    'year': None,
                    'page': None,
                    "level": None,
                    "type": 'BOOK'
                }

                tags = item['tags']
                for tag in tags:
                    #  year
                    if tag.startswith('Y') or tag.startswith('y') or tag.lower().startswith('year'):
                        data['year'] = tag[1:]
                    # page number
                    if tag.startswith('P') or tag.startswith('p'):
                        data['page'] = tag[1:]
                    # level
                    if tag.startswith('L') or tag.startswith('l'):
                        data['level'] = tag[1:]
                    # type, default book
                    if tag.startswith("T") or tag.startswith('t'):
                        data['type'] = tag[1:]

                template_str = textwrap.dedent("""\
                <details>
                    <summary>
                        <a href="{{link}}">{{title}}</a>
                    </summary>
                    {{description}} <code>year:{{year}}</code> <code>page:{{page}}</code> <code>level:{{level}}</code>
                </details>              
                """)

                template = Template(template_str)
                rendered = template.render(data)
                markdown_content += rendered + line_break
            elif item['type'] == 'Paragraph':
                normal_paragraph = item['children'][0]['content']
                markdown_content += normal_paragraph + line_break
            else:
                pass

        return markdown_content

    def write(self, markdown_list: list = None) -> None:
        transformed = self._transform(markdown_list)
        with open('README.md', 'w', encoding='utf-8') as fd:
            fd.write(transformed)


if __name__ == '__main__':
    #  -> file str
    content = MarkdownReader.read('README_SOURCE.md')

    # file str -> custom list
    markdown_parser = MarkdownParser()
    markdown_list, summary = markdown_parser.parse(content)
    print(f'Summary[after]: {summary}')

    markdown_writer = MarkdownWriter()
    markdown_writer.write(markdown_list)
