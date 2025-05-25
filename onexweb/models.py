import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.html import mark_safe

# Create your models here.

class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    author_name = models.CharField(max_length=255)
    description = models.TextField(default="The author has not disclosed any information about themselves.")
    profile_picture = models.ImageField(upload_to='author_pictures/', blank=True, null=True)

    def __str__(self):
        return self.author_name

    def image_tag(self):
        if self.profile_picture:
            return mark_safe('<img src="{}" width="50" height="50" />'.format(self.profile_picture.url))
        return ""
    image_tag.short_description = 'Profile Picture'

class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(max_length=100)
    genre_description = models.TextField()

    def __str__(self):
        return self.genre_name
    

class Novel(models.Model):
    novel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, blank=True, related_name='novels')
    genres = models.ManyToManyField(Genre, blank=True, related_name='novels')
    description = models.TextField()
    cover = models.ImageField(upload_to='novel_covers/', blank=True, null=True)

    status_choices = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('hiatus', 'Hiatus'),
        ('dropped', 'Dropped'),
    ]
    status = models.CharField(max_length=50, choices=status_choices, default='ongoing')
    
    last_updated = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def was_updated_recently(self):
        return self.last_updated >= timezone.now() - datetime.timedelta(days=1)
    
    was_updated_recently.admin_order_field = 'last_updated'

    def cover_tag(self):
        if self.cover:
            return mark_safe('<img src="{}" width="50" height="50" />'.format(self.cover.url))
        return ""
    
    cover_tag.short_description = 'Cover Image'

    def get_latest_chapter(self):
        return self.chapter_set.order_by('-published_date').first() if self.chapter_set.exists() else None
    
    def first_five_chapters(self):
        return self.chapter_set.order_by('chapter_number')[:5] if self.chapter_set.exists() else []

    def star_rating(self):
        ratings = self.rating_set.all()
        if not ratings:
            return 0
        total_stars = sum(rating.stars for rating in ratings)
        return total_stars / ratings.count() if ratings.count() > 0 else 0, ratings.count()
    
    def trending_score(self):
        # Calculate average rating
        ratings = self.rating_set.all()
        avg_rating = sum(r.stars for r in ratings) / ratings.count() if ratings.exists() else 0

        # Calculate recency weight
        days_since_update = (timezone.now() - self.last_updated).days
        recency_weight = 1 / (days_since_update + 1)  # +1 to avoid division by zero

        # Trending score
        return avg_rating * recency_weight

class Chapter(models.Model):
    chapter_id = models.AutoField(primary_key=True)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    chapter_number = models.IntegerField()
    title = models.CharField(max_length=255)
    published_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    def __str__(self):
        return f"{self.novel.name} - Chapter {self.chapter_number}"
    
    def previous_chapter(self):
        return self.novel.chapter_set.filter(chapter_number__lt=self.chapter_number).order_by('-chapter_number').first()
    
    def next_chapter(self):
        return self.novel.chapter_set.filter(chapter_number__gt=self.chapter_number).order_by('chapter_number').first()

@receiver(post_save, sender=Chapter)
def update_novel_last_updated(sender, instance, **kwargs):
    instance.novel.last_updated = instance.published_date
    instance.novel.save()

# Uncomment the following code if you want to implement comments on novels    
#class Comment(models.Model):
#    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
#    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Assuming you have a User model
#    content = models.TextField()
#    created_at = models.DateTimeField(auto_now_add=True)

#    # Can I 'reply' to a comment?
#    # Answer: Yes, you can create a self-referential foreign key to allow replies to comments.
#    
#    # parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')#

#    def __str__(self):
#        return f"Comment by {self.author} on {self.novel.name}"
    
class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Assuming you have a User model
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Assuming a rating scale of 1 to 5
    # should this be called rating or stars, or something else?
    # Answer: "Rating" is a common term, but "stars" is also widely used. You can choose based on your preference.
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # likes = models.ManyToManyField('auth.User', related_name='liked_ratings', blank=True)

    def __str__(self):
        return f"Rating by {self.user} on {self.novel.name}"
    
    #def count_likes(self):
    #    return self.likes.count()
    
# Give groups for Normal Users, Authors, and Admins
# Answer: This is typically done in Django's admin.py or using Django's built-in permissions system. You can create groups and assign permissions to them.
