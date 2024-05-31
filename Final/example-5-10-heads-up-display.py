import math

from scripts.core.base import Base
from scripts.core_ext.camera import Camera
from scripts.core_ext.mesh import Mesh
from scripts.core_ext.renderer import Renderer
from scripts.core_ext.scene import Scene
from scripts.core_ext.texture import Texture
from scripts.geometry.box import BoxGeometry
from scripts.geometry.rectangle import RectangleGeometry
from scripts.material.texture import TextureMaterial
from scripts.extras.movement_rig import MovementRig
from scripts.extras.grid import GridHelper
from scripts.extras.text_texture import TextTexture


class Example(Base):
    """
    Demonstrate a heads-up display (HUD): a transparent layer containing some images
    (for example, with a text), rendered after the main scene, and appearing on the top layer.
    Move the camera: WASDRF(move), QE(turn), TG(look).
    """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0, 1.5, 5])
        self.scene.add(self.rig)

        crate_geometry = BoxGeometry()
        crate_material = TextureMaterial(Texture("scripts/images/crate.jpg"))
        crate = Mesh(crate_geometry, crate_material)
        crate.translate(0, 0.5, 0)
        self.scene.add(crate)

        grid = GridHelper(grid_color=[1, 1, 1], center_color=[1, 1, 0])
        grid.rotate_x(-math.pi / 2)
        self.scene.add(grid)

        self.hud_scene = Scene()
        self.hud_camera = Camera()
        self.hud_camera.set_orthographic(0, 800, 0, 600, 1, -1)

        label_geometry1 = RectangleGeometry(
            width=400, height=200,
            position=[0, 600],
            alignment=[0, 1]
        )
        label_material1 = TextureMaterial(Texture("scripts/images/crate-simulator.png"))
        label1 = Mesh(label_geometry1, label_material1)
        self.hud_scene.add(label1)

        label_geometry2 = RectangleGeometry(
            width=200, height=200,
            position=[800, 0],
            alignment=[1, 0]
        )
        message = TextTexture(
            text="Version 1.0",
            system_font_name="Ink Free",
            font_size=32,
            font_color=[127, 255, 127],
            image_width=200,
            image_height=200,
            transparent=True
        )
        label_material2 = TextureMaterial(message)
        label2 = Mesh(label_geometry2, label_material2)
        self.hud_scene.add(label2)

    def update(self):
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)
        self.renderer.render(
            scene=self.hud_scene,
            camera=self.hud_camera,
            clear_color=False
        )


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()
