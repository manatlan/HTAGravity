import os
from unittest.mock import patch, MagicMock
import pytest
from htag import Tag, ChromeApp, WebApp

class MyTestApp(Tag.App):
    pass

@pytest.fixture(autouse=True)
def cleanup_env():
    # Make sure HTAG_RELOADER is clean before each test
    if "HTAG_RELOADER" in os.environ:
        del os.environ["HTAG_RELOADER"]
    yield
    if "HTAG_RELOADER" in os.environ:
        del os.environ["HTAG_RELOADER"]


@patch("htag.runners.chrome.threading.Thread")
@patch("htag.runners.chrome.subprocess.Popen")
@patch("htag.runners.chrome.uvicorn.run")
@patch("htag.runners.chrome.ChromeApp._run_with_reloader")
def test_chromeapp_reload_master(mock_run_reloader, mock_uvicorn, mock_popen, mock_thread):
    """
    Test ChromeApp with reload=True when it's the MASTER process.
    It should launch Chrome and start the watcher.
    It should NOT start uvicorn.
    """
    runner = ChromeApp(MyTestApp)
    runner.run(reload=True)
    
    # Assert App was tagged for reload
    assert getattr(MyTestApp, "_reload", False) is True

    # Assert uvicorn and browser are NOT handled normally, but rather reloader is called
    mock_run_reloader.assert_called_once()
    mock_uvicorn.assert_not_called()

    # We mock thread so the browser launch logic doesn't actually execute async in the background
    mock_thread.assert_called_once()


@patch("htag.runners.chrome.threading.Thread")
@patch("htag.runners.chrome.subprocess.Popen")
@patch("htag.runners.chrome.uvicorn.run")
@patch("htag.runners.chrome.ChromeApp._run_with_reloader")
def test_chromeapp_reload_child(mock_run_reloader, mock_uvicorn, mock_popen, mock_thread):
    """
    Test ChromeApp with reload=True when it's the CHILD WORKER process.
    It should NOT launch chrome again, and it should run uvicorn.
    """
    os.environ["HTAG_RELOADER"] = "1"
    
    runner = ChromeApp(MyTestApp)
    runner.run(reload=True)

    # Assert reloader is NOT started again
    mock_run_reloader.assert_not_called()

    # Assert Uvicorn IS started
    mock_uvicorn.assert_called_once()

    # Thread (browser launch) should NOT be called in child
    mock_thread.assert_not_called()


@patch("htag.runners.web.threading.Thread")
@patch("htag.runners.web.webbrowser.open")
@patch("htag.runners.web.uvicorn.run")
@patch("htag.runners.web.WebApp._run_with_reloader")
def test_webapp_reload_master(mock_run_reloader, mock_uvicorn, mock_open, mock_thread):
    """
    Test WebApp with reload=True (and open_browser=True) when it's the MASTER process.
    It should open the browser and start the watcher.
    """
    runner = WebApp(MyTestApp)
    runner.run(open_browser=True, reload=True)
    
    assert getattr(MyTestApp, "_reload", False) is True

    mock_run_reloader.assert_called_once()
    mock_uvicorn.assert_not_called()
    mock_thread.assert_called_once()


@patch("htag.runners.web.threading.Thread")
@patch("htag.runners.web.webbrowser.open")
@patch("htag.runners.web.uvicorn.run")
@patch("htag.runners.web.WebApp._run_with_reloader")
def test_webapp_reload_child(mock_run_reloader, mock_uvicorn, mock_open, mock_thread):
    """
    Test WebApp with reload=True when it's the CHILD WORKER process.
    It should NOT open the browser again, and should start uvicorn.
    """
    os.environ["HTAG_RELOADER"] = "1"
    
    runner = WebApp(MyTestApp)
    runner.run(open_browser=True, reload=True)

    mock_run_reloader.assert_not_called()
    mock_uvicorn.assert_called_once()
    mock_thread.assert_not_called()


@patch("htag.runners.base.subprocess.Popen")
@patch("htag.runners.base.time.sleep")
def test_base_run_with_reloader(mock_sleep, mock_popen):
    """
    Test the base watcher loop logic. We simulate that the child process 
    will immediately exit so it doesn't infinite loop.
    """
    from htag.runners.base import BaseRunner
    
    # Fake process that returns 0 (normal exit) immediately
    mock_process = MagicMock()
    mock_process.poll.return_value = 0
    mock_process.returncode = 0
    mock_popen.return_value = mock_process
    
    runner = BaseRunner(MyTestApp)
    
    # We call it. Because process.poll() returns 0 immediately, 
    # the while process.poll() is None condition is false, and it breaks cleanly.
    runner._run_with_reloader()
    
    mock_popen.assert_called_once()
    assert "HTAG_RELOADER" in mock_popen.call_args.kwargs.get("env", {})
