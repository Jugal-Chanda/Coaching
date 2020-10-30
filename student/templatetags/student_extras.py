from django import template
from datetime import datetime,timezone

register = template.Library()


@register.filter
def teacher_filter(teacher):
    if teacher:
        return "("+ teacher+ ")"
    return ""


@register.filter
def datetime_diff(creted_datetime):
    current_datetime = datetime.now(timezone.utc)
    return current_datetime - creted_datetime
