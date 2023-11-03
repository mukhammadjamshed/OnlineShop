from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

UserModel = get_user_model()


class CategoryModel(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class BrandModel(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')


class ProductTagModel(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Product Tag')
        verbose_name_plural = _('Product Tags')


class SizeModel(models.Model):
    title = models.CharField(max_length=3, verbose_name=_('title'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Size')
        verbose_name_plural = _('Sizes')


class ColorModel(models.Model):
    code = models.CharField(max_length=10, verbose_name=_('code'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('color')
        verbose_name_plural = _('colors')


class ProductModel(models.Model):
    title = models.CharField(max_length=250, verbose_name=_('title'))
    image = models.ImageField(upload_to='products', verbose_name=_('image'))
    price = models.FloatField(verbose_name=_('price'))
    real_price = models.FloatField(verbose_name=_('real price'), default=0)
    sizes = models.ManyToManyField(SizeModel, related_name='products')
    colors = models.ManyToManyField(ColorModel, related_name='products')
    wishlist = models.ManyToManyField(UserModel, related_name='wishlist')
    discount = models.PositiveIntegerField(
        default=0,
        validators=
        [
            MinValueValidator(0),
            MaxValueValidator(100)
        ], verbose_name=_('discount')
    )
    short_description = models.TextField(verbose_name=_('short_description'))
    long_description = RichTextUploadingField(verbose_name=_('long_description'))
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name=_('category')
    )
    brand = models.ForeignKey(
        BrandModel,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name=_('brand')
    )
    tags = models.ManyToManyField(
        ProductTagModel,
        related_name='products',
        verbose_name=_('tags')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.title

    @staticmethod
    def get_from_cart(request):
        cart = request.session.get('cart', [])
        return ProductModel.objects.filter(
            pk__in=cart
        )

    def is_discount(self):
        return self.discount != 0

    def is_new(self):
        difference = datetime.now(pytz.timezone('Asia/Tashkent')) - self.created_at
        return difference.days <= 3

    def get_related_products(self):
        # return self.category.products.exclude(pk=self.pk)
        return ProductModel.objects.filter(category_id=self.category_id).exclude(pk=self.pk)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class ProductImageModel(models.Model):
    product = models.ForeignKey(
        ProductModel,
        related_name='images',
        on_delete=models.CASCADE,
        verbose_name=_('product')
    )
    image = models.ImageField(upload_to='products', verbose_name=_('image'))

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')
