import sys
import time

from threading import Thread

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render_to_response
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.template import RequestContext, loader, Context
from django.forms.models import modelformset_factory
import datetime




from crpt201511.constants import *
from crpt201511.user_utils import *
from crpt201511.env_utils import *
from crpt201511.trace import *
from crpt201511.settings import CRPT_URL



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
                        return redirect('/index/')
                else:
                    # Return a 'disabled account' error message
                    context = {'form': form}
                    return redirect('/login/?next=%s' % request.path)
            else:
                # Return an 'invalid login' error message.
                context = {'form': form}
                return TemplateResponse(request, 'crpt201511/login.html', context)
        else:
            context = {'form': form}
            return TemplateResponse(request, 'crpt201511/login.html', context)
    else:
        form = AuthenticationForm(request)
        context = {'form': form,
                   'is_login': 'is_login',
            }
        return TemplateResponse(request, 'crpt201511/login_bootstrap.html', context)

@ensure_csrf_cookie
def my_logout(request):
    person = get_person(request)
    logout(request)
    t = Thread(target=trace_action, args=(TRACE_LOGOUT, person, person.name + " - " + person.role.name))
    t.start()
    template = loader.get_template('crpt201511/logout_bootstrap.html')
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

@ensure_csrf_cookie
@login_required
def index(request):
    """
    View for the list of sections of the index card

    :param request:
    :return:
    """
    try:
        assessment_list = None
        assessments_paginated = None
        user = None
        person = None

        # get username from session
        username = request.session.get('username')
        person = get_person_by_username(username)

        if not username or not person:
            return redirect('my_login')
        try:
            pass

        except:
            raise Exception(sys.exc_info())

        # paginator = Paginator(assessment_list, ITEMS_PER_PAGE)  # Limit items per page
        # page = request.GET.get('page')
        try:
            # assessments_paginated = paginator.page(page)
            pass
        except:
            #print("Unexpected error:", sys.exc_info())
            # assessments_paginated = paginator.page(1)
            pass

        template = loader.get_template('crpt201511/index.html')
        context = RequestContext(request, {
            'assessments_list': assessments_paginated,
            'username': username,
            'user': user,
            'person': person,
        })
        return HttpResponse(template.render(context))
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response("crpt201511/error.html",
                                      {"error_description": sys.exc_info(),
                                       "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))


def my_copyright(request):
    """
    View for the my_copyright page

    :param request:
    :return:
    """
    try:
        raise Exception("TEST EXCEPTION!!!")



        username = request.session.get('username')
        try:
            index_card = None
            #index_card = IndexCard.objects.get(username=username)
        except:
            index_card = None
        template = loader.get_template('crpt201511/my_copyright.html')
        context = RequestContext(request, {
            'username': username,
            'is_copyright': 'is_copyright',
        })
        return HttpResponse(template.render(context))
    except:
        """
        if debug_is_on():
            raise
        else:
        """
        return render_to_response("crpt201511/error.html",
                                      {"error_description": sys.exc_info(),
                                       "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))

