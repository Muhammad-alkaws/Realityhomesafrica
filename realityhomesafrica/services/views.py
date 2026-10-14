from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import TradesmanProfile, PortfolioItem, ServiceRequest
from .forms import TradesmanProfileForm, PortfolioItemForm, ServiceRequestForm


def tradesman_list(request):
    """Public: browse all verified tradesmen, filterable by trade and city."""
    tradesmen = TradesmanProfile.objects.select_related('user')
    trade = request.GET.get('trade', '')
    city = request.GET.get('city', '')
    if trade:
        tradesmen = tradesmen.filter(trade_category=trade)
    if city:
        tradesmen = tradesmen.filter(location_city__icontains=city)
    from .models import TRADE_CATEGORIES
    return render(request, 'services/tradesman_list.html', {
        'tradesmen': tradesmen,
        'trade_categories': TRADE_CATEGORIES,
        'selected_trade': trade,
        'selected_city': city,
    })


def tradesman_profile(request, pk):
    """Public: view a tradesman's full profile and portfolio."""
    profile = get_object_or_404(TradesmanProfile, pk=pk)
    portfolio = profile.portfolio.all()
    form = ServiceRequestForm() if request.user.is_authenticated and request.user.is_client else None
    return render(request, 'services/tradesman_profile.html', {
        'profile': profile,
        'portfolio': portfolio,
        'form': form,
    })


@login_required
def tradesman_dashboard(request):
    """Tradesman manages their profile, portfolio, and incoming requests."""
    if not request.user.is_tradesman:
        raise PermissionDenied
    profile, _ = TradesmanProfile.objects.get_or_create(
        user=request.user,
        defaults={'trade_category': 'other'}
    )
    if request.method == 'POST':
        form = TradesmanProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect('services:tradesman_dashboard')
    else:
        form = TradesmanProfileForm(instance=profile)
    portfolio = profile.portfolio.all()
    service_requests = profile.requests.order_by('-created_at')
    return render(request, 'services/tradesman_dashboard.html', {
        'form': form,
        'profile': profile,
        'portfolio': portfolio,
        'service_requests': service_requests,
    })


@login_required
def add_portfolio_item(request):
    if not request.user.is_tradesman:
        raise PermissionDenied
    profile = get_object_or_404(TradesmanProfile, user=request.user)
    if request.method == 'POST':
        form = PortfolioItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.tradesman = profile
            item.save()
            messages.success(request, "Portfolio item added!")
            return redirect('services:tradesman_dashboard')
    else:
        form = PortfolioItemForm()
    return render(request, 'services/portfolio_form.html', {'form': form})


@login_required
def request_service(request, tradesman_pk):
    """Client sends a service request to a tradesman."""
    if not request.user.is_client:
        raise PermissionDenied
    profile = get_object_or_404(TradesmanProfile, pk=tradesman_pk)
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            sr = form.save(commit=False)
            sr.client = request.user
            sr.tradesman = profile
            sr.save()
            messages.success(request, f"Request sent to {profile.user.username}!")
            return redirect('services:tradesman_profile', pk=tradesman_pk)
    else:
        form = ServiceRequestForm()
    return render(request, 'services/request_service.html', {'form': form, 'profile': profile})


@login_required
def tradesman_requests(request):
    """Tradesman sees all incoming service requests."""
    if not request.user.is_tradesman:
        raise PermissionDenied
    profile = get_object_or_404(TradesmanProfile, user=request.user)
    reqs = profile.requests.order_by('-created_at')
    return render(request, 'services/tradesman_requests.html', {'requests': reqs})
