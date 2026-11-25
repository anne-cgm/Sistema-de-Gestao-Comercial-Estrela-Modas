from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Usuario


@login_required
def usuarios(request):
    if not request.user.is_superuser:
        return redirect('mais_opcoes')
    return render(request, 'estrela_modas/usuarios.html', {
        'usuarios': Usuario.objects.all(),
    })
