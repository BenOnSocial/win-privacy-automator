import os
from privacy_and_security_settings import DiagnosticsAndFeedbackPage
from privacy_and_security_settings import RecommendationsAndOffersPage
from privacy_and_security_settings import SearchPage
from privacy_and_security_settings import SpeechPage


def main():
    with DiagnosticsAndFeedbackPage() as settings:
        settings.send_optional_diagnostics_data = False
        settings.improve_language_recognition_and_suggestions = False
        settings.enable_diagnostics_data_viewer = False
        settings.delete_diagnostics_data()
        settings.feedback_frequency = "Never"

    with RecommendationsAndOffersPage() as settings:
        settings.enable_personalized_offers = False
        settings.allow_language_list_access = False
        settings.enable_improve_start_and_search_results = False
        settings.show_notifications_in_settings = False
        settings.show_recommendations_and_offers_in_settings = False
        settings.enable_advertising_id = False

    with SearchPage() as settings:
        settings.enable_search_history = False
        settings.clear_device_search_history()
        settings.enable_show_search_highlights = False
        settings.enable_search_microsoft_account = False
        settings.enable_search_work_or_home_account = False

    with SpeechPage() as settings:
        settings.enable_online_speech_recognition = False


if __name__ == "__main__":
    main()
