from django.db import models
from django .contrib.auth.models import User
from django.conf import settings

class Author(models.Model):
    name=models.CharField(max_length=150)
    country=models.CharField(max_length=100)
    birth_year=models.PositiveIntegerField()
    bio=models.TextField(blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name=models.CharField(
        max_length=100,
        unique=True
        )
    description=models.TextField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title=models.CharField(max_length=150)
    author=models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books"
    )
    pages=models.PositiveIntegerField()
    price=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    stock=models.PositiveIntegerField(default=0)
    publication_year=models.PositiveIntegerField()
    is_active=models.BooleanField(default=True)
    category=models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books"
    )
    description=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    cover=models.ImageField(
        null=True,
        upload_to="books/cover/",
        blank=True
    )
    def __str__(self):
        return self.title

class BookImage(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="books/images/"
    )

class Favorite(models.Model):
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    book=models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="favorited_by"
    )
    created_at = models.DateTimeField(
        auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "book"],
                name="unique_user_book_favorite")]

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart - {self.user.username}"

    @property
    def total_price(self):
        return sum(
            item.subtotal
            for item in self.items.all()
        )


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "book"],
                name="unique_cart_book"
            )
        ]

    @property
    def subtotal(self):
        return self.book.price * self.quantity

    def __str__(self):
        return f"{self.book.title} - {self.quantity}"

class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveIntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "book"],
                name="unique_user_book_review"
            )
        ]

        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.rating}"