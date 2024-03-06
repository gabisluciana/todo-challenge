from django.db.models import Q
from django_filters import filters as d_filters, FilterSet
from rest_framework import filters


from tasks.models import Tasks


class TaskFilter(FilterSet):
    content = d_filters.CharFilter(method="filter_content")
    date = d_filters.DateFilter(field_name="created_at", lookup_expr="date__exact")

    def filter_content(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))

    class Meta:
        model = Tasks
        fields = (
            "title",
            "description",
            "created_at",
        )
