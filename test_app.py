import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Team, Player

manager = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9ZdjBUS081MDk5bm04RG0zRVY0cCJ9.eyJpc3MiOiJodHRwczovL2Rldi1uZmZrbXY5NS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY1ZTY0N2VjMGU1OWUwMDc2ZjE3OGE4IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MDE2MTc5ODAsImV4cCI6MTYwMTYyNTE4MCwiYXpwIjoiUlFVRHVhNjl4dkU4NjdLUmJHa1JLMDZqdTc3QTZJNUsiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTpwbGF5ZXJzIiwiY3JlYXRlOnRlYW1zIiwiZGVsZXRlOnBsYXllcnMiLCJkZWxldGU6dGVhbXMiLCJlZGl0OnBsYXllcnMiLCJlZGl0OnRlYW1zIl19.NzXeDpA2deIqEOGkY9U3j3Xxat8iCKTMHRdtI85q-UoKGXVP1Vja7Kx36asrk_nYfgNlZeKOU-KqdbTQgNnDxXYe2Ep02Zam_wZNNKU5NWfoLLWlNIm1WOn3TJ4SSuzrBJO1GsYCRCh11-erlr0suo3Me9Vo9_KjDRyijBJNAqo6acJcush1feDC-Xjvgd0iNtmMfBCx1FC517_qMBlHz8-aVC4zp8fGGyrl13eLS2dPhUL9pkGzLwj5Xs2VFl6OFSjotmErMjePsxZ1HabnExIkm8gsKKLZHDP7jXQb3B5WlGNxwS9t5JrriJaAiCuAbKLMuq9TlntpemBWezh8Qg'

coach = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9ZdjBUS081MDk5bm04RG0zRVY0cCJ9.eyJpc3MiOiJodHRwczovL2Rldi1uZmZrbXY5NS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY3NGJkZDliYmJkODIwMDY4NjliNDQ4IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MDE2MTk0NTMsImV4cCI6MTYwMTYyNjY1MywiYXpwIjoiUlFVRHVhNjl4dkU4NjdLUmJHa1JLMDZqdTc3QTZJNUsiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTpwbGF5ZXJzIiwiZGVsZXRlOnBsYXllcnMiLCJlZGl0OnBsYXllcnMiXX0.E3W8sS5gPz7nTkNcXX7do5FIfogalbpJtIpV9ZP2VYGasqa5qDmwnUAgLnMcXnNudiI1Vh-0wVF7Sgulls-pRmK36k-mxcrKuJQofmYxporJKMwkEJInTVjIh32Res92VBDMiJ1n6r5AU-LAd-m9XeeP6xfKyjHlHOgb1Jmyp_hxj7pb-4H7uJ8GcgihPnkuUCOdejHxM2c-VX3fmf3_3HG30uC_p_qVm5D31_XxqL0hWB0U87T1_11WzNO7WDKQ7RZMkU4V7GfKEdbsX9KsWkBuzHONo7ceewtRVhJFn58QQgvXSP7AnOapA7GD5SiwjZmaVwt1h9bbYSbeHOQyPw'
class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = "postgresql://postgres:password@localhost:5432/capstone"
        self.manager = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9ZdjBUS081MDk5bm04RG0zRVY0cCJ9.eyJpc3MiOiJodHRwczovL2Rldi1uZmZrbXY5NS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY1ZTY0N2VjMGU1OWUwMDc2ZjE3OGE4IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MDE2NDg0MDEsImV4cCI6MTYwMTY1NTYwMSwiYXpwIjoiUlFVRHVhNjl4dkU4NjdLUmJHa1JLMDZqdTc3QTZJNUsiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTpwbGF5ZXJzIiwiY3JlYXRlOnRlYW1zIiwiZGVsZXRlOnBsYXllcnMiLCJkZWxldGU6dGVhbXMiLCJlZGl0OnBsYXllcnMiLCJlZGl0OnRlYW1zIl19.VZg3DBV6GVzujOYdlWFjSqAOAnzujRLizFB-n3cYjDJ73epjFz-MOe7UURMOAXcao6qgdqa0DTc02W_AFZs-FfsvOc3k71qVkAqcL76VpABegIfdiy4Gmtsq7GHuAmI4J3UReol7nEvJjHWfZ6nXA3Hy_lvP5mJE2teEXcZjBrvFZELEkbCn7H4Y_75FOOIvycOaPT04c171fMvYC1CU828RFqC1a_-aqomGT1q1-MKscbSZKgDGtC_ryqeF2RnHoA_pI0J3y_RkXgt-Jtdn9dbroWZbkXlUxHFjeQhtQtUEaH4SPxnPiSf9GHCuVb36wrwOTEOaKJ9DS9-08j76gQ'

        self.coach = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9ZdjBUS081MDk5bm04RG0zRVY0cCJ9.eyJpc3MiOiJodHRwczovL2Rldi1uZmZrbXY5NS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY3NGJkZDliYmJkODIwMDY4NjliNDQ4IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MDE2MTk0NTMsImV4cCI6MTYwMTYyNjY1MywiYXpwIjoiUlFVRHVhNjl4dkU4NjdLUmJHa1JLMDZqdTc3QTZJNUsiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTpwbGF5ZXJzIiwiZGVsZXRlOnBsYXllcnMiLCJlZGl0OnBsYXllcnMiXX0.E3W8sS5gPz7nTkNcXX7do5FIfogalbpJtIpV9ZP2VYGasqa5qDmwnUAgLnMcXnNudiI1Vh-0wVF7Sgulls-pRmK36k-mxcrKuJQofmYxporJKMwkEJInTVjIh32Res92VBDMiJ1n6r5AU-LAd-m9XeeP6xfKyjHlHOgb1Jmyp_hxj7pb-4H7uJ8GcgihPnkuUCOdejHxM2c-VX3fmf3_3HG30uC_p_qVm5D31_XxqL0hWB0U87T1_11WzNO7WDKQ7RZMkU4V7GfKEdbsX9KsWkBuzHONo7ceewtRVhJFn58QQgvXSP7AnOapA7GD5SiwjZmaVwt1h9bbYSbeHOQyPw'

        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.drop_all()
            self.db.create_all()


    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_teams(self):

        response = self.client().get('/teams')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_teams2(self):
        response = self.client().get('/teams', headers={'Authorization':'Bearer ' + self.manager})
        self.assertEqual(response.status_code, 200)

    def test_create_delete_player(self):


        create_response = self.client().post('/players', headers={'Authorization':'Bearer ' + self.manager},
        json = {
                "first_name": "Kobe",
                "last_name": "Bryant",
                "image": "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.wb9Mi7pfm_e_yO88jzb4KAHaE8%26pid%3DApi&f=1",
                "team_id": 21,
                "number": "24",
                "position": "SG"
                })


        # response = self.client().delete('/questions/{}'.format(question.id))
        # data = json.loads(response.data)


        # question = Question.query.filter(Question.id == question.id).one_or_none()


        self.assertEqual(create_response.status_code, 200)



        self.assertEqual(question, None)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
