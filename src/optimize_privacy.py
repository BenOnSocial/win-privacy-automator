import os
from pywinauto.application import Application
from pywinauto import Desktop


def disable_toggle(window, group_title_re, toggle_title_re):
    group = window.child_window(title_re=group_title_re, control_type="Group")
    toggle = group.child_window(title_re=toggle_title_re, control_type="Button")

    if not toggle.exists() or not toggle.is_visible():
        expand_btn = group.child_window(title="Show more settings")
        if expand_btn.exists():
            expand_btn.click_input()
            toggle.wait("visible", timeout=3)

    if toggle.get_toggle_state() == 1:
        toggle.click_input()

def click_button(window, group_title_re, button_title_re):
    group = window.child_window(title_re=group_title_re, control_type="Group")
    button = group.child_window(title_re=button_title_re, control_type="Button")

    if not button.exists() or not button.is_visible():
        expand_btn = group.child_window(title="Show more settings")
        if expand_btn.exists():
            expand_btn.click_input()
            button.wait("visible", timeout=3)

    button.click_input()


def main():
    # Navigate directly to the Privacy & Security > Diagnostics & feedback window.
    os.system("start ms-settings:privacy-feedback")

    # Get the handle for the Settings window.
    settings_window = Desktop(backend="uia").window(title="Settings")
    settings_window.wait("visible", timeout=10)

    # Turn OFF optional diagnostic data collection.
    disable_toggle(window=settings_window, group_title_re="Diagnostic data", toggle_title_re="Send optional diagnostic data")

    # # Turn OFF Diagnostic Data Viewer.
    disable_toggle(window=settings_window, group_title_re="View diagnostic data", toggle_title_re="Turn on the Diagnostic Data Viewer.*")

    # Delete existing diagnostic data.
    click_button(window=settings_window, group_title_re="Delete diagnostic data", button_title_re="Delete")

if __name__ == "__main__":
    main()