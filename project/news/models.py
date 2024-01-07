from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    content_creator = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_content = models.SmallIntegerField(default=0)

    def update_rating(self):
        posts_rating = 0
        comment_rating = 0
        posts_comment_rating = 0
        posts = Post.objects.filter(creator=self)
        print(type(posts))
        for p in posts:
            posts_rating += p.rating
        comments = Comment.objects.filter(comment_to_user=self.content_creator)
        for c in comments:
            comment_rating += c.comment_rating
        posts_comment = Comment.objects.filter(comment_to_post__creator=self)
        for pc in posts_comment:
            posts_comment_rating += pc.comment_rating
        self.rating_content = posts_rating * 3 + comment_rating + posts_comment_rating
        self.save()

    def __str__(self):
        return f'{self.content_creator}, {self.rating_content}'


class Category(models.Model):
    type_name = models.CharField(max_length=128, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories', blank=True)

    def __str__(self):
        return f'{self.type_name}'


class Post(models.Model):
    news = 'новость'
    article = 'статья'
    CATEGORY = [(news, 'новость'), (article, 'статья')]
    creator = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_choice = models.CharField(max_length=7, choices=CATEGORY, default=news)
    creation_time = models.DateTimeField(auto_now=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    content_text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content_text[0:124] + '...'

    def __str__(self):
        return f'{self.title}, {self.preview()}, {self.post_category}'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post_to_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    post_to_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post_to_post}, из категории: {self.post_to_category}'


class Comment(models.Model):
    comment_to_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now=True)
    comment_rating = models.SmallIntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return f'{self.comment_time}, {self.comment_text}'
