from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from rest_framework import viewsets
from django.shortcuts import render
from django.http import HttpResponse

from django.views import View, generic
from django.urls import reverse_lazy
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import redirect

from .models import Novel, Chapter, Author, Genre, Rating
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
        latest_novels = self.get_queryset().order_by('-last_updated')[:10]
        random_novels = self.get_queryset().order_by('?')[:10]  # Randomly select 5 novels
        
        trending_filter = Novel.objects.all()
        sorted_novels = sorted(trending_filter, key=lambda x: x.trending_score(), reverse=True) # but then that's expensive
        trending_novels = sorted_novels[:10]  # Get top 5 trending novels

        # Add genres with novel counts
        genres = (
            Genre.objects.annotate(novel_count=Count('novels'))
            .order_by('-novel_count', 'genre_name')
        )

        context['latest_novels'] = latest_novels
        context['random_novels'] = random_novels
        context['trending_novels'] = trending_novels
        context['placeholder_image'] = placeholder_image_url  # Placeholder image URL
        context['genres'] = genres  # Add genres to context
        # Example: get the cover image of the first novel, if any
        return context
        
class SignUpView(generic.CreateView):
    model = User
    template_name = 'registration/signup.html'
    form_class = UserCreationForm  # You can create a custom form for user registration
    success_url = reverse_lazy('login')  # Redirect to login page after successful signup

    def form_valid(self, form):
        # You can add additional logic here if needed, like sending a welcome email
        return super().form_valid(form)

class NovelListView(generic.ListView):
    template_name = 'onexweb/novel_list.html'
    context_object_name = 'novels'
    paginate_by = 18

    def get_queryset(self):
        queryset = Novel.objects.all()
        keywords = self.request.GET.get('keywords')
        if keywords:
            queryset = queryset.filter(name__icontains=keywords)
        author = self.request.GET.get('author')
        if author:
            queryset = queryset.filter(authors__author_name__icontains=author)

        genre_ids = self.request.GET.getlist('genres')
        if genre_ids:
            genre_ids = [int(gid) for gid in genre_ids if gid.isdigit()]
            queryset = queryset.filter(genres__pk__in=genre_ids).distinct()

        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        sort = self.request.GET.get('sort', 'latest')
        if sort == 'latest':
            queryset = queryset.order_by('-last_updated')
        elif sort == 'az':
            queryset = queryset.order_by('name')
        elif sort == 'random':
            queryset = queryset.order_by('?')
        elif sort == 'trending':
            # Trending: sort by trending_score (expensive, so fetch all and sort in Python)
            novels = list(queryset)
            novels.sort(key=lambda x: x.trending_score(), reverse=True)
            return novels
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', 'latest')
        context['placeholder_image'] = placeholder_image_url
        context['keywords'] = self.request.GET.get('keywords', '')
        # Add genres with novel counts for sidebar if needed
        context['genres'] = (
            Genre.objects.annotate(novel_count=Count('novels'))
            .order_by('-novel_count', 'genre_name')
        )
        return context
    
class AdvancedSearchView(generic.ListView):
    # This is a lazy way to implement advanced search as it submits to NovelListView
    model = Novel
    template_name = 'onexweb/advanced_search.html'
    context_object_name = 'novel'    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        return context

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

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'onexweb/author_detail.html'
    context_object_name = 'author'
    paginate_by = 18 # Number of novels per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Here you can add additional context if needed, like novels by the author
        context['novels'] = self.object.novels.all()
        sort = self.request.GET.get('sort', 'latest')
        context['sort'] = sort
        if sort == 'latest':
            context['novels'] = context['novels'].order_by('-last_updated')
        elif sort == 'az':
            context['novels'] = context['novels'].order_by('name')
        elif sort == 'random':
            context['novels'] = context['novels'].order_by('?')
        elif sort == 'trending':
            # Trending: sort by trending_score (expensive, so fetch all and sort in Python)
            novels = list(context['novels'])
            novels.sort(key=lambda x: x.trending_score(), reverse=True)
            context['novels'] = novels
        return context

class GenreDetailView(generic.DetailView):
    model = Genre
    template_name = 'onexweb/genre_detail.html'
    context_object_name = 'genre'
    paginate_by = 18  # Number of novels per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Here you can add additional context if needed, like novels in this genre
        context['novels'] = self.object.novels.all()
        sort = self.request.GET.get('sort', 'latest')
        context['sort'] = sort
        if sort == 'latest':
            context['novels'] = context['novels'].order_by('-last_updated')
        elif sort == 'az':
            context['novels'] = context['novels'].order_by('name')
        elif sort == 'random':
            context['novels'] = context['novels'].order_by('?')
        elif sort == 'trending':
            # Trending: sort by trending_score (expensive, so fetch all and sort in Python)
            novels = list(context['novels'])
            novels.sort(key=lambda x: x.trending_score(), reverse=True)
            context['novels'] = novels
        return context

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

# Can I make a Chapter viewset for a specific novel?
# Yes, you can create a Chapter viewset that filters chapters based on the novel they belong to.

# Note: The above views are basic examples. In a real application, you would typically use Django's class-based views or function-based views to handle requests and responses more effectively.
# You would also need to set up URL routing to connect these views to specific URLs in your application.
# Additionally, you might want to implement authentication and permissions for your API views.

class RatingView(View):
    @method_decorator(login_required, name='dispatch')
    def post(self, request, novel_id):
        novel = get_object_or_404(Novel, pk=novel_id)
        action = request.POST.get('action')
        stars = request.POST.get('stars')
        content = request.POST.get('content', '').strip()
        user = request.user

        user_rating = Rating.objects.filter(novel=novel, user=user).first()

        if action == 'add' and not user_rating:
            if stars:
                Rating.objects.create(
                    novel=novel,
                    user=user,
                    stars=int(stars),
                    content=content if content else None
                )
        elif action == 'edit' and user_rating:
            if stars:
                user_rating.stars = int(stars)
                user_rating.content = content if content else None
                user_rating.save()
        elif action == 'delete' and user_rating:
            user_rating.delete()

        return redirect('novel_rating', novel_id=novel.novel_id)

    def get(self, request, novel_id):
        novel = get_object_or_404(Novel, pk=novel_id)
        ratings = Rating.objects.filter(novel=novel).select_related('user').order_by('-created_at')
        user_rating = None
        if request.user.is_authenticated:
            user_rating = ratings.filter(user=request.user).first()
        context = {
            'novel': novel,
            'ratings': ratings,
            'user_rating': user_rating,
            'placeholder_image': placeholder_image_url,
        }
        return render(request, 'onexweb/rating.html', context)

# Something like the audit log of changes made to the novels, chapters, etc.
class RecentChangesView(generic.ListView):
    model = Chapter # Assuming you want to show recent changes in chapters
    template_name = 'onexweb/recent_changes.html'
    context_object_name = 'recent_changes'
    paginate_by = 20

    def get_queryset(self):
        queryset = Chapter.objects.order_by('-published_date')
        return queryset
    
    # This will be like a table of recent changes, showing the timestamp and the chapter title.
    # Example: <timestamp> - <chapter title> from Novel <novel title>

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
        

class RandomNovelView(View):
    def get(self, request):
        # Here you would typically query the database for a random novel and pass it to a template
        novel = Novel.objects.order_by('?').first()  # Get a random novel
        if novel:
            return redirect('novel_detail', pk=novel.pk)
        else:
            return HttpResponse("No novels available")

# API ViewSets for Author, Genre, and Novel
# This is legacy code, but it can be useful for building an API with Django REST Framework.
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