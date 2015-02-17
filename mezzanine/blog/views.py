# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from future.builtins import str
from future.builtins import int
from calendar import month_name

from django.http import Http404
from django.shortcuts import get_object_or_404

from mezzanine.blog.models import BlogPost, BlogCategory,Estudio
from mezzanine.blog.feeds import PostsRSS, PostsAtom
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.views import render, paginate
from mezzanine.utils.models import get_user_model

User = get_user_model()

def blog_post_list(request, tag=None, year=None, month=None, username=None,
                   category=None, template="blog/blog_post_list.html"):
    """
    Display a list of blog posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``blog/blog_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    settings.use_editable()
    templates = []
    blog_posts = BlogPost.objects.published(for_user=request.user)
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        blog_posts = blog_posts.filter(keywords__keyword=tag)
    if year is not None:
        blog_posts = blog_posts.filter(publish_date__year=year)
        if month is not None:
            blog_posts = blog_posts.filter(publish_date__month=month)
            try:
                month = month_name[int(month)]
            except IndexError:
                raise Http404()
    if category is not None:
        category = get_object_or_404(BlogCategory, slug=category)
        blog_posts = blog_posts.filter(categories=category)
        templates.append(u"blog/blog_post_list_%s.html" %
                          str(category.slug))
    author = None
    if username is not None:
        author = get_object_or_404(User, username=username)
        blog_posts = blog_posts.filter(user=author)
        templates.append(u"blog/blog_post_list_%s.html" % username)

    prefetch = ("categories", "keywords__keyword")
    blog_posts = blog_posts.select_related("user").prefetch_related(*prefetch)
    blog_posts = paginate(blog_posts, request.GET.get("page", 1),
                          settings.BLOG_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    context = {"blog_posts": blog_posts, "year": year, "month": month,
               "tag": tag, "category": category, "author": author}
    templates.append(template)
    return render(request, templates, context)


##inicio historiaC
def blog_post_historia(request, slug,template="blog/blog_post_historia.html"):
    """Display a list of contenidos that are filtered by slug,
    """
    templates = []
    #listamos todos los pacientes..
    pacientes = BlogPost.objects.published(for_user=request.user)
    paciente = get_object_or_404(pacientes, title=slug)
    lista_estudios=Estudio.objects.all()    
    lista_estudios=lista_estudios.filter(paciente__title=slug).order_by("-created")
    templates.append(u"blog/blog_post_historia_%s.html" % str(slug))
    #Fecha,estudio_grupo,estudio_item,valor
    context = {"estudios": lista_estudios,"paciente":paciente}
    templates.append(template)
    return render(request, templates, context)        
##EndHC
from reportlab.pdfgen import canvas
def blog_post_pdf(request,slug):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    blog_posts = BlogPost.objects.published(for_user=request.user).select_related()
    blog_post = get_object_or_404(blog_posts, slug=slug)
    context = {"blog_post": blog_post, "editable_obj": blog_post}
    #templates = [u"blog/blog_post_detail_%s.html" % str(slug), template]
    #return render(request, templates, context)

    return response

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
    
def blog_post_detail(request, slug, year=None, month=None, day=None,
                     template="blog/blog_post_detail.html"):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="'+slug+'.pdf"'
    p = canvas.Canvas(response)
    #image DRAW
    from PIL import Image
    import os
    page_offset = 7*cm 
    page_width, page_height = p._pagesize
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    path=PROJECT_ROOT+"\logo.jpg"
    #print path
    try:
        image = Image.open(path)
    except:
        print "NO LO ENCUENTRA"

    image_width, image_height = image.size
    #p.setFillColorRGB(0,0,255) #choose your font colour
    p.drawImage(path, 60, 760, width=87, height=30,
                     preserveAspectRatio=True)
    #eimagedraw
    # Create the PDF object, using the response object as its "file."
    blog_posts = BlogPost.objects.published(for_user=request.user).select_related()
    blog_post = get_object_or_404(blog_posts, slug=slug)
    #antecedentes_personales
    p_content   = str(blog_post.antecedentes_personales)
    #print p_content
    textobject = p.beginText(7*cm, 19.2*cm)
    for c in p_content:
        if c == '\n':
            textobject.textLine()
        elif c == '\r':
            pass # do nothing
        else:
            textobject.textOut(c)
    p.drawText(textobject)
    #motivo de consulta
    p_content   = str(blog_post.motivo_de_consulta)
    textobject = p.beginText(6*cm, 29.7*cm - 8*cm)
    for c in p_content:
        if c == '\n':
            textobject.textLine()
        elif c == '\r':
            pass # do nothing
        else:
            textobject.textOut(c)
    p.drawText(textobject)
    #diagnostico
    p_content   = str(blog_post.diagnostico)
    textobject = p.beginText(7*cm, 29.7*cm - 18.5*cm)
    for c in p_content:
        if c == '\n':
            textobject.textLine()
        elif c == '\r':
            pass # do nothing
        else:
            textobject.textOut(c)
    p.drawText(textobject)
    # biomicroscopia
    p_content   = str(blog_post.bmc.bio)
    textobject = p.beginText(7*cm, 29.7*cm - 15.5*cm)
    for c in p_content:
        if c == '\n':
            textobject.textLine()
        elif c == '\r':
            pass # do nothing
        else:
            textobject.textOut(c)
    p.drawText(textobject)
    #tratamiento
    p_content   = str(blog_post.dyt_tratamiento)
    textobject = p.beginText(7*cm, 29.7*cm - 22.5*cm)
    for c in p_content:
        if c == '\n':
            textobject.textLine()
        elif c == '\r':
            pass # do nothing
        else:
            textobject.textOut(c)
    p.drawText(textobject)
    #fondo_de_ojos_obi
    p_content   = str(blog_post.obi_fondo)
    textobject = p.beginText(7*cm, 29.7*cm - 17*cm)
    for c in p_content:
        if c == '\n':
            textobject.textLine()
        elif c == '\r':
            pass # do nothing
        else:
            textobject.textOut(c)
    p.drawText(textobject)
         
    Max_y=29.7*cm
    rpt=[{"x":2*cm,"y":4.5*cm,"texto":"Paciente:","tag":"l","z":blog_post.nombre},
         {"x":13.5*cm,"y":4.5*cm,"texto":"Fecha de Nac.:","tag":"l","z":str(blog_post.fecha_de_nacimento)},
         {"x":2*cm,"y":5.5*cm,"texto":"D.N.I.:","tag":"l","z":blog_post.title},#2
         {"x":2*cm,"y":6*cm,"texto":"Obra Social / N°:","tag":"l","z":str(blog_post.obra_social)+"/"+(blog_post.obra_social_numero)},
         {"x":2*cm,"y":6.5*cm,"texto":"Domicilio:","tag":"l","z":blog_post.domicilio},#4
         {"x":2*cm,"y":7*cm,"texto":"Teléfonos:","tag":"l","z":str(blog_post.telefono)},
         {"x":2*cm,"y":8*cm,"texto":"Motivo de Consulta:","tag":"ml","z":""},
         {"x":2*cm,"y":10.5*cm,"texto":"Antecedentes Personales:","tag":"ml","z":""},
         {"x":2*cm,"y":12.5*cm,"texto":"Ref. O.D.:","tag":"l","z":blog_post.r_od},#6
         {"x":12*cm,"y":12.5*cm,"texto":"O.I.:","tag":"l","z":blog_post.r_oi},
         {"x":2*cm,"y":13.5*cm,"texto":"A.V. S.C. O.D.:","tag":"l","z":blog_post.av_sc_od},#8
         {"x":12*cm,"y":13.5*cm,"texto":"S.C. O.I.:","tag":"l","z":blog_post.av_sc_oi},
         {"x":2*cm,"y":14*cm,"texto":"A.V. C.C. O.D.:","tag":"l","z":blog_post.av_cc_od},
         {"x":12*cm,"y":14*cm,"texto":"C.C. O.I.:","tag":"l","z":blog_post.av_cc_oi},                
         {"x":2*cm,"y":14.5*cm,"texto":"P.O. O.D.:","tag":"l","z":blog_post.po_od},#12
         {"x":12*cm,"y":14.5*cm,"texto":"O.I.:","tag":"l","z":blog_post.po_oi},
         {"x":2*cm,"y":15.5*cm,"texto":"BIOMICROSCOPIA:","tag":"ml","z":""},
         {"x":2*cm,"y":17*cm,"texto":"FONDO DE OJOS OBI:","tag":"ml","z":blog_post.title},#16
         {"x":2*cm,"y":18.5*cm,"texto":"Diagnostico:","tag":"ml","z":blog_post.title},
         {"x":2*cm,"y":22.5*cm,"texto":"Tratamiento:","tag":"ml","z":blog_post.title},
         {"x":2*cm,"y":27.5*cm,"texto":"Observaciones:","tag":"ml","z":""},                             
                ]
    for e in rpt:
            #print str(Max_y-e["y"])
            #print e["texto"]
            p.drawString(e["x"], Max_y-e["y"], e["texto"])
            if e["tag"]=="l":
                p.drawString(e["x"]+(len(e["texto"].upper())*0.2*cm), Max_y-e["y"], e["z"])    
    # Close the PDF object cleanly, and we're done.
    blog_posts = BlogPost.objects.published(for_user=request.user).select_related()
    blog_post = get_object_or_404(blog_posts, slug=slug)
    context = {"blog_post": blog_post, "editable_obj": blog_post}
    #templates = [u"blog/blog_post_detail_%s.html" % str(slug), template]
    #return render(request, templates, context)
    #p.drawString(100,200,blog_post.nombre)
    p.showPage()
    p.save()
    


    return response
    

def blog_post_feed(request, format, **kwargs):
    """
    Blog posts feeds - maps format to the correct feed view.
    """
    try:
        return {"rss": PostsRSS, "atom": PostsAtom}[format](**kwargs)(request)
    except KeyError:
        raise Http404()
def blog_post_add(request):
    raise Http404()
