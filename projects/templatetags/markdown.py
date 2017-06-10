from django import template
from markdown import markdown as to_markdown
register = template.Library()

def markdown(value):
    return to_markdown(value)


register.filter('markdown', markdown)
