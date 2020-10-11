from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from core.serializers import RegistrationSerializer, UpdateSerializer
from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User
from .models import MyUser
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            print("account",account)
            data['status'] = "Successfully registered."
            data['id'] = account.id
            data['email'] = account.email
            try:
                token = Token.objects.get(user=account).key
                data['token'] = token
            except Token.DoesNotExist:
                data['token'] = "Not exist"
                print("token does not exist")

        else:
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)
        return Response(data)

class update_user(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateSerializer
    queryset = MyUser.objects.all()

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_view(request, pk):
    try:
        user = MyUser.objects.get(id=pk)
    except MyUser.DoesNotExist:
        return Response({'Error:':'The User does not exists'},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        user.delete()
        data = {'Success':'User deleted successfully'}
        return Response({'Success':'User deleted successfully'},status=status.HTTP_204_NO_CONTENT)
