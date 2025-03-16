import logging

from fastapi import Security, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID
from starlette import status

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="http://keycloak:8080/realms/reports-realm/protocol/openid-connect/auth",
    tokenUrl="http://keycloak:8080/realms/reports-realm/protocol/openid-connect/token",
)

keycloak_openid = KeycloakOpenID(
    server_url="http://keycloak:8080/",
    client_id="reports-backend",
    realm_name="reports-realm",
    client_secret_key="supersecret",
)


def get_payload(token: str = Security(oauth2_scheme)) -> dict:
    logger.debug("Starting access check.")

    try:
        payload = keycloak_openid.decode_token(token)
        logger.debug("Payload parsed successfully.")
    except Exception as e:
        logger.error("Token validation error occurred: %s", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation error: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.debug("Checking for 'prothetic_user' role.")
    roles = payload.get("realm_access", {}).get("roles", [])
    if "prothetic_user" not in roles:
        logger.warning("User does not have the 'prothetic_user' role.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Insufficient permissions",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info("User has the 'prothetic_user' role. Access granted.")
    return payload
