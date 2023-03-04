import md_toc


def generate_toc_in_place(md_file, toc_marker="<!--TOC-->"):
    toc = md_toc.build_toc(md_file)
    # md_toc.write_string_on_file_between_markers(md_file, toc, toc_marker)
    return toc


toc = generate_toc_in_place("foo.md")
print(toc)
# 对中文的支持会出现GBK问题

# - [Table of contents](#table-of-contents)
# - [bar](#bar)
#   - [is](#is)
#   - [a](#a)
#     - [foo](#foo)
#     - [foo 2](#foo-2)
#   - [file](#file)
#   - [bye](#bye)