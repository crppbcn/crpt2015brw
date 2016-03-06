from __future__ import division

from threading import Thread

import math

from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext, loader
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
from crpt201511.utils.mail_utils import send_comments_email


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
        menu_horizontal_elem_width = math.floor(100/len(menu_elements))

        # get subsection
        if subsection_id:
            subsection = CityIDSection.objects.get(id=subsection_id)
        else:
            try:
                subsection = CityIDSection.objects.filter(parent=section).order_by('order')[:1].get()
            except:
                subsection = None

        # elements of left menu
        if section:
            left_elements = CityIDSection.objects.filter(parent_id=section.id).order_by('order')

        # considerations at section and subsection level
        considerations = CityIDSectionConsideration.objects.filter(element=section).order_by('id')
        if subsection:
            # concatenate querysets same type
            considerations = considerations | CityIDSectionConsideration.objects.filter(element=subsection).\
                order_by('id')

        # comments
        if subsection:
            comments = AssessmentCityIDSectionComment.objects.filter(element=subsection, assessment=assessment).\
                order_by('date_created')
        else:
            comments = AssessmentCityIDSectionComment.objects.filter(element=section, assessment=assessment).\
                order_by('date_created')

        # formset definition
        fs = modelformset_factory(AssessmentCityIDQuestion, max_num=1, exclude=[], form=AssessmentCityIDQuestionForm)

        """
        print("request: ")
        print(str(request.POST))
        sys.stdout.flush()
        """

        if request.method == 'POST':
            f_set = fs(request.POST, request.FILES)

            if f_set and f_set.is_valid():

                if f_set and f_set.is_valid():
                    not_applicable_responses_treatment(f_set)
                    trace_updated_fields(f_set, person, assessment)
                    # treatment for user added choices ("please specify")
                    for f in f_set:
                        data = f.cleaned_data
                        try:
                            # add new choice to the list
                            other_choice = data['other']
                            if other_choice != "":
                                print("other_choice: " + other_choice)
                                a_cid_other_tx = AssessmentCityIDChoicesOtherTx()
                                a_cid_other_tx.assessment = assessment
                                a_cid_other_tx.name = other_choice
                                a_cid_other_tx.save()
                                # add new selected choice
                                question = f.save(commit=False)
                                response = data['response']
                                response = response[:len(response)-1]
                                new_str = ", u'" + str(a_cid_other_tx.id) + "']"
                                response += new_str
                                question.response = response
                                question.save()
                            else:
                                f.save()
                        except KeyError:
                            # n_a field not found
                            pass
                    f_set.save()
                    # file upload processing
                    file_list = []
                    remote_folder_name = get_remote_folder_name(assessment, section)

                    # process all forms in formset to save file upload information
                    for i in range(len(f_set)):
                        q_u_f = AssessmentCityIDQuestion.objects.get(pk=request.POST['form-' + str(i) + '-cityidquestion_ptr'])
                        file_list_temp = request.FILES.getlist('form-' + str(i) + '-files')
                        for one_file in file_list_temp:
                            file_list.append(one_file)
                            acid_uf = AssessmentCityIDQuestionFile()

                            print("File: " + str(one_file))
                            sys.stdout.flush()


                            acid_uf.name = str(one_file)
                            acid_uf.remote_folder = remote_folder_name
                            acid_uf.question = q_u_f
                            acid_uf.save()
                    # save files to FTP
                    my_ftp = MyFTP()
                    for one_file in file_list:
                        my_ftp.upload_memory_file(one_file, remote_folder_name, str(one_file))

                else:
                    print("f_set not informed or not valid!")
                    print(str(f_set.errors))
                    sys.stdout.flush()

                # navigate to next section
                url_to_redirect = "/city_id/" + assessment_id + SLASH
                if subsection:
                    if subsection.next_one:
                        print("1.section: " + subsection.parent.name)
                        print("1.subsection: " + subsection.next_one.name)
                        url_to_redirect += str(subsection.parent.id) + SLASH + str(subsection.next_one.id) + SLASH
                    else:
                        if subsection.parent.next_one:
                            print("2.section: " + subsection.parent.next_one.name)
                            url_to_redirect += str(subsection.parent.next_one.id) + SLASH
                        else:
                            print("3.section: " + subsection.parent.name)
                            url_to_redirect += str(subsection.parent.id) + SLASH
                else:
                    print("4.section: " + section.next_one.name)
                    url_to_redirect += str(section.next_one.id) + SLASH

                # print("url_to_redirect: " + url_to_redirect)
                return redirect(url_to_redirect, context_instance=RequestContext(request))
            else:
                # additional treatment of errors if needed
                if f_set:
                    print("f_set errors: " + str(f_set.errors))
                sys.stdout.flush()
        else:
            # formsets
            query_set = AssessmentCityIDQuestion.objects.filter(section=subsection).order_by('order')
            f_set = fs(queryset=query_set)

        # return page
        template = loader.get_template(TEMPLATE_CITY_ID_PAGE)
        context = RequestContext(request, {
            'fs': f_set,
            'person': person,
            'left_elements': left_elements,
            'menu_elements': menu_elements,
            'menu_horizontal_elem_width': menu_horizontal_elem_width,
            'page': "city_id",
            'assessment': assessment,
            'section': section,
            'subsection': subsection,
            'comments': comments,
            'considerations': considerations,
        })
        return HttpResponse(template.render(context))
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR, {"error_description": sys.exc_info(), "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))


@ensure_csrf_cookie
@login_required
def add_section_comment(request):
    """
    View to add comment to a section

    :param request:
    :return:
    """
    try:
        person = get_person(request)

        if request.method == "POST":
            # get values from form
            assessment_id = request.POST['assessment_id']
            section_id = request.POST['section_id']
            comment = request.POST['textComments']

            # get section and assessment
            section = CityIDSection.objects.get(id=section_id)
            assessment = Assessment.objects.get(id=assessment_id)
            # create comment
            my_comment = AssessmentCityIDSectionComment()
            my_comment.assessment = assessment
            my_comment.element = section
            my_comment.comment = comment
            my_comment.person = person
            my_comment.save()

            # trace action
            trace_action(TRACE_COMMENT, person, "User added comment in section: " + section.name)

            # send mail
            try:
                send_mail = request.POST['send_mail']
                t = Thread(target=send_comments_email, args=(my_comment.comment, section, person))
                t.start()
                # send_comments_email(my_comment.comment, section, person)
            except:
                # checkbox not set
                pass

            # redirect to section page
            url_to_redirect = "/city_id/" + assessment_id + SLASH
            if section.parent:
                url_to_redirect += str(section.parent.id) + SLASH
            url_to_redirect += str(section.id) + SLASH

            return redirect(url_to_redirect, context_instance=RequestContext(request))
        else:
            raise Exception("GET call to add new section comment")
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR, {"error_description": sys.exc_info(), "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))
