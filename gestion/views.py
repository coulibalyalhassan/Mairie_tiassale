from multiprocessing import context
from pyexpat.errors import messages
from django.contrib import messages
from django.http import JsonResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *

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
            context["en_tetes"]=En_tete.objects.filter(section__nom__iexact="contact")
            context["contacts"]=Contact.objects.all()
            if request.method == 'POST':
                form = MessageMairieForm(request.POST)
                if form.is_valid():
                   form.save()
            else:
                form = MessageMairieForm()
            context['form']=MessageMairieForm
        
        elif s == "actualites":
            context["en_tetes"]=En_tete.objects.filter(section__nom__iexact="actualites")
            context["actualites"]=Actualite.objects.all()

        elif s == "histoire":
            context["histoires"]=Histoire.objects.all()

        elif s == "conseillez_municipal":
            context["en_tetes"]=En_tete.objects.filter(section__nom__iexact="conseillez_municipal")
            context["teams"]=Team.objects.all()

        elif s == "nombre":
            context["nombres"]=Nombre.objects.all()

        elif s == "banner":
            context["banners"]=Banner.objects.filter(page=slug)

        elif s == "image":
            context["en_tetes"]=En_tete.objects.filter(section__nom__iexact="image")
            context["images"]=Image.objects.all()

        elif s == "le_maire":
            context["maires"]=Maire.objects.all()

        elif s == "lieu_visite":
            context["en_tetes"]=En_tete.objects.filter(section__nom__iexact="lieu_visite")
            context["siteVisites"]=SiteVisite.objects.all()

        elif s== "legalisation":
            if request.method == "POST" and request.FILES.get('fichier'):
                try:
                    type_id = request.POST.get('type_id')
                    file_obj = request.FILES.get('fichier')

                    type_leg = Legislation.objects.get(id=type_id)

            # 🔥 Création d'une nouvelle demande
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
            context["en_tetes"]=En_tete.objects.filter(section__nom__iexact="services")
            context["services"]=Service.objects.all()
            context["piecelist"]=ServiceList.objects.all()

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
                    retrait_f = demande.date_retrait.strftime('%d/%m/%Y') if demande.date_retrait else "à préciser"
            
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
    return render(request, 'accueil.html', context)

def detail_actualite(request, id):
    detail = get_object_or_404(Actualite, id=id)
    details = DetailActualite.objects.filter(actualite_id=id)
    context = {
        'detail': detail
        ,'details': details
    }
    return render(request, 'detail_actualites.html', context)