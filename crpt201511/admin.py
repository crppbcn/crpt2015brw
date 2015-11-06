from django.contrib import admin

import crpt201511.models

admin.site.register(crpt201511.models.TraceAction)
admin.site.register(crpt201511.models.City)
admin.site.register(crpt201511.models.Role)
admin.site.register(crpt201511.models.Person)
admin.site.register(crpt201511.models.Dimension)
admin.site.register(crpt201511.models.HazardCategory)
admin.site.register(crpt201511.models.Hazard)


class AssessmentVersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'name', 'date_released')

admin.site.register(crpt201511.models.AssessmentVersion, AssessmentVersionAdmin)


class ElementAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')

admin.site.register(crpt201511.models.Element, ElementAdmin)


class CityIDCharFieldAdmin(admin.ModelAdmin):
    list_display = ('question', 'section', 'version')

admin.site.register(crpt201511.models.CityIDCharFieldStatement, CityIDCharFieldAdmin)


class CityIDTextFieldAdmin(admin.ModelAdmin):
    list_display = ('question', 'section', 'version')

admin.site.register(crpt201511.models.CityIDTextFieldStatement, CityIDTextFieldAdmin)


class AssessmentCityIDCharFieldQuestionAdmin(admin.ModelAdmin):
    list_display = ('statement', 'assessment')

admin.site.register(crpt201511.models.AssessmentCityIDCharFieldQuestion, AssessmentCityIDCharFieldQuestionAdmin)


class AssessmentCityIDTextFieldQuestionAdmin(admin.ModelAdmin):
    list_display = ('statement', 'assessment')

admin.site.register(crpt201511.models.AssessmentCityIDTextFieldQuestion, AssessmentCityIDTextFieldQuestionAdmin)