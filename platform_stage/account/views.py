import os
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse, reverse_lazy

from account.forms import *
from stage import settings
from stageapp.permission import user_is_student 


def get_success_url(request):

    """
    Handle Success Url After LogIN

    """
    if 'next' in request.GET and request.GET['next'] != '':
        return request.GET['next']
    else:
        return reverse('stageapp:home')



def employee_registration(request):

    """
    Handle Student Registration

    """
    form = StudentRegistrationForm(request.POST or None)
    if form.is_valid():
        form = form.save()
        return redirect('account:login')
    context={
        
            'form':form
        }

    return render(request,'account/student-registration.html',context)


def employer_registration(request):

    """
    Handle Student Registration 

    """

    form = EmployerRegistrationForm(request.POST or None)
    if form.is_valid():
        form = form.save()
        return redirect('account:login')
    context={
        
            'form':form
        }

    return render(request,'account/employer-registration.html',context)


@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_student
def employee_edit_profile(request, id=id):

    """
    Handle Student Profile Update Functionality

    """

    user = get_object_or_404(User, id=id)
    form = StudentProfileEditForm(request.POST or None, instance=user)
    if form.is_valid():
        form = form.save()
        messages.success(request, 'Your Profile Was Successfully Updated!')
        return redirect(reverse("account:edit-profile", kwargs={
                                    'id': form.id
                                    }))
    context={
        
            'form':form
        }

    return render(request,'account/student-edit-profile.html',context)



def user_logIn(request):

    """
    Provides users to logIn

    """

    form = UserLoginForm(request.POST or None)
    

    if request.user.is_authenticated:
        return redirect('/')
    
    else:
        if request.method == 'POST':
            if form.is_valid():
                auth.login(request, form.get_user())
                return HttpResponseRedirect(get_success_url(request))
    context = {
        'form': form,
    }

    return render(request,'account/login.html',context)

def user_logOut(request):
    """
    Provide the ability to logout
    """
    auth.logout(request)
    messages.success(request, 'You are Successfully logged out')
    return redirect('account:login')

@login_required(login_url=reverse_lazy('accounts:login'))
def upload_cv(request):
    if request.method == 'POST':
        form = CVForm(request.POST, request.FILES)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.user = request.user
            cv.save()
            return redirect('account/profile')  # Redirigez l'utilisateur vers son profil après avoir téléchargé le CV
    else:
        form = CVForm()
    return render(request, 'account/upload_cv.html', {'form': form})

@login_required(login_url=reverse_lazy('accounts:login'))
def view_cv(request):
    try:
        # Récupérer le CV de l'utilisateur connecté
        cv = CV.objects.get(user=request.user)
        # Construire le chemin vers le fichier CV dans le répertoire des médias
        cv_path = os.path.join(settings.MEDIA_ROOT, str(cv.cv_file))
        # Lire le contenu du fichier CV
        with open(cv_path, 'rb') as f:
            pdf_data = f.read()
        # Renvoyer une réponse HttpResponse avec le contenu du PDF
        response = HttpResponse(pdf_data, content_type='application/pdf')
        # Définir le nom de fichier pour le téléchargement ou l'affichage dans le navigateur
        response['Content-Disposition'] = f'inline;filename="{cv.cv_file.name}"'
        return response
    except CV.DoesNotExist:
        raise Http404("CV non trouvé pour cet utilisateur")
    except FileNotFoundError:
        raise Http404("Fichier CV introuvable")