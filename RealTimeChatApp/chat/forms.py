from django import forms
from .models import ChatGroup


# class GroupForm(forms.ModelForm):

#     class Meta:

#         model = ChatGroup

#         fields = [
#             'name',
#             'members'
#         ]

#         widgets = {
#             'members': forms.CheckboxSelectMultiple()
#         }
# class GroupForm(forms.ModelForm):

#     class Meta:
#         model = ChatGroup
#         fields = ['name', 'members']

#         widgets = {
#             'name': forms.TextInput(
#                 attrs={
#                     'class': 'form-control',
#                     'placeholder': 'Enter Group Name'
#                 }
#             ),

#             'members': forms.CheckboxSelectMultiple()
#         }


from django import forms
from .models import ChatGroup


class GroupForm(forms.ModelForm):

    class Meta:
        model = ChatGroup

        fields = [
            'name',
            'group_photo',
            'members'
        ]
