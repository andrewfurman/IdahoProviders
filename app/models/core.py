
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

__all__ = ['Network', 'County', 'Hospital', 'CountyNetwork', 'HospitalNetwork']

class TimestampMixin:
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

class Network(TimestampMixin, Base):
    __tablename__ = "network"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    code = Column(String(8), nullable=False, unique=True)

    county_links = relationship("CountyNetwork", cascade="all, delete-orphan", passive_deletes=True)
    hospital_links = relationship("HospitalNetwork", cascade="all, delete-orphan", passive_deletes=True)

class County(TimestampMixin, Base):
    __tablename__ = "county"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

class Hospital(TimestampMixin, Base):
    __tablename__ = "hospital"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)

class CountyNetwork(Base):
    __tablename__ = "county_network"
    id = Column(Integer, primary_key=True)
    county_id = Column(Integer, ForeignKey("county.id", ondelete="CASCADE"), nullable=False)
    network_id = Column(Integer, ForeignKey("network.id", ondelete="CASCADE"), nullable=False)

class HospitalNetwork(Base):
    __tablename__ = "hospital_network"
    id = Column(Integer, primary_key=True)
    hospital_id = Column(Integer, ForeignKey("hospital.id", ondelete="CASCADE"), nullable=False)
    network_id = Column(Integer, ForeignKey("network.id", ondelete="CASCADE"), nullable=False)
    effective_date = Column(Date)
    status = Column(String(40))
