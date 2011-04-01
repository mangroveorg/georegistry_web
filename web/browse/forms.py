from django import forms
from simple_locations.models import Area

class FeatureUploadForm(forms.Form):
    """ Create / update a geographic feature and save it into Mango DB """
    areas=Area.objects.all()
    l=[]
    for a in areas:
        if str(a.kind) == 'country':
            x=(a.two_letter_iso_country_code, a.name )

            l.append(x)
        if str(a.kind) == 'subdivision':
            subd = "%s (%s)" % (a.name , a.parent.name)
            combined= "%s-%s" % (a.parent.two_letter_iso_country_code, a.two_letter_iso_subdivision_code)
            x=(combined, subd )
            l.append(x)
        
    country_and_subdivision_choices=tuple(l)
    
    country_subdivision_code = forms.TypedChoiceField(label="Geography",        
                                          choices=country_and_subdivision_choices)