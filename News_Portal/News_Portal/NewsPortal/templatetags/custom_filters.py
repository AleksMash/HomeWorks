from django import template
import re

register = template.Library()

pattern=r"\bсук[аи]+\w*\b|\bбляд\w*\b|\b\w*ху[ий]\w*\b|\b\w*[её]ба[тнл]\w*\b|\b\w*пизд\w*\b"
p=re.compile(pattern,re.IGNORECASE)

@register.filter(name='Censor')
def censor_text(value):
    return p.sub('***', value)