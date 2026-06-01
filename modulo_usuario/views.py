from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

def registro_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('username')
        pass_input = request.POST.get('password')
        confirm_pass = request.POST.get('confirm_password')

        if pass_input != confirm_pass:
            return render(request, 'registro.html', {'error': 'Las contraseñas no coinciden'})
        
        if User.objects.filter(username=user_input).exists():
            return render(request, 'registro.html', {'error': 'El usuario ya existe'})

        nuevo_user = User.objects.create_user(username=user_input, password=pass_input)
        nuevo_user.save()
        return redirect('login') 

    return render(request, 'modulo_usuario/registro.html')

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user)
            return redirect('/inicio/') 
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
            
    return render(request, 'modulo_usuario/login.html')

