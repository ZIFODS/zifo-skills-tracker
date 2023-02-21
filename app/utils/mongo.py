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
        logger.info("Starting MongoDB client")
        self._motor_client = AsyncIOMotorClient(
            config.MONGODB_HOST, config.MONGODB_PORT
        )
        logger.info("Connected to MongoDB")
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

    async def get_user_by_external_id(
        self, external_user: ExternalUser
    ) -> Optional[InternalUser]:
        """
        Returns a user from the database, based on the user's id from Azure.

        Parameters
        ----------
        external_user : ExternalUser
            An object representing a user with information from Azure.

        Returns
        -------
        internal_user : Optional[InternalUser]
            A user object as defined in this application. If no user is found, returns None.
        """
        encrypted_external_id = await self._encrypt_external_id(external_user)

        mongo_user = await self._users_coll.find_one(
            {"external_id": encrypted_external_id}
        )

        if mongo_user:
            return InternalUser(
                internal_id=mongo_user["internal_id"],
                external_id=mongo_user["external_id"],
                username=mongo_user["username"],
                created_at=mongo_user["created_at"],
            )

        return None

    async def get_user_by_internal_id(self, internal_id: str) -> Optional[InternalUser]:
        """
        Returns a user from the database, based on the internal id.

        Parameters
        ----------
        internal_id : str
            The unique id of the user as defined in this application

        Returns
        -------
        internal_user : Optional[InternalUser]
            A user object as defined in this application. If no user is found, returns None.
        """
        mongo_user = await self._users_coll.find_one({"_id": internal_id})

        if mongo_user:
            return InternalUser(
                internal_id=mongo_user["internal_id"],
                external_id=mongo_user["external_id"],
                username=mongo_user["username"],
                created_at=mongo_user["created_at"],
            )

        return None

    async def create_internal_user(self, external_user: ExternalUser) -> InternalUser:
        """
        Creates a internal user in the database based on the user's information from Azure.

        Parameters
        ----------
        external_user : ExternalUser
            An object representing a user with information from Azure.

        Returns
        -------
        internal_user : InternalUser
            A user object as defined in this application
        """
        encrypted_external_id = await self._encrypt_external_id(external_user)
        unique_identifier = str(uuid4())

        result = await self._users_coll.insert_one(
            dict(
                _id=unique_identifier,
                internal_id=unique_identifier,
                external_id=encrypted_external_id,
                username=external_user.username,
                created_at=datetime.datetime.utcnow(),
            )
        )

        mongo_user_id = result.inserted_id

        mongo_user = await self._users_coll.find_one({"_id": mongo_user_id})

        return InternalUser(
            internal_id=mongo_user["internal_id"],
            external_id=mongo_user["external_id"],
            username=mongo_user["username"],
            created_at=mongo_user["created_at"],
        )

    async def update_internal_user(
        self, internal_user: InternalUser
    ) -> Optional[InternalUser]:
        """
        Updates an internal user's information in the database.

        Parameters
        ----------
        internal_user : InternalUser
            A user object as defined in this application

        Returns
        -------
        internal_user : Optional[InternalUser]
            A user object as defined in this application. If no user is found, returns None.
        """
        result = await self._users_coll.update_one(
            {"internal_id": internal_user.internal_id},
            {"$set": internal_user.dict()},
        )

        if result.modified_count:
            return internal_user

        return None

    async def _encrypt_external_id(sefl, external_user: ExternalUser) -> str:
        """
        Encrypt the user id received from Azure. These ids are
        used to uniquely identify a user in the system of the external provider and
        are usually public. However, it is better to be stored encrypted just in case.

        Parameters
        ----------
        external_user : ExternalUser
            An object representing a user with information from Azure.

        Returns
        -------
        encrypted_external_id : str
            The encrypted external user id
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

        encrypted_external_id = bcrypt.using(salt=salt).hash(external_user.id)
        return encrypted_external_id


# Initialize db client
db_client = MongoClient()
