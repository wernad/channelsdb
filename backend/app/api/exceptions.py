from fastapi import HTTPException


class ProteinNotFound(HTTPException):
    def __init__(self, protein_id: str):
        self.status_code = 404
        self.detail = f"Protein with ID '{protein_id}' not found in ChannelsDB."


class UnsupportedDBType(HTTPException):
    def __init__(self, db_type: str):
        self.status_code = 400
        self.detail = f"Database type {db_type} is not supported."
