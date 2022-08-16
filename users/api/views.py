from rest_framework.authtoken.admin import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


from rest_framework import status

from users.api.serializers import RegistrationSerializer


@api_view(['POST', ])
def logout_view(request):
    if request.method == 'POST':
        # for user in User.objects.all():
        #     print(user.username)
        # for user in Account.objects.all():
        #     print(user.username)

        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST', ])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email

            #token = Token.objects.get(user=account).key
            token = Token.objects.get(created=account).key
            data['token'] = token

        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST', ])
def test_view(request):
    if request.method == 'POST':
        print(request.data)

        return Response(status=status.HTTP_200_OK)


