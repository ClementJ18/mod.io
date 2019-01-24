import unittest

import test.test_async_client
import test.test_async_game
import test.test_async_mod
import test.test_async_objects

loader = unittest.TestLoader()
suite  = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test.test_async_client))
suite.addTests(loader.loadTestsFromModule(test.test_async_game))
suite.addTests(loader.loadTestsFromModule(test.test_async_mod))
suite.addTests(loader.loadTestsFromModule(test.test_async_objects))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
