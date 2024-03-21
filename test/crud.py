from src.__main__  import app

from . import StrongboxTest


# Rendi parametrico questo test per tutte le classi in ALLOWED_CLASSES
class CrudTes(StrongboxTest):


    def setUp(self):
        self.app = app.test_client()
        self.app.post('/instances/Note', json={'params': {'title': 'Test Note', 'content': 'Test Content'}})

    def test_create_instance(self):
        response = self.app.post('/instances/Note', json={'params': {'title': 'Test Note', 'content': 'Test Content'}})
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertIn('title', data)
        self.assertEqual(data['title'], 'Test Note')

    def test_get_instance_by_id(self):
        response = self.app.get('/instances/Note/1')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('title', data)

    def test_update_instance(self):
        response = self.app.patch('/instances/Note/1', json={'title': 'Updated Title'})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('title', data)
        self.assertEqual(data['title'], 'Updated Title')

    def test_delete_instance(self):
        response = self.app.delete('/instances/Note/1')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Note with id 1 deleted successfully')
