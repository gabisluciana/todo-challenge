from rest_framework.serializers import ModelSerializer

from tasks.models import Tasks


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Tasks
        fields = (
            "id",
            "title",
            "description",
            "done",
            "created_at",
        )
        extra_kwargs = {"done": {"read_only": True}}
