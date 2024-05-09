# ryPub EPub Reader

ryPub EPub Reader is a straightforward Python application designed to read ePub files on your computer. It offers theme switching, embedded font support, and image handling to enhance your reading experience. Enjoy continuous reading with vertical scrolling using your mouse wheel or the up and down arrow keys.

## Features

- **Read EPub Files**: Open and read any ePub file with ease.
- **Theme Toggling**: Switch between a light or dark theme according to your preference, for a comfortable reading experience.
- **Embedded Fonts**: Custom fonts are utilized to improve readability.
- **Image Handling**: Displays images embedded within ePub files correctly.
- **Keyboard Navigation**: Navigate through the pages using keyboard shortcuts.

#### Visit the [Releases](https://github.com/ryd3v/rypub-qt/releases) page for a pre-compiled executable.

### Build Prerequisites

To build ensure you have the following software installed on your system:

- Python 3.6 or later
- pip (Python package installer)

### Build

Clone the repository:

```bash
git clone https://github.com/ryd3v/rypub-qt
```

```bash
pip install -r requirements.txt
```

## Built With

- [PyQt6](https://pypi.org/project/PyQt6/) The GUI toolkit used

- [EbookLib](https://pypi.org/project/EbookLib/) Library for reading and manipulating ePub files
