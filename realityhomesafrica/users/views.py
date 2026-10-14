from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import ClientRegisterForm, AgentRegisterForm, TradesmanRegisterForm, MessageForm
from .models import CustomUser, Message


def choose_role(request):
    """Landing page: user picks their role before registering."""
    return render(request, 'users/choose_role.html')


def register_client(request):
    if request.method == 'POST':
        form = ClientRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your client account is ready.")
            return redirect('listings:homepage')
    else:
        form = ClientRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'role': 'Client'})


def register_agent(request):
    if request.method == 'POST':
        form = AgentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome Agent {user.username}! Start listing properties.")
            return redirect('listings:agent_dashboard')
    else:
        form = AgentRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'role': 'Agent'})


def register_tradesman(request):
    if request.method == 'POST':
        form = TradesmanRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Set up your tradesman profile.")
            return redirect('services:tradesman_dashboard')
    else:
        form = TradesmanRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'role': 'Tradesman'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('listings:homepage')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', 'listings:property_list')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('listings:homepage')


@login_required
def inbox(request):
    received = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'users/inbox.html', {'messages_list': received})


@login_required
def message_detail(request, pk):
    msg = get_object_or_404(Message, pk=pk, receiver=request.user)
    if not msg.is_read:
        msg.is_read = True
        msg.save()
    return render(request, 'users/message_detail.html', {'msg': msg})


@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(CustomUser, pk=receiver_id)
    property_ref_id = request.GET.get('property', None)
    property_ref = None
    if property_ref_id:
        from listings.models import Property
        property_ref = Property.objects.filter(pk=property_ref_id).first()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = receiver
            msg.property_ref = property_ref
            msg.save()
            messages.success(request, f"Message sent to {receiver.username}!")
            return redirect('users:inbox')
    else:
        form = MessageForm()
    return render(request, 'users/send_message.html', {
        'form': form,
        'receiver': receiver,
        'property_ref': property_ref,
    })
