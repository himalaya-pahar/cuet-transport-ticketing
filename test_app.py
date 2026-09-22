import unittest
from fastapi.testclient import TestClient
from main import app
from database import get_db, SessionLocal
from security import hashing
import models

client = TestClient(app)


class TestCUETTransportAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup test entities if not already in DB
        db = SessionLocal()
        try:
            # Ensure test admin
            admin = db.query(models.Admin).filter(models.Admin.username == "testadmin").first()
            if not admin:
                admin = models.Admin(
                    username="testadmin",
                    name="Test Admin",
                    email="testadmin@cuet.ac.bd",
                    password=hashing.hash_password("adminpass123")
                )
                db.add(admin)

            # Ensure test bus
            bus = db.query(models.Bus).filter(models.Bus.name == "Karnafuli").first()
            if not bus:
                bus = models.Bus(
                    name="Karnafuli",
                    route="Campus to Bahaddarhat",
                    password=hashing.hash_password("buspass123"),
                    is_active=True
                )
                db.add(bus)

            # Ensure test teacher
            teacher = db.query(models.Teacher).filter(models.Teacher.id == 9999).first()
            if not teacher:
                teacher = models.Teacher(
                    id=9999,
                    name="Prof. Test User",
                    department="CSE",
                    email="proftest@cuet.ac.bd",
                    phone="01700000000",
                    is_active=True
                )
                db.add(teacher)

            db.commit()
        finally:
            db.close()

    def test_01_health_check(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "online")

    def test_02_login_admin_and_bus(self):
        # 1. Admin login
        admin_res = client.post(
            "/login/admin",
            data={"username": "testadmin", "password": "adminpass123"}
        )
        self.assertEqual(admin_res.status_code, 200)
        admin_data = admin_res.json()
        self.assertIn("access_token", admin_data)
        self.assertEqual(admin_data["role"], "admin")

        # 2. Bus login
        bus_res = client.post(
            "/login/bus",
            data={"username": "Karnafuli", "password": "buspass123"}
        )
        self.assertEqual(bus_res.status_code, 200)
        bus_data = bus_res.json()
        self.assertIn("access_token", bus_data)
        self.assertEqual(bus_data["role"], "bus")

        # 3. Unified login test (Admin)
        uni_admin = client.post("/login", data={"username": "testadmin", "password": "adminpass123"})
        self.assertEqual(uni_admin.status_code, 200)
        self.assertEqual(uni_admin.json()["role"], "admin")

        # 4. Unified login test (Bus)
        uni_bus = client.post("/login", data={"username": "Karnafuli", "password": "buspass123"})
        self.assertEqual(uni_bus.status_code, 200)
        self.assertEqual(uni_bus.json()["role"], "bus")

    def test_03_role_authorization_enforcement(self):
        # Bus tries to view admins (should be forbidden)
        bus_res = client.post(
            "/login/bus",
            data={"username": "Karnafuli", "password": "buspass123"}
        )
        bus_token = bus_res.json()["access_token"]
        res = client.get("/admin/", headers={"Authorization": f"Bearer {bus_token}"})
        self.assertEqual(res.status_code, 403)

        # Admin tries to view admins (should succeed)
        admin_res = client.post(
            "/login/admin",
            data={"username": "testadmin", "password": "adminpass123"}
        )
        admin_token = admin_res.json()["access_token"]
        res = client.get("/admin/", headers={"Authorization": f"Bearer {admin_token}"})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

    def test_04_teacher_operations(self):
        admin_res = client.post(
            "/login/admin",
            data={"username": "testadmin", "password": "adminpass123"}
        )
        admin_token = admin_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {admin_token}"}

        # View teachers
        res = client.get("/teacher/", headers=headers)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(res.json()) > 0)

        # View single teacher
        res = client.get("/teacher/9999", headers=headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["name"], "Prof. Test User")

    def test_05_bus_scan_and_debounce(self):
        bus_res = client.post(
            "/login/bus",
            data={"username": "Karnafuli", "password": "buspass123"}
        )
        bus_token = bus_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {bus_token}"}

        # Clean old scans for teacher 9999 to test
        db = SessionLocal()
        db.query(models.Logs).filter(models.Logs.teacher_id == 9999).delete()
        db.commit()
        db.close()

        # 1. Successful scan
        scan_res = client.post("/scan/", json={"teacher_id": 9999}, headers=headers)
        self.assertEqual(scan_res.status_code, 201)
        data = scan_res.json()
        self.assertEqual(data["teacher_id"], 9999)
        self.assertEqual(data["bus_name"], "Karnafuli")

        # 2. Immediate double-tap (should return 400 debounce error)
        double_scan = client.post("/scan/", json={"teacher_id": 9999}, headers=headers)
        self.assertEqual(double_scan.status_code, 400)
        self.assertIn("Duplicate scan", double_scan.json()["detail"])

    def test_06_bill_endpoints(self):
        admin_res = client.post(
            "/login/admin",
            data={"username": "testadmin", "password": "adminpass123"}
        )
        admin_token = admin_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {admin_token}"}

        # Trigger bill generation
        gen_res = client.post("/bill/generate", headers=headers)
        self.assertEqual(gen_res.status_code, 200)
        self.assertIn("bills_generated", gen_res.json())

        # View bills
        bills_res = client.get("/bill/", headers=headers)
        self.assertEqual(bills_res.status_code, 200)
        self.assertIsInstance(bills_res.json(), list)


if __name__ == "__main__":
    unittest.main()
