# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from future.builtins import str

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Ownable, RichText, Slugged,TimeStamped
from mezzanine.generic.fields import CommentsField, RatingField
from mezzanine.utils.models import AdminThumbMixin, upload_to



class BlogPost(Displayable, Ownable, AdminThumbMixin):
    """
    A blog post.
    """
    categories = models.ManyToManyField("BlogCategory",
                                        verbose_name=_("Categories"),
                                        blank=True, related_name="blogposts")
    allow_comments = models.BooleanField(verbose_name=_("Allow comments"),
                                         default=True)
    comments = CommentsField(verbose_name=_("Comments"))
    related_posts = models.ManyToManyField("self",
                                 verbose_name=_("Related posts"), blank=True)

    admin_thumb_field = "featured_image"

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ("-publish_date",)

        
    def get_absolute_url(self):
        """
        URLs for blog posts can either be just their slug, or prefixed
        with a portion of the post's publish date, controlled by the
        setting ``BLOG_URLS_DATE_FORMAT``, which can contain the value
        ``year``, ``month``, or ``day``. Each of these maps to the name
        of the corresponding urlpattern, and if defined, we loop through
        each of these and build up the kwargs for the correct urlpattern.
        The order which we loop through them is important, since the
        order goes from least granualr (just year) to most granular
        (year/month/day).
        """
        url_name = "blog_post_detail"
        kwargs = {"slug": self.slug}
        date_parts = ("year", "month", "day")
        if settings.BLOG_URLS_DATE_FORMAT in date_parts:
            url_name = "blog_post_detail_%s" % settings.BLOG_URLS_DATE_FORMAT
            for date_part in date_parts:
                date_value = str(getattr(self.publish_date, date_part))
                if len(date_value) == 1:
                    date_value = "0%s" % date_value
                kwargs[date_part] = date_value
                if date_part == settings.BLOG_URLS_DATE_FORMAT:
                    break
        return reverse(url_name, kwargs=kwargs)

    # These methods are deprecated wrappers for keyword and category
    # access. They existed to support Django 1.3 with prefetch_related
    # not existing, which was therefore manually implemented in the
    # blog list views. All this is gone now, but the access methods
    # still exist for older templates.

    def category_list(self):
        from warnings import warn
        warn("blog_post.category_list in templates is deprecated"
             "use blog_post.categories.all which are prefetched")
        return getattr(self, "_categories", self.categories.all())

    def keyword_list(self):
        from warnings import warn
        warn("blog_post.keyword_list in templates is deprecated"
             "use the keywords_for template tag, as keywords are prefetched")
        try:
            return self._keywords
        except AttributeError:
            keywords = [k.keyword for k in self.keywords.all()]
            setattr(self, "_keywords", keywords)
            return self._keywords


