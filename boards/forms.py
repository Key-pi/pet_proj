from django import forms

from .models import Board, Post, Topic, Image  # , Photo


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
    file_field = forms.FileField(widget=forms.FileInput(attrs={'multiple': True,
                                                               'onchange': 'readURL(this);',
                                                               'accept': ".jpg, .jpeg, .png",
                                                               }), required=False)

    class Meta:
        model = Topic
        exclude = ('views', 'board', 'starter')



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ('name', 'description')


class PhotoForm(forms.ModelForm):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    # file_field = forms.FileField(required=False, widget=forms.FileInput(attrs={
    #     'multiple': True,
    #     'class': 'js-upload-photos',
    #     'id': 'fileupload',
    # }))

    class Meta:
        model = Image
        fields = ('file_field', )


# class GalleryImagesForm(forms.ModelForm):
#     class Meta:
#         model = GalleryImages
#         fields = ('file', )


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
