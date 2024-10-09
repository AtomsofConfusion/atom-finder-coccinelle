import unittest

def main():
    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner()

    suite = loader.discover(start_dir='tests', pattern='test_*.py')
    runner.run(suite)