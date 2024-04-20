from decimal import Decimal

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.urls import reverse
from django.utils.safestring import mark_safe

from explotacio import models
from globg.utils import str_to_float_or_zero

@permission_required('explotacio.change_entradesdematerial', raise_exception=True)
def nova_entrada_de_material(request):
    if request.method == 'POST':
        # recuperem els paràmetres: linia_id, quantitat
        linia_id = request.POST.get('linia_id') # És el detall de la comanda
        quantitat = str_to_float_or_zero(request.POST.get('quantitat'))
        # recuperem la linia de la comanda
        linia = get_object_or_404(models.DetallComandaProveidor, pk=linia_id)
        if quantitat <= 0:
            messages.error(request, 'La quantitat ha de ser un número vàlid')
            return render(request, 'explotacio/crear-entrades-de-material.html', {'linia': linia})
            #return redirect('/admin/explotacio/detallcomandaproveidor/') # request.path''
        # creem la nova entrada de material
        entrada = models.EntradesDeMaterial.objects.create(
            detall_comanda_proveidor = linia,
            quantitat = quantitat
        )
        linia.processada = True
        linia.save()
        #url = "{% url \'admin:explotacio_entradadematerial_change\'" + str(entrada.id) + " %}"
        #url = f"/admin/explotacio/entradesdematerial/{entrada.id}/change/"
        url = "/admin/explotacio/entradesdematerial/?actiu__exact=1"
        missatge = mark_safe(f'S\'ha creat la <a href="{url}">Nova entrada de material</a>')
        messages.success(request, missatge)
    return redirect('admin:explotacio_detallcomandaproveidor_changelist')
    #return redirect('/admin/explotacio/detallcomandaproveidor/')
    

@permission_required('explotacio.change_entradesdematerial', raise_exception=True)
def enviar_material_al_estoc(request):

    if request.method == 'POST':
        # recuperem els paràmetres: linia_id, capacitat_id, quantitat
        capacitat_id = request.POST.get('capacitat_id')
        linia_id = request.POST.get('linia_id') # És l'entrada de material
        quantitat = Decimal(str_to_float_or_zero(request.POST.get('quantitat')))

        # V a l i d a c i o n s

        # recuperem la linia de la comanda
        linia = get_object_or_404(models.EntradesDeMaterial, pk=linia_id)
        capacitats = models.Capacitat.objects.filter(tipus=linia.detall_comanda_proveidor.article.tipus.tipus_capacitat)
        if quantitat <= 0:
            messages.error(request, 'La quantitat ha de ser un número vàlid')
            return render(request, 'explotacio/enviar-material-al-estoc.html', {'linia': linia, 'capacitats': capacitats})
        
        if linia.quantitat < linia.assignats_a_corral + quantitat:
            messages.error(request, 'La quantitat introduïda mes la quantitat assignada a un corral no pot ser superior a la quantitat de la comanda')
            return render(request, 'explotacio/enviar-material-al-estoc.html', {'linia': linia, 'capacitats': capacitats})

        # B D

        # creem la nova entrada d'estoc
        capacitat = get_object_or_404(models.Capacitat, pk=capacitat_id)
        # Si hi ha una entrada d'estoc per aquest tipus de producte i capacitat, l'afegim a la mateixa entrada
        entrada = models.CapacitatEstoc.objects.filter(
            capacitat = capacitat,
            tipus_producte = linia.detall_comanda_proveidor.article.tipus
        ).first()
        if entrada:
            entrada.quantitat += quantitat
            entrada.save()
        else:
            entrada = models.CapacitatEstoc.objects.create(
                capacitat = capacitat,
                quantitat = quantitat,
                tipus_producte = linia.detall_comanda_proveidor.article.tipus
            )
            
        # Actualitzem l'entrada de material
        linia.assignats_a_corral += quantitat
        # Si assignats_a_corral = quantitat, posarem actiu = False
        if linia.assignats_a_corral == linia.quantitat:
            messages.success(request, "Es dona per finalitzada l'entrada de material")
            linia.actiu = False
        linia.save()

        #url = "/admin/explotacio/entradesdematerial/?actiu__exact=1"
        url = '/admin/explotacio/capacitatestoc/'
        missatge = mark_safe(f'S\'ha creat la <a href="{url}">Nova entrada a l\'estoc</a>')
        messages.success(request, missatge)

    return redirect('admin:explotacio_capacitatestoc_changelist')


@permission_required('explotacio.change_capacitatestoc', raise_exception=True)
def moure_estoc_entre_capacitats_del_mateix_tipus(request):
    if request.method == 'POST':
        # recuperem els paràmetres: linia_id, capacitat_id, quantitat
        capacitat_id = request.POST.get('capacitat_id')
        linia_id = request.POST.get('linia_id') # És l'entrada de material
        quantitat = Decimal(str_to_float_or_zero(request.POST.get('quantitat')))

        # V a l i d a c i o n s

        # recuperem la linia de la comanda
        linia = get_object_or_404(models.CapacitatEstoc, pk=linia_id)
        capacitats = models.Capacitat.objects.filter(tipus=linia.capacitat.tipus).exclude(pk=linia.capacitat.pk)
        if quantitat <= 0:
            messages.error(request, 'La quantitat ha de ser un número vàlid')
            return render(request, 'explotacio/moure-estoc-entre-capacitats-del-mateix-tipus.html', {'linia': linia, 'capacitats': capacitats})
        
        if quantitat > linia.quantitat:
            messages.error(request, 'La quantitat introduïda és més gran que la quantitat disponible')
            return render(request, 'explotacio/moure-estoc-entre-capacitats-del-mateix-tipus.html', {'linia': linia, 'capacitats': capacitats})

        # B D

        # creem la nova entrada d'estoc
        capacitat = get_object_or_404(models.Capacitat, pk=capacitat_id)
        # Si hi ha una entrada d'estoc per aquest tipus de producte i capacitat, l'afegim a la mateixa entrada
        estoc = models.CapacitatEstoc.objects.filter(
            capacitat = capacitat,
            tipus_producte = linia.tipus_producte
        ).first()
        if estoc:
            estoc.quantitat += quantitat
            estoc.save()
        else:
            messages.success(request, "S'ha creat un nou estoc a la capacitat seleccionada")
            estoc = models.CapacitatEstoc.objects.create(
                capacitat = capacitat,
                quantitat = quantitat,
                tipus_producte = linia.tipus_producte
            )

        # Actualitzem l'estoc actual
        linia.quantitat -= quantitat
        linia.save()
        messages.success(request, "S'han actualitzat els estocs corresponents")

    return redirect('admin:explotacio_capacitatestoc_changelist')