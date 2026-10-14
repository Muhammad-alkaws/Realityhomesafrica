from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Property, PropertyImage, Inspection, Favorite
from .forms import PropertyForm, InspectionRequestForm
from .filters import PropertyFilter


def homepage(request):
    """SaaS homepage: hero + stats + live listings + tradesmen + services."""
    from services.models import TradesmanProfile
    from users.models import CustomUser

    featured_properties = Property.objects.filter(is_available=True).order_by('-created_at')[:6]
    recent_properties   = Property.objects.filter(is_available=True).order_by('-created_at')[:12]
    tradesmen           = TradesmanProfile.objects.filter(is_verified=True).select_related('user')[:6]

    # Platform stats
    total_properties  = Property.objects.filter(is_available=True).count()
    total_agents      = CustomUser.objects.filter(is_agent=True).count()
    total_tradesmen   = TradesmanProfile.objects.count()
    total_clients     = CustomUser.objects.filter(is_client=True).count()

    # City breakdown for stats
    from django.db.models import Count
    cities = (Property.objects
              .filter(is_available=True)
              .values('city')
              .annotate(count=Count('id'))
              .order_by('-count')[:4])

    return render(request, 'listings/homepage.html', {
        'featured_properties': featured_properties,
        'recent_properties': recent_properties,
        'tradesmen': tradesmen,
        'total_properties': total_properties,
        'total_agents': total_agents,
        'total_tradesmen': total_tradesmen,
        'total_clients': total_clients,
        'cities': cities,
    })


def property_list(request):
    """Full browse page with search filters."""
    queryset = Property.objects.filter(is_available=True)
    f = PropertyFilter(request.GET, queryset=queryset)
    return render(request, 'listings/property_list.html', {
        'filter': f,
        'properties': f.qs,
        'count': f.qs.count(),
    })


def property_detail(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    inspection_form = InspectionRequestForm()
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, property=prop).exists()
    return render(request, 'listings/property_detail.html', {
        'property': prop,
        'inspection_form': inspection_form,
        'is_favorited': is_favorited,
        'images': prop.images.all(),
    })


@login_required
def agent_dashboard(request):
    if not request.user.is_agent:
        raise PermissionDenied
    my_properties = Property.objects.filter(agent=request.user)
    pending_inspections = Inspection.objects.filter(agent=request.user, status='pending').count()
    return render(request, 'listings/agent_dashboard.html', {
        'properties': my_properties,
        'pending_inspections': pending_inspections,
    })


@login_required
def property_create(request):
    if not request.user.is_agent:
        raise PermissionDenied
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.agent = request.user
            prop.save()
            files = request.FILES.getlist('images')
            for i, f in enumerate(files):
                PropertyImage.objects.create(property=prop, image=f, is_primary=(i == 0))
            primary = request.FILES.get('primary_image')
            if primary:
                PropertyImage.objects.create(property=prop, image=primary, is_primary=True)
            messages.success(request, "Property listed successfully!")
            return redirect('listings:agent_dashboard')
    else:
        form = PropertyForm()
    return render(request, 'listings/property_form.html', {'form': form, 'action': 'Create'})


@login_required
def property_update(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if prop.agent != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=prop)
        if form.is_valid():
            form.save()
            files = request.FILES.getlist('images')
            for f in files:
                PropertyImage.objects.create(property=prop, image=f, is_primary=False)
            messages.success(request, "Property updated!")
            return redirect('listings:agent_dashboard')
    else:
        form = PropertyForm(instance=prop)
    return render(request, 'listings/property_form.html', {'form': form, 'action': 'Update', 'property': prop})


@login_required
def property_delete(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if prop.agent != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        prop.delete()
        messages.success(request, "Property deleted.")
        return redirect('listings:agent_dashboard')
    return render(request, 'listings/property_confirm_delete.html', {'property': prop})


@login_required
@require_POST
def request_inspection(request, pk):
    if not request.user.is_client:
        return JsonResponse({'success': False, 'error': 'Only clients can book inspections.'}, status=403)
    prop = get_object_or_404(Property, pk=pk)
    form = InspectionRequestForm(request.POST)
    if form.is_valid():
        inspection = form.save(commit=False)
        inspection.property = prop
        inspection.client = request.user
        inspection.agent = prop.agent
        inspection.save()
        return JsonResponse({'success': True, 'message': 'Inspection request sent!'})
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@login_required
def agent_inspections(request):
    if not request.user.is_agent:
        raise PermissionDenied
    inspections = Inspection.objects.filter(agent=request.user).order_by('status', '-created_at')
    return render(request, 'listings/agent_inspections.html', {'inspections': inspections})


@login_required
@require_POST
def confirm_inspection(request, pk):
    if not request.user.is_agent:
        raise PermissionDenied
    inspection = get_object_or_404(Inspection, pk=pk, agent=request.user)
    inspection.status = 'confirmed'
    inspection.save()
    messages.success(request, "Inspection confirmed.")
    return redirect('listings:agent_inspections')


@login_required
@require_POST
def cancel_inspection(request, pk):
    inspection = get_object_or_404(Inspection, pk=pk)
    if inspection.agent != request.user and inspection.client != request.user:
        raise PermissionDenied
    inspection.status = 'cancelled'
    inspection.save()
    messages.success(request, "Inspection cancelled.")
    return redirect('listings:agent_inspections' if request.user.is_agent else 'listings:client_inspections')


@login_required
def client_inspections(request):
    inspections = Inspection.objects.filter(client=request.user).order_by('-created_at')
    return render(request, 'listings/client_inspections.html', {'inspections': inspections})


@login_required
@require_POST
def toggle_favorite(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, property=prop)
    if not created:
        fav.delete()
        favorited = False
    else:
        favorited = True
    count = prop.favorited_by.count()
    return JsonResponse({'favorited': favorited, 'count': count})


@login_required
def favorites_list(request):
    favs = Favorite.objects.filter(user=request.user).select_related('property')
    return render(request, 'listings/favorites.html', {'favorites': favs})


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
