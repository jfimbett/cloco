#!/usr/bin/env python3
"""
Cross-Platform Notification Hook

Fires on Notification events to alert the user when Claude needs attention.
Works on Windows (PowerShell balloon), macOS (osascript), Linux (notify-send).
Falls back to printing to stderr if no notification system is available.

Hook Event: Notification
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys


def notify_windows(title: str, message: str) -> None:
    """Show a Windows balloon notification via PowerShell."""
    ps_script = (
        "Add-Type -AssemblyName System.Windows.Forms; "
        "$n = New-Object System.Windows.Forms.NotifyIcon; "
        "$n.Icon = [System.Drawing.SystemIcons]::Information; "
        "$n.Visible = $true; "
        f"$n.ShowBalloonTip(5000, '{title}', '{message}', "
        "[System.Windows.Forms.ToolTipIcon]::Info); "
        "Start-Sleep -Seconds 5; "
        "$n.Dispose()"
    )
    subprocess.Popen(
        ["powershell.exe", "-WindowStyle", "Hidden", "-Command", ps_script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def notify_macos(title: str, message: str) -> None:
    """Show a macOS desktop notification."""
    subprocess.run(
        ["osascript", "-e", f'display notification "{message}" with title "{title}"'],
        capture_output=True,
    )


def notify_linux(title: str, message: str) -> None:
    """Show a Linux desktop notification."""
    subprocess.run(["notify-send", title, message], capture_output=True)


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    message = hook_input.get("message", "Claude needs attention")
    title = hook_input.get("title", "Claude Code")

    # Sanitize for shell safety
    message = message.replace("'", "").replace('"', "")[:200]
    title = title.replace("'", "").replace('"', "")[:100]

    system = platform.system()
    try:
        if system == "Windows":
            notify_windows(title, message)
        elif system == "Darwin":
            notify_macos(title, message)
        elif system == "Linux":
            notify_linux(title, message)
    except Exception:
        pass  # Notification failure is never fatal

    return 0


if __name__ == "__main__":
    sys.exit(main())
