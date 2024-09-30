# core/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .serializers import CustomUserSerializer, CustomUserUpdateSerializer
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)

        # Verifica se o usuário atual é o proprietário da conta ou é um admin
        if request.user != user and not request.user.is_staff:
            raise PermissionDenied(
                "Você não tem permissão para atualizar este usuário."
            )

        serializer = CustomUserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCreditsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        amount = request.data.get("amount")
        if not amount or float(amount) <= 0:
            return Response(
                {"error": "Valor inválido."}, status=status.HTTP_400_BAD_REQUEST
            )

        request.user.balance += float(amount)
        request.user.save()
        return Response(
            {
                "message": "Créditos adicionados com sucesso.",
                "new_balance": request.user.balance,
            }
        )


class AutomationCaptureView(APIView):
    permission_classes = [IsAuthenticated]
    cost = 10.00

    def get(self, request):
        request.user.balance -= self.cost
        request.user.save()
        return Response({"message": "Automation Capture"})


class AutomationBlastView(APIView):
    permission_classes = [IsAuthenticated]
    cost = 15.00

    def get(self, request):
        request.user.balance -= self.cost
        request.user.save()
        return Response({"message": "Automation Blast"})


class TaskSendMailView(APIView):
    permission_classes = [IsAuthenticated]
    cost = 5.00

    def get(self, request):
        request.user.balance -= self.cost
        request.user.save()
        return Response({"message": "Task Send Mail"})


class TaskPaymentView(APIView):
    permission_classes = [IsAuthenticated]
    cost = 20.00

    def get(self, request):
        request.user.balance -= self.cost
        request.user.save()
        return Response({"message": "Task Payment"})
