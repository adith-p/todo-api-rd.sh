from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework import permissions
from django.core.paginator import Paginator
from .serializer import UserSerializer, TodoSerializer, GetAllTodoSerializer
from .models import Todo

from .permission import CustomIsAuthPermission, CustomIsAuthorPermission

# Create your views here.


class UserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        return Response(data=serializer.errors, status=status.HTTP_201_CREATED)


class TodosView(APIView):
    permission_classes = [CustomIsAuthPermission]

    def get(self, request):
        page = int(request.query_params.get("page", 1))
        limit = int(request.query_params.get("limit", 10))

        todo_object = Todo.objects.all()
        paginator = Paginator(todo_object, limit)
        page_obj = paginator.get_page(page)

        todo_serializer = TodoSerializer(page_obj.object_list, many=True)
        final_serializer = GetAllTodoSerializer(
            data={
                "data": todo_serializer.data,
                "page": page,
                "limit": limit,
                "total": paginator.count,
            }
        )
        final_serializer.is_valid(raise_exception=True)
        return Response(data=final_serializer.data)

    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoView(APIView):
    permission_classes = [CustomIsAuthorPermission]

    def put(self, request, pk):

        todo_item = Todo.objects.filter(pk=pk).first()
        self.check_object_permissions(request, todo_item)
        serializer = TodoSerializer(todo_item)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        todo_item = Todo.objects.filter(pk=pk).first()
        if todo_item:

            self.check_object_permissions(request, todo_item)
            todo_item.delete()
            return Response(
                data={"message": "item deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            data={"message": "item does not exist"}, status=status.HTTP_400_BAD_REQUEST
        )
