from rest_framework import viewsets
from todos.models import Todo

from todos.serializers import TodoSerializer

# Create your views here.


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
