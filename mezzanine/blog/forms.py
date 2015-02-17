from __future__ import unicode_literals

from django import forms

from mezzanine.blog.models import BlogPost,Estudio
from mezzanine.core.models import CONTENT_STATUS_DRAFT


# These fields need to be in the form, hidden, with default values,
# since it posts to the blog post admin, which includes these fields
# and will use empty values instead of the model defaults, without
# these specified.
hidden_field_defaults = ("status", "gen_description", "allow_comments")


class BlogPostForm(forms.ModelForm):
    """
    Model form for ``BlogPost`` that provides the quick blog panel in the
    admin dashboard.
    """

    class Meta:
        model = BlogPost
        fields = ("title","nombre","domicilio","fecha_de_nacimento",
            "telefono","email","obra_social","obra_social_numero",
            "obra_social_plan","motivo_de_consulta","antecedentes_personales",
            "antecedentes_personales_p","observaciones","status") 
        #+ hidden_field_defaults


    #def __init__(self):
    #    initial = {}
    #    for field in hidden_field_defaults:
    #        initial[field] = BlogPost._meta.get_field(field).default
    #    initial["status"] = CONTENT_STATUS_DRAFT
    #    super(BlogPostForm, self).__init__(initial=initial)
    #    for field in hidden_field_defaults:
    #      self.fields[field].widget = forms.HiddenInput()

        
class EstudioForm(forms.ModelForm):
    """
    Modelo para armar el custom form de estudio
    """
    class Meta:
        model = Estudio
        exclude=('title','paciente','slug')
        widgets = {
            #
            'dyt_diagnostico':forms.Textarea(attrs={'cols':'20','rows':'3'}),
            'dyt_tratamiento':forms.Textarea(attrs={'cols':'20','rows':'3'}),
            'dyt_consulta':forms.Textarea(attrs={'cols':'20','rows':'3'}),
            'bmc_bio':forms.Textarea(attrs={'cols':'30','rows':'3'}),
            'obi_fondo':forms.Textarea(attrs={'cols':'30','rows':'3'}),


            #Refractometria
             #OD
            'r_e_od': forms.NumberInput(attrs={'min':'-1','max':'1', 'step': '.25'}),
            'r_e_oi': forms.NumberInput(attrs={'min':'-1','max':'1', 'step': '.25'}),

            'r_c_od': forms.NumberInput(attrs={'min':'-1','max':'1', 'step': '.25'}),
            'r_eje_od': forms.NumberInput(attrs={'min':'0','max':'180','step': '1'}),
             #OI
            'r_c_oi': forms.NumberInput(attrs={'min':'-1','max':'1', 'step': '.25'}),
            'r_eje_oi': forms.NumberInput(attrs={'min':'0','max':'180','step': '1'}),
           
            #Keratometria 
             #K1
            'k_k1_od':forms.NumberInput(attrs={'step':'.1'}),
            'k_k1_oi':forms.NumberInput(attrs={'step':'.1'}),
             #K2
            'k_k2_od':forms.NumberInput(attrs={'step':'.1'}),
            'k_k2_oi':forms.NumberInput(attrs={'step':'.1'}),
            #Lentes
             #OD
            'l_c_od':forms.NumberInput(attrs={'min':'-1','max':'1', 'step': '.25'}),
            'l_e_od':forms.NumberInput(attrs={'min':'-1','max':'1', 'step': '.25'}),
            'l_eje_od':forms.NumberInput(attrs={'min':'0','max':'180','step': '1'}),
             #OI
            'l_c_oi':forms.NumberInput(attrs={'min':'-1','max':'1', 'step': '.25'}),
            'l_e_oi':forms.NumberInput(attrs={'min':'-1','max':'1', 'step': '.25'}),
            'l_eje_oi':forms.NumberInput(attrs={'min':'0','max':'180','step': '1'}),
            #Paquimetria
            'pq_od':forms.NumberInput(attrs={'min':'0','max':'700','step': '1'}),
            'pq_oi':forms.NumberInput(attrs={'min':'0','max':'700','step': '1'}), 
            # Ecometria
            "eco_k1_od":forms.NumberInput(attrs={'min':'0','max':'50','step': '.1'}),
            "eco_k1_oi":forms.NumberInput(attrs={'min':'0','max':'50','step': '.1'}),
            "eco_k2_od":forms.NumberInput(attrs={'min':'0','max':'50','step': '1'}),
            "eco_k2_oi":forms.NumberInput(attrs={'min':'0','max':'50','step': '1'}),
            "eco_axl_od":forms.NumberInput(attrs={'min':'0','max':'40'}),
            "eco_axl_oi":forms.NumberInput(attrs={'min':'0','max':'40'}),
            "eco_acd_od":forms.NumberInput(attrs={'min':'0','max':'15','step': '.01'}),
            "eco_acd_oi":forms.NumberInput(attrs={'min':'0','max':'15','step': '.01'}),
            "eco_lens_od":forms.NumberInput(attrs={'min':'0','max':'20','step': '.01'}),
            "eco_lens_oi":forms.NumberInput(attrs={'min':'0','max':'20','step': '1'}),
            "eco_l1a1_od":forms.NumberInput(attrs={'min':'0','max':'300','step': '.1'}),
            "eco_l1a1_oi":forms.NumberInput(attrs={'min':'0','max':'300','step': '.1'}),
            "eco_lio_od":forms.NumberInput(attrs={'min':'-20','max':'40','step': '.25'}),
            "eco_lio_oi":forms.NumberInput(attrs={'min':'-20','max':'40','step': '.25'}),
            "eco_refr_od":forms.NumberInput(attrs={'min':'-5','max':'5','step': '.01'}),
            "eco_refr_oi":forms.NumberInput(attrs={'min':'-5','max':'5','step': '.01'}),          
        }
    
