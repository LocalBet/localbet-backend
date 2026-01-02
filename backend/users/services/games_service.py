"""
Mini games service with server-authoritative logic.
"""

import random
from uuid import UUID

from backend.users.actions import UserActions
from backend.users.models import User, WalletTransaction


class GamesService:
    """
    Service for mini games (roulette, card flip).
    Server-authoritative to prevent cheating.
    """

    __connection: any
    WIN_PROBABILITY = 0.40  # MVP: 40% win rate

    def __init__(self, connection: any) -> None:
        """
        GamesService constructor.

        Args:
            connection: Database connection.
        """
        self.__connection = connection

    def play_roulette(
        self, user: User, bet_amount: int, bet_type: str, number: int | None, user_actions: UserActions
    ) -> tuple[str, int, dict, UUID]:
        """
        Play roulette game (server-authoritative).

        Args:
            user (User): The user playing.
            bet_amount (int): Amount to bet.
            bet_type (str): 'red', 'black', or 'number'.
            number (int | None): Specific number if bet_type='number'.
            user_actions (UserActions): User actions for updating balance.

        Returns:
            tuple: (result, winnings, game_details, transaction_id)

        Raises:
            ValueError: If invalid bet_type or insufficient balance.
        """
        if user.coins < bet_amount:
            raise ValueError("Insufficient balance")

        if bet_type not in ('red', 'black', 'number'):
            raise ValueError("Invalid bet_type. Must be 'red', 'black', or 'number'.")

        if bet_type == 'number' and (number is None or not 0 <= number <= 36):
            raise ValueError("Number must be between 0-36 for bet_type='number'.")

        # Server generates random result
        spun_number = random.randint(0, 36)
        spun_color = self._get_roulette_color(spun_number)

        # Determine win/loss
        won = False
        multiplier = 1

        if bet_type == 'red' or bet_type == 'black':
            # Color bet: 2x multiplier
            won = (bet_type == spun_color)
            multiplier = 2
        elif bet_type == 'number':
            # Number bet: 35x multiplier (standard roulette)
            won = (number == spun_number)
            multiplier = 35

        # MVP: Adjust win probability to 40% (override if random doesn't favor player)
        random_chance = random.random()
        if random_chance < self.WIN_PROBABILITY and not won:
            # Force win
            won = True
        elif random_chance >= self.WIN_PROBABILITY and won:
            # Force loss
            won = False

        # Calculate winnings
        winnings = bet_amount * multiplier if won else 0
        net_change = winnings - bet_amount

        # Update user balance
        user.coins += net_change
        user_actions.update(user=user)

        # Create wallet transaction
        transaction = WalletTransaction(
            user_id=user.id,
            amount=net_change,
            transaction_type='minigame_win' if won else 'minigame_loss',
            description=f"Ruleta: {'Ganaste' if won else 'Perdiste'} apostando {bet_amount} en {bet_type}",
        )
        self._save_transaction(transaction)

        game_details = {
            "game": "roulette",
            "spun_number": spun_number,
            "spun_color": spun_color,
            "bet_type": bet_type,
            "bet_number": number,
        }

        return ('won' if won else 'lost', winnings, game_details, transaction.id)

    def play_cardflip(
        self, user: User, bet_amount: int, guess: str, user_actions: UserActions
    ) -> tuple[str, int, dict, UUID]:
        """
        Play card flip game (server-authoritative).

        Args:
            user (User): The user playing.
            bet_amount (int): Amount to bet.
            guess (str): 'heads' or 'tails'.
            user_actions (UserActions): User actions for updating balance.

        Returns:
            tuple: (result, winnings, game_details, transaction_id)

        Raises:
            ValueError: If invalid guess or insufficient balance.
        """
        if user.coins < bet_amount:
            raise ValueError("Insufficient balance")

        if guess not in ('heads', 'tails'):
            raise ValueError("Invalid guess. Must be 'heads' or 'tails'.")

        # Server flips card
        card_result = random.choice(['heads', 'tails'])

        # Determine win/loss (2x multiplier)
        won = (guess == card_result)

        # MVP: Adjust win probability to 40%
        random_chance = random.random()
        if random_chance < self.WIN_PROBABILITY and not won:
            won = True
            card_result = guess  # Override result
        elif random_chance >= self.WIN_PROBABILITY and won:
            won = False
            card_result = 'tails' if guess == 'heads' else 'heads'

        # Calculate winnings
        winnings = bet_amount * 2 if won else 0
        net_change = winnings - bet_amount

        # Update user balance
        user.coins += net_change
        user_actions.update(user=user)

        # Create wallet transaction
        transaction = WalletTransaction(
            user_id=user.id,
            amount=net_change,
            transaction_type='minigame_win' if won else 'minigame_loss',
            description=f"Volteo de carta: {'Ganaste' if won else 'Perdiste'} apostando {bet_amount}",
        )
        self._save_transaction(transaction)

        game_details = {
            "game": "cardflip",
            "card_result": card_result,
            "your_guess": guess,
        }

        return ('won' if won else 'lost', winnings, game_details, transaction.id)

    def _get_roulette_color(self, number: int) -> str:
        """Get color for roulette number (European roulette)."""
        if number == 0:
            return 'green'
        red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        return 'red' if number in red_numbers else 'black'

    def _save_transaction(self, transaction: WalletTransaction) -> None:
        """Save wallet transaction to database."""
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
