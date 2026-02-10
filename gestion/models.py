import uuid
from django.db import models
import random
import string
from django.utils import timezone
from django.utils.text import slugify

class Page(models.Model):
     nom = models.CharField(max_length=32, verbose_name="Nom de la page")
     sections = models.ManyToManyField(
         'Section',
         through='PageSection',  # Indique le modèle à utiliser pour la relation
         related_name='pages'  # Nom pour la relation inverse (Section.pages)
     )
     def __str__(self):
         return f"Page {self.nom}"


class Section(models.Model):
     nom = models.CharField(max_length=255, verbose_name="Nom de la section")
     
     def __str__(self):
         return f"Section {self.nom}"


class PageSection(models.Model):
     page = models.ForeignKey(
         'Page',
         on_delete=models.CASCADE,
         verbose_name="Page hôte"
     )
     section = models.ForeignKey(
         'Section',
         on_delete=models.CASCADE,
         verbose_name="Section incluse"
     )
     ordre = models.PositiveIntegerField(
         verbose_name="Ordre dans la page"
     )

     class Meta:
         # S'assurer qu'une page ne peut avoir qu'une seule section à un ordre donné
         unique_together = (('page', 'ordre'), ('page', 'section'),)

         # Définir l'ordre par défaut pour les requêtes sur ce modèle
         ordering = ['ordre']

     def __str__(self):
         return f"Ordre {self.ordre}: {self.section.nom} dans {self.page.nom}"



