# 🏗️ Code Templates for Bifrost Trader

## 🎯 **Microservice Template**

### **Service Structure**
```
services/[service-name]/
├── __init__.py
├── main.py                 # FastAPI application
├── models/
│   ├── __init__.py
│   └── [service]_models.py # SQLAlchemy models
├── api/
│   ├── __init__.py
│   ├── endpoints/
│   │   ├── __init__.py
│   │   └── [resource].py   # API endpoints
│   └── dependencies.py     # FastAPI dependencies
├── services/
│   ├── __init__.py
│   └── [service]_service.py # Business logic
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_endpoints.py
│   └── test_services.py
├── requirements.txt
└── README.md
```

### **main.py Template**
```python
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .api.dependencies import get_database
from .api.endpoints import [resource]
from .services.[service]_service import [Service]Service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting [Service Name] Service")
    yield
    # Shutdown
    logger.info("Shutting down [Service Name] Service")

app = FastAPI(
    title="[Service Name] Service",
    description="[Service Description]",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router([resource].router, prefix="/api/v1/[resource]", tags=["[resource]"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "[service-name]"}

@app.get("/")
async def root():
    return {"message": "[Service Name] Service", "version": "1.0.0"}
```

## 🔌 **API Endpoints Template**

### **Endpoint Structure**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from ...models.[service]_models import [Model]
from ...api.dependencies import get_database
from ...services.[service]_service import [Service]Service
from ...schemas.[service]_schemas import [Model]Create, [Model]Update, [Model]Response

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[[Model]Response])
async def get_[resources](
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_database)
):
    """Get all [resources]"""
    try:
        service = [Service]Service(db)
        return service.get_[resources](skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Error getting [resources]: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/{id}", response_model=[Model]Response)
async def get_[resource](id: int, db: Session = Depends(get_database)):
    """Get [resource] by ID"""
    try:
        service = [Service]Service(db)
        [resource] = service.get_[resource](id)
        if not [resource]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="[Resource] not found"
            )
        return [resource]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting [resource] {id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/", response_model=[Model]Response)
async def create_[resource](
    [resource]_data: [Model]Create,
    db: Session = Depends(get_database)
):
    """Create new [resource]"""
    try:
        service = [Service]Service(db)
        return service.create_[resource]([resource]_data)
    except Exception as e:
        logger.error(f"Error creating [resource]: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.put("/{id}", response_model=[Model]Response)
async def update_[resource](
    id: int,
    [resource]_data: [Model]Update,
    db: Session = Depends(get_database)
):
    """Update [resource]"""
    try:
        service = [Service]Service(db)
        [resource] = service.update_[resource](id, [resource]_data)
        if not [resource]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="[Resource] not found"
            )
        return [resource]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating [resource] {id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.delete("/{id}")
async def delete_[resource](id: int, db: Session = Depends(get_database)):
    """Delete [resource]"""
    try:
        service = [Service]Service(db)
        success = service.delete_[resource](id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="[Resource] not found"
            )
        return {"message": "[Resource] deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting [resource] {id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
```

## 🗄️ **Database Models Template**

### **SQLAlchemy Model Template**
```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional

from shared.database.connection import Base

class [Model](Base):
    """[Model Description]"""
    
    __tablename__ = "[table_name]"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Required fields
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Optional fields
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Foreign keys
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    # user = relationship("User", back_populates="[related_field]")
    
    def __repr__(self):
        return f"<[Model](id={self.id}, name='{self.name}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
```

### **TimescaleDB Model Template**
```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional

from shared.database.connection import Base

class [TimeSeriesModel](Base):
    """[Model Description] - TimescaleDB Hypertable"""
    
    __tablename__ = "[table_name]"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Time field (required for TimescaleDB)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Symbol reference
    symbol_id = Column(Integer, ForeignKey("market_symbol.id"), nullable=False, index=True)
    
    # Time-series data fields
    open_price = Column(Numeric(10, 4), nullable=False)
    high_price = Column(Numeric(10, 4), nullable=False)
    low_price = Column(Numeric(10, 4), nullable=False)
    close_price = Column(Numeric(10, 4), nullable=False)
    volume = Column(Integer, nullable=False)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    symbol = relationship("MarketSymbol", back_populates="[related_field]")
    
    def __repr__(self):
        return f"<[TimeSeriesModel](id={self.id}, symbol_id={self.symbol_id}, timestamp='{self.timestamp}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "symbol_id": self.symbol_id,
            "open_price": float(self.open_price) if self.open_price else None,
            "high_price": float(self.high_price) if self.high_price else None,
            "low_price": float(self.low_price) if self.low_price else None,
            "close_price": float(self.close_price) if self.close_price else None,
            "volume": self.volume,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
```

## 🧪 **Test Templates**

### **Unit Test Template**
```python
import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from ..models.[service]_models import [Model]
from ..services.[service]_service import [Service]Service
from ..schemas.[service]_schemas import [Model]Create, [Model]Update

class Test[Service]Service:
    """Test cases for [Service]Service"""
    
    @pytest.fixture
    def mock_db(self):
        """Mock database session"""
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self, mock_db):
        """Service instance with mocked database"""
        return [Service]Service(mock_db)
    
    @pytest.fixture
    def sample_[resource]_data(self):
        """Sample [resource] data"""
        return [Model]Create(
            name="Test [Resource]",
            description="Test description"
        )
    
    def test_create_[resource](self, service, mock_db, sample_[resource]_data):
        """Test creating a [resource]"""
        # Arrange
        mock_[resource] = Mock(spec=[Model])
        mock_[resource].id = 1
        mock_[resource].name = "Test [Resource]"
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        # Act
        result = service.create_[resource](sample_[resource]_data)
        
        # Assert
        assert result is not None
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
    
    def test_get_[resource](self, service, mock_db):
        """Test getting a [resource] by ID"""
        # Arrange
        mock_[resource] = Mock(spec=[Model])
        mock_[resource].id = 1
        mock_[resource].name = "Test [Resource]"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_[resource]
        
        # Act
        result = service.get_[resource](1)
        
        # Assert
        assert result is not None
        assert result.id == 1
        assert result.name == "Test [Resource]"
    
    def test_get_[resource]_not_found(self, service, mock_db):
        """Test getting a non-existent [resource]"""
        # Arrange
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Act
        result = service.get_[resource](999)
        
        # Assert
        assert result is None
```

## 📋 **Schema Templates**

### **Pydantic Schema Template**
```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class [Model]Base(BaseModel):
    """Base schema for [Model]"""
    name: str = Field(..., min_length=1, max_length=255, description="[Resource] name")
    description: Optional[str] = Field(None, description="[Resource] description")
    is_active: bool = Field(True, description="Whether [resource] is active")

class [Model]Create([Model]Base):
    """Schema for creating [Model]"""
    pass

class [Model]Update(BaseModel):
    """Schema for updating [Model]"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None

class [Model]Response([Model]Base):
    """Schema for [Model] response"""
    id: int = Field(..., description="[Resource] ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True
```

## 🎯 **Usage Guidelines**

### **Template Customization**
1. **Replace Placeholders**: Replace `[Service]`, `[Model]`, `[resource]` with actual names
2. **Add Specific Fields**: Add service-specific fields and logic
3. **Customize Validation**: Add specific validation rules
4. **Update Relationships**: Define proper database relationships
5. **Add Business Logic**: Implement service-specific business logic

### **Best Practices**
1. **Follow Patterns**: Use established patterns from existing services
2. **Add Tests**: Always include comprehensive tests
3. **Document Code**: Add clear docstrings and comments
4. **Handle Errors**: Implement proper error handling
5. **Validate Input**: Use Pydantic for input validation

---

**Remember**: These templates are starting points. Customize them for your specific service needs and always follow the patterns established in your knowledge base.
