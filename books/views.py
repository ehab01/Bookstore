from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book, BorrowRecord
from .serializers import BorrowRecordSerializer
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter , OpenApiResponse

class BorrowBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(name='book_id', description='ID of the book to borrow', required=True, type=int),
        ],
        responses={
            200: OpenApiResponse(description='Book borrowed successfully'),
            400: OpenApiResponse(description='Book not available')
        }
    )
    def post(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')
        try:
            book = Book.objects.get(id=book_id, is_available=True)
        except Book.DoesNotExist:
            return Response({'error': 'Book not available'}, status=status.HTTP_400_BAD_REQUEST)

        borrow_record = BorrowRecord.objects.create(book=book, borrower=request.user)
        book.is_available = False
        book.save()

        return Response({'message': 'Book borrowed successfully'}, status=status.HTTP_200_OK)


class ReturnBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(name='record_id', description='ID of the borrow record to return', required=True, type=int),
        ],
        responses={
            200: OpenApiResponse(description='Book returned successfully'),
            400: OpenApiResponse(description='Invalid borrow record')
        }
    )
    def post(self, request, *args, **kwargs):
        record_id = request.data.get('record_id')
        try:
            borrow_record = BorrowRecord.objects.get(id=record_id, borrower=request.user, return_date__isnull=True)
        except BorrowRecord.DoesNotExist:
            return Response({'error': 'Invalid borrow record'}, status=status.HTTP_400_BAD_REQUEST)

        borrow_record.return_date = timezone.now()
        borrow_record.book.is_available = True
        borrow_record.book.save()
        borrow_record.save()

        return Response({'message': 'Book returned successfully'}, status=status.HTTP_200_OK)


class BorrowRecordListView(generics.ListAPIView):
    serializer_class = BorrowRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: BorrowRecordSerializer(many=True)}
    )
    def get_queryset(self):
        user = self.request.user
        return BorrowRecord.objects.filter(borrower=user)
