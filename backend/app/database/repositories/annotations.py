from sqlmodel import Session, select

from app.database.models import Annotation


class AnnotationsRepository:
    def find_annotations_by_channel_id(self, session: Session, channel_id: int):
        statement = select(Annotation).where(Annotation.channel_id == channel_id)
        annotations = session.exec(statement).all()
        return annotations
