import os
from pywinauto import Desktop


class Page(object):
    def __init__(self, page_path):
        self._page_path = page_path
        self._window = None

    def __enter__(self):
        os.system(f"start {self._page_path}")

        # Get the handle for the Settings window.
        self._window = Desktop(backend="uia").window(title="Settings")
        self._window.wait("visible", timeout=10)

    def __exit__(self, exc_type, exc, tb):
        if self._window and self._window.exists():
            self._window.close()

    def _get_group(self, title):
        return self._window.child_window(title=title, control_type="Group")

    def _expand_group(self, group):
        expand_btn = group.child_window(title="Show more settings")
        if expand_btn.exists():
            expand_btn.click_input()

    def _press_button(self, parent, title=None, auto_id=None):
        button = None

        if title:
            button = parent.child_window(title=title, control_type="Button")
        elif auto_id:
            button = parent.child_window(auto_id=auto_id, control_type="Button")

        button.iface_invoke.Invoke()

    def _get_toggle_state(self, parent, auto_id):
        toggle = parent.child_window(auto_id=auto_id, control_type="Button")
        return toggle.get_toggle_state() == 1

    def _get_toggle_state_from_collapsable_group(self, parent, auto_id):
        toggle = parent.child_window(auto_id=auto_id, control_type="Button")

        if not toggle.exists() or not toggle.is_visible():
            self._expand_group(parent)
            toggle.wait("visible", timeout=3)

        return toggle.get_toggle_state() == 1

    def _set_toggle_state(self, parent, auto_id, new_state):
        toggle = parent.child_window(auto_id=auto_id, control_type="Button")
        current_state = toggle.get_toggle_state() == 1
        if current_state != new_state:
            toggle.iface_toggle.Toggle()

    def _set_toggle_state_from_collapsable_group(self, parent, auto_id, new_state):
        toggle = parent.child_window(auto_id=auto_id, control_type="Button")
        if not toggle.exists() or not toggle.is_visible():
            self._expand_group(parent)
            toggle.wait("visible", timeout=3)

        current_state = toggle.get_toggle_state() == 1
        if current_state != new_state:
            toggle.iface_toggle.Toggle()


class DiagnosticsAndFeedbackPage(Page):
    def __init__(self):
        super().__init__(page_path="ms-settings:privacy-feedback")

        self._send_optional_diagnostic_data_auto_id = (
            "SystemSettings_Privacy_Diagnostic_Data_Toggle_2_ToggleSwitch"
        )
        self._improve_language_recognition_auto_id = (
            "SystemSettings_Privacy_ImproveInkType_Toggle_2_ToggleSwitch"
        )
        self._enable_diagnostics_data_viewer_auto_id = (
            "SystemSettings_Privacy_Telemetry_Viewer_Toggle_2_ToggleSwitch"
        )
        self._delete_diagnostic_data_auto_id = (
            "SystemSettings_Privacy_Device_Delete_2_Button"
        )
        self._feedback_frequency_auto_id = (
            "SystemSettings_Privacy_Change_Feedback_Frequency_ComboBox"
        )

    def __enter__(self):
        super().__enter__()

        # Pre-locate groups.
        self._diagnostics_data_group = self._window.child_window(
            title="Diagnostic data", control_type="Group"
        )
        self._improve_inking_and_typing_group = self._window.child_window(
            title="Improve inking and typing", control_type="Group"
        )
        self._view_diagnostics_data_group = self._window.child_window(
            title="View diagnostic data", control_type="Group"
        )
        self._delete_diagnostics_data_group = self._window.child_window(
            title="Delete diagnostic data", control_type="Group"
        )
        self.feedback_group = self._window.child_window(
            title="Feedback", control_type="Group"
        )

        return self

    @property
    def send_optional_diagnostics_data(self):
        return self._get_toggle_state_from_collapsable_group(
            parent=self._diagnostics_data_group,
            auto_id=self._send_optional_diagnostic_data_auto_id,
        )

    @send_optional_diagnostics_data.setter
    def send_optional_diagnostics_data(self, value):
        self._set_toggle_state_from_collapsable_group(
            parent=self._diagnostics_data_group,
            auto_id=self._send_optional_diagnostic_data_auto_id,
            new_state=value,
        )

    @property
    def improve_language_recognition_and_suggestions(self):
        if not self.send_optional_diagnostics_data:
            return False

        return self._get_toggle_state_from_collapsable_group(
            self._improve_inking_and_typing_group,
            auto_id=self._improve_language_recognition_auto_id,
        )

    @improve_language_recognition_and_suggestions.setter
    def improve_language_recognition_and_suggestions(self, value):
        if not self.send_optional_diagnostics_data:
            return  # Send optional diagnostic data is directly linked to the Improve inking and typing setting. If Send optional diagnostic data is disabled, this setting can't be toggled.

        self._set_toggle_state_from_collapsable_group(
            parent=self._improve_inking_and_typing_group,
            auto_id=self._improve_language_recognition_auto_id,
            new_state=value,
        )

    @property
    def enable_diagnostics_data_viewer(self):
        return self._get_toggle_state_from_collapsable_group(
            self._view_diagnostics_data_group,
            auto_id=self._enable_diagnostics_data_viewer_auto_id,
        )

    @enable_diagnostics_data_viewer.setter
    def enable_diagnostics_data_viewer(self, value):
        self._set_toggle_state_from_collapsable_group(
            parent=self._view_diagnostics_data_group,
            auto_id=self._enable_diagnostics_data_viewer_auto_id,
            new_state=value,
        )

    def delete_diagnostics_data(self):
        button = self._delete_diagnostics_data_group.child_window(
            auto_id=self._delete_diagnostic_data_auto_id
        )

        if not button.exists() or not button.is_visible():
            self._expand_group(self._delete_diagnostics_data_group)
            button.wait("visible", timeout=3)

        button.iface_invoke.Invoke()

    @property
    def feedback_frequency(self):
        combobox = self.feedback_group.child_window(
            auto_id=self._feedback_frequency_auto_id, control_type="ComboBox"
        )

        selection_pattern = combobox.iface_selection
        selection = selection_pattern.GetCurrentSelection()

        if selection and selection.Length > 0:
            return selection.GetElement(0).CurrentName

        return None

    @feedback_frequency.setter
    def feedback_frequency(self, value):
        combobox = self.feedback_group.child_window(
            auto_id=self._feedback_frequency_auto_id, control_type="ComboBox"
        )

        if combobox.get_expand_state() == 0:
            combobox.iface_expand_collapse.Expand()

        item = combobox.child_window(title=value, control_type="ListItem")
        item.iface_selection_item.Select()


