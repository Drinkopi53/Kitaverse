from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, ConfigVariableBool, Vec3, loadPrcFile
from direct.gui.DirectGui import *
import sys
import json
import urllib.request
import urllib.parse
import math

class KitaverseMobileClient(ShowBase):
    def __init__(self):
        # Load optimized configuration for mobile devices
        loadPrcFile("app/client/config_optimized.prc")
        
        # Initialize the ShowBase class
        ShowBase.__init__(self)
        
        # Set window properties for mobile
        self.setup_mobile_window()
        
        # Create a simple scene
        self.create_scene()
        
        # Create UI elements
        self.create_mobile_ui()
        
        # Set up touch/mouse controls
        self.setup_mobile_controls()
        
        # Server connection state
        self.server_url = "http://localhost:8000"
        self.current_space = None
        self.user_id = 1
        self.user_name = "Villager"
        self.user_position = Vec3(0, 0, 0)
        
        # Load space definitions
        self.load_space_definitions()
        
    def setup_mobile_window(self):
        """Set window properties optimized for mobile devices"""
        props = WindowProperties()
        props.setSize(800, 600)  # Will be scaled on mobile
        props.setTitle("Kitaverse - Mobile")
        self.win.requestProperties(props)
        
        # Disable mouse control for camera
        self.disableMouse()
        
    def load_space_definitions(self):
        """Load space definitions from JSON file"""
        try:
            with open("app/client/spaces.json", "r") as f:
                self.space_definitions = json.load(f)
        except FileNotFoundError:
            # Default space definitions if file not found
            self.space_definitions = {
                "spaces": [
                    {
                        "id": 1,
                        "name": "Community Center",
                        "type": "meeting",
                        "description": "A place for village meetings and discussions",
                        "capacity": 30
                    },
                    {
                        "id": 2,
                        "name": "Village Market",
                        "type": "market",
                        "description": "Buy and sell goods with other villagers",
                        "capacity": 100
                    },
                    {
                        "id": 3,
                        "name": "Festival Grounds",
                        "type": "festival",
                        "description": "Celebrate festivals and cultural events",
                        "capacity": 200
                    }
                ]
            }
        
    def create_scene(self):
        """Create a basic 3D scene optimized for mobile"""
        # Create a simple ground plane
        self.scene = self.loader.loadModel("models/misc/sphere")
        self.scene.reparentTo(self.render)
        self.scene.setScale(50, 50, 1)  # Smaller than desktop version
        self.scene.setPos(0, 0, -2)
        
        # Add lighting
        self.add_lighting()
        
    def add_lighting(self):
        """Add minimal lighting to the scene"""
        # Only ambient light to save resources
        ambient_light = self.loader.loadModel("models/misc/ambient_light")
        ambient_light.reparentTo(self.render)
        ambient_light.setColor((0.5, 0.5, 0.5, 1))
        
    def create_mobile_ui(self):
        """Create mobile-friendly UI elements"""
        # Title
        self.title = OnscreenText(text="Kitaverse",
                                  style=1,
                                  fg=(1, 1, 1, 1),
                                  pos=(0, 0.9),
                                  align=TextNode.ACenter,
                                  scale=0.08,  # Smaller text for mobile
                                  wordwrap=12)
        
        # Status text
        self.status_text = OnscreenText(text="Tap 'Connect' to begin",
                                       style=1,
                                       fg=(1, 1, 1, 1),
                                       pos=(0, 0.8),
                                       align=TextNode.ACenter,
                                       scale=0.05,
                                       wordwrap=12)
        
        # Space info
        self.space_info = OnscreenText(text="",
                                      style=1,
                                      fg=(1, 1, 1, 1),
                                      pos=(0, -0.7),
                                      align=TextNode.ACenter,
                                       scale=0.05,
                                       wordwrap=12)
        
        # Mobile buttons
        self.connect_button = DirectButton(text="Connect",
                                          scale=0.1,
                                          pos=(-0.7, 0, -0.9),
                                          command=self.connect_to_server)
                                          
        self.space1_button = DirectButton(text="Meetings",
                                         scale=0.1,
                                         pos=(-0.3, 0, -0.9),
                                         command=lambda: self.enter_space(1))
                                         
        self.space2_button = DirectButton(text="Market",
                                         scale=0.1,
                                         pos=(0.1, 0, -0.9),
                                         command=lambda: self.enter_space(2))
                                         
        self.space3_button = DirectButton(text="Festival",
                                         scale=0.1,
                                         pos=(0.5, 0, -0.9),
                                         command=lambda: self.enter_space(3))
        
    def setup_mobile_controls(self):
        """Set up touch-based controls for mobile"""
        # Accept mouse events as touch events
        self.accept("mouse1", self.on_touch_start)
        self.accept("mouse1-up", self.on_touch_end)
        
        # Accept escape key to exit
        self.accept("escape", sys.exit)
        
    def on_touch_start(self):
        """Handle touch start event"""
        # Get mouse position
        if self.mouseWatcherNode.hasMouse():
            x = self.mouseWatcherNode.getMouseX()
            y = self.mouseWatcherNode.getMouseY()
            
            # Simple touch area detection for movement
            if y < -0.5:  # Bottom part of screen
                if x < -0.3:
                    self.move_left()
                elif x > 0.3:
                    self.move_right()
                else:
                    self.move_forward()
        
    def on_touch_end(self):
        """Handle touch end event"""
        pass
        
    def move_forward(self):
        """Move the user forward"""
        self.user_position.y += 1
        self.status_text.setText(f"Moved forward")
        
    def move_backward(self):
        """Move the user backward"""
        self.user_position.y -= 1
        self.status_text.setText(f"Moved backward")
        
    def move_left(self):
        """Move the user left"""
        self.user_position.x -= 1
        self.status_text.setText(f"Moved left")
        
    def move_right(self):
        """Move the user right"""
        self.user_position.x += 1
        self.status_text.setText(f"Moved right")
        
    def connect_to_server(self):
        """Connect to the backend server"""
        try:
            # Test connection
            url = f"{self.server_url}/"
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())
            
            self.status_text.setText(f"Connected!")
            # Enable space buttons after connection
            self.space1_button["state"] = "normal"
            self.space2_button["state"] = "normal"
            self.space3_button["state"] = "normal"
        except Exception as e:
            self.status_text.setText(f"Failed: {str(e)}")
            
    def enter_space(self, space_id):
        """Enter a virtual space"""
        try:
            # Prepare user data
            user_data = {
                "id": self.user_id,
                "name": self.user_name,
                "position": {
                    "x": self.user_position.x,
                    "y": self.user_position.y,
                    "z": self.user_position.z
                }
            }
            
            # Send request to server
            url = f"{self.server_url}/spaces/{space_id}/enter"
            data = json.dumps(user_data).encode('utf-8')
            req = urllib.request.Request(url, data=data, 
                                         headers={'Content-Type': 'application/json'})
            response = urllib.request.urlopen(req)
            result = json.loads(response.read())
            
            # Update UI
            self.current_space = result["space"]
            self.space_info.setText(f"In {self.current_space['name']}\\nUsers: {self.current_space['current_users']}/{self.current_space['capacity']}")
            self.status_text.setText(f"Entered {self.current_space['name']}")
            
            # Load space-specific environment
            self.load_space_environment(space_id)
            
        except Exception as e:
            self.status_text.setText(f"Failed: {str(e)}")
            
    def load_space_environment(self, space_id):
        """Load environment specific to the space type"""
        # Find space definition
        space_def = None
        for space in self.space_definitions["spaces"]:
            if space["id"] == space_id:
                space_def = space
                break
                
        if not space_def:
            return
            
        # Clear existing environment objects
        for child in self.render.getChildren():
            if child != self.scene and child.getName() != "ambient_light":
                child.removeNode()
                
        # Load space-specific models based on type
        if space_def["type"] == "meeting":
            self.create_meeting_environment()
        elif space_def["type"] == "market":
            self.create_market_environment()
        elif space_def["type"] == "festival":
            self.create_festival_environment()
            
    def create_meeting_environment(self):
        """Create environment for community center (meetings)"""
        # Create a large table in the center
        table = self.loader.loadModel("models/misc/cylinder")
        table.reparentTo(self.render)
        table.setScale(2, 2, 0.1)  # Smaller than desktop version
        table.setPos(0, 0, 0)
        table.setColor(0.4, 0.2, 0.1, 1)
        
        # Create a few chairs around the table
        for i in range(4):
            angle = (i / 4) * 2 * 3.14159
            x = 3 * math.cos(angle)
            y = 3 * math.sin(angle)
            
            chair = self.loader.loadModel("models/misc/box")
            chair.reparentTo(self.render)
            chair.setScale(0.3, 0.3, 0.8)
            chair.setPos(x, y, 0)
            chair.setColor(0.6, 0.4, 0.2, 1)
            
    def create_market_environment(self):
        """Create environment for village market"""
        # Create a few market stalls
        for i in range(3):
            angle = (i / 3) * 2 * 3.14159
            x = 6 * math.cos(angle)
            y = 6 * math.sin(angle)
            
            stall = self.loader.loadModel("models/misc/cylinder")
            stall.reparentTo(self.render)
            stall.setScale(1, 1, 0.8)
            stall.setPos(x, y, 0)
            stall.setColor(0.7, 0.5, 0.3, 1)
            
    def create_festival_environment(self):
        """Create environment for festival grounds"""
        # Create a performance stage
        stage = self.loader.loadModel("models/misc/cube")
        stage.reparentTo(self.render)
        stage.setScale(5, 3, 0.3)
        stage.setPos(0, 6, 0)
        stage.setColor(0.9, 0.1, 0.1, 1)
        
        # Create a few decorative elements
        for i in range(6):
            angle = (i / 6) * 2 * 3.14159
            x = 10 * math.cos(angle)
            y = 10 * math.sin(angle)
            
            decoration = self.loader.loadModel("models/misc/sphere")
            decoration.reparentTo(self.render)
            decoration.setScale(0.3, 0.3, 0.3)
            decoration.setPos(x, y, 0)
            decoration.setColor(1, 1, 0, 1)

# Run the application
if __name__ == "__main__":
    app = KitaverseMobileClient()
    app.run()