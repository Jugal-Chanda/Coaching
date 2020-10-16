from django import template

register = template.Library()


@register.filter
def teacher_filter(teacher):
    if teacher:
        return "("+ teacher+ ")"
    return ""
