from __future__ import division
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template import RequestContext, loader
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponse
from django.forms.models import modelformset_factory


from crpt201511.utils.user_utils import *
from crpt201511.models import *
from crpt201511.utils.env_utils import *
from crpt201511.utils.assessment_utils import *
from crpt201511.settings import CRPT_URL
from crpt201511.forms import AssessmentStakeholderForm


@ensure_csrf_cookie
@login_required
def stakeholder_groups(request, assessment_id):
    """
    View for stakeholders
    :param request:
    :return:
    """
    try:
        person = get_person(request)
        assessment = Assessment.objects.get(id=assessment_id)
        # check person has rights for the assessment. TODO: Constants
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        stakeholder_groups = StakeholderGroup.objects.all().order_by('id')

        template = loader.get_template(TEMPLATE_STAKEHOLDERS_GROUPS_PAGE)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'stakeholder_groups': stakeholder_groups,
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
def stakeholders(request, assessment_id, sg_id, st_id=None, s_id=None):
    """
    View for the stakeholders page

    :param request:
    :param assessment_id:
    :param sg_id:
    :param st_id:
    :param s_id:
    :return:
    """
    try:
        person = get_person(request)
        assessment = Assessment.objects.get(id=assessment_id)
        # check person has rights for the assessment. TODO: Constants
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        # stakeholders group
        sg = StakeholderGroup.objects.get(id=sg_id)
        # stakeholder types
        sts = StakeholderType.objects.filter(stakeholder_group=sg).order_by('id')
        # stakeholder type
        if st_id:
            st = StakeholderType.objects.get(id=st_id)
        else:
            st = sts[:1].get()
        # stakeholder
        if s_id:
            s = Stakeholder.objects.get(id=s_id)
        else:
            s = Stakeholder.objects.filter(stakeholder_type=st).order_by('id')[:1].get()

        # get considerations
        considerations = StakeholderGroupConsideration.objects.filter(stakeholder_group=sg).order_by('id')

        # formset
        fs = modelformset_factory(AssessmentStakeholder, max_num=0, exclude=[], form=AssessmentStakeholderForm)

        if request.method == 'POST':

            f_set = fs(request.POST, request.FILES)
            if f_set and f_set.is_valid():
                f_set.save()

                # redirect to next page
                url_to_redirect_base = '/stakeholders/' + str(assessment_id) + SLASH
                url_to_redirect_sg = url_to_redirect_base + str(sg.id) + SLASH
                url_to_redirect_st = url_to_redirect_sg + str(st.id) + SLASH
                if s.next_one:
                    url_to_redirect = url_to_redirect_sg + str(s.next_one.stakeholder_type.id) + SLASH + \
                                      str(s.next_one.id) + SLASH
                else:
                    if st.next_one:
                        url_to_redirect = url_to_redirect_sg + str(st.next_one.id) + SLASH
                    else:
                        if sg.next_one:
                            url_to_redirect = url_to_redirect_base + str(sg.next_one.id) + SLASH
                        else:
                            url_to_redirect = url_to_redirect_sg

                return redirect(url_to_redirect, context_instance=RequestContext(request))

            else:
                print(str(f_set.errors))
                sys.stdout.flush()

        else:
            query_set = AssessmentStakeholder.objects.filter(assessment=assessment, stakeholder=s).order_by('id')
            f_set = fs(queryset=query_set)

        # return page
        template = loader.get_template(TEMPLATE_STAKEHOLDERS_PAGE)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'fs': f_set,
            'stakeholder_types': sts,
            'stakeholder_group': sg,
            'stakeholder_type': st,
            'stakeholder': s,
            'considerations': considerations,
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
def hazard_type_detail(request, assessment_id, ht_id):
    """
    View for the hazard type detail page

    :param request:
    :return:
    """
    try:
        person = get_person(request)
        assessment = Assessment.objects.get(id=assessment_id)
        # check person has rights for the assessment. TODO: Constants
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        # get hazard type, description and examples
        ht = HazardType.objects.get(id=ht_id)

        # considerations as list of subtypes. listed in template for each subtype
        considerations = HazardSubtype.objects.filter(hazard_type=ht).order_by('id')

        # formset definition
        fs = modelformset_factory(AssessmentHazardType, max_num=0, exclude=[], form=AssessmentHazardTypeForm)

        if request.method == 'POST':

            f_set = fs(request.POST, request.FILES)
            if f_set and f_set.is_valid():
                f_set.save()

                # redirect to next page
                url_to_redirect = '/hazard_type_interrelations/' + assessment_id + SLASH + ht_id
                return redirect(url_to_redirect, context_instance=RequestContext(request))

            else:
                print(str(f_set.errors))
                sys.stdout.flush()

        else:
            query_set = AssessmentHazardType.objects.filter(hazard_type=ht).order_by('id')
            f_set = fs(queryset=query_set)



        # return page
        template = loader.get_template(TEMPLATE_HAZARDS_DETAIL_PAGE)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'selected': "HT_DETAIL",
            'ht': ht,
            'fs': f_set,
            'considerations': considerations,
            'is_hazard_detail':True,
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
def hazard_type_interrelations(request, assessment_id, ht_id):
    """
    View for the hazard type interrelations page

    :param request:
    :return:
    """
    try:
        person = get_person(request)
        assessment = Assessment.objects.get(id=assessment_id)
        # check person has rights for the assessment. TODO: Constants
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        # get hazard type, description and examples
        ht = HazardType.objects.get(id=ht_id)
        aht = AssessmentHazardType.objects.get(assessment=assessment, hazard_type=ht)

        # considerations as list of subtypes. listed in template for each subtype
        considerations = HazardSubtype.objects.filter(hazard_type=ht).order_by('id')

        # formset definition
        fs_factory_causes = modelformset_factory(AssessmentHazardCause, max_num=0, exclude=[])
        fs_factory_consequences = modelformset_factory(AssessmentHazardConsequence, max_num=0, exclude=[])

        if request.method == 'POST':

            fs_causes = fs_factory_causes(request.POST, request.FILES, prefix='fs_causes')
            fs_consequences = fs_factory_consequences(request.POST, request.FILES, prefix='fs_consequences')

            if fs_causes and fs_causes.is_valid() and fs_consequences and fs_consequences.is_valid():
                fs_causes.save()
                fs_consequences.save()

                # redirect to next page
                url_to_redirect = '/hazard_type_impacts/' + assessment_id + SLASH + ht_id
                return redirect(url_to_redirect, context_instance=RequestContext(request))

            else:
                if fs_causes.errors:
                    print(str(fs_causes.errors))
                if fs_consequences.errors:
                    print(str(fs_consequences.errors))
                sys.stdout.flush()

        else:
            query_set = AssessmentHazardCause.objects.filter(a_h_type=aht).order_by('id')
            fs_causes = fs_factory_causes(queryset=query_set, prefix='fs_causes')
            query_set = AssessmentHazardConsequence.objects.filter(a_h_type=aht).order_by('id')
            fs_consequences = fs_factory_consequences(queryset=query_set, prefix='fs_consequences')

        # return page
        template = loader.get_template(TEMPLATE_HAZARDS_INTERRELATIONS_PAGE)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'selected': "HT_INTERRELATIONS",
            'ht': ht,
            'fs_causes': fs_causes,
            'fs_consequences': fs_consequences,
            'considerations': considerations,
            'is_hazard_detail': True,
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
def hazard_type_impacts(request, assessment_id, ht_id, element_id=None):
    """
    View for the hazard type interrelations page

    :param request:
    :return:
    """
    try:
        person = get_person(request)
        assessment = Assessment.objects.get(id=assessment_id)
        # check person has rights for the assessment. TODO: Constants
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        # get hazard type, description and examples
        ht = HazardType.objects.get(id=ht_id)
        aht = AssessmentHazardType.objects.get(assessment=assessment, hazard_type=ht)

        # considerations as list of subtypes. listed in template for each subtype
        considerations = HazardSubtype.objects.filter(hazard_type=ht).order_by('id')

        # formset definition
        fs = modelformset_factory(AssessmentElementImpact, max_num=0, exclude=[])

        if request.method == 'POST':

            f_set = fs(request.POST, request.FILES)
            if f_set and f_set.is_valid():
                f_set.save()

                # redirect to next page
                url_to_redirect = '/hazard_type_detail/' + assessment_id + SLASH + ht_id
                return redirect(url_to_redirect, context_instance=RequestContext(request))

            else:
                print(str(f_set.errors))
                sys.stdout.flush()

        else:
            query_set = AssessmentElementImpact.objects.filter(a_h_type=aht, assessment=assessment).order_by('id')
            f_set = fs(queryset=query_set)

        template = loader.get_template(TEMPLATE_HAZARDS_IMPACTS_PAGE)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'fs': f_set,
            'selected': "HT_IMPACTS",
            'ht': ht,
            'considerations': considerations,
            'is_hazard_detail': True,
        })
        return HttpResponse(template.render(context))
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR,
                                      {"error_description": sys.exc_info(), "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))
