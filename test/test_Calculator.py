from unittest import TestCase
from model.StaticClasses.Calculator import Calculator

class TestCalculator(TestCase):
    def test_get_bytearray(self):
        self.assertEqual(Calculator.get_bytearray(0), bytearray(b'\x00'))
        self.assertEqual(Calculator.get_bytearray(1), bytearray(b'\x01'))
        self.assertEqual(Calculator.get_bytearray(22), bytearray(b'\x16'))
        self.assertEqual(Calculator.get_bytearray(222222222), bytearray(b'\x0d\x3e\xd7\x8e'))
        self.assertEqual(Calculator.get_bytearray(12345), bytearray(b'\x30\x39'))

