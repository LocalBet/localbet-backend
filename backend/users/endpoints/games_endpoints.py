"""
Mini games endpoints.
"""

from fastapi import APIRouter, Request, status

from backend.auth.middlewares import UserMustBeLoggedMiddleware
from backend.database import get_database_connection
from backend.shared.infrastructure import MiddlewareWrapper
from backend.shared.infrastructure.errors import HTTPError
from backend.users.actions import PostgreSQLUserActions
from backend.users.schemas import RoulettePlaySchema, CardFlipPlaySchema, GameResultSchema
from backend.users.services import GamesService

route = APIRouter(route_class=MiddlewareWrapper(middlewares=[UserMustBeLoggedMiddleware]))


@route.post(
    path="/roulette/play",
    summary="Play roulette mini game.",
    description="Server-authoritative roulette game with 40% win rate.",
    status_code=status.HTTP_200_OK,
    response_model=GameResultSchema,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "title": "InsufficientBalance",
                            "message": "Insufficient balance",
                        }
                    }
                }
            }
        },
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
async def play_roulette(request: Request, game_data: RoulettePlaySchema) -> GameResultSchema:
    """
    Play roulette mini game.

    Args:
        request (Request): The request containing the logged user.
        game_data (RoulettePlaySchema): Game parameters.

    Returns:
        GameResultSchema: Game result with winnings and new balance.
    """
    logged_user = request.state.logged_user

    try:
        with get_database_connection() as database_connection:
            user_actions = PostgreSQLUserActions(connection=database_connection)
            games_service = GamesService(connection=database_connection)

            result, winnings, game_details, transaction_id = games_service.play_roulette(
                user=logged_user,
                bet_amount=game_data.bet_amount,
                bet_type=game_data.bet_type,
                number=game_data.number,
                user_actions=user_actions,
            )

        return GameResultSchema(
            result=result,
            winnings=winnings,
            new_balance=logged_user.coins,
            game_details=game_details,
            transaction_id=str(transaction_id),
        )

    except ValueError as exception:
        raise HTTPError(
            status_code=status.HTTP_400_BAD_REQUEST,
            title="ValidationError",
            message=str(exception),
        ) from exception


@route.post(
    path="/cardflip/play",
    summary="Play card flip mini game.",
    description="Server-authoritative card flip game with 40% win rate.",
    status_code=status.HTTP_200_OK,
    response_model=GameResultSchema,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "title": "InsufficientBalance",
                            "message": "Insufficient balance",
                        }
                    }
                }
            }
        },
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
async def play_cardflip(request: Request, game_data: CardFlipPlaySchema) -> GameResultSchema:
    """
    Play card flip mini game.

    Args:
        request (Request): The request containing the logged user.
        game_data (CardFlipPlaySchema): Game parameters.

    Returns:
        GameResultSchema: Game result with winnings and new balance.
    """
    logged_user = request.state.logged_user

    try:
        with get_database_connection() as database_connection:
            user_actions = PostgreSQLUserActions(connection=database_connection)
            games_service = GamesService(connection=database_connection)

            result, winnings, game_details, transaction_id = games_service.play_cardflip(
                user=logged_user,
                bet_amount=game_data.bet_amount,
                guess=game_data.guess,
                user_actions=user_actions,
            )

        return GameResultSchema(
            result=result,
            winnings=winnings,
            new_balance=logged_user.coins,
            game_details=game_details,
            transaction_id=str(transaction_id),
        )

    except ValueError as exception:
        raise HTTPError(
            status_code=status.HTTP_400_BAD_REQUEST,
            title="ValidationError",
            message=str(exception),
        ) from exception
