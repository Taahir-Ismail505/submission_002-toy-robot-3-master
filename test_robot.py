# import unittest
# from unittest.mock import patch
# import robot
# from io import StringIO
# import sys
# from test_base import run_unittests
# from test_base import captured_io


# class MyTestCase(unittest.TestCase):
#         # @patch("sys.stdin", StringIO("forward 10\nforward 5\REPLAY SILENT abd\nreplaysilent\noff"))
#         def test_step3_replay_silent_invalid(self):
#             with captured_io(StringIO('HAL\nforward 10\nforward 5\nREPLAY SILENT abd\nreplay silent\noff\n')) as (out, err):
#                     robot.robot_start()
#             self.maxDiff = None
#             output = out.getvalue().strip()
#             self.assertEqual("""What do you want to name your robot? HAL: Hello kiddo!
# HAL: What must I do next?  > HAL moved forward by 10 steps.
#  > HAL now at position (0,10).
# HAL: What must I do next?  > HAL moved forward by 5 steps.
#  > HAL now at position (0,15).
# HAL: What must I do next? HAL: Sorry, I did not understand 'REPLAY SILENT abd'.
# HAL: What must I do next?  > HAL replayed 2 commands silently.
#  > HAL now at position (0,30).
# HAL: What must I do next? HAL: Shutting down..""", output)
