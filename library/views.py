from django.shortcuts import render
from django.views.generic import TemplateView, ListView,DetailView
from .models import Author,Book,Category
from django.db.models import Q ,Avg, Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Book, Favorite, Cart , CartItem , Review
from .forms import ReviewForm, BookForm
from django.contrib.admin.views.decorators import staff_member_required

class HomeView(TemplateView):
    template_name="books/home.html"

class BookListView(ListView):
    model=Book
    template_name="books/book_list.html"
    context_object_name="books"
    paginate_by=3

    def get_queryset(self):
        books = Book.objects.filter(is_active=True)

        query = self.request.GET.get("q")
        category = self.request.GET.get("category")
        sort = self.request.GET.get("sort")

        # Search
        if query:
            books = books.filter(
                Q(title__icontains=query) |
                Q(author__name__icontains=query)
            )

        # Filter
        if category:
            books = books.filter(
                category__name__icontains=category
            )

        # Sort
        if sort == "price_asc":
            books = books.order_by("price")

        elif sort == "price_desc":
            books = books.order_by("-price")

        elif sort == "title_asc":
            books = books.order_by("title")

        elif sort == "title_desc":
            books = books.order_by("-title")

        return books
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.all()

        return context

     
class BookDetailView(DetailView):
    model=Book
    template_name="books/book_detail.html"
    context_object_name="book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

         # Get all reviews
        context["reviews"] = self.object.reviews.all()

            # Calculate average rating
        context["average_rating"] = self.object.reviews.aggregate(
            Avg("rating")
        )["rating__avg"]

        # Count reviews
        context["review_count"] = self.object.reviews.count()

        return context


@login_required
def add_to_favorites(request, pk):

    book = get_object_or_404(Book, pk=pk)

    Favorite.objects.get_or_create(
        user=request.user,
        book=book
    )

    return redirect("book_detail", pk=book.pk)

@login_required
def my_favorites(request):

    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related("book")

    return render(
        request,
        "books/my_favorites.html",
        {"favorites": favorites}
    )

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(
        Book,
        id=book_id,
        is_active=True
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart_detail")

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        "books/cart_detail.html",
        {
            "cart": cart,
        }
    )

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    cart_item.delete()

    return redirect("cart_detail")

@login_required
def remove_from_favorites(request, pk):
    favorite = get_object_or_404(
        Favorite,
        pk=pk,
        user=request.user
    )

    favorite.delete()

    return redirect("my_favorites")

@login_required
def increase_cart_item(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        pk=item_id,
        cart__user=request.user
    )

    if cart_item.quantity < cart_item.book.stock:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart_detail")

@login_required
def decrease_cart_item(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        pk=item_id,
        cart__user=request.user
    )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect("cart_detail")

@login_required
def add_review(request, book_id):

    book = get_object_or_404(
        Book,
        pk=book_id
    )

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.user = request.user
            review.book = book

            review.save()

            return redirect(
                "book_detail",
                pk=book.pk
            )

    else:

        form = ReviewForm()

    return render(
        request,
        "books/add_review.html",
        {
            "form": form,
            "book": book,
        }
    )

@login_required
def edit_review(request, review_id):

    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user
    )

    if request.method == "POST":

        form = ReviewForm(
            request.POST,
            instance=review
        )

        if form.is_valid():

            form.save()

            return redirect(
                "book_detail",
                pk=review.book.pk
            )

    else:

        form = ReviewForm(
            instance=review
        )

    return render(
        request,
        "books/edit_review.html",
        {
            "form": form,
            "review": review,
        }
    )


@login_required
def delete_review(request, review_id):

    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user
    )

    book_id = review.book.pk

    if request.method == "POST":

        review.delete()

        return redirect(
            "book_detail",
            pk=book_id
        )

    return render(
        request,
        "books/delete_review.html",
        {
            "review": review,
        }
    )


@staff_member_required
def create_book(request):

    if request.method == "POST":

        form = BookForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect("book_list")

    else:

        form = BookForm()

    return render(
        request,
        "books/create_book.html",
        {
            "form": form,
        }
    )

@staff_member_required
def update_book(request, pk):

    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":

        form = BookForm(
            request.POST,
            request.FILES,
            instance=book
        )

        if form.is_valid():

            form.save()

            return redirect("book_list")

    else:

        form = BookForm(instance=book)

    return render(
        request,
        "books/update_book.html",
        {
            "form": form,
            "book": book,
        }
    )

@staff_member_required
def delete_book(request, pk):

    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":

        book.delete()

        return redirect("book_list")

    return render(
        request,
        "books/delete_book.html",
        {
            "book": book,
        }
    )