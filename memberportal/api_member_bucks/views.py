from memberbucks.models import MemberBucks

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class MemberBucksTransactions(APIView):
    """
    get: This method returns a member's memberbucks transactions.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        recent_transactions = MemberBucks.objects.filter(user=request.user).order_by(
            "date"
        )[::-1][:100]

        def get_transaction(transaction):
            return transaction.get_transaction_display()

        return Response(
            map(get_transaction, recent_transactions), status=status.HTTP_200_OK
        )


class MemberBucksBalance(APIView):
    """
    get: This method returns a member's memberbucks balance.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response(
            {"balance": request.user.profile.memberbucks_balance},
            status=status.HTTP_200_OK,
        )
