from django import forms


class CommentForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Leave a comment!"
            })
    )


# class FileFieldForm(forms.Form):
#     file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
#

class UploadFieldForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


# class DocumentForm(forms.Form):
#     docfile = forms.FileField(
#         label='Select a file',
#         help_text='max. 42 megabytes'
#     )

