from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Notification

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

def mark_notification_read(request, pk):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        messages.success(request, 'Notification marked as read.')
    return redirect('notifications:notification_list')
