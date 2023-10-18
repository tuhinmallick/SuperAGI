from __future__ import annotations
import requests

from sqlalchemy import Column, Integer, String

# from superagi.models import AgentConfiguration
from superagi.models.base_model import DBBaseModel

marketplace_url = "https://app.superagi.com/api"
# marketplace_url = "http://localhost:8001"

class Vectordbs(DBBaseModel):
    """
    Represents an vector db entity.
    Attributes:
        id (int): The unique identifier of the agent.
        name (str): The name of the database.
        db_type (str): The name of the db agent.
        organisation_id (int): The identifier of the associated organisation.
    """

    __tablename__ = 'vector_dbs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    db_type = Column(String)
    organisation_id = Column(Integer)

    def __repr__(self):
        """
        Returns a string representation of the Vector db object.
        Returns:
            str: String representation of the Vector db.
        """
        return f"Vector(id={self.id}, name='{self.name}', db_type='{self.db_type}' organisation_id={self.organisation_id}, updated_at={self.updated_at})"

    @classmethod
    def get_vector_db_from_id(cls, session, vector_db_id):
        return session.query(Vectordbs).filter(Vectordbs.id == vector_db_id).first()

    @classmethod
    def fetch_marketplace_list(cls):
        headers = {'Content-Type': 'application/json'}
        response = requests.get(
            f"{marketplace_url}/vector_dbs/marketplace/list",
            headers=headers,
            timeout=10,
        )
        return response.json() if response.status_code == 200 else []

    @classmethod
    def get_vector_db_from_organisation(cls, session, organisation):
        return (
            session.query(Vectordbs)
            .filter(Vectordbs.organisation_id == organisation.id)
            .all()
        )

    @classmethod
    def add_vector_db(cls, session, name, db_type, organisation):
        vector_db = Vectordbs(name=name, db_type=db_type, organisation_id=organisation.id)
        session.add(vector_db)
        session.commit()
        return vector_db

    @classmethod
    def delete_vector_db(cls, session, vector_db_id):
        session.query(Vectordbs).filter(Vectordbs.id == vector_db_id).delete()
        session.commit()