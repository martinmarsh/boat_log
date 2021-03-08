import pytest
import pytest_splinter
import splinter

from splinter import Browser
executable_path = {'executable_path': '</path/to/chrome>'}

mybrowser = Browser('chrome', **executable_path)

"""
@pytest.fixture
def admin_browser(request, browser_instance_getter):
    """"""
    # browser_instance_getter function receives parent fixture -- our admin_browser
    return browser_instance_getter(request, admin_browser)
"""

def test_browsers():
    """Test using 2 browsers at the same time."""
    mybrowser.visit('http://127.0.0.1:8000/admin/')