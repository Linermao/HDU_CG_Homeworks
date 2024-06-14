import math
import pygame
import sys

from scripts.render.renderer import Renderer
from scripts.scene import Scene
from scripts.camera.camera import Camera
from scripts.core.mesh import Mesh
from scripts.material.texture import Texture

from scripts.light.light import AmbientLight, DirectionalLight, PointLight
from scripts.material.phong import PhongMaterial
from scripts.material.texture_material import TextureMaterial

from scripts.geometry.geometry import BoxGeometry, RectangleGeometry, SphereGeometry, OBJGeometry

from scripts.camera.movement_rig import MovementRig

from scripts.core.input import Input
from scripts.core.utils import Utils

class Example():
    """
    Render shadows using shadow pass by depth buffers for the directional light.
    """

    def __init__(self, screen_size=(512, 512)):
        # Initialize all pygame modules
        pygame.init()
        # Indicate rendering details
        display_flags = pygame.DOUBLEBUF | pygame.OPENGL
        # Initialize buffers to perform antialiasing
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        # Use a core OpenGL profile for cross-platform compatibility
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        # Create and display the window
        self._screen = pygame.display.set_mode(screen_size, display_flags)
        # Set the text that appears in the title bar of the window
        pygame.display.set_caption("Graphics Window")
        # Determine if main loop is active
        self._running = True
        # Manage time-related data and operations
        self._clock = pygame.time.Clock()
        # Manage user input
        self._input = Input()
        # number of seconds application has been running
        self._time = 0
        # Print the system information
        Utils.print_system_info()
    
    @property
    def delta_time(self):
        return self._delta_time

    @property
    def input(self):
        return self._input

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    def initialize(self):
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.rig = MovementRig(units_per_second=5)
        self.rig.add(self.camera)
        self.rig.set_position([0, 2, 15])

        ambient_light = AmbientLight(color=[0.05, 0.05, 0.05])
        self.scene.add(ambient_light)

        self.directional_light = DirectionalLight(color=[0.9, 0.9, 0.9], direction=[-1, 0, 0])
        self.directional_light.set_position([10, 0, 0])
        self.scene.add(self.directional_light)

        # direct_helper = DirectionalLightHelper(self.directional_light)
        # self.directional_light.add(direct_helper)

        sky_geometry = SphereGeometry(radius=50)
        sky_material = TextureMaterial(texture=Texture(file_name="images/space.jpg"))
        sky = Mesh(sky_geometry, sky_material)
        self.scene.add(sky)

        Geometry_earth = SphereGeometry(radius=1.0)
        Geometry_sun = SphereGeometry(radius=3)
        Geometry_moon = SphereGeometry(radius=0.5)
        Geometry_airplane = OBJGeometry(size=0.05)
       
        phong_material_earth = PhongMaterial(
            texture=Texture("images/earth.jpeg"),
            number_of_light_sources=2,
            use_shadow=True
        )
        
        phong_material_sun = TextureMaterial(
            texture=Texture("images/sun.jpeg")
        )

        phong_material_moon = PhongMaterial(
            texture=Texture("images/moon.png"),
            number_of_light_sources=2,
            use_shadow=True
        )
        
        phong_material_airplane = PhongMaterial(
            texture=Texture("images/metal.png"),
            number_of_light_sources=2,
            use_shadow=True
        )

        earth = Mesh(Geometry_earth, phong_material_earth)
        earth.set_position([0, 0, 0])
        self.scene.add(earth)

        sun = Mesh(Geometry_sun, phong_material_sun)
        sun.set_position([20, 0, 0])
        self.scene.add(sun)

        moon = Mesh(Geometry_moon, phong_material_moon)
        moon.set_position([-5, 0, 0])
        self.scene.add(moon)

        airplane = Mesh(Geometry_airplane, phong_material_airplane)
        airplane.set_position([0, 2, 0])
        airplane.rotate_x(90)
        self.scene.add(airplane)

        '''
        Geometry_box = BoxGeometry()

        phong_material_box = PhongMaterial(
            texture=Texture("images/crate.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        box = Mesh(Geometry_box, phong_material_box)
        box.set_position([0, 5, 0])
        self.scene.add(box)
        '''

        self.sun = sun
        self.earth = earth
        self.moon = moon
        self.airplane = airplane
        
        self.renderer.enable_shadows(self.directional_light)

    def update(self):
        #"""
        self.sun.rotate_y(0.00005, True)

        self.directional_light.rotate_y(0.0005, False)
        self.sun.rotate_y(0.0005, False)

        self.earth.rotate_y(0.01, True)
        self.moon.rotate_y(0.005, True)
        self.moon.rotate_y(0.005, False)
        self.airplane.rotate_z(0.005, True)
        #"""
        self.rig.update(self.input, self.delta_time)

        self.renderer.render(self.scene, self.camera)

    def run(self):
        # Startup #
        self.initialize()
        # main loop #
        while self._running:
            # process input #
            self._input.update()
            if self._input.quit:
                self._running = False
            # seconds since iteration of run loop
            self._delta_time = self._clock.get_time() / 1000
            # Increment time application has been running
            self._time += self._delta_time
            # Update #
            self.update()
            # Render #
            # Display image on screen
            pygame.display.flip()
            # Pause if necessary to achieve 60 FPS
            self._clock.tick(60)
        # Shutdown #
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Example(screen_size=[800, 600]).run()