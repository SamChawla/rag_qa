""" Define the database models for the application. """

import uuid
from sqlalchemy import Column, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from app.db import Base

class Document(Base):
    """ A document with a name and content. """
    __tablename__ = "documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now)

class Embedding(Base):
    """ An embedding for a document chunk. """
    __tablename__ = "embeddings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    chunk = Column(Text, nullable=False)
    embedding = Column(ARRAY(Text), nullable=False)  # Store as list of strings for now

class UserSelectedDocument(Base):
    """ A user-selected document. """
    __tablename__ = "user_selected_documents"
    user_id = Column(String, primary_key=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), primary_key=True)
