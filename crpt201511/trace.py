import sys

from crpt201511.models import TraceAction


def trace_action(action_name, person, description=None):
    try:
        new_log = TraceAction()
        new_log.action = action_name
        new_log.description = description
        new_log.person = person
        new_log.save()
    except:
        print("Error tracing action: " + action_name)
        print("Error: " + str(sys.exc_info()))