class RecommendationsAndOffersPage(Page):
    def __init__(self):
        super().__init__(page_path="ms-settings:privacy-general")

        self._enable_personalized_offers_auto_id = (
            "SystemSettings_Privacy_TailoredExperiences2_ToggleSwitch"
        )
        self._allow_language_list_access_auto_id = (
            "SystemSettings_Language_Web_Content_Control_ToggleSwitch"
        )
        self._enable_improve_start_and_search_results_auto_id = (
            "SystemSettings_Privacy_StoreAppUsage_ToggleSwitch"
        )
        self._show_notifications_in_settings_auto_id = (
            "SystemSettings_Privacy_EnableAccountNotificationsInSettings_ToggleSwitch"
        )
        self._show_recommendations_and_offers_in_settings_auto_id = (
            "SystemSettings_Privacy_EnableSuggestionsInSettings_ToggleSwitch"
        )
        self._enable_advertising_id_auto_id = (
            "SystemSettings_Privacy_AdvertisingIdEnabled_ToggleSwitch"
        )

    def __enter__(self):
        super().__enter__()

        # Pre-locate groups.
        self._personalized_offers_group = self._window.child_window(
            title="Personalized offers", control_type="Group"
        )

        return self

    @property
    def enable_personalized_offers(self):
        return self._get_toggle_state(
            self._personalized_offers_group,
            auto_id=self.enable_personalized_offers_auto_id,
        )

    @enable_personalized_offers.setter
    def enable_personalized_offers(self, value):
        self._set_toggle_state(
            parent=self._personalized_offers_group,
            auto_id=self._enable_personalized_offers_auto_id,
            new_state=value,
        )

    @property
    def allow_language_list_access(self):
        return self._get_toggle_state(
            parent=self._window, auto_id=self._allow_language_list_access_auto_id
        )

    @allow_language_list_access.setter
    def allow_language_list_access(self, value):
        self._set_toggle_state(
            parent=self._window,
            auto_id=self._allow_language_list_access_auto_id,
            new_state=value,
        )

    @property
    def enable_improve_start_and_search_results(self):
        return self._get_toggle_state(
            parent=self._window,
            auto_id=self._enable_improve_start_and_search_results_auto_id,
        )

    @enable_improve_start_and_search_results.setter
    def enable_improve_start_and_search_results(self, value):
        self._set_toggle_state(
            parent=self._window,
            auto_id=self._enable_improve_start_and_search_results_auto_id,
            new_state=value,
        )

    @property
    def show_notifications_in_settings(self):
        return self._get_toggle_state(
            parent=self._window,
            auto_id=self._show_notifications_in_settings_auto_id,
        )

    @show_notifications_in_settings.setter
    def show_notifications_in_settings(self, value):
        self._set_toggle_state(
            parent=self._window,
            auto_id=self._show_notifications_in_settings_auto_id,
            new_state=value,
        )

    @property
    def show_recommendations_and_offers_in_settings(self):
        return self._get_toggle_state(
            parent=self._window, auto_id=self._show_notifications_in_settings_auto_id
        )

    @show_recommendations_and_offers_in_settings.setter
    def show_recommendations_and_offers_in_settings(self, value):
        self._set_toggle_state(
            parent=self._window,
            auto_id=self._show_recommendations_and_offers_in_settings_auto_id,
            new_state=value,
        )

    @property
    def enable_advertising_id(self):
        return self._get_toggle_state(
            parent=self._window, auto_id=self._enable_advertising_id_auto_id
        )

    @enable_advertising_id.setter
    def enable_advertising_id(self, value):
        self._set_toggle_state(
            parent=self._window,
            auto_id=self._enable_advertising_id_auto_id,
            new_state=value,
        )


