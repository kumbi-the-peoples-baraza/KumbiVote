from rest_framework import viewsets

from .models import User, UserProfile
from .serializers import UserProfileSerializer, UserSerializer

# from utils import generate_blockchain_id, register_on_blockchain


# User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


# class RegisterView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             blockchain_id = generate_blockchain_id(user)
#             user.blockchain_id = blockchain_id
#             user.save()
#             register_on_blockchain(user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
