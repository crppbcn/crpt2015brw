from __future__ import division

from threading import Thread

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext, loader
from django.template.response import TemplateResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from crpt201511.utils.user_utils import *
from crpt201511.constants import *
from crpt201511.models import *
from crpt201511.trace import *
from crpt201511.utils.env_utils import *


# ###############################################
#
# User views
#
################################################

@ensure_csrf_cookie
def my_login(request):
    username = ''
    password = ''
    user = None

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login_response = login(request, user)
                    request.session['username'] = username
                    # control if UN-Habitat or expert staff
                    person = get_person_by_user(user)
                    t = Thread(target=trace_action, args=(TRACE_LOGIN, person, person.name + " - " + person.role.name))
                    t.start()
                    if person.role.name == ROLES[ROLE_CRPT_TEAM_ITEM]:
                        # TODO: set web section for crpt team
                        return redirect('/crpt_team/')
                    else:
                        trace_action(TRACE_LOGIN, person,)
                        return redirect('/welcome')
                else:
                    # Return a 'disabled account' error message
                    context = {'form': form}
                    return redirect('/login/?next=%s' % request.path)
            else:
                # Return an 'invalid login' error message.
                context = {'form': form}
                return TemplateResponse(request, TEMPLATE_LOGIN, context)
        else:
            context = {'form': form}
            return TemplateResponse(request, TEMPLATE_LOGIN, context)
    else:
        form = AuthenticationForm(request)
        context = {'form': form,
                   'is_login': 'is_login',
            }
        return TemplateResponse(request, TEMPLATE_LOGIN, context)


@ensure_csrf_cookie
@login_required
def my_logout(request):
    person = get_person(request)
    logout(request)
    t = Thread(target=trace_action, args=(TRACE_LOGOUT, person, person.name + " - " + person.role.name))
    t.start()
    template = loader.get_template(TEMPLATE_LOGOUT)
    context = RequestContext(request, {'is_logout': "logout"})
    return HttpResponse(template.render(context))


@ensure_csrf_cookie
def my_change_password(request):
    try:
        if request.method == 'POST':
            form = PasswordChangeForm(data=request.POST, user=request.user)
            if form.is_valid():
                # change password
                #raise Exception("EL USUARIO: " + request.user.username)
                #raise Exception("EL pwd: " + str(request.POST['new_password1']).strip())
                u = User.objects.get(username=request.user.username)
                u.set_password(str(request.POST['new_password1']).strip())
                u.save()
                # logout
                logout(request)
                # return to index page
                return redirect('/index/')
            else:
                context = {'form': form, 'is_login':'is_login'}
                return TemplateResponse(request, 'crpt201511/change_password.html', context)
        else:
            form = PasswordChangeForm(request)
            context = {'form': form,
                       'is_login':'is_login',
                }
            return TemplateResponse(request, 'crpt201511/change_password.html', context)
    except:
        if debug_is_on():
            raise
        else:
            return redirect("/index/", context_instance=RequestContext(request))