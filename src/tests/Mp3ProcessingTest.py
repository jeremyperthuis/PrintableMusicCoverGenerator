import unittest
from src import Mp3Processing


class Mp3ProcessingTest(unittest.TestCase):
    def test_scanFolder(self):
        M= Mp3Processing("F:\\Users\\Jeremy\\Developpement\\PrintableMusicCoverGenerator\\testCD")
        self.assertEqual(self.M.list_mp3, 12)


if __name__ == '__main__':
    unittest.main()
