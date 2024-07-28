from django.urls import path
from .views import BorrowBookView, ReturnBookView, BorrowRecordListView
app_name = "bookstore_api"
urlpatterns = [
    path('borrow/', BorrowBookView.as_view(), name='borrow_book'),
    path('return/', ReturnBookView.as_view(), name='return_book'),
    path('records/', BorrowRecordListView.as_view(), name='borrow_records'),
]

