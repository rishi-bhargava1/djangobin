from pygments import highlight
from  pygments import lexers
from pygments.formatters import html

formatter = html.HtmlFormatter(full=True)
lex = lexers.get_lexer_by_name("python")

code = """
    def func():
         # function body
         print("hello world!")
    """

with open("out.html", "w") as f:
     highlight(code, lex, formatter, outfile=f)
