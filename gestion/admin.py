from django.contrib import admin
from .models import *
from django.utils.html import format_html

class PageSectionInline(admin.TabularInline):
    model = PageSection
    extra = 1  # Nombre de lignes vides à afficher par défaut
    verbose_name = "Section configurée"
    verbose_name_plural = "Configuration de l'ordre des sections"
    # On rend l'interface plus compacte et intuitive
    autocomplete_fields = ['section'] # Utile si vous avez 100+ sections

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'get_sections_count')
    search_fields = ('nom',)
    inlines = [PageSectionInline]
    
    def get_sections_count(self, obj):
        return obj.sections.count()
    get_sections_count.short_description = "Nombre de sections"

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
    # Permet de trouver rapidement une section dans l'autocomplete de PageAdmin
    ordering = ('nom',)

# Optionnel : permettre de voir la table de liaison seule
@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = ('page', 'ordre', 'section')
    list_filter = ('page',)
    list_editable = ('ordre',) # Permet de changer l'ordre directement dans la liste

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    # Aperçu rapide dans la liste
    list_display = ('display_icon', 'nom', 'type_service', 'tarif', 'ordre', 'demande_en_ligne')
    list_editable = ('ordre', 'demande_en_ligne')
    search_fields = ('nom', 'type_service')
    list_filter = ('demande_en_ligne', 'type_service')
    
    # Organisation du formulaire de création
    fieldsets = (
        ('Informations Générales', {
            'fields': (('nom', 'type_service'), 'description', 'icon', 'ordre')
        }),
        ('Détails Pratiques', {
            'fields': (('tarif', 'delai'), ('horaire', 'demande'))
        }),
        ('Démarches & Pièces', {
            'fields': ('demande_en_ligne', 'conditions')
        }),
    )

    def display_icon(self, obj):
     if obj.icon:
        # Si c'est un ImageField, on garde .url
        # Si c'est un CharField qui contient un lien, on enlève .url
        try:
            return format_html('<img src="{}" style="width: 30px; height: 30px;" />', obj.icon.url)
        except AttributeError:
            # Si c'est une simple chaîne de caractères (URL directe)
            return format_html('<img src="{}" style="width: 30px; height: 30px;" />', obj.icon)
     return "No Icon"

@admin.register(ServiceList)
class ServiceListAdmin(admin.ModelAdmin):
    list_display = ('service', 'pieces_requises_online', 'pieces_requises_place')
    list_filter = ('service',)
    search_fields = ('pieces_requises_online', 'pieces_requises_place')

@admin.register(DemandeService)
class DemandeServiceAdmin(admin.ModelAdmin):
    # La liste vue par l'agent de mairie
    list_display = ('numero_demande', 'nom_demandeur', 'service', 'colored_statut', 'date_soumission')
    list_filter = ('statut', 'service', 'date_soumission')
    search_fields = ('numero_demande', 'nom_demandeur', 'email_demandeur')
    readonly_fields = ('numero_demande', 'date_soumission') # On ne touche pas à l'ID technique
    
    # Organisation par blocs logiques (Fieldsets)
    fieldsets = (
        ('État de la Demande', {
            'fields': ('numero_demande', 'statut', 'date_retrait')
        }),
        ('Informations du Demandeur', {
            'fields': (('nom_demandeur', 'email_demandeur', 'tel_demandeur'),)
        }),
        ('Détails du Service', {
            'fields': ('service', 'nom_service')
        }),
        ('Bloc Naissance', {
            'classes': ('collapse',), # Le bloc est caché par défaut pour gagner de la place
            'fields': (('nom', 'prenom'), ('date_naissance', 'lieu_naissance'), ('nom_pere', 'nom_mere'))
        }),
        ('Bloc Copie Existante', {
            'classes': ('collapse',),
            'fields': ('annee_acte', 'numero_extrait', 'nom_concerne')
        }),
        ('Bloc Mariage', {
            'classes': ('collapse',),
            'fields': (('nom_epoux1', 'nom_epoux2'), ('date_mariage', 'lieu_mariage'))
        }),
        ('Bloc Décès', {
            'classes': ('collapse',),
            'fields': ('nom_defunt', 'date_deces', 'lien_parente')
        }),
    )

    # Pour mettre de la couleur sur les statuts dans la liste
    def colored_statut(self, obj):
        colors = {
            'attente': '#E67E22',  # Orange
            'en_cours': '#3498DB', # Bleu
            'pret': '#2ECC71',     # Vert
            'retire': '#95A5A6',   # Gris
            'rejete': '#E74C3C',   # Rouge
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 5px 10px; border-radius: 15px; font-weight: bold; font-size: 0.8rem;">{}</span>',
            colors.get(obj.statut, '#ccc'),
            obj.get_statut_display()
        )
    colored_statut.short_description = "Statut"

