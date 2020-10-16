from django import template

register = template.Library()


@register.filter
def batch_filter(batch):
    if batch:
        return "("+ batch+ ")"
    return ""
