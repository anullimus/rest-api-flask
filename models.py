from app import sa, session, Base

class Inventory(Base):
    __tablename__ = 'inventory'
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(100), nullable=False)
    description = sa.Column(sa.String(500), nullable=False)