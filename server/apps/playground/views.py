from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from server.apps.playground.models import Item
from server.apps.playground.serializers import ItemSerializer
from server.utils.pagination import PageNumberWithSizePagination


# Create your views here.
@api_view(["GET", "POST"])
def hello(request):
    if request.method == "GET":
        message = "Hello World by GET method"
    else:
        message = "Hello World by POST method"

    return Response({"message": message})


class HiView(APIView):
    def _customMsg(self, method):
        return f"Hi Hi by {method} method! :)"

    def get(self, request):
        return Response({"message": self._customMsg("GET")})

    def post(self, request):
        return Response({"message": self._customMsg("POST")})


# # Version 1
# class ItemListView(APIView):
#     def get(self, request):
#         items = Item.objects.all()
#         serializer = ItemSerializer(items, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ItemSerializer(data=request.data)
#         ## Basic Usage
#         # if not serializer.is_valid():
#         #     return Response(serializer.errors, status=400)

#         # Item.objects.create(**serializer.validated_data)

#         ## Advanced Usage
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response({"status": "ok", **serializer.data}, status=201)


# # Version 2
# class ItemListView(CreateModelMixin, ListModelMixin, GenericAPIView):
#     # The variable name is fixed.
#     serializer_class = ItemSerializer
#     queryset = Item.objects.all()

#     def get(self, request):
#         return self.list(request)

#     def post(self, request):
#         return self.create(request)


# Version 3
class ItemListView(ListCreateAPIView):
    # The variable name is fixed.
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


# # Use Generic & Mixin
# # class ItemDetailView(APIView): # Version 1
# class ItemDetailView(GenericAPIView, RetrieveModelMixin):  # Version 2
#     serializer_class = ItemSerializer
#     queryset = Item.objects.all()  # Version 2
#     # # Version 1 - APIView
#     # def get_item(self, pk):
#     #     try:
#     #         item = Item.objects.get(id=pk)
#     #     except Item.DoesNotExist:
#     #         raise Http404

#     #     return item

#     # Version 1 - APIView
#     # def get(self, request, pk):
#     #     item = self.get_item(pk)
#     #     serializer = ItemSerializer(item)
#     #     return Response(serializer.data)

#     # Version 2 - GenericAPIView
#     # def get(self, request, pk):
#     #     item = self.get_object()
#     #     serializer = self.get_serializer(item)
#     #     return Response(serializer.data)

#     # Version 3 - GenericAPIView + RetrieveModelMixin
#     def get(self, request, pk):
#         return self.retrieve(request, pk)

#     def delete(self, request, pk):
#         item = self.get_object()
#         item.delete()
#         return Response({"delete": "done"}, status=204)

#     def put(self, request, pk):
#         item = self.get_object()

#         serializer = self.get_serializer(item, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data)

#     def patch(self, request, pk):
#         item = self.get_object()

#         serializer = self.get_serializer(item, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data)


## Version 3 - RetrieveUpdateDestroyAPIView
class ItemDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


## Version 4 - Final ! ViewSet!
class ItemViewSet(ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    pagination_class = PageNumberWithSizePagination
    page_size = 5
    filter_backends = [  # 允許被使用的 filter 種類
        OrderingFilter,  # 排序型的 filter
        SearchFilter,  # 搜尋型的 filter
        DjangoFilterBackend,  # 特定欄位的 filter
    ]
    ordering_fields = ["name", "id"]  # 排序型的 filter 允許使用者指定的欄位有哪些
    ordering = ["id"]  # 如果使用者沒有指定的話排序型 filter 要用來排序的欄位
    search_fields = ["name", "description"]  # 關鍵字要在哪些欄位中被搜尋 #search
    filterset_fields = ["is_active", "name"]
