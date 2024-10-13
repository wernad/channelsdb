from sqlmodel import Session, select
from database.models import Tunnel


def find_channel_by_structure_id(session: Session, structure_id: str):
    statement = select(Tunnel).where(Tunnel.structure_id == structure_id)
    tunnel = session.exec(statement).first()
    return tunnel
