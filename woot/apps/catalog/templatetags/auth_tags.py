from django.template import Library, Node, TemplateSyntaxError
from uuid import uuid4

register = Library()


class UUIDNode(Node):
    """
    Implements the logic of this tag.
    """
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = str(uuid4())
        return ''


def do_uuid(parser, token):
    """
    The purpose of this template tag is to generate a random
    UUID and store it in a named context variable.

    Sample usage:
        {% uuid var_name %}
        var_name will contain the generated UUID
    """
    try:
        tag_name, var_name = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError("%r tag requires exactly one argument" %
                                  token.contents.split()[0])
    return UUIDNode(var_name)

do_uuid = register.tag('uuid', do_uuid)
