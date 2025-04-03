""" This module contains the Pydantic models for the API requests and responses. """

from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    """ Request model for querying documents. """
    user_id: str
    question: str

class SelectDocumentsRequest(BaseModel):
    """ Request model for selecting documents. """
    user_id: str
    document_ids: List[str]