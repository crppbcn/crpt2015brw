import django.dispatch

recalculate_element_score = django.dispatch.Signal(providing_args=["element"])


