from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework import permissions

from users.serializers import ProfileSerializers, UserRegisterSerializer
from .models import Profile

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


# class ProfileViewSet(viewsets.ModelViewSet):
#     serializer_class = ProfileSerializers
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Profile.objects.filter(user=self.request.user)

class ProfileRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter()

    def update(self, request, *args, **kwargs):
        user = self.kwargs['pk']
        if self.request.user.id != user:
            return Response({"error": 'You cannot update this profile!'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
