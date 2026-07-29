import unittest
from main import calculate_pi


class TestCalculatePi(unittest.TestCase):
    """Test cases for the calculate_pi function."""
    
    def test_pi_calculation(self):
        """Test that calculate_pi returns pi to 5 decimal places."""
        result = calculate_pi()
        expected = 3.14159
        
        self.assertEqual(result, expected,
                         f"Expected {expected}, but got {result}")
    
    def test_pi_is_float(self):
        """Test that the result is a float."""
        result = calculate_pi()
        self.assertIsInstance(result, float,
                              "Result should be a float")
    
    def test_pi_accuracy(self):
        """Test that the result is close to the actual value of pi."""
        result = calculate_pi()
        actual_pi = 3.141592653589793
        
        # Check that result is within 0.000005 of actual pi (5 decimal places accuracy)
        self.assertAlmostEqual(result, actual_pi, places=5,
                               msg=f"Calculated pi {result} is not accurate enough")


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
