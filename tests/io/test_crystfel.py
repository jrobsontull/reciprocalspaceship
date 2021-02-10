import unittest
import pytest
from os.path import dirname, abspath, join
from os import remove
import gemmi
import reciprocalspaceship as rs


def test_read_crystfel_mtz(IOtest_mtz):
    """
    rs.read_crystfel should raise ValueError when given file without
    .stream suffix
    """
    with pytest.raises(ValueError):
        rs.io.read_crystfel(IOtest_mtz)


class TestPrecognition(unittest.TestCase):
    def test_read_stream(self):

        datadir = join(abspath(dirname(__file__)), '../data/crystfel')


        # Read HKL without providing cell / spacegroup
        hewl = rs.io.read_crystfel(join(datadir, 'crystfel.stream'))

        self.assertEqual(list(hewl.index.names), ["H", "K", "L"])
        self.assertTrue('I' in hewl.columns)
        self.assertTrue('sigmaI' in hewl.columns)
        self.assertTrue('BATCH' in hewl.columns)
        self.assertTrue('s1x' in hewl.columns)
        self.assertTrue('s1y' in hewl.columns)
        self.assertTrue('s1z' in hewl.columns)
        self.assertTrue('BATCH' in hewl.columns)
        self.assertIsInstance(hewl, rs.DataSet)
        self.assertIsInstance(hewl["I"], rs.DataSeries)
        self.assertIsInstance(hewl["sigmaI"], rs.DataSeries)
        self.assertIsInstance(hewl["ewald_offset"], rs.DataSeries)
        self.assertIsNone(hewl.spacegroup)
        self.assertIsNone(hewl.cell)

        # chech values specific to the stream
        self.assertTrue(len(hewl.index.unique()) < len(hewl.index))
        self.assertTrue(
            hewl['ewald_offset'].min() < 0 < hewl['ewald_offset'].max())
        self.assertEqual(len(hewl.BATCH.unique()),
                         2111)  # grep -c 'Begin crystal' crystfel.stream

        return
