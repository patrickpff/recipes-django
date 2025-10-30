from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tag.models import Tag

from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer


class RecipeApiV2Pagination(PageNumberPagination):
    page_size = 9


class RecipeApiV2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeApiV2Pagination
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.query_params.get('category_id', None)

        if category_id is not None and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(
        instance=tag,
        many=False,
    )
    return Response(serializer.data)
