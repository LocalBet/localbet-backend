"""
Wallet service for managing wallet transactions and token purchases.
"""

from datetime import datetime
from uuid import UUID

from backend.users.actions import UserActions
from backend.users.models import User, WalletTransaction
from backend.users.schemas import WalletTransactionSchema


class WalletService:
    """
    Service for wallet operations: transaction history and token purchases.
    """

    __connection: any

    def __init__(self, connection: any) -> None:
        """
        WalletService constructor.

        Args:
            connection: Database connection.
        """
        self.__connection = connection

    def get_transactions(
        self, user_id: UUID, limit: int = 10, offset: int = 0
    ) -> tuple[list[WalletTransactionSchema], int]:
        """
        Get paginated wallet transactions for a user.

        Args:
            user_id (UUID): User ID.
            limit (int): Number of transactions to return.
            offset (int): Offset for pagination.

        Returns:
            tuple: (list of transactions, total count)
        """
        # Query database for transactions
        query = """
            SELECT id, amount, transaction_type, description, created_at
            FROM wallet_transactions
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(query, (str(user_id), limit, offset))
            rows = cursor.fetchall()

        # Get total count for pagination
        count_query = "SELECT COUNT(*) FROM wallet_transactions WHERE user_id = %s"
        with self.__connection.cursor() as cursor:
            cursor.execute(count_query, (str(user_id),))
            total = cursor.fetchone()[0]

        # Convert to schemas
        transactions = [
            WalletTransactionSchema(
                id=str(row[0]),
                amount=row[1],
                transaction_type=row[2],
                description=row[3],
                created_at=row[4],
            )
            for row in rows
        ]

        return transactions, total

    def purchase_tokens(
        self, user: User, amount: int, user_actions: UserActions
    ) -> tuple[UUID, int]:
        """
        Purchase tokens (MVP: free tokens, no real payment).

        Args:
            user (User): The user purchasing tokens.
            amount (int): Amount of tokens to purchase.
            user_actions (UserActions): User actions for updating user.

        Returns:
            tuple: (transaction_id, new_balance)
        """
        # Add coins to user
        user.add_coins(amount)

        # Save updated user
        user_actions.update(user=user)

        # Create wallet transaction
        transaction = WalletTransaction(
            user_id=user.id,
            amount=amount,
            transaction_type="purchase",
            description=f"Compra de {amount} tokens",
        )

        # Save transaction to database
        insert_query = """
            INSERT INTO wallet_transactions (id, user_id, amount, transaction_type, description, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(
                insert_query,
                (
                    str(transaction.id),
                    str(transaction.user_id),
                    transaction.amount,
                    transaction.transaction_type,
                    transaction.description,
                    transaction.created_at,
                ),
            )

        return transaction.id, user.coins
