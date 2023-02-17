import datetime
import hashlib
import logging
from typing import Optional
from uuid import uuid4

from motor.motor_asyncio import AsyncIOMotorClient
from passlib.hash import bcrypt
from pymongo.errors import ServerSelectionTimeoutError

from app import config
from app.models.auth import ExternalUser, InternalUser
from app.utils.exceptions import DatabaseConnectionError

logger = logging.getLogger(__name__)


class MongoClient:
    """Database client interface"""

    def __init__(self):
        mongodb_uri = (
            f"mongodb://"
            f"{config.MONGODB_HOST}:"
            f"{config.MONGODB_PORT}/"
            f"{config.MONGODB_DATABASE}?"
            f"authSource={config.MONGODB_COLLECTION}"
        )
        self._motor_client = AsyncIOMotorClient(mongodb_uri)
        # Mongo database
        self._db = self._motor_client[config.MONGODB_DATABASE]
        # Mongo collections
        self._users_coll = self._db["users"]
        self._session = None

    async def close_connection(self):
        """
        Closes a connection to the database.
        """
        self._motor_client.close()

    async def start_session(self):
        """
        Starts a session in the database.

        Usually called once at the start of the service.
        Stays open as long as the service is running.

        Raises
        ------
        DatabaseConnectionError
            If the connection to the database cannot be established.
        """
        try:
            self._session = await self._motor_client.start_session()
        except ServerSelectionTimeoutError as exc:
            raise DatabaseConnectionError(exc)

    async def end_session(self):
        """
        Ends a session in the database.
        """
        await self._session.end_session()

    async def get_user_by_external_sub_id(
        self, external_user: ExternalUser
    ) -> Optional[InternalUser]:
        """
        Returns a user from the database, based on the external sub_id of
        the authentication provider.

        Parameters
        ----------
        external_user : ExternalUser
            An object representing a user with information based on the external provider's service.

        Returns
        -------
        internal_user : Optional[InternalUser]
            A user object as defined in this application. If no user is found, returns None.
        """
        encrypted_external_sub_id = await self._encrypt_external_sub_id(external_user)

        mongo_user = await self._users_coll.find_one(
            {"external_sub_id": encrypted_external_sub_id}
        )

        if mongo_user:
            return InternalUser(
                internal_sub_id=mongo_user["internal_sub_id"],
                external_sub_id=mongo_user["external_sub_id"],
                username=mongo_user["username"],
                created_at=mongo_user["created_at"],
            )

        return None

    async def get_user_by_internal_sub_id(
        self, internal_sub_id: str
    ) -> Optional[InternalUser]:
        """
        Returns a user from the database, based on the internal sub_id

        Parameters
        ----------
        internal_sub_id : str
            The unique id of the user as defined in this application

        Returns
        -------
        internal_user : Optional[InternalUser]
            A user object as defined in this application. If no user is found, returns None.
        """
        mongo_user = await self._users_coll.find_one({"_id": internal_sub_id})

        if mongo_user:
            return InternalUser(
                internal_sub_id=mongo_user["internal_sub_id"],
                external_sub_id=mongo_user["external_sub_id"],
                username=mongo_user["username"],
                created_at=mongo_user["created_at"],
            )

        return None

    async def create_internal_user(self, external_user: ExternalUser) -> InternalUser:
        """
        Creates a user in the database based on the external sub_id of
        the authentication provider.

        The user will also be assigned an internal sub_id for authentication
        within the internal system (backend application)

        Parameters
        ----------
        external_user : ExternalUser
            An object representing a user with information based on the external provider's service.

        Returns
        -------
        internal_user : InternalUser
            A user object as defined in this application
        """
        encrypted_external_sub_id = await self._encrypt_external_sub_id(external_user)
        unique_identifier = str(uuid4())

        result = await self._users_coll.insert_one(
            dict(
                _id=unique_identifier,
                internal_sub_id=unique_identifier,
                external_sub_id=encrypted_external_sub_id,
                username=external_user.username,
                created_at=datetime.datetime.utcnow(),
            )
        )

        mongo_user_id = result.inserted_id

        mongo_user = await self._users_coll.find_one({"_id": mongo_user_id})

        return InternalUser(
            internal_sub_id=mongo_user["internal_sub_id"],
            external_sub_id=mongo_user["external_sub_id"],
            username=mongo_user["username"],
            created_at=mongo_user["created_at"],
        )

    async def update_internal_user(
        self, internal_user: InternalUser
    ) -> Optional[InternalUser]:
        """
        Updates a user in the database.

        Parameters
        ----------
        internal_user : InternalUser
            A user objects as defined in this application

        Returns
        -------
        internal_user : Optional[InternalUser]
            A user object as defined in this application. If no user is found, returns None.
        """
        result = await self._users_coll.update_one(
            {"internal_sub_id": internal_user.internal_sub_id},
            {"$set": internal_user.dict()},
        )

        if result.modified_count:
            return internal_user

        return None

    async def _encrypt_external_sub_id(sefl, external_user: ExternalUser) -> str:
        """
        Encrypt the subject id received from the external provider. These ids are
        used to uniquely identify a user in the system of the external provider and
        are usually public. However, it is better to be stored encrypted just in case.

        Parameters
        ----------
        external_user : ExternalUser
            An object representing a user with information based on the external provider's service.

        Returns
        -------
        encrypted_external_sub_id : str
            The encrypted external subject id
        """
        salt = external_user.email.lower()
        salt = salt.replace(" ", "")
        # Hash the salt so that the email is not plain text visible in the database
        salt = hashlib.sha256(salt.encode()).hexdigest()
        # bcrypt requires a 22 char salt
        if len(salt) > 21:
            salt = salt[:21]

        # As per passlib the last character of the salt should always be one of [.Oeu]
        salt = salt + "O"

        encrypted_external_sub_id = bcrypt.using(salt=salt).hash(
            external_user.external_sub_id
        )
        return encrypted_external_sub_id
