from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import GroupFile

from .models import (
    Message,
    ChatGroup,
    GroupMessage,
    GroupFile
)

from .forms import GroupForm

from file_share.models import SharedFile
from notification.models import Notification


@login_required
def user_list(request):

    users = User.objects.exclude(
        id=request.user.id
    )

    return render(
        request,
        'chat/user_list.html',
        {
            'users': users
        }
    )


@login_required
def private_chat(request, user_id):

    receiver = get_object_or_404(
        User,
        id=user_id
    )

    Message.objects.filter(
        sender=receiver,
        receiver=request.user,
        is_read=False
    ).update(
        is_read=True
    )

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) |
        Q(sender=receiver, receiver=request.user)
    ).order_by('timestamp')

    files = SharedFile.objects.filter(
        Q(sender=request.user, receiver=receiver) |
        Q(sender=receiver, receiver=request.user)
    ).order_by('-uploaded_at')

    if request.method == 'POST':

        msg = request.POST.get('message')

        if msg:

            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                message=msg
            )

            Notification.objects.create(
                user=receiver,
                message=f"{request.user.username} sent you a message"
            )

        if request.FILES.get('file'):

            SharedFile.objects.create(
                sender=request.user,
                receiver=receiver,
                file=request.FILES['file']
            )

            Notification.objects.create(
                user=receiver,
                message=f"{request.user.username} shared a file with you"
            )

        return redirect(
            'private_chat',
            user_id=receiver.id
        )

    return render(
        request,
        'chat/private_chat.html',
        {
            'receiver': receiver,
            'messages': messages,
            'files': files
        }
    )


@login_required
def room(request, room_name):

    return render(
        request,
        'chat/room.html',
        {
            'room_name': room_name
        }
    )


@login_required
def create_group(request):

    if request.method == 'POST':

        form = GroupForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            group = form.save(commit=False)

            group.admin = request.user

            group.save()

            form.save_m2m()

            group.members.add(request.user)

            for member in group.members.all():

                if member != request.user:

                    Notification.objects.create(
                        user=member,
                        message=f"You were added to group '{group.name}'"
                    )

            return redirect(
                'group_list'
            )

    else:

        form = GroupForm()

    return render(
        request,
        'chat/create_group.html',
        {
            'form': form
        }
    )


@login_required
def group_list(request):

    groups = ChatGroup.objects.filter(
        members=request.user
    )

    return render(
        request,
        'chat/group_list.html',
        {
            'groups': groups
        }
    )


@login_required
def group_chat(request, group_id):

    group = get_object_or_404(
        ChatGroup,
        id=group_id
    )

    messages = GroupMessage.objects.filter(
        group=group
    ).order_by(
        'timestamp'
    )

    files = GroupFile.objects.filter(
        group=group
    ).order_by(
        '-uploaded_at'
    )

    if request.method == 'POST':

        msg = request.POST.get(
            'message'
        )

        if msg:

            GroupMessage.objects.create(
                group=group,
                sender=request.user,
                message=msg
            )

        if request.FILES.get('file'):

            GroupFile.objects.create(
                group=group,
                sender=request.user,
                file=request.FILES['file']
            )

        for member in group.members.all():

            if member != request.user:

                Notification.objects.create(
                    user=member,
                    message=f"{request.user.username} sent a message in {group.name}"
                )

        return redirect(
            'group_chat',
            group.id
        )

    return render(
        request,
        'chat/group_chat.html',
        {
            'group': group,
            'messages': messages,
            'files': files
        }
    )


@login_required
def add_member(request, group_id):

    group = get_object_or_404(
        ChatGroup,
        id=group_id
    )

    if request.user != group.admin:

        return redirect(
            'group_chat',
            group.id
        )

    available_users = User.objects.exclude(
        id__in=group.members.all()
    )

    if request.method == 'POST':

        user_id = request.POST.get('user')

        if user_id:

            user = User.objects.get(
                id=user_id
            )

            group.members.add(user)

            Notification.objects.create(
                user=user,
                message=f"You were added to group '{group.name}'"
            )

            return redirect(
                'group_chat',
                group.id
            )

    return render(
        request,
        'chat/add_member.html',
        {
            'group': group,
            'users': available_users
        }
    )


@login_required
def remove_member(
    request,
    group_id,
    user_id
):

    group = get_object_or_404(
        ChatGroup,
        id=group_id
    )

    if request.user != group.admin:

        return redirect(
            'group_chat',
            group.id
        )

    user = get_object_or_404(
        User,
        id=user_id
    )

    if user != group.admin:

        group.members.remove(user)

        Notification.objects.create(
            user=user,
            message=f"You were removed from group '{group.name}'"
        )

    return redirect(
        'group_chat',
        group.id
    )


@login_required
def edit_group(
    request,
    group_id
):

    group = get_object_or_404(
        ChatGroup,
        id=group_id
    )

    if request.user != group.admin:

        return redirect(
            'group_chat',
            group.id
        )

    if request.method == 'POST':

        group.name = request.POST.get(
            'group_name'
        )

        if request.FILES.get(
            'group_photo'
        ):

            group.group_photo = request.FILES[
                'group_photo'
            ]

        group.save()

        return redirect(
            'group_chat',
            group.id
        )

    return render(
        request,
        'chat/edit_group.html',
        {
            'group': group
        }
    )


@login_required
def delete_group(
    request,
    group_id
):

    group = get_object_or_404(
        ChatGroup,
        id=group_id
    )

    if request.user != group.admin:

        return redirect(
            'group_chat',
            group.id
        )

    if request.method == 'POST':

        for member in group.members.all():

            if member != request.user:

                Notification.objects.create(
                    user=member,
                    message=f"Group '{group.name}' has been deleted"
                )

        group.delete()

        return redirect(
            'group_list'
        )

    return render(
        request,
        'chat/delete_group.html',
        {
            'group': group
        }

    )


@login_required
def group_info(
    request,
    group_id
):

    group = get_object_or_404(
        ChatGroup,
        id=group_id
    )

    return render(
        request,
        'chat/group_info.html',
        {
            'group': group
        }

    )


@login_required
def delete_message(request, message_id):

    message = get_object_or_404(
        GroupMessage,
        id=message_id
    )

    if message.sender == request.user:

        message.is_deleted = True

        message.save()

    return redirect(
        'group_chat',
        group_id=message.group.id
    )


@login_required
def delete_group_file(request, file_id):

    file = get_object_or_404(
        GroupFile,
        id=file_id
    )

    # Only uploader or group admin can delete
    if (
        file.sender == request.user
        or
        file.group.admin == request.user
    ):

        group_id = file.group.id

        file.delete()

        return redirect(
            'group_chat',
            group_id=group_id
        )

    return redirect(
        'group_chat',
        group_id=file.group.id
    )


@login_required
def delete_private_file(request, file_id):

    file = get_object_or_404(
        SharedFile,
        id=file_id
    )

    if (
        file.sender == request.user
        or file.receiver == request.user
    ):

        receiver_id = (
            file.receiver.id
            if file.sender == request.user
            else file.sender.id
        )

        file.delete()

        return redirect(
            'private_chat',
            user_id=receiver_id
        )

    return redirect('user_list')
