# Windows Privacy Optimizer (UIA Automation)

An automated workstation provisioning tool built with Python and `pywinauto`.

This script automates the tedious process of disabling Windows 10/11 telemetry, diagnostic data, and targeted advertising settings on a fresh OS installation. It directly targets the modern Universal Windows Platform (UWP) Settings app using the UIAutomation (`uia`) API.

## 🎯 Purpose

Manually toggling privacy settings after every Windows reinstall is time-consuming and prone to human error. This project serves two purposes:

1. **Utility:** Instantly hardens local Windows privacy settings.
2. **Technical Demonstration:** Showcases the ability to interact with complex, modern UWP applications, navigate dynamic UI trees, and verify element states using Python.

## ✨ Key Features

- **Direct URI Navigation:** Bypasses manual Start Menu navigation by utilizing Windows URI schemes (`ms-settings:privacy-feedback`) to launch directly into the correct contexts.
- **Idempotent Execution:** The script reads the current state of toggle switches (e.g., checking the `ToggleState` property). It only executes a click if the setting is currently enabled, preventing unintended re-enabling.
- **UIA Backend:** Utilizes `pywinauto`'s `uia` backend to successfully map and control React Native/UWP desktop elements.

## 🛠 Tech Stack

- **Language:** Python 3.10+
- **Framework:** `pywinauto` (UIAutomation backend)
- **OS Target:** Windows 10 / Windows 11

## 🚀 Getting Started

### Prerequisites

- Windows 10 or 11 operating system.
- Python 3.10 or higher installed.
- Ensure your display scaling is set to 100% for the most reliable UI automation (Standard Windows limitation for GUI testing).

### Installation

Clone the repository and install the dependencies:

```powershell
git clone https://github.com/BenOnSocial/win-privacy-automator.git
cd win-privacy-automator
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Execute the main script from your terminal:

```powershell
python src/optimize_privacy.py
```

**_Note: Do not touch your mouse or keyboard while the script is running. The automation requires active window focus to toggle the UI elements._**

## 🧠 How It Works (Technical Approach)

Unlike legacy Win32 applications, the Windows Settings app does not expose standard control identifiers. This script:

1. Shell executes `ms-settings`: commands to spawn the target application.
2. Attaches `pywinauto` to the `SystemSettings.exe` process.
3. Uses custom wrapper functions to wait for specific UI elements to render.
4. Evaluates the `TogglePattern` of specific buttons (e.g., "Send optional diagnostic data") and switches them off if currently active.

### Diagnostics & feedback

https://github.com/user-attachments/assets/f4ceb401-0145-4a4f-9f4d-2a1b5e649cb2

## ⚠️ Disclaimer

This tool interacts directly with your operating system's UI. It is provided as-is. Please review the code before running it on a production machine to ensure you agree with the privacy toggles being disabled.

### Why this README works for your 6-year gap:

1. **"Idempotent Execution"**: Using this term proves you understand modern infrastructure-as-code and automation principles (scripts should be safe to run multiple times without breaking things).
2. **"UIA Backend" & "UWP"**: Shows you understand the deep technical differences between old Windows software (Win32) and modern Windows apps (Universal Windows Platform).
3. **"Automated workstation provisioning"**: Frames the project not as a hobby script, but as an enterprise IT/DevOps tool.
