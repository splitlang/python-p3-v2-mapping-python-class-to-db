from department import Department
from __init__ import CURSOR, CONN
import unittest


class TestDepartmentORM(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Department.drop_table()
        Department.create_table()

    def setUp(self):
        CURSOR.execute("DELETE FROM departments")
        CONN.commit()

    def test_create_table(self):
        Department.create_table()
        result = CURSOR.execute("PRAGMA table_info(departments)").fetchall()
        self.assertEqual(len(result), 3)

    def test_drop_table(self):
        Department.drop_table()
        result = CURSOR.execute("PRAGMA table_info(departments)").fetchall()
        self.assertEqual(len(result), 0)
        Department.create_table()  # Recreate the table for other tests

    def test_save(self):
        department = Department("Finance", "Building 1")
        department.save()
        self.assertIsNotNone(department.id)

    def test_create(self):
        department = Department.create("IT", "Building 2")
        self.assertIsNotNone(department.id)
        self.assertEqual(department.name, "IT")
        self.assertEqual(department.location, "Building 2")

    def test_update(self):
        department = Department.create("IT", "Building 2")
        department.name = "Information Technology"
        department.location = "Building 3"
        department.update()
        updated_department = CURSOR.execute("SELECT * FROM departments WHERE id = ?", (department.id,)).fetchone()
        self.assertEqual(updated_department[1], "Information Technology")
        self.assertEqual(updated_department[2], "Building 3")

    def test_delete(self):
        department = Department.create("HR", "Building 4")
        department_id = department.id
        department.delete()
        result = CURSOR.execute("SELECT * FROM departments WHERE id = ?", (department_id,)).fetchone()
