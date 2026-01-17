"""
Page Objects Package
Exports all page object classes for easy importing
"""

from framework.page_objects.base_page import BasePage
from framework.page_objects.login_page import LoginPage
from framework.page_objects.universe_summary_page import UniverseSummaryPage
from framework.page_objects.segments_page import SegmentsPage
from framework.page_objects.target_list_page import TargetListPage
from framework.page_objects.create_segment_page import CreateSegmentPage
from framework.page_objects.profile_menu_page import ProfileMenuPage

__all__ = [
    'BasePage',
    'LoginPage',
    'UniverseSummaryPage',
    'SegmentsPage',
    'TargetListPage',
    'CreateSegmentPage',
    'ProfileMenuPage'
]
