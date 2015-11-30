from __future__ import division

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
from django.forms.models import modelformset_factory, inlineformset_factory
import datetime

from crpt201511.constants import *
from crpt201511.user_utils import *
from crpt201511.env_utils import *
from crpt201511.trace import *
from crpt201511.settings import CRPT_URL
from crpt201511.models import *
from crpt201511.forms import AssessmentCityIDResponseForm


# ###############################################
#
# Common views
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


def my_copyright(request):
    """
    View for the my_copyright page

    :param request:
    :return:
    """
    try:
        username = request.session.get('username')
        try:
            index_card = None
            #index_card = IndexCard.objects.get(username=username)
        except:
            index_card = None
        template = loader.get_template(TEMPLATE_COPYRIGHT)
        context = RequestContext(request, {
            'username': username,
            'is_copyright': 'is_copyright',
        })
        return HttpResponse(template.render(context))
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR,
                                      {"error_description": sys.exc_info(),
                                       "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))

# ###############################################
#
# Navigation Views
#
################################################

@ensure_csrf_cookie
@login_required
def welcome(request):
    """
    View for the welcome page

    :param request:
    :return:
    """
    try:
        person = get_person(request)
        #try:
            # get the latest assessment from the city
        assessment = Assessment.objects.order_by('-date_started')[0]
        #except:
            #raise Exception('The City does not have any open assessment')
        template = loader.get_template(TEMPLATE_WELCOME)
        context = RequestContext(request, {
            'person': person,
            'assessment':assessment,
        })
        return HttpResponse(template.render(context))
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR,
                                      {"error_description": sys.exc_info(), "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def steps(request, assessment_id):
    """
    View for the steps page

    :param request:
    :return:
    """
    try:
        person = get_person(request)
        assessment = Assessment.objects.get(id=assessment_id)
        try:
            # TODO: implement logic to not show again welcome page
            sections = CityIDSection.objects.filter(parent=None).order_by('order')
        except:
            sections = None
        template = loader.get_template(TEMPLATE_STEPS)
        context = RequestContext(request, {
            'person': person,
            'assessment':assessment,
            'sections': sections,
        })
        return HttpResponse(template.render(context))
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR,
                                      {"error_description": sys.exc_info(), "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))


@ensure_csrf_cookie
@login_required
def city_id(request, assessment_id, element_id=None):
    """
    View for section of City ID form

    :param request:
    :return:
    """
    try:
        person = None
        section = None
        menu_elements = None
        left_elements = None
        statement_ids = []

        # get username from session
        person = get_person(request)
        # get assessment
        assessment_id = Assessment.objects.get(id=assessment_id)
        # get section
        if element_id:
            section = CityIDSection.objects.get(id=element_id)
        else:
            section =  CityIDSection.objects.all()[:1].get()
        # formset definition
        QuestionFormSet = modelformset_factory(AssessmentCityIDResponse, max_num=1, exclude=[],
                                               form=AssessmentCityIDResponseForm)
        # elements of menu
        menu_elements = CityIDSection.objects.filter(parent=None).order_by('order')
        # elements of left menu
        if section:
            left_elements = CityIDSection.objects.filter(parent_id=section.id).order_by('order')

        if request.method == 'POST':
            formset = QuestionFormSet(request.POST, request.FILES)
            if formset.is_valid():
                """
                for each in form.cleaned_data['files']:
                    Attachment.objects.create(file=each)
                """
                formset.save()
                return render_to_response(TEMPLATE_MENU_PAGE, {},\
                                      context_instance=RequestContext(request))
            else:
                if format(len(formset.errors) > 0):
                    num_errors = len(formset.errors[0])
        else:
            statements = CityIDStatement.objects.filter(section=section)
            for statement in statements:
                statement_ids.append(statement.id)

            query_set = AssessmentCityIDResponse.objects.filter(statement_id__in=statement_ids).\
                order_by('statement__order')

            formset = QuestionFormSet(queryset=query_set)

        menu_horizontal_elem_width = round(100/len(menu_elements), 2)


        template = loader.get_template(TEMPLATE_MENU_PAGE)
        context = RequestContext(request, {
            'formset': formset,
            'person': person,
            'left_elements': left_elements,
            'menu_elements': menu_elements,
            'assessment': assessment_id,
            'menu_horizontal_elem_width': menu_horizontal_elem_width,
            'page': "city_id",
        })
        return HttpResponse(template.render(context))
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR, {"error_description": sys.exc_info(), "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))


