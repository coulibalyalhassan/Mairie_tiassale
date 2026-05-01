from multiprocessing import context
from pyexpat.errors import messages
from django.contrib import messages
from django.http import JsonResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def get_page(request, slug):
    page = Page.objects.get(nom=slug)
    sections = PageSection.objects.filter(page=page)  
    navigations = Navigation.objects.all()
    footers = Footer.objects.all()
    nav_links = NavigationLink.objects.all()
    footer_links = FooterLink.objects.all()
    context = {
        'page': page,
        'navigations': navigations,
        'footers': footers,
        'nav_links': nav_links,
        'footer_links': footer_links,
        'sections': [],
    }

    for ps in sections:
        s = ps.section.nom.lower()

        if s == "contact":
            context["en_tetes_contact"]=En_tete.objects.filter(section__nom__iexact="contact")
            context["contacts"]=Contact.objects.all()
            if request.method == 'POST':
                form = MessageMairieForm(request.POST)
                if form.is_valid():
                   form.save()
            else:
                form = MessageMairieForm()
            context['form']=MessageMairieForm
        
        elif s == "actualites":
            context["en_tetes_actualites"]=En_tete.objects.filter(section__nom__iexact="actualites")
            context["actualites"]=Actualite.objects.all()

        elif s == "histoire":
            context["histoires"]=Histoire.objects.all()

        elif s == "conseillez_municipal":
            context["en_tetes_conseillez_municipal"]=En_tete.objects.filter(section__nom__iexact="conseillez_municipal")
            context["teams"]=Team.objects.all()

        elif s == "nombre":
            context["nombres"]=Nombre.objects.all()

        elif s == "banner":
            context["banners"]=Banner.objects.filter(page=slug)

        elif s == "image":
            context["en_tetes_image"]=En_tete.objects.filter(section__nom__iexact="image")
            context["images"]=Image.objects.all()

        elif s == "le_maire":
            context["maires"]=Maire.objects.all()

        elif s == "lieu_visite":
            context["en_tetes_lieu_visite"]=En_tete.objects.filter(section__nom__iexact="lieu_visite")
            context["siteVisites"]=SiteVisite.objects.all()

        elif s== "legalisation":
            if request.method == "POST" and request.FILES.get('fichier'):
                try:
                    type_id = request.POST.get('type_id')
                    file_obj = request.FILES.get('fichier')
                    type_leg = Legislation.objects.get(id=type_id)
                    demande = DemandeLegalisation.objects.create(
                          type_legalisation=type_leg,
                          fichier=file_obj)
                    return JsonResponse({'status': 'success','code': demande.code_suivi})
                except Legislation.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Type introuvable'})
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': str(e)})

            context["legalisations"] = Legislation.objects.all()
            
        elif s == "services":
            context["en_tetes_services"]=En_tete.objects.filter(section__nom__iexact="services")
            context["services"]=Service.objects.all()
            context["piecelist"]=ServiceList.objects.all()

        elif s == "suivi":
            demande = None
            type_demande = None
            erreur = None

            if request.method == "POST":
                code = request.POST.get("code")

                # Cherche dans DemandeService
                try:
                    demande = DemandeService.objects.get(numero_demande=code)
                    type_demande = "Service administratif"
                except DemandeService.DoesNotExist:
            
                    # Cherche dans DemandeLegalisation
                    try:
                        demande = DemandeLegalisation.objects.get(code_suivi=code)
                        type_demande = "Légalisation"
                    except DemandeLegalisation.DoesNotExist:
                        erreur = "Code introuvable. votre demande n'existe pas ou a été rejetée."
            context["demande"] = demande
            context["type_demande"] = type_demande
            context["erreur"] = erreur

        elif s == "slider":
            context["slides"]=Slider.objects.all()

        elif s == "modal":
            context['services']= Service.objects.all()
            if request.method == 'POST' and 'btn_service' in request.POST:
               form = DemandeServiceForm(request.POST) 
               if form.is_valid():
                  demande = form.save(commit=False)
                  service_id = request.POST.get('DemandeService_id')
                  if service_id:
                    demande.service = Service.objects.get(id=service_id)
                    demande.save() 
            
                    soumission_f = demande.date_soumission.strftime('%d/%m/%Y à %H:%M')
                    retrait = demande.date_retrait + timedelta(hours=3)
                    retrait_f = retrait.strftime('%d/%m/%Y %H:%M')
            
                    msg = (
                      f"Demande enregistrée le {soumission_f}.\n"
                      f"N° de suivi : {demande.numero_demande}.\n"
                      f"Rendez-vous pour le retrait le : {retrait_f}."
                      )         
                    messages.success(request, msg)
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                  else:
                    messages.error(request, "Erreur : Service non identifié.")
               else:
                print(form.errors)
                messages.error(request, "Veuillez vérifier les champs du formulaire.")
                return redirect(request.META.get('HTTP_REFERER', '/'))

    context["sections"] = sections
    return render(request, 'index.html', context)

