# Text Toolbox for DaVinci Resolve
A set of tools to improve and speed-up your workflow for many text-related tasks in DaVinci Resolve!

## What's included?
- **Font Viewer**
	- Font Viewer shows you all fonts that are used in your project and if they are installed to your current machine
	- This ensures that your video displays and renders properly when working with multiple people or on multiple machines.
- **Auto Rename** 
	- Auto Rename automatically renames many nodes to meaningful names
	- This greatly improves the workflow for Background, Text+, Text3D, MediaIn and MultiMerge node
- **Word Wrapper** 
	- When editing text in Fusion or on the timeline, automatically add dynamic line breaks based on word boundaries
	- This works on Text+ and Text3D nodes in Fusion, and Text+ (not Legacy Text) on the Edit and Cut pages
- **Subtitle Search** 
	- Search your subtitle tracks for certain words and jump to the position on the timeline!
	- Use this to fix bad transcriptions of uncommon words in automated subtitle transcriptions.



## Usage:
- In DaVinci Resolve, open the dropdown menu (Workspace > Scripts > Text Toolbox)
- Select the tool you want to use (Font Viewer, Word Wrapper, Subtitle Search, Auto Rename)
( - Note: Auto Rename and Word Wrapper only work on the Fusion page)
- The selected tool will open in a new window. (Auto Rename does not open in a new window, it just runs in the background)

## Install:
- Download the ["Text Toolbox for DaVinci Resolve.zip"](https://github.com/neezr/Text-Toolbox-for-DaVinci-Resolve/archive/refs/heads/main.zip) folder
- Extract the *Text Toolbox* folder and save it to:
	- Windows: *"C:\Users\\<YOUR_NAME>\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility"*
	- MacOS: *"/Library/Application Support/Blackmagic Design/DaVinci
Resolve/Fusion/Scripts/Utility"*
	- Linux: *"/opt/resolve/Fusion/Scripts/Utility"*
- If you didn't do it already, install Python (at least version 3.6) from [python.org](https://www.python.org/)
