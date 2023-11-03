from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import gettext_lazy as _


class AuthorModel(models.Model):
    name = models.CharField(max_length=125, verbose_name=_('name'))
    avatar = models.ImageField(upload_to='authors', verbose_name=_('avatar'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')


class PostTagModel(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('title'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


class PostModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    image = models.ImageField(upload_to='posts', verbose_name=_('image'))
    banner = models.ImageField(upload_to='banners', verbose_name=_('banner'))
    content = RichTextUploadingField(verbose_name=_('content'))
    author = models.ForeignKey(
        AuthorModel,
        on_delete=models.PROTECT,
        related_name='posts',
        verbose_name=_('author')
    )
    tags = models.ManyToManyField(
        PostTagModel,
        related_name='posts',
        verbose_name=_('tags')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def get_comments(self):
        return self.comments.order_by('-created_at')

    def get_prev(self):
        return self.get_previous_by_created_at()

    def get_next(self):
        return self.get_next_by_created_at()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')


class CommentModel(models.Model):
    post = models.ForeignKey(
        PostModel,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('post')
    )
    name = models.CharField(max_length=30, verbose_name=_('name'))
    email = models.EmailField(verbose_name=_('email'))
    phone_number = models.CharField(max_length=15, null=True, blank=True, verbose_name=_('phone_number'))
    comment = models.TextField(verbose_name=_('comment'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
