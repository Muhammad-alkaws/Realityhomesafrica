def unread_messages_count(request):
    """Inject unread message count into every template context."""
    if request.user.is_authenticated:
        from .models import Message
        count = Message.objects.filter(receiver=request.user, is_read=False).count()
        return {'unread_count': count}
    return {'unread_count': 0}