def detail_actualite(request, id):
    detail = get_object_or_404(Actualite, id=id)
    details = DetailActualite.objects.filter(actualite_id=id)
    context = {
        'detail': detail
        ,'details': details
    }
    return render(request, 'detail_actualites.html', context)

@login_required
@require_POST
def ajax_changer_statut_acte(request):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Accès refusé'})

    demande_id = request.POST.get('demande_id')
    demande = DemandeService.objects.filter(id=demande_id).first()
    if not demande:
        return JsonResponse({'success': False, 'message': 'Demande introuvable'})

    nouveau_statut = request.POST.get('statut')

    if nouveau_statut == 'rejete':
        demande.delete()
        return JsonResponse({'success': True, 'action': 'supprime'})
    else:
        demande.statut = nouveau_statut
        demande.save()
        return JsonResponse({
            'success': True,
            'action': 'mis_a_jour',
            'nouveau_statut': nouveau_statut,
            'display': demande.get_statut_display()
        })

@login_required
@require_POST
def ajax_changer_statut_legalisation(request):

    if not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Accès refusé'})

    demande_id = request.POST.get('demande_id')
    legalises = DemandeLegalisation.objects.filter(id=demande_id).first()
    
    doc_legalises = request.POST.get("statut")

    if doc_legalises == "rejete":
        legalises.delete()
        return JsonResponse({'success': True, 'action': 'supprime'})
    else:
        legalises.statut = doc_legalises
        legalises.save()
        return JsonResponse({
            'success': True,
            'action': 'mis_a_jour',
            'doc_legalises': doc_legalises,
            'display': legalises.get_statut_display()
        })

    
@login_required
def dashboard_mairie(request):
    if not request.user.is_staff:
        return redirect('gestion:accueil')

    demandes_services = DemandeService.objects.exclude(statut='retire').order_by('-date_soumission')
    demandes_traitees = DemandeService.objects.filter(statut='retire').order_by('-date_soumission')
    demandes_legalisation = DemandeLegalisation.objects.exclude(statut='traitee').order_by('-date')
    demandes_legalisees = DemandeLegalisation.objects.filter(statut='traitee').order_by('-date')
    messages_mairie = MessageMairie.objects.all().order_by('-id')

    stats = {
        'services': demandes_services.count(),
        'traitees': demandes_traitees.count(),
        'legalisations': demandes_legalisation.count(),
        'legalisees': demandes_legalisees.count(),
        'messages': messages_mairie.count()
    }

    context = {
        'demandes_services': demandes_services,
        'demandes_traitees': demandes_traitees,
        'demandes_legalisation': demandes_legalisation,
        'demandes_legalisees': demandes_legalisees,
        'messages_mairie': messages_mairie,
        'stats': stats,
    }

    return render(request, 'dashboard.html', context)

