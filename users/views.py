from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from users.serializers import UserSerializer


class RegisterApiView(GenericAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
