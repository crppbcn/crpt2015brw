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
        fs_char_field = modelformset_factory(AssessmentCityIDQuestionCharField, max_num=1, exclude=[],
                                             form=AssessmentCityIDQuestionCharFieldForm)
        fs_text_field = modelformset_factory(AssessmentCityIDQuestionTextField, max_num=1, exclude=[],
                                             form=AssessmentCityIDQuestionTextFieldForm)
        fs_select_field = modelformset_factory(AssessmentCityIDQuestionSelectField, max_num=1, exclude=[],
                                               form=AssessmentCityIDQuestionSelectFieldForm)
        fs_upload_field = modelformset_factory(AssessmentCityIDQuestionUploadField,
                                                max_num=1, exclude=[],
                                               form=AssessmentCityIDQuestionUploadFieldForm)

        if request.method == 'POST':
            fs_cf = fs_char_field(request.POST, request.FILES, prefix='fs_cf')
            fs_tf = fs_text_field(request.POST, request.FILES, prefix='fs_tf')
            fs_uf = fs_upload_field(request.POST, request.FILES, prefix='fs_uf')
            fs_sf = fs_select_field(request.POST, request.FILES, prefix='fs_sf')

            if fs_cf and fs_cf.is_valid() and fs_tf and fs_tf.is_valid() and fs_sf and fs_sf.is_valid():

                if fs_cf and fs_cf.is_valid():
                    not_applicable_responses_treatment(fs_cf)
                    trace_updated_fields(fs_cf, person, assessment)
                    fs_cf.save()
                else:
                    print("fs_cf not informed or not valid!")
                    print(str(fs_cf.errors))
                    sys.stdout.flush()

                if fs_tf and fs_tf.is_valid():
                    not_applicable_responses_treatment(fs_tf)
                    trace_updated_fields(fs_tf, person, assessment)
                    fs_tf.save()
                else:
                    print("fs_tf not informed or not valid!")
                    print(str(fs_tf.errors))
                    print(str(fs_tf.errors))
                    sys.stdout.flush()

                if fs_sf and fs_sf.is_valid():
                    trace_updated_fields(fs_sf, person, assessment)
                    # treatment for user added choices ("please specify")
                    for f in fs_sf:
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
                    # Not needed. Each form is saved individually
                    fs_sf.save()
                else:
                    print("fs_sf not informed or not valid!")
                    print(str(fs_sf.errors))
                    sys.stdout.flush()

                if fs_uf and fs_uf.is_valid():
                    trace_updated_fields(fs_cf, person, assessment)
                    fs_uf.save()

                    # file upload processing
                    file_list = []
                    remote_folder_name = get_remote_folder_name(assessment, section)

                    # process all forms in formset to save file upload information
                    for i in range(len(fs_uf)):
                        q_u_f = AssessmentCityIDQuestionUploadField.objects.get(pk=request.POST['fs_uf-' + str(i) + '-id'])
                        file_list_temp = request.FILES.getlist('fs_uf-' + str(i) + '-files')
                        for one_file in file_list_temp:
                            file_list.append(one_file)
                            acid_uf = AssessmentCityIDQuestionFile()
                            acid_uf.name = str(one_file)
                            acid_uf.remote_folder = remote_folder_name
                            acid_uf.question = q_u_f
                            acid_uf.save()
                    # save files to FTP
                    my_ftp = MyFTP()
                    for one_file in file_list:
                        my_ftp.upload_memory_file(one_file, remote_folder_name, str(one_file))
                else:
                    print("fs_uf not informed or not valid!")
                    print(str(fs_uf.errors))
                    sys.stdout.flush()

                # navigate to next section
                url_to_redirect = "/city_id/" + assessment_id + "/"
                if subsection:
                    if subsection.next_one:
                        print("1.section: " + subsection.parent.name)
                        print("1.subsection: " + subsection.next_one.name)
                        url_to_redirect += str(subsection.parent.id) + "/" + str(subsection.next_one.id) + "/"
                    else:
                        if subsection.parent.next_one:
                            print("2.section: " + subsection.parent.next_one.name)
                            url_to_redirect += str(subsection.parent.next_one.id) + "/"
                        else:
                            print("3.section: " + subsection.parent.name)
                            url_to_redirect += str(subsection.parent.id) + "/"
                else:
                    print("4.section: " + section.next_one.name)
                    url_to_redirect += str(section.next_one.id) + "/"

                # print("url_to_redirect: " + url_to_redirect)
                return redirect(url_to_redirect, context_instance=RequestContext(request))
            else:
                # additional treatment of errors if needed
                if fs_cf:
                    print("fs_cf errors: " + str(fs_cf.errors))
                if fs_tf:
                    print("fs_tf errors: " + str(fs_tf.errors))
                if fs_sf:
                    print("fs_sf errors: " + str(fs_sf.errors))
                if fs_uf:
                    print("fs_uf errors: " + str(fs_uf.errors))
                sys.stdout.flush()
        else:
            # formsets
            query_set = AssessmentCityIDQuestionCharField.objects.filter(section=subsection).order_by('order')
            fs_cf = fs_char_field(queryset=query_set, prefix='fs_cf')

            query_set = AssessmentCityIDQuestionTextField.objects.filter(section=subsection).order_by('order')
            fs_tf = fs_text_field(queryset=query_set, prefix='fs_tf')

            query_set = AssessmentCityIDQuestionSelectField.objects.filter(section=subsection).order_by('order')
            fs_sf = fs_select_field(queryset=query_set, prefix='fs_sf')

            query_set = AssessmentCityIDQuestionUploadField.objects.filter(section=subsection).order_by('order')
            fs_uf = fs_upload_field(queryset=query_set, prefix='fs_uf')

        # return page
        template = loader.get_template(TEMPLATE_CITY_ID_PAGE)
        context = RequestContext(request, {
            'fs_cf': fs_cf,
            'fs_tf': fs_tf,
            'fs_uf': fs_uf,
            'fs_sf': fs_sf,
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
            url_to_redirect = "/city_id/" + assessment_id + "/"
            if section.parent:
                url_to_redirect += str(section.parent.id) + "/"
            url_to_redirect += str(section.id) + "/"

            return redirect(url_to_redirect, context_instance=RequestContext(request))
        else:
            raise Exception("GET call to add new section comment")
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR, {"error_description": sys.exc_info(), "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))
