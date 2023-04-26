import uuid

from fastapi import APIRouter, HTTPException

from app.models.common import Message
from app.models.consultants import Consultant, ConsultantCreate, ConsultantList
from app.utils.neo4j_connect import Neo4jConnection

consultants_router = APIRouter(prefix="/consultants", tags=["Consultants"])


@consultants_router.get("/")
async def list_all_consultants() -> ConsultantList:
    """
    List all consultants sorted alphabetically by name.

    Returns
    -------
    ConsultantList
    """
    conn = Neo4jConnection()

    query = """
    MATCH (c:Consultant)
    UNWIND c as consultants
    WITH COLLECT(DISTINCT {name: c.name, type: labels(c)[0], email: c.email}) as consultantsOut
    RETURN consultantsOut
    """

    result = conn.query(query)

    conn.close()

    consultants = result[0][0]
    consultants.sort(key=lambda x: x["name"])

    return ConsultantList(items=consultants)


@consultants_router.get("/{consultant_email}")
async def get_consultant(consultant_email: str) -> Consultant:
    """
    Returns a single consultant using their email.

    Parameters
    ----------
    consultant_email : str
        The email of the consultant to return

    Returns
    -------
    Consultant

    Raises
    ------
    HTTPException
        404 if the consultant is not found
    """
    query = """
    MATCH (c:Consultant {email: $email})
    WITH {name: c.name, type: labels(c)[0], email: c.email} as consultantOut
    RETURN consultantOut
    """

    conn = Neo4jConnection()
    result = conn.query(query, email=consultant_email)
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Consultant not found")

    return result[0][0]


@consultants_router.post("/")
async def create_consultant(consultant: ConsultantCreate) -> Consultant:
    """
    Add a new consultant to the database.

    Parameters
    ----------
    consultant : ConsultantCreate
        The consultant to add

    Returns
    -------
    Consultant
    """
    conn = Neo4jConnection()
    exists_query = """
    MATCH (s:Consultant {email: $email})
    RETURN s
    """
    result = conn.query(exists_query, email=consultant.email)
    conn.close()
    if result:
        raise HTTPException(status_code=409, detail="Consultant already exists")

    query = """
    MERGE (c:Consultant {uid: $uid, name: $name, email: $email})
    WITH {name: c.name, type: labels(c)[0], email: c.email} as consultantOut
    RETURN consultantOut
    """
    conn = Neo4jConnection()
    result = conn.query(
        query, uid=str(uuid.uuid4()), name=consultant.name, email=consultant.email
    )
    conn.close()

    return result[0][0]


@consultants_router.delete("/{consultant_email}")
async def delete_consultant(consultant_email: str) -> Message:
    """
    Deletes a consultant from the database.

    Parameters
    ----------
    consultant_email : str
        The email of the consultant to delete

    Returns
    -------
    Message

    Raises
    ------
    HTTPException
        404 if the consultant is not found
    """
    query = """
    MATCH (c:Consultant {email: $email})
    WITH c, {name: c.name, type: labels(c)[0], email: c.email} as consultantOut
    DETACH DELETE c
    RETURN consultantOut
    """
    conn = Neo4jConnection()
    result = conn.query(query, email=consultant_email)
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Consultant not found")

    return Message(message=f"Deleted consultant {consultant_email}")