@admin.register(Actualite)
class ActualiteAdmin(admin.ModelAdmin):
    # 1. Configuration de la liste (Vue d'ensemble)
    list_display = ('preview_image', 'titre', 'colored_categorie', 'date_publication')
    list_filter = ('categorie', 'date_publication')
    search_fields = ('titre', 'contenu')
    date_hierarchy = 'date_publication' # Ajoute une barre de navigation temporelle en haut
    list_per_page = 20

    # 2. Organisation du formulaire de saisie
    fieldsets = (
        ('En-tête de l\'article', {
            'fields': ('titre', 'categorie', 'image')
        }),
        ('Contenu de l\'actualité', {
            'fields': ('contenu',),
            'description': 'Rédigez le corps de l\'article ici.'
        }),
        ('Liens et Redirection', {
            'fields': (('lien', 'suite'),),
            'classes': ('collapse',), # On cache cette partie technique par défaut
        }),
        ('Planification', {
            'fields': ('date_publication',),
        }),
    )

    # 3. Fonction pour prévisualiser l'image dans la liste
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 80px; height: 50px; object-fit: cover; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />', obj.image.url)
        return "Pas d'image"
    preview_image.short_description = "Aperçu"

    # 4. Fonction pour mettre de la couleur sur les badges de catégorie
    def colored_categorie(self, obj):
        colors = {
            'Événement': '#8e44ad', # Violet
            'Annonce': '#2980b9',   # Bleu
            'Travaux': '#d35400',   # Orange
            'Culture': '#27ae60',   # Vert
            'Sport': '#c0392b',     # Rouge
        }
        color = colors.get(obj.categorie, '#7f8c8d')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 10px; font-weight: bold; font-size: 0.75rem;">{}</span>',
            color,
            obj.categorie
        )
    colored_categorie.short_description = "Catégorie"

def image_preview(obj):
    if obj.image:
        return format_html('<img src="{}" style="width: 70px; height: auto; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);"/>', obj.image.url)
    return "Aucune image"
image_preview.short_description = "Aperçu"

@admin.register(DetailActualite)
class DetailActualiteAdmin(admin.ModelAdmin):
    # Affichage des 4 champs uniquement dans la liste
    list_display = ('actualite', 'images_actualite', 'alt', 'large_description')
    
    # Possibilité de filtrer par l'actualité parente
    list_filter = ('actualite',)
    
    # Recherche sur les champs texte
    search_fields = ('alt', 'large_description')

    # Organisation des 4 champs dans le formulaire d'ajout/modification
    fields = ('actualite', 'images_actualite', 'large_description', 'alt')

# --- ADMIN MAIRE ---
@admin.register(Maire)
class MaireAdmin(admin.ModelAdmin):
    list_display = (image_preview, 'nom', 'localiter', 'diplome')
    fieldsets = (
        ('Identité du Maire', {
            'fields': (('nom', 'image'), ('localiter', 'diplome'))
        }),
        ('Communication', {
            'fields': ('eloge', 'presentation', 'icon'),
            'description': "L'éloge apparaît généralement en citation sur le site."
        }),
    )

# --- ADMIN SLIDER ---
@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = (image_preview, 'titre', 'bouton')
    search_fields = ('titre', 'description')

# --- ADMIN EN-TETE ---
@admin.register(En_tete)
class EnTeteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'section', 'sous_titre','description',)
    list_filter = ('section',)
    search_fields = ('titre', 'description',)
    # Permet de lier rapidement une section avec recherche
    autocomplete_fields = ['section']

# --- ADMIN BANNER ---
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = (image_preview, 'nom_page', 'page', 'titre')
    list_filter = ('page',)
    # On groupe par usage pour ne pas saturer l'écran
    fieldsets = (
        ('Configuration Page', {
            'fields': (('page', 'nom_page'), 'page_html')
        }),
        ('Contenu Visuel', {
            'fields': ('image', 'titre', 'description')
        }),
    )

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (image_preview, )

