from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from reservas.models import ruta, viajero, viajero, agencia, pasaje
from django.db.models.functions import TruncDate
from django.views.generic import ListView, FormView, TemplateView, UpdateView
from reservas.models import Agencia, Ruta, Pasaje, Viaje, Viajero
from django.db.models import Count, F
from django.utils import timezone
from datetime import datetime, timedelta
from .forms import ViajerosForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

# Create your views here.
def home(request):
    transport_curiosities = [
        {'curiosity': 'El primer avión de pasajeros voló en  1908.', 'source': 'Historia del Avión'},
        {'curiosity': 'El primer automóvil de producción en masa fue el Ford Model T, lanzado en  1908.', 'source': 'Historia del Automóvil'},
        {'curiosity': 'El primer tren de alta velocidad, el Shinkansen, comenzó a operar en Japón en  1964.', 'source': 'Historia del Tren'},
        {'curiosity': 'El primer sistema de metro subterráneo fue inaugurado en Londres en  1863.', 'source': 'Historia del Metro'},
        {'curiosity': 'El primer ferry de hidrógeno, el "Hyperion", comenzó a operar en  2021.', 'source': 'Innovaciones en Transporte'},
    ]
    rutas = ruta.Ruta.objects.all()

    pasajes_disponibles = pasaje.Pasaje.objects.annotate(
        asientos_ocupados=Count('viaje')
    ).filter(
        asientos_ocupados__lt=F('capacidad'),
        fecha__gte=timezone.now().date()
    )[:6]

    
    context = {'rutas': rutas, 'transport_curiosities': transport_curiosities, 'pasajes': pasajes_disponibles}
    
    return render(request, 'web/home.html', context)

def buscar(request):
    if request.method == 'POST':
        pasajes = pasaje.Pasaje.objects.annotate(fecha_truncada=TruncDate('fecha')).filter(origen=request.POST['origen'], destino=request.POST['destino'], fecha_truncada=request.POST['fecha'])
        
        
        return render(request, 'web/pasaje.html', {'pasajes': pasajes})
    else:
        rutas = ruta.Ruta.objects.all()
        return render(request, 'web/buscar.html', {'rutas': rutas})
    
class AgenciaListView(ListView):
    model = agencia.Agencia
    context_object_name = 'agencias'
    template_name = 'web/agencias.html'
    

class ViajerosCompraView(LoginRequiredMixin, FormView):
    template_name = 'web/reservar/viajeros.html'
    form_class = ViajerosForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["asientos"] = pasaje.Pasaje.objects.get(pk=self.kwargs.get('pk')).asientos()
        return context
    
    def get_success_url(self):
        return reverse_lazy('reservar_detalles', kwargs={'pk': self.kwargs.get('pk')})
    
    def get_form_kwargs(self):
        kwargs = super(ViajerosCompraView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.request.session['viajeros_ids'] = list(form.cleaned_data['viajeros'].values_list('id', flat=True))
        return super().form_valid(form)
    
class DetallesCompraView(LoginRequiredMixin, TemplateView):
    template_name = 'web/reservar/detalles.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        viajeros_ids = self.request.session.get('viajeros_ids', [])
        viajeros = Viajero.objects.filter(id__in=viajeros_ids)
        pasaje = Pasaje.objects.get(pk=self.kwargs.get('pk'))
        context['total_pagar'] = len(viajeros) * pasaje.precio
        context['pasaje'] = pasaje
        context["viajeros"] = viajeros
        return context
    
    def post(self, request, *args, **kwargs):
        viajeros_ids = self.request.session.get('viajeros_ids', [])
        viajeros = Viajero.objects.filter(id__in=viajeros_ids)
        pasaje = Pasaje.objects.get(pk=self.kwargs.get('pk'))
        for viajero in viajeros:
            viaje = Viaje()
            viaje.pasaje = pasaje
            viaje.viajero = viajero
            viaje.user = request.user
            viaje.save()
        del self.request.session['viajeros_ids']    
        return redirect('reservar_completado')
    
class CompletadoView(LoginRequiredMixin, TemplateView):
    template_name = 'web/reservar/completado.html'
    
    
    
class ReservasListView(LoginRequiredMixin, ListView):
    model = Viaje
    context_object_name = "reservas"
    template_name = "web/reservas/lista_reservas.html"
    
    def get_queryset(self):
        user = self.request.user
        fecha_actual = timezone.now()
        viajes  = Viaje.objects.filter(user=user)
        for viaje in viajes:
            diferencia = viaje.pasaje.fecha - fecha_actual
            if diferencia.days <= 2:
                viaje.estado = 'proxima'
                viaje.save()
            elif viaje.pasaje.fecha < fecha_actual:
                viaje.estado = 'realizada'
                viaje.save()
        return viajes
    
        
class CancelarReservaView(LoginRequiredMixin, UpdateView):
    model = Viaje
    fields = ['estado']
    template_name = 'web/reservas/cancelar_reserva.html'
    success_url = reverse_lazy('reservas')
    
    def post(self, request, *args, **kwargs):
        viaje = self.get_object()
        if viaje.user == request.user:
            viaje.estado = 'cancelada'
            viaje.save()
            return redirect('reservas')
        else:
            return redirect('reservas')
    