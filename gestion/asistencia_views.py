from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from bson.errors import InvalidId
from .mongo import db
from .mongo_serializers import AsistenciaSerializer

col = db["asistencias"]


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
def asistencias_list_create(request):
    if request.method == "GET":
        filtros = {}
        for campo in ("matricula_id", "materia_id", "estudiante_id"):
            val = request.query_params.get(campo)
            if val:
                filtros[campo] = int(val)
        fecha = request.query_params.get("fecha")
        if fecha:
            filtros["fecha"] = fecha
        presente = request.query_params.get("presente")
        if presente is not None:
            filtros["presente"] = presente.lower() == "true"
        return Response([_fix_id(d) for d in col.find(filtros)])

    serializer = AsistenciaSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data.copy()
    data["fecha"] = str(data["fecha"])
    res = col.insert_one(data)
    return Response(_fix_id(col.find_one({"_id": res.inserted_id})), status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def asistencias_detail(request, id: str):
    _id = _oid(id)
    if _id is None:
        return Response({"detail": "id inválido"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        doc = col.find_one({"_id": _id})
        if not doc:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(_fix_id(doc))

    if request.method in ["PUT", "PATCH"]:
        serializer = AsistenciaSerializer(data=request.data, partial=(request.method == "PATCH"))
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data.copy()
        if "fecha" in data:
            data["fecha"] = str(data["fecha"])
        col.update_one({"_id": _id}, {"$set": data})
        doc = col.find_one({"_id": _id})
        if not doc:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(_fix_id(doc))

    result = col.delete_one({"_id": _id})
    if result.deleted_count == 0:
        return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_204_NO_CONTENT)