class Estudio(Slugged,TimeStamped):
    #clinico
    #REFRACTOMETRIA
    paciente = models.ForeignKey('BlogPost')
    #A.R.M.
    r_e_od=models.CharField(max_length=50, blank=True, null=True,verbose_name="O.D.<R> E")
    r_c_od=models.CharField(max_length=50, blank=True, null=True,verbose_name="C.")
    r_eje_od=models.CharField(max_length=50, blank=True, null=True,verbose_name="Eje")
    
    r_e_oi=models.CharField(max_length=50, blank=True, null=True,verbose_name="O.I. <R> E")
    r_c_oi=models.CharField(max_length=50, blank=True, null=True,verbose_name="C")
    r_eje_oi=models.CharField(max_length=50, blank=True, null=True,verbose_name="Eje")
    #ecoOD
    eco_k1_od= models.CharField(max_length=10, blank=True, null=True,verbose_name="O.D. K1")
    eco_k1_eje_od=models.CharField(max_length=50, blank=True, null=True,verbose_name="Eje")
    eco_k2_od= models.CharField(max_length=10, blank=True, null=True,verbose_name="O.D. K2")
    eco_k2_eje_od=models.CharField(max_length=50, blank=True, null=True,verbose_name="Eje")
    eco_axl_od= models.CharField(max_length=10, blank=True, null=True,verbose_name="O.D. AXL")
    eco_acd_od= models.CharField(max_length=10, blank=True, null=True,verbose_name="O.D. ACD")
    eco_lens_od= models.CharField(max_length=10, blank=True, null=True,verbose_name="O.D. LENS")
    eco_l1a1_od= models.CharField(max_length=10, blank=True, null=True,default="118",verbose_name="O.D. L1 A1")
    eco_lio_od= models.CharField(max_length=10, blank=True, null=True,verbose_name="O.D. LIO")
    eco_refr_od= models.CharField(max_length=10, blank=True, null=True,verbose_name="O.D. REFR")
    #ecoOI
    eco_k1_oi= models.CharField(max_length=10, blank=True, null=True,verbose_name="O.I. K1")
    eco_k1_eje_oi=models.CharField(max_length=50, blank=True, null=True,verbose_name="Eje")
    eco_k2_oi= models.CharField(max_length=10, blank=True, null=True,verbose_name="O.I. K2")
    eco_k2_eje_oi=models.CharField(max_length=50, blank=True, null=True,verbose_name="Eje")
    eco_axl_oi= models.CharField(max_length=10, blank=True, null=True,verbose_name="O.I. AXL")
    eco_acd_oi= models.CharField(max_length=10, blank=True, null=True,verbose_name="O.I. ACD")
    eco_lens_oi= models.CharField(max_length=10, blank=True, null=True,verbose_name="O.I. LENS")
    eco_l1a1_oi= models.CharField(max_length=10, blank=True, null=True,default="118",verbose_name="O.I. L1 A1")
    eco_lio_oi= models.CharField(max_length=10, blank=True, null=True,verbose_name="O.I. LIO")
    eco_refr_oi= models.CharField(max_length=10, blank=True, null=True,verbose_name="O.I. REFR")
    

    #Lentes Lejos:
    
    l_c_od=models.CharField(max_length=50, blank=True, null=True,verbose_name="O.D. E")
    l_e_od=models.CharField(max_length=50, blank=True, null=True,verbose_name=" C")
    l_eje_od=models.CharField(max_length=50, blank=True, null=True,verbose_name="Eje")

    l_c_oi=models.CharField(max_length=50, blank=True, null=True,verbose_name="O.I. E")
    l_e_oi=models.CharField(max_length=50, blank=True, null=True,verbose_name=" C")
    l_eje_oi=models.CharField(max_length=50, blank=True, null=True,verbose_name="Eje")
    #Lentes Cerca
    l_cerca_c_od=models.CharField(max_length=50, blank=True, null=True,verbose_name="O.D. E")
    l_cerca_e_od=models.CharField(max_length=50, blank=True, null=True,verbose_name=" C")
    l_cerca_eje_od=models.CharField(max_length=50, blank=True, null=True,verbose_name="Eje")

    l_cerca_c_oi=models.CharField(max_length=50, blank=True, null=True,verbose_name="O.D. E")
    l_cerca_e_oi=models.CharField(max_length=50, blank=True, null=True,verbose_name=" C")
    l_cerca_eje_oi=models.CharField(max_length=50, blank=True, null=True,verbose_name="Eje")

    #AGUDEZA VISUAL    
    av_sc_od= models.CharField(max_length=50, blank=True, null=True,verbose_name="O.D. S/C")
    av_sc_oi= models.CharField(max_length=50, blank=True, null=True,verbose_name='O.I. S/C' )
    av_cc_od= models.CharField(max_length=50, blank=True, null=True,verbose_name="O.D. C/C")
    av_cc_oi= models.CharField(max_length=50, blank=True, null=True,verbose_name="O.I. C/C")
    #Paquimetria
    pq_od=models.CharField(max_length=10, blank=True, null=True,verbose_name="O.D. PQ")
    pq_oi=models.CharField(max_length=10, blank=True, null=True,verbose_name="O.I. PQ")
    
    #BIOMICROSCOPIA y PRESION OCULAR
    bmc_bio=models.TextField(default="",blank=True,null=True,verbose_name="<B.M.C>")
    pio_od = models.CharField(max_length=50, blank=True, null=True,verbose_name="O.D. <P.I.O.>")
    pio_oi= models.CharField(max_length=50, blank=True, null=True,verbose_name="O.I. <P.I.O.>")
    obi_fondo =models.TextField(default="", blank=True, null=True,verbose_name="O.B.I.")
    dyt_consulta=models.TextField(blank=True,verbose_name="Consulta")
    dyt_diagnostico =models.TextField(blank=True,verbose_name='Diagnóstico')
    dyt_tratamiento = models.TextField(blank=True,verbose_name='Tratamiento')
    def paciente_nombre(self):
        return self.paciente.nombre
    def paciente_dni(self):
        return self.paciente.title
    def obs(self):
        return self.paciente.observaciones
    def ant_p(self):
        return self.paciente.antecedentes_personales
    def ant_pp(self):
        return self.paciente.antecedentes_personales_p


    def paciente_contiene(self):
        hidden_fields=['id', 'site', 'slug', 'created', 'updated', 'paciente',]
        ls={'',}
        html=''
        for el in sorted(self._meta.fields):
            v=getattr(self, el.name)
            if el.name not in hidden_fields:     
                if not (v==None or v==""):
                    ele=str(el.name).split('_')[0]
                    ls.add(ele)
        for e in ls:
            if e!='':
                html=html+ '<button>%s</button>' %e.upper() 
        return html

    paciente_nombre.allow_tags = True
    obs.allow_tags=True
    obs.short_description="Observaciones"
    paciente_nombre.short_description = "Paciente"
    paciente_dni.allow_tags = True
    paciente_dni.short_description = "D.N.I."
    paciente_contiene.allow_tags=True
    paciente_contiene.short_description="Contenido"




class BlogCategory(Slugged):
    """
    A category for grouping blog posts into a series.
    """

    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")
        ordering = ("title",)

    @models.permalink
    def get_absolute_url(self):
        return ("blog_post_list_category", (), {"category": self.slug})
