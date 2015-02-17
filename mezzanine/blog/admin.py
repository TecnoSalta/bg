# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mezzanine.blog.models import BlogPost,Estudio, BlogCategory
from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin
from mezzanine.twitter.admin import TweetableAdminMixin
from mezzanine.blog.forms import EstudioForm
from django import forms
blogpost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
#blogpost_fieldsets[0][1]["fields"].insert(1, "categories")
#blogpost_fieldsets[0][1]["fields"].extend(["allow_comments",])

#print '----------------SALIDA:----------------'
#print blogpost_fieldsets[1][1]

#print blogpost_fieldsets


#blogpost_fieldsets[0][1]["fields"].extend(["content", "allow_comments"])

blogpost_list_display = ["title", "nombre","user", "status","admin_nuevo_estudio", "admin_hc_link","admin_pdf_link"]
#if settings.BLOG_USE_FEATURED_IMAGE:
 #   blogpost_fieldsets[0][1]["fields"].insert(-2, "featured_image")
 #   blogpost_list_display.insert(0, "admin_thumb")
#blogpost_fieldsets.insert(1, (_("Other posts"), {
#    "classes": ("collapse-closed",),
#    "fields": ("related_posts",)}))
blogpost_list_filter = deepcopy(DisplayableAdmin.list_filter) + ("categories",)
class EstudioAdmin(admin.ModelAdmin):
    form =EstudioForm
    readonly_fields = ['obs','ant_p','ant_pp']
    list_filter = ('paciente', )
    raw_id_fields=('paciente',)
    search_fields = ('paciente__nombre','paciente__title')
    list_display = ("created", "paciente_nombre", "paciente_dni","paciente_contiene")
    fieldsets= (('Paciente', {
                   "fields": ["paciente"],
                'description': "",
                }),
            ('Ant.',{"classes":("collapse-closed",),
                "fields":('ant_p','ant_pp','obs',
                                )}),
            ('A.V. / B.M.C.', {
                    "classes": ("collapse-closed",),
                    "fields": {("av_sc_od","av_sc_oi",'pio_od','pio_oi','bmc_bio','obi_fondo',)},
                    'description': ""
                }),
            ('A.R.M.', {
                   "classes": ("collapse-closed",),
                   "fields": (
                     ("r_e_od","r_c_od","r_eje_od"),
                     ("r_e_oi","r_c_oi","r_eje_oi"),
                     ),
                'description':"",
                }),
            ('Ecometría',{"classes":("collapse-closed",),
                "fields":(
                     ("eco_k1_od","eco_k1_oi"),
                     ("eco_k2_od","eco_k2_oi"),
                     ("eco_axl_od","eco_axl_oi"),
                     ("eco_acd_od","eco_acd_oi"),
                     ("eco_lens_od","eco_lens_oi"),
                     ("eco_l1a1_od","eco_l1a1_oi"),
                     ("eco_lio_od","eco_lio_oi"),
                     ("eco_refr_od","eco_refr_oi"),
                ),
             }),
            ('Lentes', {
                   "classes": ("collapse-closed",),
                   "fields": (
                     ("av_cc_od"),("l_c_od","l_e_od","l_eje_od"),
                     ("av_cc_oi"),("l_c_oi","l_e_oi","l_eje_oi")),
                'description': "",
                }),
            ('Paqui', {
                   "classes": ("collapse-closed",),
                   "fields": (
                     "pq_od","pq_oi"),
                'description': "",
                }),
            
            
            ("D. y T.", {
                     "classes": ("collapse-closed",),
                     "fields": (("dyt_diagnostico","dyt_tratamiento"),"dyt_consulta",),
                     'description': ""
                }),
        )
        


admin.site.register(Estudio,EstudioAdmin)   
class EstudioInline(admin.TabularInline):
    model = Estudio
    #extra=0
class BlogPostAdmin(TweetableAdminMixin, DisplayableAdmin, OwnableAdmin):
    """
    Admin class for blog posts.
    """
    save_on_top=True
    extra=0
    list_filter = blogpost_list_filter
    fieldsets = blogpost_fieldsets
    list_display = blogpost_list_display
    filter_horizontal = ("categories",)
    def pacientes(self):
        return '<a href="/admin/blog/blogpost/?blogpost__id__exact=%d">%s</a>' % (self.blogpost_id, self.blogpost)
    pacientes.allow_tags = True
    



    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)


class BlogCategoryAdmin(admin.ModelAdmin):
    """
    Admin class for blog categories. Hides itself from the admin menu
    unless explicitly specified.
    """

    fieldsets = ((None, {"fields": ("title",)}),)

    def in_menu(self):
        """
        Hide from the admin menu unless explicitly set in ``ADMIN_MENU_ORDER``.
        """
        for (name, items) in settings.ADMIN_MENU_ORDER:
            if "blog.BlogCategory" in items:
                return True
        return False


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
