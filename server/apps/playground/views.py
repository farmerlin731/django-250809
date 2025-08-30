from django.http import Http404
from rest_framework.decorators import api_view
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


class ItemListView(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        Item.objects.create(**serializer.validated_data)

        return Response({"status": "ok", **serializer.validated_data}, status=201)


class ItemDetailView(APIView):
    def get(self, request, pk):
        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            raise Http404

        serializer = ItemSerializer(item)
        return Response(serializer.data)
