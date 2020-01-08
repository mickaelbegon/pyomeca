"""
Test for euler to rot and rot to euler
"""
import numpy as np

from pyomeca import RotoTrans, FrameDependentNpArray, Markers3d


def test_rotate_marker():
    # Create random RotoTrans matrices and markers positions
    nb_frames = 100
    nb_markers = 10
    random_angles = FrameDependentNpArray(np.random.rand(3, 1, nb_frames))
    rt = RotoTrans.rt_from_euler_angles(random_angles, "xyz")

    m = Markers3d(np.random.rand(3, nb_markers, nb_frames))

    # Determine the expected values for the rotations
    expected_rot = np.ndarray((4, nb_markers, nb_frames))
    for i in range(nb_markers):
        for j in range(nb_frames):
            expected_rot[:, i, j] = rt[:, :, j].dot(m[:, i, j]).squeeze()

    # Rotate via pyomeca
    computed_rot = m.rotate(rt)

    # Compare the two
    np.testing.assert_almost_equal(computed_rot, expected_rot, decimal=10)
