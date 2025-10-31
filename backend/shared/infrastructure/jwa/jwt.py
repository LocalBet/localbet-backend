"""
This module provides functions to encode and decode JSON Web Tokens (JWT).
"""

from datetime import UTC, datetime, timedelta
from typing import Annotated, Any
from uuid import uuid4

from authlib.jose import JWTClaims, JsonWebToken, jwt
from pydantic import Field, validate_call

from .jwa import JWTAlgorithm, JWTSymmetricAlgorithm, JWTType


class JWT:
    """
    Provides functions to encode and decode JSON Web Tokens (JWT).
    """

    @classmethod
    @validate_call
    def encode_token(
        cls,
        *,
        algorithm: Annotated[
            JWTAlgorithm,
            Field(
                default=...,
                description="Algorithm to sign JWT.",
                examples=[JWTSymmetricAlgorithm.HS256],
            ),
        ],
        token_type: Annotated[
            JWTType,
            Field(
                default=...,
                description="Type of JWT.",
                examples=[JWTType.ACCESS],
            ),
        ],
        secret: Annotated[
            str,
            Field(
                default=...,
                min_length=1,
                description="Secret to sign JWT.",
                examples=["secret"],
                strict=True,
            ),
        ],
        issuer: Annotated[
            str,
            Field(
                default=...,
                min_length=1,
                description="Entity that issued JWT.",
                examples=["https://example.com"],
                strict=True,
            ),
        ],
        subject: Annotated[
            str,
            Field(
                default=...,
                min_length=1,
                description="Person that will use the JWT.",
                examples=["29c0bcdc-00fc-49b3-88cd-5cc00f11b899"],
                strict=True,
            ),
        ],
        audience: Annotated[
            str,
            Field(
                default=...,
                min_length=1,
                description="Entity that JWT is intended for.",
                examples=["https://api.example.com"],
                strict=True,
            ),
        ],
        expiration_delta: Annotated[
            int,
            Field(
                default=...,
                ge=0,
                description="Time in seconds for JWT to expire.",
                examples=[600],
                strict=True,
            ),
        ],
        payload: Annotated[
            dict[str, Any] | None,
            Field(
                default=...,
                description="Payload to encode in JWT.",
                examples=[
                    {
                        "username": "JohnDoe",
                        "email": "johndoe@example.com",
                    },
                ],
            ),
        ] = None,
        not_before_delta: Annotated[
            int,
            Field(
                ge=0,
                description="Time in seconds for JWT to be valid.",
                examples=[0],
                strict=True,
            ),
        ] = 0,
        token_id: Annotated[
            Any | None,
            Field(
                default=None,
                description="Unique identifier for JWT, it must be convertible to string.",
                examples=[uuid4()],
            ),
        ] = None,
    ) -> str:
        """
        Encodes a JWT with the provided payload.

        Args:
            algorithm (JWTAlgorithm): Algorithm to sign JWT.
            token_type (JWTType): Type of JWT.
            secret (str): Secret to sign JWT.
            payload (dict[str, Any], optional): Payload to encode in JWT. Defaults to None.
            issuer (str): Entity that issued JWT.
            subject (str): Person that will use the JWT.
            audience (str): Entity that JWT is intended for.
            expiration_delta (int): Time in seconds for JWT to expire.
            not_before_delta (int, optional): Time in seconds for JWT to be valid. Defaults to 0.
            token_id (Any | None, optional): Unique identifier for JWT, it must be convertible to string. Defaults
            to None.

        Raises:
            ValidationError: If algorithm is not of type JWTAlgorithm.
            ValidationError: If token_type is not of type JWTType.
            ValidationError: If secret is not of type string.
            ValidationError: If secret is empty.
            ValidationError: If payload is not of type dictionary or None.
            ValidationError: If issuer is not of type string.
            ValidationError: If issuer is empty.
            ValidationError: If subject is not of type string.
            ValidationError: If subject is empty.
            ValidationError: If audience is not of type string.
            ValidationError: If audience is empty.
            ValidationError: If expiration_delta is not of type integer.
            ValidationError: If expiration_delta is negative.
            ValidationError: If not_before_delta is not of type integer.
            ValidationError: If not_before_delta is negative.
            ValidationError: If token_id is not of type Any or None.

        Returns:
            str: Encoded JWT.
        """
        now = datetime.now(tz=UTC)

        if payload is None:
            payload = {}

        payload["type"] = token_type
        payload["iss"] = issuer
        payload["sub"] = subject
        payload["aud"] = audience
        payload["iat"] = int(now.timestamp())
        payload["exp"] = int((now + timedelta(seconds=expiration_delta)).timestamp())
        payload["nbf"] = int((now + timedelta(seconds=not_before_delta)).timestamp())

        if token_id is not None:
            payload["jti"] = str(token_id)

        header = {}
        header["alg"] = str(algorithm)

        token_bytes: Any = jwt.encode(header=header, payload=payload, key=secret) # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
        if isinstance(token_bytes, bytes):
            return token_bytes.decode("utf-8")
        return str(token_bytes) # pyright: ignore[reportUnknownArgumentType]

    @classmethod
    @validate_call
    def decode_token(
        cls,
        *,
        token: Annotated[
            str,
            Field(
                default=...,
                min_length=1,
                description="JWT to decode.",
                examples=[
                    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJpc3N1ZXIiLCJzdWIiOiJzdWJqZWN0IiwiYXVkIjoiYXVkaWVuY2UiLCJpYXQiOjE3MjI3MTIzODIsImV4cCI6MTcyMjcxMjM4MiwibmJmIjoxNzIyNzEyMzgyLCJqdGkiOiI1NTU5NTU5Mi1lZjdkLTQ4ZTItOWYyOS1kY2RhZDc1MzY2NmEifQ.D6h3geumsl5CwNTFtf5uQAXKsYas-TnBisg-9LCernU"
                ],
                strict=True,
            ),
        ],
        token_type: Annotated[
            JWTType,
            Field(
                default=...,
                description="Type of JWT.",
                examples=[JWTType.ACCESS],
            ),
        ],
        secret: Annotated[
            str,
            Field(
                default=...,
                min_length=1,
                description="Secret to verify JWT signature.",
                examples=["secret"],
                strict=True,
            ),
        ],
        issuer: Annotated[
            str,
            Field(
                default=...,
                min_length=1,
                description="Entity that issued JWT.",
                examples=["https://example.com"],
                strict=True,
            ),
        ],
        audience: Annotated[
            str,
            Field(
                default=...,
                min_length=1,
                description="Entity that JWT is intended for.",
                examples=["https://api.example.com"],
                strict=True,
            ),
        ],
        accepted_algorithms: Annotated[
            list[JWTAlgorithm] | None,
            Field(
                default=None,
                description="List of accepted algorithms to decode JWT.",
                examples=[JWTSymmetricAlgorithm.HS256],
                strict=True,
            ),
        ] = None,
    ) -> dict[str, Any]:
        """
        Decodes the provided JWT.
        If `accepted_algorithms` is None, it will not accept any algorithm, this restriction is to avoid algorithm
        confusion exploits.

        Args:
            token (str): JWT to decode.
            token_type (JWTType): Type of JWT.
            secret (str): Secret to verify JWT signature.
            issuer (str): Entity that issued JWT.
            audience (str): Entity that JWT is intended for.
            accepted_algorithms (list[JWTAlgorithm] | None, optional): List of accepted algorithms to decode JWT.
            Defaults to None.

        Raises:
            ValidationError: If token is not of type string.
            ValidationError: If token is empty.
            ValidationError: If token_type is not of type JWTType.
            ValidationError: If secret is not of type string.
            ValidationError: If secret is empty.
            ValidationError: If issuer is not of type string.
            ValidationError: If issuer is empty.
            ValidationError: If audience is not of type string.
            ValidationError: If audience is empty.
            ValidationError: If accepted_algorithms is not of type list or None.

        Returns:
            dict[str, Any]: Decoded JWT.
        """
        if accepted_algorithms is None:
            accepted_algorithms = []

        claim_validations: dict[str, Any] = {}
        claim_validations["type"] = {"essential": True, "value": token_type}
        claim_validations["iss"] = {"essential": True, "value": issuer}
        claim_validations["aud"] = {"essential": True, "value": audience}

        jwt = JsonWebToken(algorithms=accepted_algorithms)
        claims: JWTClaims | Any = jwt.decode(  # type: ignore
            s=bytes(token, encoding="utf-8"),
            key=secret,
            claims_options=claim_validations,
        )

        claims.validate()  # type: ignore

        return_claims = dict(claims)  # type: ignore
        return_claims["type"] = JWTType(value=claims["type"])
        return_claims["iat"] = datetime.fromtimestamp(claims["iat"], tz=UTC)  # type: ignore
        return_claims["exp"] = datetime.fromtimestamp(claims["exp"], tz=UTC)  # type: ignore
        return_claims["nbf"] = datetime.fromtimestamp(claims["nbf"], tz=UTC)  # type: ignore

        return return_claims
