from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("accounts/", include("django.contrib.auth.urls")),  # new
    path("accounts/signup/", views.SignUpView.as_view(), name="signup"),
    path("novel/<int:pk>/", views.NovelDetailView.as_view(), name="novel_detail"),
    path("search/", views.NovelListView.as_view(), name="novel_list"),
    path("authors/<int:pk>/", views.AuthorDetailView.as_view(), name="author_detail"),
    path("genres/<int:pk>/", views.GenreDetailView.as_view(), name="genre_detail"),
    path("novel/<int:novel_id>/chapters/<int:chapter_id>/", views.ChapterDetailView.as_view(), name="chapter_detail"),
    path("novel/<int:novel_id>/rating/", views.RatingView.as_view(), name="novel_rating"),
    path("recent_changes/", views.RecentChangesView.as_view(), name="recent_changes"),
    path("random_novel/", views.RandomNovelView.as_view(), name="random_novel"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
