from decimal import Decimal

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils.safestring import mark_safe

from explotacio.models import CapacitatEstoc
from globg.models import CAPACITAT_TIPUS_CORRAL
from globg.utils import str_to_float_or_zero, str_to_int_or_zero
from clients import models

def afegir_articles_estoc_a_venda(request):
    if request.method == 'POST':
        capacitat_estoc = CapacitatEstoc.objects.filter(tipus_producte__tipus_capacitat=CAPACITAT_TIPUS_CORRAL)
        # recorrem els capacitat_estoc
        for ce in capacitat_estoc:
            param_name = f"quantitat_{ce.id}"
            quantitat = request.POST.get(param_name)
            # si el paràmetre existeix
            if quantitat:
                quantitat = str_to_float_or_zero(quantitat)
                if quantitat > 0:
                    venda_id = request.POST.get('venda_id')
                    # Creem la nova línia de DetallVenda
                    detall_venda = models.DetallVenda()
                    detall_venda.venda = get_object_or_404(models.Vendes, pk=venda_id)
                    detall_venda.article = ce.article
                    detall_venda.quantitat = quantitat
                    detall_venda.preu_venda = ce.article.preu_venda
                    detall_venda.save()
                    # Ens cal restar del stock
                    ce.quantitat -= Decimal(quantitat)
                    ce.save()
                    message = f"Article {ce.tipus_producte.nom} afegit a la venda {detall_venda.venda.id} amb {detall_venda.quantitat} unitats"
                    messages.success(request, message)
        return redirect('admin:clients_vendes_change', venda_id)
    return redirect('admin:clients_vendes_changelist')
    

def article_defuncio(request):
    if request.method == 'POST':
        venda_id = request.POST.get('venda_id')
        venda = get_object_or_404(models.Vendes, pk=venda_id)
        for detall_venda in venda.detallvenda_set.all():
            param_name = f"quantitat_{detall_venda.id}"
            quantitat = str_to_int_or_zero(request.POST.get(param_name))
            for i in range(int(quantitat)):
                defuncio = models.Defuncions.objects.create(detall_venda=detall_venda)
                # De moment no restem de la venda.
                message = f"Documenta i assigna el tipus de defunció a <a href='/admin/clients/defuncions/{defuncio.id}/change/'>la defunció {defuncio.id}</a>"
                messages.success(request, mark_safe(message))
        messages.success(request, mark_safe("Cal modificar el tipus i la documentació de les defuncions. <a href='/admin/clients/defuncions/'>Defuncions</a>"))
        return redirect('admin:clients_vendes_change', venda_id)
    return redirect('admin:clients_vendes_changelist')