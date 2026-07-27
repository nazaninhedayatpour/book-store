from django .urls import path
from .views import HomeView, BookListView, BookDetailView, add_to_favorites,my_favorites,add_to_cart,cart_detail
from .views import remove_from_cart,remove_from_favorites,increase_cart_item,decrease_cart_item,add_review
from .views import edit_review, delete_review
urlpatterns=[
    path("", HomeView.as_view() , name="home"),
    path("books/",BookListView.as_view(), name="book_list"),
    path("books/<int:pk>/",BookDetailView.as_view(), name="book_detail"),
    path("books/<int:pk>/favorite/",add_to_favorites,name="add_to_favorite"),
    path("favorites/",my_favorites, name="my_favorites"),
    path("cart/add/<int:book_id>/",add_to_cart,name="add_to_cart"),
    path("cart/",cart_detail,name="cart_detail"),
    path("cart/remove/<int:item_id>/",remove_from_cart,name="remove_from_cart"),
    path("favorites/remove/<int:pk>/",remove_from_favorites,name="remove_from_favorites"),
    path(
    "cart/increase/<int:item_id>/",increase_cart_item,name="increase_cart_item"),
    path("cart/decrease/<int:item_id>/",decrease_cart_item,name="decrease_cart_item"),
    path("book/<int:book_id>/review/",add_review,name="add_review"),
    path(
    "review/<int:review_id>/edit/",edit_review,name="edit_review"),
     path("review/<int:review_id>/delete/",delete_review,name="delete_review"),
    
]