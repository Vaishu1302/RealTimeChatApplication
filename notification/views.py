from django.shortcuts import render


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Notification


@login_required
def notification_list(request):

    notification = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    notification.update(
        is_read=True
    )

    return render(
        request,
        'notification/list.html',
        {
            'notification': notification
        }
    )
