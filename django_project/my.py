from django import template

content = """This is
a content
"""
t = template.Template("{{cont|linebreaks}}")
print(t.render(template.Context({'cont':content})))