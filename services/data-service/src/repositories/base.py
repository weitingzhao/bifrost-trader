"""
Base repository class for Data Service - Repository Pattern Implementation

This module provides the base repository class with common database operations,
following FastAPI best practices with async support.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy import and_, desc, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType], ABC):
    """Base repository class with common database operations."""

    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        """
        Initialize repository with model and database session.
        
        Args:
            model: SQLAlchemy model class
            db_session: Async database session
        """
        self.model = model
        self.db = db_session

    async def get_by_id(self, id: Union[int, str]) -> Optional[ModelType]:
        """
        Get a record by its ID.
        
        Args:
            id: Record ID
            
        Returns:
            Model instance or None if not found
        """
        try:
            query = select(self.model).where(self.model.id == id)
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting {self.model.__name__} by ID {id}: {e}")
            raise

    async def get_by_field(self, field_name: str, value: Any) -> Optional[ModelType]:
        """
        Get a record by a specific field value.
        
        Args:
            field_name: Field name to search by
            value: Field value to search for
            
        Returns:
            Model instance or None if not found
        """
        try:
            field = getattr(self.model, field_name)
            query = select(self.model).where(field == value)
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting {self.model.__name__} by {field_name}={value}: {e}")
            raise

    async def get_many(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        order_desc: bool = False,
        include_relationships: Optional[List[str]] = None
    ) -> List[ModelType]:
        """
        Get multiple records with pagination and filtering.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Dictionary of field filters
            order_by: Field name to order by
            order_desc: Whether to order in descending order
            include_relationships: List of relationships to include
            
        Returns:
            List of model instances
        """
        try:
            query = select(self.model)
            
            # Add relationship loading
            if include_relationships:
                for rel in include_relationships:
                    if hasattr(self.model, rel):
                        query = query.options(selectinload(getattr(self.model, rel)))
            
            # Add filters
            if filters:
                conditions = []
                for field_name, value in filters.items():
                    if hasattr(self.model, field_name):
                        field = getattr(self.model, field_name)
                        if isinstance(value, list):
                            conditions.append(field.in_(value))
                        elif isinstance(value, dict):
                            # Support for range queries like {"gte": 100, "lte": 200}
                            for op, op_value in value.items():
                                if op == "gte":
                                    conditions.append(field >= op_value)
                                elif op == "lte":
                                    conditions.append(field <= op_value)
                                elif op == "gt":
                                    conditions.append(field > op_value)
                                elif op == "lt":
                                    conditions.append(field < op_value)
                                elif op == "like":
                                    conditions.append(field.like(f"%{op_value}%"))
                        else:
                            conditions.append(field == value)
                
                if conditions:
                    query = query.where(and_(*conditions))
            
            # Add ordering
            if order_by and hasattr(self.model, order_by):
                field = getattr(self.model, order_by)
                if order_desc:
                    query = query.order_by(desc(field))
                else:
                    query = query.order_by(field)
            
            # Add pagination
            query = query.offset(skip).limit(limit)
            
            result = await self.db.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Error getting multiple {self.model.__name__} records: {e}")
            raise

    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count records with optional filtering.
        
        Args:
            filters: Dictionary of field filters
            
        Returns:
            Number of matching records
        """
        try:
            query = select(func.count(self.model.id))
            
            # Add filters
            if filters:
                conditions = []
                for field_name, value in filters.items():
                    if hasattr(self.model, field_name):
                        field = getattr(self.model, field_name)
                        if isinstance(value, list):
                            conditions.append(field.in_(value))
                        elif isinstance(value, dict):
                            # Support for range queries
                            for op, op_value in value.items():
                                if op == "gte":
                                    conditions.append(field >= op_value)
                                elif op == "lte":
                                    conditions.append(field <= op_value)
                                elif op == "gt":
                                    conditions.append(field > op_value)
                                elif op == "lt":
                                    conditions.append(field < op_value)
                                elif op == "like":
                                    conditions.append(field.like(f"%{op_value}%"))
                        else:
                            conditions.append(field == value)
                
                if conditions:
                    query = query.where(and_(*conditions))
            
            result = await self.db.execute(query)
            return result.scalar()
            
        except Exception as e:
            logger.error(f"Error counting {self.model.__name__} records: {e}")
            raise

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.
        
        Args:
            obj_in: Pydantic schema with data to create
            
        Returns:
            Created model instance
        """
        try:
            # Convert Pydantic model to dict, excluding unset fields
            obj_data = obj_in.dict(exclude_unset=True)
            
            # Create SQLAlchemy model instance
            db_obj = self.model(**obj_data)
            
            # Add to session
            self.db.add(db_obj)
            await self.db.flush()  # Flush to get the ID
            await self.db.refresh(db_obj)
            
            return db_obj
            
        except Exception as e:
            logger.error(f"Error creating {self.model.__name__}: {e}")
            await self.db.rollback()
            raise

    async def create_many(self, objs_in: List[CreateSchemaType]) -> List[ModelType]:
        """
        Create multiple records in bulk.
        
        Args:
            objs_in: List of Pydantic schemas with data to create
            
        Returns:
            List of created model instances
        """
        try:
            db_objs = []
            
            for obj_in in objs_in:
                obj_data = obj_in.dict(exclude_unset=True)
                db_obj = self.model(**obj_data)
                db_objs.append(db_obj)
            
            # Add all to session
            self.db.add_all(db_objs)
            await self.db.flush()
            
            # Refresh all objects
            for db_obj in db_objs:
                await self.db.refresh(db_obj)
            
            return db_objs
            
        except Exception as e:
            logger.error(f"Error creating multiple {self.model.__name__} records: {e}")
            await self.db.rollback()
            raise

    async def update(
        self,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update an existing record.
        
        Args:
            db_obj: Existing model instance
            obj_in: Pydantic schema or dict with update data
            
        Returns:
            Updated model instance
        """
        try:
            # Convert to dict if it's a Pydantic model
            if hasattr(obj_in, 'dict'):
                update_data = obj_in.dict(exclude_unset=True)
            else:
                update_data = obj_in
            
            # Update fields
            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            
            await self.db.flush()
            await self.db.refresh(db_obj)
            
            return db_obj
            
        except Exception as e:
            logger.error(f"Error updating {self.model.__name__}: {e}")
            await self.db.rollback()
            raise

    async def delete(self, db_obj: ModelType) -> bool:
        """
        Delete a record.
        
        Args:
            db_obj: Model instance to delete
            
        Returns:
            True if deleted successfully
        """
        try:
            await self.db.delete(db_obj)
            await self.db.flush()
            return True
            
        except Exception as e:
            logger.error(f"Error deleting {self.model.__name__}: {e}")
            await self.db.rollback()
            raise

    async def delete_by_id(self, id: Union[int, str]) -> bool:
        """
        Delete a record by ID.
        
        Args:
            id: Record ID to delete
            
        Returns:
            True if deleted successfully
        """
        try:
            query = select(self.model).where(self.model.id == id)
            result = await self.db.execute(query)
            db_obj = result.scalar_one_or_none()
            
            if db_obj:
                await self.db.delete(db_obj)
                await self.db.flush()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error deleting {self.model.__name__} by ID {id}: {e}")
            await self.db.rollback()
            raise

    async def exists(self, filters: Dict[str, Any]) -> bool:
        """
        Check if a record exists with given filters.
        
        Args:
            filters: Dictionary of field filters
            
        Returns:
            True if record exists
        """
        try:
            query = select(func.count(self.model.id))
            
            conditions = []
            for field_name, value in filters.items():
                if hasattr(self.model, field_name):
                    field = getattr(self.model, field_name)
                    conditions.append(field == value)
            
            if conditions:
                query = query.where(and_(*conditions))
            
            result = await self.db.execute(query)
            count = result.scalar()
            
            return count > 0
            
        except Exception as e:
            logger.error(f"Error checking existence of {self.model.__name__}: {e}")
            raise

    async def commit(self):
        """Commit the current transaction."""
        try:
            await self.db.commit()
        except Exception as e:
            logger.error(f"Error committing transaction: {e}")
            await self.db.rollback()
            raise

    async def rollback(self):
        """Rollback the current transaction."""
        try:
            await self.db.rollback()
        except Exception as e:
            logger.error(f"Error rolling back transaction: {e}")
            raise

