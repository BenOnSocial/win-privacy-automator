import os
from pywinauto import Desktop

class DiagnosticsAndFeedbackPage:
    def __init__(self):
        self._page_path = "start ms-settings:privacy-feedback"
        self._window = None

    def __enter__(self):
        # Navigate directly to the Privacy & Security > Diagnostics & feedback window.
        os.system(self._page_path)

        # Get the handle for the Settings window.
        self._window = Desktop(backend="uia").window(title="Settings")
        self._window.wait("visible", timeout=10)

        # Pre-locate groups.
        self._diagnostics_data_group = self._window.child_window(title="Diagnostic data", control_type="Group")
        self._view_diagnostics_data_group = self._window.child_window(title="View diagnostic data", control_type="Group")
        self._delete_diagnostics_data_group = self._window.child_window(title="Delete diagnostic data", control_type="Group")

        return self

    def __exit__(self, exc_type, exc, tb):
        if self._window and self._window.exists():
            self._window.close()

    def _expand_group(self, group):
        expand_btn = group.child_window(title="Show more settings")
        if expand_btn.exists():
            expand_btn.click_input()

    @property
    def page_path(self):
        return self._page_path

    @property
    def send_optional_diagnostics_data(self):
        toggle = self._diagnostics_data_group.child_window(title="Send optional diagnostic data", control_type="Button")

        if not toggle.exists() or not toggle.is_visible():
            self._expand_group(self._diagnostics_data_group)
            toggle.wait("visible", timeout=3)

        return toggle.get_toggle_state() == 1

    @send_optional_diagnostics_data.setter
    def send_optional_diagnostics_data(self, value):
        if self.send_optional_diagnostics_data != value:
            toggle = self._diagnostics_data_group.child_window(title="Send optional diagnostic data", control_type="Button")
            # The group should already be open after invoking the property getter
            toggle.click_input()

    @property
    def improve_language_recognition_and_suggestions(self):
        if not self.send_optional_diagnostics_data:
            return False
        else:
            pass # TODO: expand the Improve inking and typing group and get toggle state

    @improve_language_recognition_and_suggestions.setter
    def improve_language_recognition_and_suggestions(self, value):
        pass # TODO: return toggle state

    @property
    def enable_diagnostics_data_viewer(self):
        toggle = self._view_diagnostics_data_group.child_window(title="Turn on the Diagnostic Data Viewer (uses up to 1 GB of hard drive space)", control_type="Button")

        if not toggle.exists() or not toggle.is_visible():
            self._expand_group(self._view_diagnostics_data_group)
            toggle.wait("visible", timeout=3)

        return toggle.get_toggle_state() == 1

    @enable_diagnostics_data_viewer.setter
    def enable_diagnostics_data_viewer(self, value):
        if self.enable_diagnostics_data_viewer != value:
            toggle = self._view_diagnostics_data_group.child_window(title="Turn on the Diagnostic Data Viewer (uses up to 1 GB of hard drive space)", control_type="Button")
            toggle.click_input()

    def delete_diagnostics_data(self):
        button = self._delete_diagnostics_data_group.child_window(title="Delete")

        if not button.exists() or not button.is_visible():
            self._expand_group(self._delete_diagnostics_data_group)
            button.wait("visible", timeout=3)

        button.click_input()

    @property
    def feedback_frequency(self):
        combobox = self._window.child_window(title="Feedback frequency", control_type="ComboBox")
        return combobox.selected_text()

    @feedback_frequency.setter
    def feedback_frequency(self, value):
        combobox = self._window.child_window(title="Feedback frequency", control_type="ComboBox")
        if not combobox.is_visible():
            combobox.scroll_into_view()
        combobox.select(value)

