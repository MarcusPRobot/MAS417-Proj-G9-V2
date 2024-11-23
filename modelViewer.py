import os
import math
import kivy
kivy.logger.Logger.setLevel('DEBUG')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics.transformation import Matrix
from kivy.graphics import (
    RenderContext, InstructionGroup, Mesh, Color, Callback
)
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.lang import Builder

Builder.load_string("""
<ModelViewer>:
    # Removed canvas.before to avoid conflicts
""")



class ModelViewer(FloatLayout):


    def __init__(self, **kwargs):
        super(ModelViewer, self).__init__(**kwargs)
        self.canvas = RenderContext()
        self.canvas.shader.vs = '''
        $HEADER$
        #ifdef GL_ES
        precision highp float;
        #endif
        uniform mat4 modelview_mat;
        uniform mat4 projection_mat;
        attribute vec3 v_pos;
        void main(void) {
            gl_Position = projection_mat * modelview_mat * vec4(v_pos, 1.0);
        }
        '''
        self.canvas.shader.fs = '''
        $HEADER$
        #ifdef GL_ES
        precision highp float;
        #endif
        void main(void) {
            gl_FragColor = vec4(1.0);  // White color
        }
        '''
        self.scene = InstructionGroup()
        self.mesh = None

        # Set up interaction
        self._touches = []
        self._rotation = [0, 0, 0]
        self._scale = 1.0

        # Add background color
        with self.canvas:
            Color(1, 1, 1, 1)  # White background
            self.rect = Rectangle(size=self.size, pos=self.pos)
            Callback(self.update_glsl)

        self.bind(size=self._update_rect, pos=self._update_rect)

        Clock.schedule_once(self.setup_gl_context, 0)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_glsl(self, *largs):
        self.canvas['projection_mat'] = self.projection
        self.canvas['modelview_mat'] = self.transform

    def setup_gl_context(self, *args):
        # Create a perspective projection matrix
        aspect_ratio = self.width / self.height
        self.projection = Matrix().view_clip(-aspect_ratio, aspect_ratio, -1, 1, 1, 100, 1)

        # Load the model here
        self.load_model(self.model_path)
        self.update_transform()

    def load_model(self, model_path):
        if not os.path.exists(model_path):
            print(f"Model file '{model_path}' does not exist.")
            return

        vertices = []
        indices = []

        # Simple OBJ parser
        with open(model_path, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    parts = line.strip().split()
                    x, y, z = map(float, parts[1:4])
                    vertices.extend([x, y, z])
                elif line.startswith('f '):
                    parts = line.strip().split()
                    idx = [int(p.split('/')[0]) - 1 for p in parts[1:]]
                    # Handle faces with more than 3 vertices (triangulate)
                    for i in range(1, len(idx) - 1):
                        indices.extend([idx[0], idx[i], idx[i + 1]])

        # Create the mesh
        self.mesh = Mesh(
            vertices=vertices,
            indices=indices,
            mode='triangles',
            fmt=[('v_pos', 3, 'float')],
        )

        # Add the mesh to the scene
        self.scene.clear()
        self.scene.add(Color(1, 0, 0, 1))  # Red color
        self.scene.add(self.mesh)
        self.canvas.add(self.scene)

    def on_touch_down(self, touch):
        self._touches.append(touch)
        return True

    def on_touch_move(self, touch):
        if len(self._touches) == 1:
            dx = touch.dx
            dy = touch.dy
            self._rotation[1] += dx * 0.5
            self._rotation[0] -= dy * 0.5
            self.update_transform()
            self.canvas.ask_update()
        elif len(self._touches) == 2:
            # Implement zoom or other interactions
            pass
        return True

    def on_touch_up(self, touch):
        if touch in self._touches:
            self._touches.remove(touch)
        return True

    def update_transform(self):
        # Create transformation matrix
        self.transform = Matrix().scale(self._scale, self._scale, self._scale)
        self.transform = self.transform.rotate(math.radians(self._rotation[0]), 1, 0, 0)
        self.transform = self.transform.rotate(math.radians(self._rotation[1]), 0, 1, 0)
        self.transform = self.transform.rotate(math.radians(self._rotation[2]), 0, 0, 1)
        self.transform = self.transform.translate(0, 0, -5)

        self.canvas['modelview_mat'] = self.transform

class ModelViewerApp(App):
    def __init__(self, model_path, **kwargs):
        super(ModelViewerApp, self).__init__(**kwargs)
        self.model_path = model_path

    def build(self):
        viewer = ModelViewer()
        viewer.model_path = self.model_path
        return viewer

def viewModel():

    print("The models available are")
    # Choose your model:

    ## Choices:
    # Write model name/number
    # Back (return)

    """
    models_dir = "models"  # Directory where models are stored

    # Check if the models directory exists
    if not os.path.exists(models_dir):
        print(f"Error: Models directory '{models_dir}' does not exist.")
        return

    # Supported 3D file extensions
    supported_formats = ('.obj',)

    # List all model files with supported formats
    model_files = [f for f in os.listdir(models_dir) if f.lower().endswith(supported_formats)]

    if not model_files:
        print("No 3D model files found in the models directory.")
        return

    # Display available models to the user
    print("\nAvailable 3D Models:")
    for idx, model in enumerate(model_files, start=1):
        print(f"{idx}. {model}")

    # Prompt user to select a model to view
    while True:
        try:
            choice = int(input("\nEnter the number of the model you want to view (or 0 to cancel): "))
            if choice == 0:
                print("Returning to the main menu.")
                return
            elif 1 <= choice <= len(model_files):
                selected_model = model_files[choice - 1]
                model_path = os.path.join(models_dir, selected_model)
                print(f"\nLoading model: {selected_model}")

                # Launch the Kivy app to display the model
                ModelViewerApp(model_path=model_path).run()
                return
            else:
                print(f"Invalid choice. Please enter a number between {1} and {len(model_files)}, or 0 to cancel.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
