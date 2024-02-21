from django import template

from stageapp.models import BookmarkJob

register = template.Library()


@register.simple_tag(name='is_stage_already_saved')
def is_stage_already_saved(stage, user):
    applied = BookmarkJob.objects.filter(stage=stage, user=user)
    if applied:
        return True
    else:
        return False
