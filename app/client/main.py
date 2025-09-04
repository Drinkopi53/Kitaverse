from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, ConfigVariableBool, Vec3
from direct.gui.DirectGui import *
import sys
import json
import urllib.request
import urllib.parse

class KitaverseClient(ShowBase):
    def __init__(self):
        # Initialize the ShowBase class
        ShowBase.__init__(self)
        
        # Optimize for low-end devices
        self.optimize_for_mobile()
        
        # Set window properties
        self.setup_window()
        
        # Create a simple scene
        self.create_scene()
        
        # Create UI elements
        self.create_ui()
        
        # Set up key bindings
        self.setup_controls()
        
        # Server connection state
        self.server_url = "http://localhost:8000"
        self.current_space = None
        self.user_id = 1  # In a real app, this would be assigned by the server
        self.user_name = "Villager"
        self.user_position = Vec3(0, 0, 0)
        
        # Load space definitions
        self.load_space_definitions()
        
    def optimize_for_mobile(self):
        """Optimize settings for low-end devices"""
        # Reduce graphics quality
        ConfigVariableBool("framebuffer-multisample").setValue(False)
        ConfigVariableBool("multisamples").setValue(0)
        
        # Texture compression
        ConfigVariableBool("compressed-textures").setValue(True)
        
        # Reduce rendering quality
        self.camLens.setNearFar(1, 1000)
        
    def setup_window(self):
        """Set window properties for mobile optimization"""
        props = WindowProperties()
        props.setSize(800, 600)
        props.setTitle("Kitaverse - Virtual Village Spaces")
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
        """Create a basic 3D scene"""
        # Create a simple ground plane
        self.scene = self.loader.loadModel("models/misc/sphere")
        self.scene.reparentTo(self.render)
        self.scene.setScale(100, 100, 1)
        self.scene.setPos(0, 0, -5)
        
        # Add some basic environment objects
        self.create_environment()
        
        # Add lighting
        self.add_lighting()
        
    def create_environment(self):
        """Create basic environment objects"""
        # Create a simple building for the community center
        building = self.loader.loadModel("models/misc/box")
        building.reparentTo(self.render)
        building.setScale(5, 5, 3)
        building.setPos(0, 0, 0)
        building.setColor(0.8, 0.8, 0.6, 1)
        
        # Create a market stall
        stall = self.loader.loadModel("models/misc/cylinder")
        stall.reparentTo(self.render)
        stall.setScale(1, 1, 0.5)
        stall.setPos(10, 10, 0)
        stall.setColor(0.6, 0.4, 0.2, 1)
        
        # Create a festival stage
        stage = self.loader.loadModel("models/misc/cube")
        stage.reparentTo(self.render)
        stage.setScale(8, 4, 0.5)
        stage.setPos(-10, -10, 0)
        stage.setColor(0.9, 0.1, 0.1, 1)
        
    def add_lighting(self):
        """Add lighting to the scene"""
        # Ambient light
        ambient_light = self.loader.loadModel("models/misc/ambient_light")
        ambient_light.reparentTo(self.render)
        ambient_light.setColor((0.4, 0.4, 0.4, 1))
        
        # Directional light (sun)
        directional_light = self.loader.loadModel("models/misc/directional_light")
        directional_light.reparentTo(self.render)
        directional_light.setColor((0.8, 0.8, 0.8, 1))
        directional_light.setHpr(0, -45, 0)
        
    def create_ui(self):
        """Create user interface elements"""
        # Title
        self.title = OnscreenText(text="Kitaverse",
                                  style=1,
                                  fg=(1, 1, 1, 1),
                                  pos=(0, 0.9),
                                  align=TextNode.ACenter,
                                  scale=0.1,
                                  wordwrap=12)
        
        # Status text
        self.status_text = OnscreenText(text="Not connected",
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
        
        # Instructions
        self.instructions = OnscreenText(text="Controls:\nC - Connect to server\n1 - Enter Community Center\n2 - Enter Village Market\n3 - Enter Festival Grounds\nESC - Exit",
                                         style=1,
                                         fg=(1, 1, 1, 1),
                                         pos=(0, -0.9),
                                         align=TextNode.ACenter,
                                         scale=0.05,
                                         wordwrap=12)
        
    def setup_controls(self):
        """Set up key bindings"""
        self.accept("escape", sys.exit)
        self.accept("c", self.connect_to_server)
        self.accept("1", self.enter_space, [1])
        self.accept("2", self.enter_space, [2])
        self.accept("3", self.enter_space, [3])
        
        # Movement controls
        self.accept("arrow_up", self.move_forward)
        self.accept("arrow_down", self.move_backward)
        self.accept("arrow_left", self.move_left)
        self.accept("arrow_right", self.move_right)
        
    def move_forward(self):
        """Move the user forward"""
        self.user_position.y += 1
        self.status_text.setText(f"Position: {self.user_position}")
        
    def move_backward(self):
        """Move the user backward"""
        self.user_position.y -= 1
        self.status_text.setText(f"Position: {self.user_position}")
        
    def move_left(self):
        """Move the user left"""
        self.user_position.x -= 1
        self.status_text.setText(f"Position: {self.user_position}")
        
    def move_right(self):
        """Move the user right"""
        self.user_position.x += 1
        self.status_text.setText(f"Position: {self.user_position}")
        
    def connect_to_server(self):
        """Connect to the backend server"""
        try:
            # Test connection
            url = f"{self.server_url}/"
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())
            
            self.status_text.setText(f"Connected to {data['message']}")
        except Exception as e:
            self.status_text.setText(f"Connection failed: {str(e)}")
            
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
            self.space_info.setText(f"In {self.current_space['name']}\nUsers: {self.current_space['current_users']}/{self.current_space['capacity']}")
            self.status_text.setText(f"Entered {self.current_space['name']}")
            
            # Load space-specific environment
            self.load_space_environment(space_id)
            
        except Exception as e:
            self.status_text.setText(f"Failed to enter space: {str(e)}")
            
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
            if child != self.scene and child.getName() != "ambient_light" and child.getName() != "directional_light":
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
        table.setScale(4, 4, 0.2)
        table.setPos(0, 0, 0)
        table.setColor(0.4, 0.2, 0.1, 1)
        
        # Create chairs around the table
        for i in range(8):
            angle = (i / 8) * 2 * 3.14159
            x = 5 * math.cos(angle)
            y = 5 * math.sin(angle)
            
            chair = self.loader.loadModel("models/misc/box")
            chair.reparentTo(self.render)
            chair.setScale(0.5, 0.5, 1)
            chair.setPos(x, y, 0)
            chair.setColor(0.6, 0.4, 0.2, 1)
            
    def create_market_environment(self):
        """Create environment for village market"""
        import math
        
        # Create multiple market stalls
        for i in range(6):
            angle = (i / 6) * 2 * 3.14159
            x = 8 * math.cos(angle)
            y = 8 * math.sin(angle)
            
            stall = self.loader.loadModel("models/misc/cylinder")
            stall.reparentTo(self.render)
            stall.setScale(1.5, 1.5, 1)
            stall.setPos(x, y, 0)
            stall.setColor(0.7, 0.5, 0.3, 1)
            
    def create_festival_environment(self):
        """Create environment for festival grounds"""
        # Create a larger performance stage
        stage = self.loader.loadModel("models/misc/cube")
        stage.reparentTo(self.render)
        stage.setScale(10, 5, 0.5)
        stage.setPos(0, 10, 0)
        stage.setColor(0.9, 0.1, 0.1, 1)
        
        # Create decorative elements
        import math
        for i in range(12):
            angle = (i / 12) * 2 * 3.14159
            x = 15 * math.cos(angle)
            y = 15 * math.sin(angle)
            
            decoration = self.loader.loadModel("models/misc/sphere")
            decoration.reparentTo(self.render)
            decoration.setScale(0.5, 0.5, 1)
            decoration.setPos(x, y, 0)
            decoration.setColor(1, 1, 0, 1)

# Run the application
if __name__ == "__main__":
    # Import math module for environment creation
    import math
    app = KitaverseClient()
    app.run()