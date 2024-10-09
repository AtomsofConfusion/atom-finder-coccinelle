import unittest

def main():
    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner(verbosity=1)

    suite = loader.discover(start_dir='tests', pattern='test_*.py')
    runner.run(suite)