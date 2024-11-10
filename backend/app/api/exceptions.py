from fastapi import HTTPException


class ProteinNotFound(HTTPException):
    def __init__(self, protein_id: str):
        self.status_code = 404
        self.detail = f"Protein with ID '{protein_id}' not found in ChannelsDB."


class UnknownFileType(HTTPException):
    def __init__(self, file_type: str):
        self.status_code = 404
        self.detail = f"File type {file_type} not found."
