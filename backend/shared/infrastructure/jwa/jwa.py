"""
Defines the different algorithms supported by JWT.
"""

from enum import StrEnum, unique


@unique
class JWTType(StrEnum):
    """
    Enum for the different types of JWT.
    """

    ACCESS = "access"
    REFRESH = "refresh"


@unique
class JWTSymmetricAlgorithm(StrEnum):
    """
    Enum for the different symmetric algorithms supported by JWT.
    """

    HS256 = "HS256"  # HMAC using SHA-256
    HS384 = "HS384"  # HMAC using SHA-384
    HS512 = "HS512"  # HMAC using SHA-512


@unique
class JWTAsymmetricAlgorithm(StrEnum):
    """
    Enum for the different asymmetric algorithms supported by JWT.
    """

    RS256 = "RS256"  # RSASSA-PKCS1-v1_5 using SHA-256 (asymmetric)
    RS384 = "RS384"  # RSASSA-PKCS1-v1_5 using SHA-384 (asymmetric)
    RS512 = "RS512"  # RSASSA-PKCS1-v1_5 using SHA-512 (asymmetric)
    ES256 = "ES256"  # ECDSA using P-256 and SHA-256 (asymmetric)
    ES384 = "ES384"  # ECDSA using P-384 and SHA-384 (asymmetric)
    ES512 = "ES512"  # ECDSA using P-521 and SHA-512 (asymmetric)
    PS256 = "PS256"  # RSASSA-PSS using SHA-256 and MGF1 with SHA-256 (asymmetric)
    PS384 = "PS384"  # RSASSA-PSS using SHA-384 and MGF1 with SHA-384 (asymmetric)
    PS512 = "PS512"  # RSASSA-PSS using SHA-512 and MGF1 with SHA-512 (asymmetric)


JWTAlgorithm = JWTSymmetricAlgorithm | JWTAsymmetricAlgorithm