@admin.register(SiteVisite)
class SiteVisiteAdmin(admin.ModelAdmin):
    # 1. Vue liste : rapide et visuelle
    list_display = ('get_thumbnail', 'nom', 'get_colored_type', 'lieu', 'adresse')
    list_filter = ('type_lieu', 'lieu')
    search_fields = ('nom', 'description', 'adresse')
    list_per_page = 15

    # 2. Formulaire : structuré pour la rédaction
    fieldsets = (
        ('Informations de Base', {
            'fields': (('nom', 'type_lieu'), 'image')
        }),
        ('Localisation', {
            'fields': (('lieu', 'adresse'),'description'),
            'description': "Le champ 'Lieu' correspond au quartier ou à la zone (ex: Plateau, Cocody)."
        }),
    )

    # 3. Prévisualisation de l'image (Format paysage 16/9)
    def get_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: 60px; object-fit: cover; border-radius: 8px; border: 1px solid #ddd;" />', obj.image.url)
        return "Aucune image"
    get_thumbnail.short_description = "Aperçu du site"

    # 4. Badges colorés par type de lieu
    def get_colored_type(self, obj):
        colors = {
            'Monument': '#1a252f',      # Sombre / Historique
            'Place': '#3498db',         # Bleu
            'Parc': '#27ae60',          # Vert
            'Marché': '#f39c12',        # Orange
            'Édifice': '#8e44ad',       # Violet
            'Site naturel': '#16a085',  # Émeraude
            'Infrastructure': '#7f8c8d' # Gris
        }
        color = colors.get(obj.type_lieu, '#bdc3c7')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: bold;">{}</span>',
            color,
            obj.get_type_lieu_display()
        )
    get_colored_type.short_description = "Catégorie"

