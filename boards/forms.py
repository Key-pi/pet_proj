from django import forms

from .models import Board, Post, Topic, GalleryImages  # , Photo


# from django.core.files import File
# from PIL import Image


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ('name', 'description')


class GalleryImagesForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput)

    class Meta:
        model = GalleryImages
        fields = ('image', )


# class PhotoForm(forms.ModelForm):
#     x = forms.FileField(widget=forms.HiddenInput())
#     y = forms.FileField(widget=forms.HiddenInput())
#     width = forms.FileField(widget=forms.HiddenInput())
#     height = forms.FileField(widget=forms.HiddenInput())
#
#     class Meta:
#         model = Photo
#         fields = ('file', 'x', 'y', 'width', 'height', )
#
#     def save(self, commit=True):
#         photo = super(PhotoForm, self).save()
#
#         x = self.cleaned_data.get('x')
#         y = self.cleaned_data.get('y')
#         w = self.cleaned_data.get('width')
#         h = self.cleaned_data.get('height')
#
#         image = Image.open(photo.file)
#         cropped_image = image.crop((x, y, w+x, h+y))
#         resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
#         resized_image.save(photo.file.path)
#
#         return photo
