import os
from diagnostics_and_feedback_page import DiagnosticsAndFeedbackPage

def main():
    with DiagnosticsAndFeedbackPage() as settings:
        # Turn OFF optional diagnostic data collection.
        settings.send_optional_diagnostics_data = False

        # Turn OFF Diagnostic Data Viewer.
        settings.enable_diagnostics_data_viewer = False

        # Delete existing diagnostic data.
        settings.delete_diagnostics_data()

        # Disable feedback requests
        settings.feedback_frequency = "Never"

if __name__ == "__main__":
    main()