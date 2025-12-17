"""
Wallet endpoints.
"""

from fastapi import APIRouter, Request, Query, status

from backend.auth.middlewares import UserMustBeLoggedMiddleware
from backend.database import get_database_connection
from backend.shared.infrastructure import MiddlewareWrapper
from backend.shared.infrastructure.errors import HTTPError
from backend.users.actions import PostgreSQLUserActions
from backend.users.schemas import (
    WalletTransactionsListSchema,
    PurchaseTokensSchema,
    PurchaseTokensResponseSchema,
)
from backend.users.services import WalletService

route = APIRouter(route_class=MiddlewareWrapper(middlewares=[UserMustBeLoggedMiddleware]))


@route.get(
    path="/transactions",
    summary="Get wallet transaction history.",
    description="Get paginated list of wallet transactions for the current user.",
    status_code=status.HTTP_200_OK,
    response_model=WalletTransactionsListSchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "title": "Unauthorized",
                            "message": "The provided access token is invalid.",
                        }
                    }
                }
            }
        },
    },
)
async def get_wallet_transactions(
    request: Request,
    limit: int = Query(default=10, ge=1, le=100, description="Number of transactions to return"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
) -> WalletTransactionsListSchema:
    """
    Get paginated wallet transaction history for the current user.

    Args:
        request (Request): The request containing the logged user.
        limit (int): Number of transactions to return (max 100).
        offset (int): Offset for pagination.

    Returns:
        WalletTransactionsListSchema: List of transactions with pagination info.
    """
    logged_user = request.state.logged_user

    with get_database_connection() as database_connection:
        wallet_service = WalletService(connection=database_connection)
        transactions, total = wallet_service.get_transactions(
            user_id=logged_user.id,
            limit=limit,
            offset=offset,
        )

    return WalletTransactionsListSchema(transactions=transactions, total=total)


@route.post(
    path="/purchase",
    summary="Purchase tokens.",
    description="Purchase tokens (MVP: free tokens, no real payment).",
    status_code=status.HTTP_201_CREATED,
    response_model=PurchaseTokensResponseSchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "title": "Unauthorized",
                            "message": "The provided access token is invalid.",
                        }
                    }
                }
            }
        },
    },
)
async def purchase_tokens(
    request: Request,
    purchase_data: PurchaseTokensSchema,
) -> PurchaseTokensResponseSchema:
    """
    Purchase tokens (MVP: free tokens without real payment).

    Args:
        request (Request): The request containing the logged user.
        purchase_data (PurchaseTokensSchema): Purchase details.

    Returns:
        PurchaseTokensResponseSchema: Transaction confirmation with new balance.
    """
    logged_user = request.state.logged_user

    with get_database_connection() as database_connection:
        user_actions = PostgreSQLUserActions(connection=database_connection)
        wallet_service = WalletService(connection=database_connection)

        transaction_id, new_balance = wallet_service.purchase_tokens(
            user=logged_user,
            amount=purchase_data.amount,
            user_actions=user_actions,
        )

    return PurchaseTokensResponseSchema(
        transaction_id=str(transaction_id),
        amount=purchase_data.amount,
        new_balance=new_balance,
    )
