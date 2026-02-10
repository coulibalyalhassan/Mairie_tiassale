from django import forms
from .models import *

class MessageMairieForm(forms.ModelForm):
    class Meta:
        model = MessageMairie
        fields = ['nom', 'prenom', 'email', 'telephone','message']

    def clean_telephone(self):
        tel = self.cleaned_data.get('telephone')
        if not tel.isdigit():
            raise forms.ValidationError("Le numéro de téléphone doit contenir uniquement des chiffres.")
        return tel


class DemandeServiceForm(forms.ModelForm):
    class Meta:
        model = DemandeService
        fields = [
            'nom', 'prenom', 'date_naissance', 'lieu_naissance', 
            'nom_pere', 'nom_mere', 'annee_acte', 'numero_extrait', 
            'nom_concerne', 'date_mariage', 'lieu_mariage', 
            'nom_epoux1', 'nom_epoux2', 'nom_defunt', 'date_deces', 
            'lien_parente', 'nom_demandeur', 'email_demandeur', 'tel_demandeur'
        ]
