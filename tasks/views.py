from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from tasks.serializers import TaskSerializer
from tasks.filters import TaskFilter


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = TaskFilter

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(author=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["patch"])
    def done(self, request, pk=None):
        task = self.get_object()
        if not task.done:
            task.done = True
            task.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_304_NOT_MODIFIED)