@admin.register(MessageMairie)
class MessageMairieAdmin(admin.ModelAdmin):
    # On affiche uniquement les champs qui existent dans ton modèle
    list_display = ('nom', 'prenom', 'email', 'telephone', 'message_court', 'repondre')
    
    # On met tout en lecture seule pour éviter les erreurs de manipulation
    readonly_fields = ('nom', 'prenom', 'email', 'telephone', 'message')

    # 1. Coupe le message s'il est trop long pour l'affichage
    def message_court(self, obj):
        if obj.message:
            return obj.message[:50] + "..."
        return "-"
    message_court.short_description = "Message"

    # 2. Ajoute un bouton simple pour répondre
    def repondre(self, obj):
        return format_html(
            '<a href="mailto:{}" style="background-color: #007bff; color: white; padding: 5px 10px; border-radius: 3px; text-decoration: none;">Écrire</a>',
            obj.email
        )
    repondre.short_description = "Action"

    # Empêche de créer un message manuellement (évite les erreurs de champs vides)
    def has_add_permission(self, request):
        return False
    
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste
    list_display = ('nom_mairie', 'telephone', 'email', 'localisation', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: auto; border-radius: 5px;" />', obj.image.url)
        return "Pas d'image"
    
    # Organisation du formulaire par sections (Fieldsets)
    fieldsets = (
        ('Identité de la Mairie', {
            'fields': ('nom_mairie', 'email', 'telephone'),
            'description': "Informations principales de l'administration"
        }),
        ('Localisation Physique', {
            'fields': ('localisation', 'adresse_ville', 'adresse_postal'),
            'classes': ('collapse',), # Section repliable si besoin
        }),
        ('Coordonnées GPS (Google Maps)', {
            'fields': (('latitude', 'longitude'),), # Côte à côte
            'description': "Récupérez ces données par un clic droit sur Google Maps"
        }),
        ('Horaires d\'Ouverture', {
            'fields': (
                ('jour_semaine', 'heure'), 
                ('jour_samedi', 'heure_samedi')
            ),
        }),
        ('Note Importante', {
            'fields': ('NB','image'),
        }),
    )

    # Aide à la saisie
    def save_model(self, request, obj, form, change):
        # On peut ajouter ici une logique de validation si besoin
        super().save_model(request, obj, form, change)

@admin.register(Histoire)
class HistoireAdmin(admin.ModelAdmin):
    # Organisation par sections pour éviter les longs formulaires
    fieldsets = (
        ("Introduction", {
            'fields': ('titre', 'description1', 'description2', 'description3')
        }),
        ("Le Fleuve Bandama", {
            'fields': ('image', 'description_bandama'),
            'description': "Section dédiée à l'illustration et l'explication du fleuve."
        }),
        ("Contenu Multimédia", {
            'fields': ('titre_video', 'lien_video'),
        }),
    )
    
    list_display = ('titre', 'aperçu_image', 'titre_video')
    readonly_fields = ('aperçu_image_grande',)

    def aperçu_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: auto; border-radius: 5px;" />', obj.image.url)
        return "Pas d'image"
    
    def aperçu_image_grande(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 300px; border-radius: 10px;" />', obj.image.url)
        return "Aucun aperçu disponible"

@admin.register(Nombre)
class NombreAdmin(admin.ModelAdmin):
    list_display = ('nom_ville', 'nombre_habitants', 'nombre_quartiers', 'nombre_villages','nombre_hopitaux', 'nombre_ecoles', 'nombre_services')
    list_editable = ('nombre_habitants', 'nombre_quartiers', 'nombre_villages', 'nombre_hopitaux', 'nombre_ecoles', 'nombre_services')
    
    # Regroupement des statistiques
    fieldsets = (
        ("Identification", {'fields': ('nom_ville',)}),
        ("Statistiques Territoriales", {
            'fields': ('nombre_quartiers', 'nombre_villages')
        }),
        ("Population & Social", {
            'fields': ('nombre_habitants', 'nombre_hopitaux', 'nombre_ecoles')
        }),
        ("Économie & Services", {
            'fields': ('nombre_services',),
        }),
    )

@admin.register(Navigation)
class NavigationAdmin(admin.ModelAdmin):
    list_display = ('nom_mairie', 'aperçu_logo')
    
    def aperçu_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="width: 40px; background: #eee; padding: 2px;" />', obj.logo.url)
        return "-"

@admin.register(NavigationLink)
class NavigationLinkAdmin(admin.ModelAdmin):
    list_display = ("nom_page", "lien_page")


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ('nom_mairie', 'annee_copyright', 'logo', 'aperçu_image',)
    
    def aperçu_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 40px; background: #eee; padding: 2px;" />', obj.image.url)
        return "-"

@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ('nom_page', 'lien_page', 'icon_reseau','lien_reseau','nom_service')
    search_fields = ("nom_page", "icon_reseau", "nom_service")

    fieldsets = (
        ("Les differentes pages ", {
            'fields': ('nom_page', 'lien_page')
        }),
        ("Réseaux Sociaux", {
            'fields': ('icon_reseau', 'lien_reseau'),
            'description': "Utilisez les classes FontAwesome (ex: fa-facebook)"
        }),
        ("Services Mairie", {
            'fields': ('nom_service', 'modal_service'),
            'description': "Nom du service pour le lien dans le footer (ex: Acte de naissance) et ID du modal correspondant (ex: naissance)"
        }),
    )

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom','fonction', 'icon','aperçu_image')
    readonly_fields = ('aperçu_image_grande',)

    def aperçu_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: auto; border-radius: 5px;" />', obj.image.url)
        return "Pas d'image"
    
    def aperçu_image_grande(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 300px; border-radius: 10px;" />', obj.image.url)
        return "Aucun aperçu disponible"
    
@admin.register(Legislation)
class LegislationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'sous_titre', 'icone')
    search_fields = ('titre', 'sous_titre')
    list_filter = ('titre',)
    
    fieldsets = (
        ("Informations de Base", {
            'fields': ('titre', 'sous_titre', 'icone')
        }),)

@admin.register(DemandeLegalisation)
class DemandeLegalisationAdmin(admin.ModelAdmin):

    list_display = (
        "code_suivi",
        "type_legalisation",
        "date",
        "telecharger_fichier",
    )

    list_filter = (
        "type_legalisation",
        "date",
    )

    search_fields = (
        "code_suivi",
        "type_legalisation__titre",
    )

    ordering = ("-date",)

    readonly_fields = (
        "code_suivi",
        "date",
    )

    list_per_page = 25

    date_hierarchy = "date"   # 🔥 navigation par date en haut

    # 📂 Bouton téléchargement rapide
    def telecharger_fichier(self, obj):
        if obj.fichier:
            return format_html(
                '<a class="button" href="{}" target="_blank">📥 Télécharger</a>',
                obj.fichier.url
            )
        return "Aucun fichier"

    telecharger_fichier.short_description = "Fichier"
    