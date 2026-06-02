from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from bson.errors import InvalidId
from .mongo import db
from .mongo_serializers import ActividadSerializer

col = db["actividades"]


def _fix_id(doc):
    doc = dict(doc)
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc


def _oid(id_str: str):
    try:
        return ObjectId(id_str)
    except InvalidId:
        return None


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def actividades_list_create(request):
    if request.method == "GET":
        filtros = {}
        materia_id = request.query_params.get("materia_id")
        if materia_id:
            filtros["materia_id"] = int(materia_id)
        tipo = request.query_params.get("tipo")
        if tipo:
            filtros["tipo"] = tipo
        activo = request.query_params.get("activo")
        if activo is not None:
            filtros["activo"] = activo.lower() == "true"
        return Response([_fix_id(d) for d in col.find(filtros)])

    serializer = ActividadSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data.copy()
    if data.get("fecha_limite"):
        data["fecha_limite"] = str(data["fecha_limite"])
    res = col.insert_one(data)
    return Response(_fix_id(col.find_one({"_id": res.inserted_id})), status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def actividades_detail(request, id: str):
    _id = _oid(id)
    if _id is None:
        return Response({"detail": "id inválido"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        doc = col.find_one({"_id": _id})
        if not doc:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(_fix_id(doc))

    if request.method in ["PUT", "PATCH"]:
        serializer = ActividadSerializer(data=request.data, partial=(request.method == "PATCH"))
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data.copy()
        if data.get("fecha_limite"):
            data["fecha_limite"] = str(data["fecha_limite"])
        col.update_one({"_id": _id}, {"$set": data})
        doc = col.find_one({"_id": _id})
        if not doc:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(_fix_id(doc))

    result = col.delete_one({"_id": _id})
    if result.deleted_count == 0:
        return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_204_NO_CONTENT)