class Service(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    horaire = models.CharField(max_length=255, blank=True)
    demande = models.CharField(max_length=255, blank=True)
    type_service = models.CharField(max_length=255)
    conditions = models.TextField(blank=True)
    tarif = models.CharField(max_length=255, blank=True)
    delai = models.CharField(max_length=255, blank=True)
    demande_en_ligne = models.BooleanField(default=False)
    icon = models.CharField(max_length=255, blank=True, null=True, default="baby")
    ordre = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["ordre", "nom"]

    def __str__(self):
        return self.nom
    
class ServiceList(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    pieces_requises_online = models.CharField(max_length=255,blank=True)
    pieces_requises_place = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return f"{self.service}"

class DemandeService(models.Model):
    numero_demande = models.CharField(max_length=255, unique=True, editable=False)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    statut = models.CharField(
        max_length=20,
        choices=[
            ('attente', 'En attente'),
            ('en_cours', 'En cours'),
            ('pret', 'Prêt à retirer'),
            ('retire', 'Retiré'),
            ('rejete', 'Rejeté'),
        ],
        default='attente'
    )
    date_soumission = models.DateTimeField(auto_now_add=True)
    date_retrait = models.DateTimeField(null=True, blank=True)
    nom_demandeur = models.CharField(max_length=100) 
    email_demandeur = models.EmailField()
    tel_demandeur = models.CharField(max_length=20)

    nom = models.CharField(max_length=100, blank=True, null=True)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    lieu_naissance = models.CharField(max_length=200, blank=True, null=True)
    nom_pere = models.CharField(max_length=100, blank=True, null=True)
    nom_mere = models.CharField(max_length=100, blank=True, null=True)
    
    annee_acte = models.IntegerField(blank=True, null=True)
    numero_extrait = models.CharField(max_length=50, blank=True, null=True)
    nom_concerne = models.CharField(max_length=100, blank=True, null=True)

    date_mariage = models.DateField(blank=True, null=True)
    lieu_mariage = models.CharField(max_length=200, blank=True, null=True)
    nom_epoux1 = models.CharField(max_length=100, blank=True, null=True)
    nom_epoux2 = models.CharField(max_length=100, blank=True, null=True)

    nom_defunt = models.CharField(max_length=100, blank=True, null=True)
    date_deces = models.DateField(blank=True, null=True)
    lien_parente = models.CharField( max_length=50, blank=True )

    class Meta:
        ordering = ['-date_soumission']

    def __str__(self):
        return f"{self.numero_demande} ({self.service.nom})"

    def save(self, *args, **kwargs):
        if not self.numero_demande:
            date_str = timezone.now().strftime('%Y%m%d')
            random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            self.numero_demande = f"DEM-{date_str}-{random_str}"
        super().save(*args, **kwargs)
    
class Actualite(models.Model):
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    lien = models.CharField(max_length=255)
    image = models.ImageField(upload_to="actu")
    categorie = models.CharField(max_length=255
    ,choices=[('Événement', 'Événement'),
            ('Annonce', 'Annonce'),
            ('Travaux', 'Travaux'),
            ('Culture', 'Culture'),
            ('Sport', 'Sport')],default="Annonce")
    suite = models.CharField(max_length=255)
    date_publication = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_publication']

    def __str__(self):
        return self.titre
    
class DetailActualite(models.Model):
    actualite = models.ForeignKey(Actualite, on_delete=models.CASCADE, related_name='details')
    large_description = models.TextField()
    images_actualite = models.ImageField(upload_to="detail_actu")
    alt = models.CharField(max_length=255, blank=True)
    titre = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Détail de {self.actualite.titre}"

class SiteVisite(models.Model):
    nom = models.CharField(max_length=255)
    type_lieu = models.CharField(max_length=255,choices=[('Monument', 'Monument historique'),
        ('Place publique', 'Place publique'),
        ('Parc ou jardin', 'Parc ou jardin'),
        ('Marché', 'Marché'),
        ('Édifice religieux', 'Édifice religieux'),
        ('Site naturel', 'Site naturel'),
        ('Infrastructure', 'Infrastructure publique'),
        ('Hotel', 'Hôtel'),
        ('école','école')],default="Autres")
    description = models.TextField()
    image = models.ImageField(upload_to="ville")
    adresse = models.CharField(max_length=255)
    lieu = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nom

class MessageMairie(models.Model): #dans le footer
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField()
    telephone = models.CharField(max_length=255)
    message = models.TextField()
    
    def __str__(self):
        return self.nom

class Contact(models.Model): #sur page contact
    nom_mairie = models.CharField(max_length=255)
    localisation = models.CharField(max_length=255)
    adresse_ville = models.CharField(max_length=255)
    adresse_postal = models.CharField(max_length=255, blank=True)
    telephone = models.CharField(max_length=255)
    image = models.ImageField(upload_to="contact", blank=True, null=True)
    email = models.EmailField(max_length=255)
    jour_semaine = models.CharField(max_length=255)
    heure = models.CharField(max_length=255)
    jour_samedi = models.CharField(max_length=255)
    heure_samedi = models.CharField(max_length=255)
    NB = models.TextField(blank=True)
    latitude = models.DecimalField(
        max_digits=12,
        decimal_places=9,
        blank=True,
        null=True
    )
    longitude = models.DecimalField(
        max_digits=12,
        decimal_places=9,
        blank=True,
        null=True
    )
    
    def __str__(self):
        return self.nom_mairie
    
class Maire(models.Model):
    image = models.ImageField(upload_to="maire", blank=True, null=True)
    nom = models.CharField(max_length=255, blank=True, null=True)
    localiter = models.CharField(max_length=255, blank=True, null=True)
    eloge = models.CharField(max_length=255, blank=True, null=True)
    presentation = models.TextField()
    diplome = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nom
    
class Slider(models.Model):
    titre = models.CharField(max_length=255)
    description = models.CharField(max_length=555)
    lien = models.CharField(max_length=255)
    bouton = models.CharField(max_length=255)
    image = models.ImageField(upload_to="slider")

    def __str__(self):
        return self.titre
    
class En_tete(models.Model):
    section = models.ForeignKey(Section , on_delete=models.CASCADE)
    titre = models.CharField( max_length=500)
    sous_titre = models.CharField(max_length=500, blank=True)
    descriprion = models.CharField(max_length=500)

    def __str__(self):
        return self.titre
    
class Image(models.Model):
    image = models.ImageField(upload_to="image")
    titre = models.CharField(max_length=250)

    def __str__(self):
        return self.titre
    
class Banner(models.Model):
    choix=[
        ('accueil', 'Accueil'),
        ('mairie', 'Mairie'),
        ('services', 'Services'),
        ('contact', 'Contact'),
        ('actualites', 'Actualités'),
    ]
    page = models.CharField(max_length=50, choices=choix, unique=True)
    image = models.ImageField(upload_to="banner")
    page_html = models.CharField(max_length=250)
    nom_page = models.CharField(max_length=250)
    titre = models.CharField(max_length=255)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.nom_page
    
class Histoire(models.Model):
    titre = models.CharField(max_length=255)
    description1 = models.TextField()
    description2 = models.TextField()
    description3 = models.TextField()
    image = models.ImageField(upload_to="histoire")
    description_bandama = models.TextField()
    titre_video = models.CharField(max_length=255)
    lien_video = models.FileField(upload_to="video_histoire")

    def __str__(self):
        return self.titre

class Nombre(models.Model):
    nom_ville = models.CharField(max_length=255)
    nombre_quartiers = models.IntegerField()
    nombre_habitants = models.IntegerField()
    nombre_villages = models.IntegerField()
    nombre_hopitaux = models.IntegerField()
    nombre_ecoles = models.IntegerField()
    nombre_services = models.IntegerField()

    def __str__(self):
        return self.nom_ville
    
class Navigation(models.Model):
    logo = models.ImageField(upload_to="navigation")
    nom_mairie = models.CharField(max_length=255)
    slogan = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_mairie
    
class NavigationLink(models.Model):
    nom_page = models.CharField(max_length=255)
    lien_page = models.CharField(max_length=255)
    ordre = models.IntegerField()

    def __str__(self):
        return self.nom_page
    
class Footer(models.Model):
    logo = models.ImageField(upload_to="footer")
    nom_mairie = models.CharField(max_length=255)
    annee_copyright = models.CharField(max_length=255)
    image = models.ImageField(upload_to="footer_image", blank=True, null=True)

    def __str__(self):
        return self.nom_mairie
    
class FooterLink(models.Model):
    nom_page = models.CharField(max_length=255)
    lien_page = models.CharField(max_length=255)
    lien_reseau = models.CharField(max_length=255, blank=True)
    icon_reseau = models.CharField(max_length=255, blank=True)
    nom_service = models.CharField(max_length=255, blank=True)
    modal_service = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nom_page

class Team(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    image = models.ImageField(upload_to="team")
    fonction = models.CharField(max_length=255,default="Conseiller municipal")

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Legislation(models.Model):
    titre = models.CharField(max_length=255)
    sous_titre = models.CharField(max_length=255, blank=True)
    icone = models.CharField(max_length=255)

    def __str__(self):
        return self.titre
    
class DemandeLegalisation(models.Model):
    type_legalisation = models.ForeignKey(Legislation, on_delete=models.CASCADE)
    fichier = models.FileField(upload_to="demandes/")
    date = models.DateTimeField(auto_now_add=True)
    code_suivi = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.code_suivi:
            self.code_suivi = "LEG-" + uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.type_legalisation.titre} - {self.code_suivi}"