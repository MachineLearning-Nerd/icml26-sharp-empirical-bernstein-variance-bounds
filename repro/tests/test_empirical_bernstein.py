import unittest
from fractions import Fraction

import numpy as np

from repro.src.analyze_author_full import analyse_array
from repro.src.verify_empirical_bernstein import psi_e, scalar_multiplier


class EmpiricalBernsteinTest(unittest.TestCase):
    def test_psi_is_positive(self):
        self.assertGreater(psi_e(Fraction(1, 2)), 0)

    def test_corrected_scalar_multiplier_is_supermartingale_step(self):
        atoms = ((Fraction(1, 4), Fraction(1, 2)), (Fraction(3, 4), Fraction(1, 2)))
        value = scalar_multiplier(atoms, Fraction(0), Fraction(1, 16), Fraction(1, 16), Fraction(1, 2), 1)
        self.assertLessEqual(value, 1)

    def test_omitting_mean_correction_fails(self):
        atoms = ((Fraction(1, 4), Fraction(1, 2)), (Fraction(3, 4), Fraction(1, 2)))
        value = scalar_multiplier(atoms, Fraction(0), Fraction(1, 16), Fraction(1, 16), Fraction(1, 2), 1, False)
        self.assertGreater(value, 1)

    def test_author_artifact_shape_is_strict(self):
        with self.assertRaises(ValueError):
            analyse_array("uniform.npy", np.zeros((1, 49, 12)))


if __name__ == "__main__":
    unittest.main()
