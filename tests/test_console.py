#!/usr/bin/python3
import unittest
from unittest.mock import patch
from io import StringIO
import os
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User

class TestConsole(unittest.TestCase):
    """Test cases for the console module"""

    @classmethod
    def setUpClass(cls):
        """Set up the console for testing"""
        cls.console = HBNBCommand()

    def setUp(self):
        """Set up for each test"""
        self.console.preloop()

    def tearDown(self):
        """Tear down after each test"""
        self.console.postcmd(False, '')

    @classmethod
    def tearDownClass(cls):
        """Clean up resources after all tests"""
        del cls.console

    def test_emptyline(self):
        """Test Cases for empty line"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("\n")
            self.assertEqual('', f.getvalue())

    def test_create(self):
        """Test Cases for do_create"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel\n")
            output = f.getvalue().strip()
            self.assertTrue(len(output) == 36)  # UUID length

            # Test creating an instance with parameters
            self.console.onecmd('create User email="test@test.com" password="pass"\n')
            output = f.getvalue().strip()
            self.assertTrue(len(output) == 36)  # UUID length

    def test_show(self):
        """Test Cases for do_show"""
        with patch('sys.stdout', new=StringIO()) as f:
            # Create an instance
            self.console.onecmd("create BaseModel\n")
            uuid = f.getvalue().strip()

            # Test showing an instance
            self.console.onecmd(f"show BaseModel {uuid}\n")
            output = f.getvalue().strip()
            self.assertTrue(f"BaseModel {uuid}" in output)

            # Test showing with invalid class
            self.console.onecmd("show InvalidClass 123\n")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class doesn't exist **")

            # Test showing with invalid instance ID
            self.console.onecmd("show BaseModel invalid_id\n")
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

    def test_all(self):
        """Test Cases for do_all"""
        with patch('sys.stdout', new=StringIO()) as f:
            # Create instances
            self.console.onecmd("create BaseModel\n")
            self.console.onecmd("create User\n")
            self.console.onecmd("create BaseModel\n")

            # Test showing all instances of a class
            self.console.onecmd("all BaseModel\n")
            output = f.getvalue().strip()
            self.assertTrue("BaseModel" in output)
            self.assertTrue(output.count("BaseModel") == 2)

            # Test showing all instances with invalid class
            self.console.onecmd("all InvalidClass\n")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class doesn't exist **")

    def test_destroy(self):
        """Test Cases for do_destroy"""
        with patch('sys.stdout', new=StringIO()) as f:
            # Create an instance
            self.console.onecmd("create BaseModel\n")
            uuid = f.getvalue().strip()

            # Test destroying an instance
            self.console.onecmd(f"destroy BaseModel {uuid}\n")
            output = f.getvalue().strip()
            self.assertEqual(output, "")

            # Test destroying with invalid class
            self.console.onecmd("destroy InvalidClass 123\n")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class doesn't exist **")

            # Test destroying with invalid instance ID
            self.console.onecmd("destroy BaseModel invalid_id\n")
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

if __name__ == "__main__":
    unittest.main()
