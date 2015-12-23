from __future__ import division

from threading import Thread

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.forms.models import modelformset_factory, inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext, loader
from django.template.response import TemplateResponse
from django.views.decorators.csrf import ensure_csrf_cookie


from crpt201511.utils.assessment_utils import *
from crpt201511.utils.user_utils import *

from crpt201511.constants import *
from crpt201511.models import *
from crpt201511.settings import CRPT_URL
from crpt201511.trace import *
from crpt201511.utils.env_utils import *
from crpt201511.forms import *
from crpt201511.utils.form_utils import *
from crpt201511.my_ftp import MyFTP

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
        # try:
        # get the latest assessment from the city
        assessment = Assessment.objects.order_by('-date_started')[0]
        # except:
            # raise Exception('The City does not have any open assessment')
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
def city_id(request, assessment_id, section_id=None, subsection_id=None):
    """
    View for section of City ID form

    :param request:
    :param assessment_id: assessment id
    :param section_id: section id
    :param subsection_id: subsection id
    :return:
    """
    try:
        left_elements = None

        # get username from session
        person = get_person(request)
        # get assessment
        assessment = Assessment.objects.get(id=assessment_id)
        # check person has rights for the assessment. TODO: Constants
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        # get section
        if section_id:
            section = CityIDSection.objects.get(id=section_id)
        else:
            section = CityIDSection.objects.all().order_by('order')[:1].get()

        # elements of menu
        menu_elements = CityIDSection.objects.filter(parent=None).order_by('order')
        # adjustment of horizontal menu
        menu_horizontal_elem_width = round(100/len(menu_elements), 2)

        # get selected section name
        selected_section_name = section.name

        # get subsection
        if subsection_id:
            subsection = CityIDSection.objects.get(id=subsection_id)
        else:
            subsection = CityIDSection.objects.filter(parent=section).order_by('order')[:1].get()
        subsection_selected_name = subsection.name

        # elements of left menu
        if section:
            left_elements = CityIDSection.objects.filter(parent_id=section.id).order_by('order')

        # formset definition
        fs_char_field = modelformset_factory(AssessmentCityIDQuestionCharField, max_num=1, exclude=[])
        fs_text_field = modelformset_factory(AssessmentCityIDQuestionTextField, max_num=1, exclude=[])
        fs_upload_field = modelformset_factory(AssessmentCityIDQuestionUploadField,
                                                max_num=1, exclude=[],
                                               form=AssessmentCityIDQuestionUploadFieldForm)

        if request.method == 'POST':
            fs_cf = fs_char_field(request.POST, request.FILES, prefix='fs_cf')
            fs_tf = fs_text_field(request.POST, request.FILES, prefix='fs_tf')
            fs_uf = fs_upload_field(request.POST, request.FILES, prefix='fs_uf')

            #print("fs_cf: " + str(fs_cf))
            #print("fs_tf: " + str(fs_tf))
            #print("fs_uf: " + str(fs_uf))
            sys.stdout.flush()


            if fs_cf.is_valid():
                fs_cf.save()
            else:
                print("fs_cf not valid!")
                sys.stdout.flush()

            if fs_tf.is_valid():
                fs_tf.save()
            else:
                print("fs_tf not valid!")
                sys.stdout.flush()

            print("FILES " + str(request.FILES))

            file_list = []
            remote_folder_name = get_remote_folder_name(assessment, section)

            for i in range(len(fs_uf)):
                f = fs_uf.forms[i]
                q_u_f = f.save()

                file_list_temp = request.FILES.getlist('fs_uf-' + str(i) + '-files')
                for file in file_list_temp:
                    file_list.append(file)
                    acid_uf = AssessmentCityIDQuestionFile()
                    acid_uf.name = str(file)
                    acid_uf.remote_folder = remote_folder_name
                    acid_uf.question = q_u_f
                    acid_uf.save()
                    # TODO: constants
                    q_u_f.placeholder = "Files already uploaded: " + str(len(file_list_temp))
                    if len(q_u_f.response) > 0:
                        q_u_f.response = q_u_f.response + "&013" + str(file)
                    else:
                        q_u_f.response = str(file)
                    q_u_f.save()

            my_ftp = MyFTP()
            for file in file_list:
                # TODO: helper to construct remote folder
                my_ftp.upload_memory_file(file, remote_folder_name , str(file))



            if fs_uf.is_valid():


                fs_uf.save()
            else:
                print("fs_uf not valid!")
                sys.stdout.flush()

                """
                for each in form.cleaned_data['files']:
                    Attachment.objects.create(file=each)
                """

                # TODO: send to main section of CityID or keep the same section??

            # return render_to_response(TEMPLATE_CITY_ID_PAGE, {}, \
            #                              context_instance=RequestContext(request))
        else:
            # formsets
            query_set = AssessmentCityIDQuestionCharField.objects.filter(section=subsection).order_by('order')
            fs_cf = fs_char_field(queryset=query_set, prefix='fs_cf')
            set_form_hidden_fields(fs_cf, ['question_long', 'version', 'section', 'assessment'])

            query_set = AssessmentCityIDQuestionTextField.objects.filter(section=subsection).order_by('order')
            fs_tf = fs_text_field(queryset=query_set, prefix='fs_tf')
            set_form_hidden_fields(fs_tf, ['question_long', 'version', 'section', 'assessment'])

            query_set = AssessmentCityIDQuestionUploadField.objects.filter(section=subsection).order_by('order')
            fs_uf = fs_upload_field(queryset=query_set, prefix='fs_uf')
            set_form_hidden_fields(fs_uf, ['question_long', 'version', 'section', 'assessment'])


        #TODO: delete! it is a test!
        #fs_cf = None
        #fs_tf = None
        #fs_uf = None

        template = loader.get_template(TEMPLATE_CITY_ID_PAGE)
        context = RequestContext(request, {
            'fs_cf': fs_cf,
            'fs_tf': fs_tf,
            'fs_uf': fs_uf,
            'person': person,
            'left_elements': left_elements,
            'menu_elements': menu_elements,
            'assessment': assessment_id,
            'menu_horizontal_elem_width': menu_horizontal_elem_width,
            'page': "city_id",
            'assessment': assessment,
            'section': section,
            'subsection': subsection,
        })
        return HttpResponse(template.render(context))
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR, {"error_description": sys.exc_info(), "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))


# ###############################################
#
# TEST
#
################################################
def test(request):
    # get assessment
    assessment = Assessment.objects.all()[:1]
    # formsets
    FormsetQtype1 = modelformset_factory(QuestionType1)
    FormsetQtype2 = modelformset_factory(QuestionType2)
    FormsetQtype3 = modelformset_factory(QuestionType3)
    # querysets
    qset_qtype1 = QuestionType1.objects.all()
    qset_qtype2 = QuestionType2.objects.all()
    qset_qtype3 = QuestionType3.objects.all()
    # formsets to template
    fset_qtype1 = FormsetQtype1(queryset=qset_qtype1)
    fset_qtype2 = FormsetQtype1(queryset=qset_qtype2)
    fset_qtype3 = FormsetQtype1(queryset=qset_qtype3)
    # return to template
    template = loader.get_template(TEMPLATE_TEST)
    context = RequestContext(request, {
        'fset_qtype1': fset_qtype1,
        'fset_qtype2': fset_qtype2,
        'fset_qtype3': fset_qtype3,
    })
    return HttpResponse(template.render(context))