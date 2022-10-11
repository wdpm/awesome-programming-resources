from jinja2 import Template

template_str = """\
{% for item in range(seq) -%}
    {{item}}
{%- endfor %}
"""

template = Template(template_str)
data = {"seq": 10}
rendered = template.render(data)

print(rendered)
