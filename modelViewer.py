import os
import math
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.resources import resource_find
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import (
    glEnable, glDisable, GL_DEPTH_TEST, glDisable, GL_CULL_FACE
)
from kivy.graphics import (
    RenderContext, Callback, PushMatrix, PopMatrix,
    Color, Translate, Rotate, Scale, Mesh, UpdateNormalMatrix
)
import pywavefront

class Renderer(Widget):
    def __init__(self, **kwargs):
        # Initialize the RenderContext with compute_normal_mat=True
        self.canvas = RenderContext(compute_normal_mat=True)

        # Load the shader source
        shader_path = resource_find('simple.glsl')
        if not shader_path:
            raise FileNotFoundError("Shader file 'simple.glsl' not found.")
        self.canvas.shader.source = shader_path

        # Check for shader compilation errors
        if not self.canvas.shader.success:
            print("Shader compilation failed:")
            print(self.canvas.shader.log)
            raise RuntimeError("Shader compilation failed")

        # Load the OBJ model using pywavefront
        model_path = resource_find("simple.obj")
        if not model_path:
            raise FileNotFoundError("The model file 'monkey.obj' could not be found.")

        # Load the scene using pywavefront
        self.scene = pywavefront.Wavefront(
            model_path, collect_faces=True, create_materials=True
        )

        super(Renderer, self).__init__(**kwargs)

        with self.canvas:
            # Ensure setup_gl_context is called before any OpenGL operations
            self.cb = Callback(self.setup_gl_context)
            PushMatrix()
            self.setup_scene()
            PopMatrix()
            self.cb = Callback(self.reset_gl_context)

        Clock.schedule_interval(self.update_glsl, 1 / 60.)

    def setup_gl_context(self, *args):
        glEnable(GL_DEPTH_TEST)
        # You can enable backface culling if needed
        # glEnable(GL_CULL_FACE)

    def reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)

    def update_glsl(self, delta):
        # Update the projection and modelview matrices
        aspect = self.width / float(self.height)
        projection = Matrix().view_clip(-aspect, aspect, -1, 1, 1, 100, 1)
        self.canvas['projection_mat'] = projection
        # Update the rotation
        self.rot.angle += delta * 30

    def setup_scene(self):
        try:
            print("Setting up the scene...")
            # Set up the scene with transformations
            Color(1, 1, 1, 1)
            PushMatrix()
            # Adjust the scale and translation to fit the model in view
            Scale(0.5, 0.5, 0.5)
            Translate(0, -0.5, -3)
            self.rot = Rotate(0, 0, 1, 0)

            # Extract mesh data from the loaded scene
            vertices = []
            indices = []
            idx_offset = 0

            for name, mesh in self.scene.meshes.items():
                material = mesh.material
                # Use material colors if available, otherwise default to white
                diffuse_color = getattr(material, 'diffuse', [1.0, 1.0, 1.0])
                ambient_color = getattr(material, 'ambient', [0.1, 0.1, 0.1])
                self.canvas['diffuse_color'] = diffuse_color
                self.canvas['ambient_color'] = ambient_color

                # Each vertex has 8 components: [x, y, z, nx, ny, nz, u, v]
                mesh_vertices = mesh.vertices
                mesh_indices = [i + idx_offset for i in range(len(mesh_vertices) // 8)]
                vertices.extend(mesh_vertices)
                indices.extend(mesh_indices)
                idx_offset += len(mesh_vertices) // 8

            UpdateNormalMatrix()

            if not vertices or not indices:
                print("No vertices or indices found in the model file.")
                return

            # Ensure indices are within valid range
            max_index = (len(vertices) // 8) - 1
            for idx in indices:
                if idx < 0 or idx > max_index:
                    print(f"Invalid index detected: {idx}")
                    return

            # Print sample data for debugging
            print(f"Loaded {len(vertices) // 8} vertices and {len(indices) // 3} triangles.")

            # Define the vertex format to match the shader attributes
            vertex_format = [
                ('v_pos', 3, 'float'),
                ('v_normal', 3, 'float'),
                ('v_tc0', 2, 'float'),
            ]

            # Create the Mesh
            self.mesh = Mesh(
                vertices=vertices,
                indices=indices,
                fmt=vertex_format,
                mode='triangles',
            )

            self.canvas.add(self.mesh)
            PopMatrix()
            print("Scene setup complete.")
        except Exception as e:
            print(f"Error during scene setup: {e}")

class RendererApp(App):
    def build(self):
        return Renderer()

if __name__ == "__main__":
    RendererApp().run()
