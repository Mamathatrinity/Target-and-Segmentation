@echo off
python -m pytest tests/ui/test_segments.py::test_seg_pos_004 tests/ui/test_segments.py::test_seg_pos_005 tests/ui/test_segments.py::test_seg_pos_006 tests/ui/test_segments.py::test_seg_pos_007 -v --alluredir=allure-results --clean-alluredir
pause
