from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from reservas.models.pasaje import Viaje
from reservas.forms.viajeroForm import ViajeroForm

class ViajeListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Viaje
    context_object_name = 'viajes'
    template_name = 'viajes/lista_viajes.html'
    
    def test_func(self):
        return self.request.user.is_staff
    
class ViajeCreateView(LoginRequiredMixin, CreateView):
    pass

class ViajeUpdateView(LoginRequiredMixin, UpdateView):
    pass

class ViajeDeleteView(LoginRequiredMixin, DeleteView):
    pass