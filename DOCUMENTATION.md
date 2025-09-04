# Kitaverse - Virtual Village Spaces

Kitaverse is a mini Metaverse built with Panda3D and FastAPI that enables remote villages to create "virtual public spaces" for meetings, markets, and festivals without requiring VR headsets. Users can access these virtual spaces using just a basic smartphone, reducing social isolation.

## Project Overview

This project implements a browser-based 3D virtual environment that allows villagers in remote areas to:
- Hold community meetings in a virtual Community Center
- Buy and sell goods at a virtual Village Market
- Celebrate festivals and cultural events in virtual Festival Grounds

The application is specifically optimized to run on low-end smartphones ("HP kentang") commonly found in remote areas.

## Technology Stack

- **Frontend**: 
  - Panda3D for 3D rendering
  - HTML/CSS/JavaScript for web interface
  - Mobile-optimized client for low-end devices

- **Backend**: 
  - FastAPI (Python) for high-performance API
  - RESTful endpoints for space management
  - User tracking and space capacity management

- **Deployment**: 
  - Docker-ready for easy deployment
  - Cross-platform compatibility

## Directory Structure

```
kitaverse/
├── app/
│   ├── backend/           # FastAPI server
│   │   ├── main.py        # Main server application
│   │   └── README.md      # Backend documentation
│   └── client/            # Panda3D client
│       ├── main.py        # Desktop client
│       ├── mobile.py      # Mobile-optimized client
│       ├── index.html     # Web interface
│       ├── config.json    # Client configuration
│       ├── spaces.json    # Space definitions
│       └── README.md      # Client documentation
├── dist/                  # Distribution packages
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker deployment configuration
├── README.md             # Project documentation
├── start_server.bat      # Windows server startup script
├── test_kitaverse.py     # Test suite
└── package.py            # Distribution packaging tool
```

## Features

### Virtual Spaces

1. **Community Center** (Meetings)
   - Round table for discussions
   - Presentation area
   - Capacity for 30 users

2. **Village Market** (Commerce)
   - Market stalls for vendors
   - Goods display areas
   - Capacity for 100 users

3. **Festival Grounds** (Events)
   - Performance stage
   - Dance floor
   - Decorative elements
   - Capacity for 200 users

### Mobile Optimization

- Reduced graphics quality settings
- Compressed textures
- Simplified 3D models
- Touch-based controls
- Low resource usage

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone or download the repository:
   ```bash
   git clone <repository-url>
   cd kitaverse
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Alternative) Use the installation scripts:
   - Windows: Run `install.bat`
   - Linux/Mac: Run `install.sh`

## Running the Application

### Method 1: Using Startup Scripts

1. Start the backend server:
   - Windows: Double-click `start_server.bat`
   - Linux/Mac: Run `python app/backend/main.py`

2. Open the client:
   - Open `app/client/index.html` in a web browser

### Method 2: Manual Execution

1. Start the backend server:
   ```bash
   python app/backend/main.py
   ```

2. In another terminal, run the client:
   ```bash
   python app/client/main.py  # Desktop version
   # or
   python app/client/mobile.py  # Mobile-optimized version
   ```

3. Open the web interface:
   - Open `app/client/index.html` in a web browser

## API Endpoints

The FastAPI backend provides the following endpoints:

- `GET /` - Root endpoint with welcome message
- `GET /spaces` - List all available virtual spaces
- `GET /spaces/{space_id}` - Get details about a specific space
- `POST /spaces/{space_id}/enter` - Enter a virtual space
- `POST /spaces/{space_id}/leave` - Leave a virtual space
- `GET /spaces/{space_id}/users` - Get users in a specific space

## Testing

Run the test suite to verify the installation:

```bash
python test_kitaverse.py
```

## Packaging and Distribution

Create a distribution package for sharing:

```bash
python package.py
```

This creates a ZIP file in the `dist/` directory containing all necessary files.

## Docker Deployment

Build and run with Docker:

```bash
docker build -t kitaverse .
docker run -p 8000:8000 kitaverse
```

## Future Enhancements

1. **Multi-user Support**
   - Avatar system for users
   - Real-time position tracking
   - User-to-user communication

2. **Enhanced Features**
   - Voice chat functionality
   - Text chat system
   - File sharing in meeting spaces

3. **Improved Mobile Experience**
   - Native mobile apps (Android/iOS)
   - Offline mode for areas with poor connectivity
   - Customizable village spaces

4. **Additional Spaces**
   - Educational facilities
   - Healthcare consultation rooms
   - Gaming areas for entertainment

## Optimization for Low-end Devices

Kitaverse is specifically designed for low-end smartphones with:

- Minimal system requirements
- Reduced graphics processing
- Efficient memory usage
- Fast loading times
- Touch-optimized interface

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Panda3D community for the 3D engine
- FastAPI for the backend framework
- All contributors to this project