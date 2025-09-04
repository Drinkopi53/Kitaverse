# Kitaverse

Kitaverse is a mini Metaverse built with Panda3D and FastAPI that enables remote villages to create "virtual public spaces" for meetings, markets, and festivals without requiring VR headsets. Users can access these virtual spaces using just a basic smartphone, reducing social isolation.

## Features

- **Browser-based 3D Environment**: Built with Panda3D for cross-platform compatibility
- **Virtual Public Spaces**: 
  - Community Centers for meetings and discussions
  - Village Markets for buying and selling goods
  - Festival Grounds for cultural celebrations
- **Low-end Device Support**: Optimized to run on basic smartphones
- **No VR Required**: Accessible through any modern web browser
- **FastAPI Backend**: High-performance API for real-time interactions

## Technology Stack

- **Frontend**: Panda3D (3D engine), HTML/CSS/JavaScript
- **Backend**: FastAPI (Python web framework)
- **Communication**: WebSocket for real-time interactions
- **Deployment**: Docker-ready for easy deployment

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/kitaverse.git
   cd kitaverse
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the backend server:
   ```bash
   python app/backend/main.py
   ```

4. Open `app/client/index.html` in a web browser

## Usage

1. Connect to the server using the "Connect" button
2. Choose a virtual space from the sidebar:
   - Community Center: For meetings and discussions
   - Village Market: For buying and selling goods
   - Festival Grounds: For celebrations and cultural events
3. Use arrow keys to navigate and mouse to look around

## Optimization for Low-end Devices

Kitaverse is specifically designed to run on low-end smartphones:
- Low polygon models
- Compressed textures
- Level of Detail (LOD) systems
- Occlusion culling
- Minimal resource usage

## Future Enhancements

- Multi-user support with avatars
- Voice chat functionality
- Customizable village spaces
- Mobile app versions
- Offline mode for areas with poor connectivity