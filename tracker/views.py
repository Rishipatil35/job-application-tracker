from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import RegisterForm, ApplicationForm
from .models import JobApplication


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    base = JobApplication.objects.filter(user=request.user)
    applications = base
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')
    if query:
        applications = applications.filter(Q(company__icontains=query) | Q(role__icontains=query))
    if status in JobApplication.Status.values:
        applications = applications.filter(status=status)
    counts = {row['status']: row['total'] for row in base.values('status').annotate(total=Count('id'))}
    return render(request, 'tracker/dashboard.html', {
        'applications': applications, 'query': query, 'selected_status': status,
        'statuses': JobApplication.Status.choices, 'total': base.count(),
        'applied': counts.get('applied', 0), 'interviews': counts.get('interview', 0), 'offers': counts.get('offer', 0),
        'rejected': counts.get('rejected', 0)})

@login_required
def add_application(request):
    form = ApplicationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        application = form.save(commit=False)
        application.user = request.user
        application.save()
        return redirect('dashboard')
    return render(request, 'tracker/form.html', {'form': form, 'heading': 'Add Application'})

@login_required
def edit_application(request, pk):
    application = get_object_or_404(JobApplication, pk=pk, user=request.user)
    form = ApplicationForm(request.POST or None, instance=application)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'tracker/form.html', {'form': form, 'heading': 'Edit Application'})

@login_required
@require_POST
def delete_application(request, pk):
    application = get_object_or_404(JobApplication, pk=pk, user=request.user)
    application.delete()
    return redirect('dashboard')
