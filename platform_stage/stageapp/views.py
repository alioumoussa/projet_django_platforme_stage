from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.core.serializers import serialize
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from account.models import User
from stageapp.forms import *
from stageapp.models import *
from stageapp.permission import *
User = get_user_model()


# def is_ajax(request):
#     return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
def home_view(request):

    published_jobs = Stage.objects.filter(is_published=True).order_by('-timestamp')
    jobs = published_jobs.filter(is_closed=False)
    total_candidates = User.objects.filter(role='student').count()
    total_companies = User.objects.filter(role='employer').count()
    paginator = Paginator(jobs, 3)
    page_number = request.GET.get('page',None)
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        stage_lists=[]
        stage_objects_list = page_obj.object_list.values()
        for stage_list in stage_objects_list:
            stage_lists.append(stage_list)
        

        next_page_number = None
        if page_obj.has_next():
            next_page_number = page_obj.next_page_number()

        prev_page_number = None       
        if page_obj.has_previous():
            prev_page_number = page_obj.previous_page_number()

        data={
            'stage_lists':stage_lists,
            'current_page_no':page_obj.number,
            'next_page_number':next_page_number,
            'no_of_page':paginator.num_pages,
            'prev_page_number':prev_page_number
        }    
        return JsonResponse(data)
    
    context = {

    'total_candidates': total_candidates,
    'total_companies': total_companies,
    'total_jobs': len(jobs),
    'total_completed_jobs':len(published_jobs.filter(is_closed=True)),
    'page_obj': page_obj
    }
    # print('ok')
    return render(request, 'stageapp/index.html', context)

