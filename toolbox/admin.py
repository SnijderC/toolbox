# -*- coding: utf-8 -*-
"""
        The admin pages need some work to make it more comfortable to contributors..
        Sorry not much documented, have not really put much effort into this since
        Django kind of just works even if it's not perfect and the front-end had
        more priority.
        
        If you feel this should change, feel free to contribute..
"""

from toolbox.models import Tool, Platform, Category, License, Advice, Property, ParentCategories, MainNav, Formfactor
from forms import CommonFieldsForm, LicenseForm
from django.contrib import admin

def make_published(modeladmin, request, queryset):
    """
        Mass mark an item as published from the admin interface.
    """ 
    queryset.update(published=True)
make_published.short_description = "Mark selected items as published"

def make_unpublished(modeladmin, request, queryset):
    """
        Mass mark an item as unpublished from the admin interface.
    """ 
    queryset.update(published=False)
make_unpublished.short_description = "Mark selected items as unpublished"

def contributor_name(obj):
    return ("%s %s" % (obj.user.first_name, obj.user.last_name))
contributor_name.short_description = 'contributor'

class CommonFieldsAdmin(admin.ModelAdmin):
    form            = CommonFieldsForm
    actions         = [make_published,make_unpublished]
    list_display    = ('title', contributor_name, 'slug','credit')
    
class LicenseAdmin(admin.ModelAdmin):
    form    = LicenseForm

class ParentCategoriesAdmin(admin.ModelAdmin):
    filter_horizontal   = ('categories',)

class FormfactorAdmin(admin.ModelAdmin):
    filter_horizontal   = ('platforms',)

class MainNavAdmin(admin.ModelAdmin):
    #filter_horizontal   = ('categories',) # somehow this doesn't work?!
    pass
class ToolAdmin(CommonFieldsAdmin):
    filter_horizontal   = ('categories', 'platforms', 'pros', 'cons', 'alternative','formfactors')
    fieldsets = (
        (None, {
            'fields': (('title', 'slug'), 'image', 'intro_md','content_md'),
        }),
        ('Tagging', {
            'fields': ('license',('categories', 'alternative'),('formfactors','platforms')),
        }),
        ('Properties', {
            'fields': ('url', 'author', 'author_url', 'appstore', 'playstore', 'marketplace', ('pros','cons'), 'cost', 'risk', ('user', 'credit'), ('published', 'feature_score')),
        })
    )
    
class AdviceAdmin(CommonFieldsAdmin):
    fieldsets = (
        (None, {
            'fields': (('title', 'time', 'slug'), 'image', 'intro_md','content_md'),
        }),
        ('Tagging', {
            'fields': ('categories', ('formfactors','platforms'), 'related')
        }),
        ('Properties', {
            'fields': (('user', 'credit'), ('published', 'feature_score'))
        })
    )
    filter_horizontal = ('categories', 'platforms','formfactors','related')

adminlist = (
                (Advice, AdviceAdmin),
                (Tool, ToolAdmin),
                (License, LicenseAdmin),    
                Platform,
                Category,
                (ParentCategories, ParentCategoriesAdmin),
                Property,
                (MainNav, MainNavAdmin),
                (Formfactor, FormfactorAdmin),
            )


"""
    This is a fix for a feature that i think is missing in Django
    admin.site.register does work with tuples but doesn't work when 
    you add FormAdmins and ModelAdmins, quick fix:
"""

for item in adminlist:
    if isinstance(item, (list, tuple)):
            admin.site.register(item[0], item[1])
    else:
        admin.site.register(item)



                      