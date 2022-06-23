from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView

from users.serializers import UserRegisterSerializer

# Create your views here.


@api_view(['GET', 'POST'])
def register_user(request):
    serializer = UserRegisterSerializer()
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.data)


class RegisterUserAPIView(CreateAPIView):
    """
    View to Register the New User.
    """
    serializer_class = UserRegisterSerializer
