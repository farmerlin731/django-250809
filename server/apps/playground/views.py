from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from server.apps.playground.models import Item
from server.apps.playground.serializers import ItemSerializer


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


# class ItemDetailView(APIView): # Version 1
class ItemDetailView(GenericAPIView):  # Version 2
    serializer_class = ItemSerializer
    queryset = Item.objects.all()  # Version 2
    # # Version 1
    # def get_item(self, pk):
    #     try:
    #         item = Item.objects.get(id=pk)
    #     except Item.DoesNotExist:
    #         raise Http404

    #     return item

    def get(self, request, pk):
        # item = self.get_item(pk)  # Version 1 - APIView
        item = self.get_object()  # Version 2 - GenericAPIView
        # serializer = ItemSerializer(item) # Version 1 - APIView
        serializer = self.get_serializer(item)  # Version 2 - GenericAPIView
        return Response(serializer.data)

    def delete(self, request, pk):
        item = self.get_object()
        item.delete()
        return Response({"delete": "done"}, status=204)

    def put(self, request, pk):
        item = self.get_object()

        serializer = self.get_serializer(item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def patch(self, request, pk):
        item = self.get_object()

        serializer = self.get_serializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
