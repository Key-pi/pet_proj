from django.contrib import admin

from .models import Blogger, Board, Post, Reader, Topic

# from django.contrib.auth.admin import UserAdmin
# from .models import User


def make_boards_disable(modeladmin, request, queryset):
    for board in queryset:
        board.is_active = False
        board.save()


make_boards_disable.short_description = 'Make boards disable'


class BoardAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    actions = [make_boards_disable, ]


admin.site.register(Blogger)
admin.site.register(Reader)
admin.site.register(Board, BoardAdmin)
admin.site.register(Topic)
admin.site.register(Post)

# @admin.register
# class BloggerInline(admin.StackedInline):
#     model = Blogger
#     can_delete = False
#     fk_name = 'user'
#     verbose_name_plural = 'Blogger'
#
#
#
# class ReaderInline(admin.StackedInline):
#     model = Reader
#     can_delete = False
#     fk_name = 'user'
#     verbose_name_plural = 'Reader'
#
#
#
# class CustomUserAdmin(UserAdmin):
#     inlines = (BloggerInline,)
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
#     list_select_related = ('blogger', 'reader')
#
#
#
# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
