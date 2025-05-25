from django.contrib.auth.models import User
from rest_framework import viewsets
from django.shortcuts import render
from django.http import HttpResponse

from django.views import View, generic

from .models import Novel, Chapter, Author, Genre
from django.db import models
from onexweb.serializers import AuthorSerializer, GenreSerializer, NovelSerializer

from rest_framework.viewsets import ReadOnlyModelViewSet
from django.shortcuts import get_object_or_404

placeholder_image_url = 'https://placehold.co/150x200'

# Create your views here.
class IndexView(generic.ListView):
    model = Novel
    template_name = 'onexweb/index.html'
    context_object_name = 'latest_novels'

    # Novel has a method called get_cover_url() that returns the URL of the cover image.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_novels = self.get_queryset().order_by('-last_updated')[:5]
        context['latest_novels'] = latest_novels
        context['placeholder_image'] = placeholder_image_url  # Placeholder image URL
        # Example: get the cover image of the first novel, if any
        return context
        

class NovelListView(generic.ListView):
    template_name = 'onexweb/novel_list.html'
    context_object_name = 'novels'

    def get_queryset(self):
        # Here you would typically query the database for novels based on search criteria
        return Novel.objects.all()  # You can add filtering logic here based on request parameters
    
class NovelDetailView(generic.DetailView):
    model = Novel
    template_name = 'onexweb/novel_detail.html'
    context_object_name = 'novel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Here you can add additional context if needed, like chapters of the novel
        context['placeholder_image'] = placeholder_image_url  # Placeholder image URL
        context['chapters'] = self.object.chapter_set.order_by('published_date')[:5]
        context['authors'] = self.object.authors.all()
        context['genres'] = self.object.genres.all()
        context['chapters'] = self.object.chapter_set.all()
        # You can also add any other related objects or data you want to display
        context['ratings'] = self.object.star_rating()
        return context

class AuthorListView(View):
    def get(self, request):
        # Here you would typically query the database for authors and pass them to a template
        return HttpResponse("List of Authors")
        # Example: authors = Author.objects.all()
        # return render(request, 'author_list.html', {'authors': authors})

class AuthorDetailView(View):
    def get(self, request, author_id):
        # Here you would typically query the database for a specific author and pass it to a template
        return HttpResponse(f"Details of Author {author_id}")
        # Example: author = Author.objects.get(author_id=author_id)
        # return render(request, 'author_detail.html', {'author': author})

class GenreListView(View):
    def get(self, request):
        # Here you would typically query the database for genres and pass them to a template
        return HttpResponse("List of Genres")
        # Example: genres = Genre.objects.all()
        # return render(request, 'genre_list.html', {'genres': genres})

class GenreDetailView(View):
    def get(self, request, genre_id):
        # Here you would typically query the database for a specific genre and pass it to a template
        return HttpResponse(f"Details of Genre {genre_id}")
        # Example: genre = Genre.objects.get(genre_id=genre_id)
        # return render(request, 'genre_detail.html', {'genre': genre})

class ChapterListView(View):
    def get(self, request, novel_id):
        # Here you would typically query the database for chapters of a specific novel and pass them to a template
        return HttpResponse(f"List of Chapters for Novel {novel_id}")
        # Example: chapters = Chapter.objects.filter(novel_id=novel_id)
        # return render(request, 'chapter_list.html', {'chapters': chapters})

class ChapterDetailView(generic.DetailView):
    model = Chapter
    template_name = 'onexweb/chapter_detail.html'
    context_object_name = 'chapter'

    def get_object(self, queryset=None):
        novel_id = self.kwargs.get('novel_id')
        chapter_id = self.kwargs.get('chapter_id')
        # Ensure the chapter belongs to the given novel, or 404
        return get_object_or_404(Chapter, pk=chapter_id, novel_id=novel_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Here you can add additional context if needed, like the novel this chapter belongs to
        context['novel'] = self.object.novel
        return context


class AuthorViewSet(ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    # You can add pagination, filtering, and other configurations here if needed

class GenreViewSet(ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # You can add pagination, filtering, and other configurations here if needed

class NovelViewSet(ReadOnlyModelViewSet):
    queryset = Novel.objects.all()
    serializer_class = NovelSerializer
    # You can add pagination, filtering, and other configurations here if needed

# Can I make a Chapter viewset for a specific novel?
# Yes, you can create a Chapter viewset that filters chapters based on the novel they belong to.


# Note: The above views are basic examples. In a real application, you would typically use Django's class-based views or function-based views to handle requests and responses more effectively.
# You would also need to set up URL routing to connect these views to specific URLs in your application.
# Additionally, you might want to implement authentication and permissions for your API views.