from django import template

register = template.Library()

@register.simple_tag
def url_add(request, field, value):
      data = request.GET.copy()
      data[field] = value
      return data.urlencode()