class SearchPage(Page):
    def __init__(self):
        super().__init__(page_path="ms-settings:search")

        self._enable_search_history_auto_id = (
            "SystemSettings_Search_MyDeviceHistory_ToggleSwitch"
        )
        self._enable_show_search_highlights_auto_id = (
            "SystemSettings_Search_DynamicSearchBox_ToggleSwitch"
        )
        self._enable_search_microsoft_account_auto_id = (
            "SystemSettings_Search_CloudSearchMSA_ToggleSwitch"
        )
        self._enable_search_work_or_home_account_auto_id = (
            "SystemSettings_Search_CloudSearchAAD_ToggleSwitch"
        )

    def __enter__(self):
        super().__enter__()

        # Pre-locate groups.
        self._search_history_group = self._get_group(title="Search history")
        self._clear_device_search_history_group = self._get_group(
            title="Clear device search history"
        )
        self._search_my_accounts_group = self._get_group(title="Search my accounts")

        return self

    @property
    def enable_search_history(self):
        return self._get_toggle_state_from_collapsable_group(
            parent=self._search_history_group,
            auto_id=self._enable_search_history_auto_id,
        )

    @enable_search_history.setter
    def enable_search_history(self, value):
        self._set_toggle_state_from_collapsable_group(
            parent=self._search_history_group,
            auto_id=self._enable_search_history_auto_id,
            new_state=value,
        )

    def clear_device_search_history(self):
        self._press_button(
            parent=self._clear_device_search_history_group, title="Clear"
        )

    @property
    def enable_show_search_highlights(self):
        return self._set_toggle_state(
            parent=self._window, auto_id=self._enable_show_search_highlights_auto_id
        )

    @enable_show_search_highlights.setter
    def enable_show_search_highlights(self, value):
        self._set_toggle_state(
            parent=self._window,
            auto_id=self._enable_show_search_highlights_auto_id,
            new_state=value,
        )

    @property
    def enable_search_microsoft_account(self):
        return self._get_toggle_state(
            parent=self._search_my_accounts_group,
            auto_id=self._enable_search_microsoft_account_auto_id,
        )

    @enable_search_microsoft_account.setter
    def enable_search_microsoft_account(self, value):
        self._set_toggle_state(
            parent=self._search_my_accounts_group,
            auto_id=self._enable_search_microsoft_account_auto_id,
            new_state=value,
        )

    @property
    def enable_search_work_or_home_account(self):
        return self._get_toggle_state(
            parent=self._search_my_accounts_group,
            auto_id=self._enable_search_work_or_home_account_auto_id,
        )

    @enable_search_work_or_home_account.setter
    def enable_search_work_or_home_account(self, value):
        self._set_toggle_state(
            parent=self._search_my_accounts_group,
            auto_id=self._enable_search_work_or_home_account_auto_id,
            new_state=value,
        )


class SpeechPage(Page):
    def __init__(self):
        super().__init__(page_path="ms-settings:privacy-speech")

        self._online_speech_recognition_auto_id = (
            "SystemSettings_Privacy_Speech_AllowSpeechServices_ToggleSwitch"
        )

    def __enter__(self):
        super().__enter__()

        # Pre-locate groups.
        self._online_speech_recognition_group = self._window.child_window(
            title="Online speech recognition", control_type="Group"
        )

        return self

    @property
    def enable_online_speech_recognition(self):
        return self._get_toggle_state(
            self._online_speech_recognition_group,
            auto_id=self._online_speech_recognition_auto_id,
        )

    @enable_online_speech_recognition.setter
    def enable_online_speech_recognition(self, value):
        self._set_toggle_state(
            parent=self._online_speech_recognition_group,
            auto_id=self._online_speech_recognition_auto_id,
            new_state=value,
        )
