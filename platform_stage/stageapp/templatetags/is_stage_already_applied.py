from django import template

from stageapp.models import Applicant

register = template.Library()


@register.simple_tag(name='is_stage_already_applied')
def is_stage_already_applied(stage, user):
    applied = Applicant.objects.filter(stage=stage, user=user)
    if applied:
        return True
    else:
        return False