@cache_page(60 * 15)
def stage_list_View(request):
    """

    """
    stage_list = Stage.objects.filter(is_published=True,is_closed=False).order_by('-timestamp')
    paginator = Paginator(stage_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {

        'page_obj': page_obj,

    }
    return render(request, 'stageapp/stage-list.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def create_stage_View(request):
    """
    Provide the ability to create stage post
    """
    form = StageForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    categories = Category.objects.all()

    if request.method == 'POST':

        if form.is_valid():

            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(
                    request, 'You are successfully posted your stage! Please wait for review.')
            return redirect(reverse("stageapp:single-stage", kwargs={
                                    'id': instance.id
                                    }))

    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'stageapp/post-stage.html', context)


def single_stage_view(request, id):
    """
    Provide the ability to view stage details
    """
    if cache.get(id):
        stage = cache.get(id)
    else:
        stage = get_object_or_404(Stage, id=id)
        cache.set(id,stage , 60 * 15)
    related_stage_list = stage.tags.similar_objects()

    paginator = Paginator(related_stage_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'stage': stage,
        'page_obj': page_obj,
        'total': len(related_stage_list)

    }
    return render(request, 'stageapp/stage-single.html', context)


def search_result_view(request):
    """
        User can search stage with multiple fields

    """

    stage_list = Stage.objects.order_by('-timestamp')

    # Keywords
    if 'stage_title_or_company_name' in request.GET:
        stage_title_or_company_name = request.GET['stage_title_or_company_name']

        if stage_title_or_company_name:
            stage_list = stage_list.filter(title__icontains=stage_title_or_company_name) | stage_list.filter(
                company_name__icontains=stage_title_or_company_name)

    # location
    if 'location' in request.GET:
        location = request.GET['location']
        if location:
            stage_list = stage_list.filter(location__icontains=location)

    # Stage Type
    if 'stage_type' in request.GET:
        stage_type = request.GET['stage_type']
        if stage_type:
            stage_list = stage_list.filter(stage_type__iexact=stage_type)

    # stage_title_or_company_name = request.GET.get('text')
    # location = request.GET.get('location')
    # stage_type = request.GET.get('type')

    #     stage_list = Stage.objects.all()
    #     stage_list = stage_list.filter(
    #         Q(stage_type__iexact=stage_type) |
    #         Q(title__icontains=stage_title_or_company_name) |
    #         Q(location__icontains=location)
    #     ).distinct()

    # stage_list = Stage.objects.filter(stage_type__iexact=stage_type) | Stage.objects.filter(
    #     location__icontains=location) | Stage.objects.filter(title__icontains=text) | Stage.objects.filter(company_name__icontains=text)

    paginator = Paginator(stage_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {

        'page_obj': page_obj,

    }
    return render(request, 'stageapp/result.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_student
def apply_stage_view(request, id):

    form = JobApplyForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = Applicant.objects.filter(user=user, stage=id)

    if not applicant:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully applied for this stage!')
                return redirect(reverse("stageapp:single-stage", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("stageapp:single-stage", kwargs={
                'id': id
            }))

    else:

        messages.error(request, 'You already applied for the Stage!')

        return redirect(reverse("stageapp:single-stage", kwargs={
            'id': id
        }))


@login_required(login_url=reverse_lazy('account:login'))
def dashboard_view(request):
    """
    """
    jobs = []
    savedjobs = []
    appliedjobs = []
    total_applicants = {}
    if request.user.role == 'employer':

        jobs = Stage.objects.filter(user=request.user.id)
        for stage in jobs:
            count = Applicant.objects.filter(stage=stage.id).count()
            total_applicants[stage.id] = count

    if request.user.role == 'student':
        savedjobs = BookmarkJob.objects.filter(user=request.user.id)
        appliedjobs = Applicant.objects.filter(user=request.user.id)
    context = {

        'jobs': jobs,
        'savedjobs': savedjobs,
        'appliedjobs':appliedjobs,
        'total_applicants': total_applicants
    }

    return render(request, 'stageapp/dashboard.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def delete_stage_view(request, id):

    stage = get_object_or_404(Stage, id=id, user=request.user.id)

    if stage:

        stage.delete()
        messages.success(request, 'Your Stage Post was successfully deleted!')

    return redirect('stageapp:dashboard')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def make_complete_stage_view(request, id):
    stage = get_object_or_404(Stage, id=id, user=request.user.id)

    if stage:
        try:
            stage.is_closed = True
            stage.save()
            messages.success(request, 'Your Stage was marked closed!')
        except:
            messages.success(request, 'Something went wrong !')
            
    return redirect('stageapp:dashboard')



@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def all_applicants_view(request, id):

    all_applicants = Applicant.objects.filter(stage=id)

    context = {

        'all_applicants': all_applicants
    }

    return render(request, 'stageapp/all-applicants.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_student
def delete_bookmark_view(request, id):

    stage = get_object_or_404(BookmarkJob, id=id, user=request.user.id)

    if stage:

        stage.delete()
        messages.success(request, 'Saved Stage was successfully deleted!')

    return redirect('stageapp:dashboard')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def applicant_details_view(request, id):

    applicant = get_object_or_404(User, id=id)
    cv = applicant.cv

    context = {

        'applicant': applicant,
        'cv' : cv
    }

    return render(request, 'stageapp/applicant-details.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_student
def stage_bookmark_view(request, id):

    form = JobBookmarkForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = BookmarkJob.objects.filter(user=request.user.id, stage=id)

    if not applicant:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully save this stage!')
                return redirect(reverse("stageapp:single-stage", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("stageapp:single-stage", kwargs={
                'id': id
            }))

    else:
        messages.error(request, 'You already saved this Stage!')

        return redirect(reverse("stageapp:single-stage", kwargs={
            'id': id
        }))


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def stage_edit_view(request, id=id):
    """
    Handle Stage Update

    """

    stage = get_object_or_404(Stage, id=id, user=request.user.id)
    categories = Category.objects.all()
    form = JobEditForm(request.POST or None, instance=stage)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # for save tags
        # form.save_m2m()
        messages.success(request, 'Your Stage Post Was Successfully Updated!')
        return redirect(reverse("stageapp:single-stage", kwargs={
            'id': instance.id
        }))
    context = {

        'form': form,
        'categories': categories
    }

    return render(request, 'stageapp/stage-edit.html', context)
