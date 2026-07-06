import unittest

from converter import run_conversion


class ConverterTests(unittest.TestCase):
    def test_decimal_to_binary(self):
        self.assertEqual(run_conversion("1", "42"), "101010")

    def test_binary_to_ascii(self):
        self.assertEqual(run_conversion("4", "01001000 01101001"), "Hi")

    def test_decimal_to_ascii(self):
        self.assertEqual(run_conversion("8", "65 66 67"), "ABC")

    def test_utf8_decimal_round_trip(self):
        self.assertEqual(run_conversion("9", "cafe"), "99 97 102 101")

    def test_rejects_invalid_binary(self):
        with self.assertRaises(ValueError):
            run_conversion("2", "10201")


if __name__ == "__main__":
    unittest.main()
