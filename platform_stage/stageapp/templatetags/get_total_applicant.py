from django import template
register = template.Library()


@register.simple_tag(name='get_total_applicant')
def get_total_applicant(total_applicants , stage):

    return total_applicants[stage.id]
  
     



        

