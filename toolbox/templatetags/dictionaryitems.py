from django import template
register = template.Library()


@register.assignment_tag
def dictitem(dictionary, key):
    """
        Return the value for a key in a dict.

        This is a feature that is missing in Jinja AFAIK.

        Syntax kinda sucks but it works fine..

        To use it, you first have to put the value in a new string variable.
        Like so:

        {% dictitem [dict] [key] as [new-string-var] %}

        Now you can use new-string-var..
    """
    if (key[0] == key[-1] and key[0] in ('"', "'")):
        key = key[1:-1]
    return dictionary[key]
