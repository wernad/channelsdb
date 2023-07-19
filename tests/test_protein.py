from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


class TestPDB:
    def test_stored(self, stored_pdbs):
        response = client.get(f'/pdb/{stored_pdbs}')
        assert response.status_code == 200
        json = response.json()
        assert isinstance(json, dict)
        assert 'Annotations' in json
        assert 'Channels' in json

    def test_invalid_pdbid(self):
        response = client.get('/pdb/some_invalid_pdb_id')
        assert response.status_code == 400


class TestAssembly:
    def test_stored(self, stored_pdbs):
        response = client.get(f'/assembly/{stored_pdbs}')
        assert response.status_code == 200
        assert str(response.json()).isnumeric()

    def test_invalid_pdbid(self):
        response = client.get('/assembly/some_invalid_pdb_id')
        assert response.status_code == 400


class TestAnnotations:
    def test_stored(self, stored_pdbs):
        response = client.get(f'/annotations/{stored_pdbs}')
        assert response.status_code == 200
        json = response.json()
        assert isinstance(json, dict)
        assert 'EntryAnnotations' in json
        assert 'ResidueAnnotations' in json

    def test_invalid_pdbid(self):
        response = client.get('/annotations/some_invalid_pdb_id')
        assert response.status_code == 400


class TestDownloadPNG:
    def test_stored(self, stored_pdbs):
        response = client.get(f'/download/png/{stored_pdbs}', follow_redirects=False)
        assert response.status_code in (200, 307)
        if response.status_code == 200:
            assert response.headers['content-type'] == 'image/png'

    def test_invalid_pdbid(self):
        response = client.get('/download/png/some_invalid_pdb_id')
        assert response.status_code == 400
