from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from .forms import ChapterAdminForm

# Register your models here.
from .models import Author, Genre, Novel, Chapter, Rating

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_id', 'author_name', 'description', 'image_tag')
    # How can I display the profile picture in the fieldsets?
    # Answer: You can use the image_tag method in the list_display to show the profile picture. Since you already have it in the list_display, it will show up in the admin interface.

    search_fields = ('author_name',)
    list_filter = ('author_name',)
    ordering = ('author_id',)
    list_per_page = 10
    list_editable = ('description',)
    fieldsets = (
        (None, {
            'fields': ('author_name', 'description')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('profile_picture',),
        }),
    )
    prepopulated_fields = {'description': ('author_name',)}
    
    def has_add_permission(self, request):
        return True
    def has_change_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    def has_view_permission(self, request, obj=None):
        return True
    
class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre_id', 'genre_name', 'genre_description')
    search_fields = ('genre_name',)
    list_filter = ('genre_name',)
    ordering = ('genre_id',)
    list_per_page = 10
    list_editable = ('genre_description',)
    fieldsets = (
        (None, {
            'fields': ('genre_name', 'genre_description')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (),
        }),
    )
    prepopulated_fields = {'genre_description': ('genre_name',)}
    def has_add_permission(self, request):
        return True
    def has_change_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    def has_view_permission(self, request, obj=None):
        return True
    
class NovelAdmin(admin.ModelAdmin):
    list_display = ('novel_id', 'name', 'status', 'last_updated', 'cover_tag')
    search_fields = ('name',)
    list_filter = ('status', 'authors', 'genres')
    ordering = ('novel_id',)
    list_per_page = 10
    list_editable = ('status',)
    fieldsets = (
        (None, {
            'fields': ('name', 'authors', 'genres', 'description')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('status', 'cover',), 
        }),
    )
    prepopulated_fields = {'description': ('name',)}
    def has_add_permission(self, request):
        return True
    def has_change_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    def has_view_permission(self, request, obj=None):
        return True
    
class ChapterAdmin(admin.ModelAdmin):
    form = ChapterAdminForm # Use the custom form for Chapter model

    list_display = ('novel', 'chapter_number', 'title', 'published_date')
    search_fields = ('title',)
    list_filter = ('novel',)
    ordering = ('novel', 'chapter_number')
    list_per_page = 10
    list_editable = ('title',)
    fieldsets = (
        (None, {
            'fields': ('novel', 'chapter_number', 'title', 'content')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('published_date',),
        }),
    )
    prepopulated_fields = {'content': ('title',)}
    def has_add_permission(self, request):
        return True
    def has_change_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    def has_view_permission(self, request, obj=None):
        return True
    
    class Media:
        js = ('admin/js/chapter_admin.js',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('next_chapter_number/', self.admin_site.admin_view(self.next_chapter_number))
        ]
        return custom_urls + urls

    def next_chapter_number(self, request):
        novel_id = request.GET.get('novel_id')
        if novel_id:
            last_chapter = Chapter.objects.filter(novel_id=novel_id).order_by('-chapter_number').first()
            next_number = (last_chapter.chapter_number + 1) if last_chapter else 1
            return JsonResponse({'next_chapter_number': next_number})
        return JsonResponse({'next_chapter_number': 1})

    
class RatingAdmin(admin.ModelAdmin):
    list_display = ('novel', 'user', 'stars', 'content', 'created_at')
    search_fields = ('user',)
    list_filter = ('novel',)
    ordering = ('novel', 'created_at')
    list_per_page = 10
    
    # can't edit, but can delete
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return True
    def has_view_permission(self, request, obj=None):
        return True
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Filter out ratings that are not related to the current user
        if request.user.is_authenticated:
            return qs.filter(user=request.user)
        return qs.none()
    
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('novel', 'author', 'created_at')
#     search_fields = ('author',)
#     list_filter = ('novel',)
#     ordering = ('novel', 'created_at')
#     list_per_page = 10
#     list_editable = ('author',)
#     fieldsets = (
#         (None, {
#             'fields': ('novel', 'author', 'content')
#         }),
#         ('Advanced options', {
#             'classes': ('collapse',),
#             'fields': ('created_at',),
#         }),
#     )
#     prepopulated_fields = {'content': ('author',)}
#     def has_add_permission(self, request):
#         return True
#     def has_change_permission(self, request, obj=None):
#         return True
#     def has_delete_permission(self, request, obj=None):
#         return True
#     def has_view_permission(self, request, obj=None):
#         return True

admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Novel, NovelAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Rating, RatingAdmin)