#!/usr/bin/python3
import math
import pygame
import sys

from scripts.renderer import Renderer
from scripts.scene import Scene
from scripts.camera import Camera
from scripts.mesh import Mesh
from scripts.texture import Texture

from scripts.core.light import AmbientLight, DirectionalLight, PointLight
from scripts.material.phong import PhongMaterial
from scripts.material.texture import TextureMaterial

from scripts.geometry.geometry import BoxGeometry, RectangleGeometry, SphereGeometry

from scripts.extras.movement_rig import MovementRig
from scripts.extras.directional_light import DirectionalLightHelper

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
        self.renderer = Renderer([0.2, 0.2, 0.2])
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0, 2, 5])

        ambient_light = AmbientLight(color=[0.2, 0.2, 0.2])
        self.scene.add(ambient_light)

        self.directional_light = DirectionalLight(color=[0.5, 0.5, 0.5], direction=[-1, -1, 0])
        self.directional_light.set_position([2, 4, 0])
        self.scene.add(self.directional_light)
        
        direct_helper = DirectionalLightHelper(self.directional_light)
        self.directional_light.add(direct_helper)

        sky_geometry = SphereGeometry(radius=50)
        sky_material = TextureMaterial(texture=Texture(file_name="images/sky.jpg"))
        sky = Mesh(sky_geometry, sky_material)
        self.scene.add(sky)

        sphere_geometry = SphereGeometry()
        phong_material_brickwall_shadow = PhongMaterial(
            texture=Texture("images/brick-wall.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        box_geometry = BoxGeometry()
        phong_material_crate_shadown = PhongMaterial(
            texture=Texture("images/crate.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        phong_material_grass_shadown = PhongMaterial(
            texture=Texture("images/grass.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )
        sphere1 = Mesh(sphere_geometry, phong_material_brickwall_shadow)
        sphere1.set_position([-2, 1.2, 0])
        self.scene.add(sphere1)

        sphere2 = Mesh(sphere_geometry, phong_material_brickwall_shadow)
        sphere2.set_position([1, 2.2, -0.5])
        self.scene.add(sphere2)

        box = Mesh(box_geometry, phong_material_crate_shadown)
        box.set_position([0, 0.5, 0])
        self.scene.add(box)

        self.renderer.enable_shadows(self.directional_light)

        floor = Mesh(RectangleGeometry(width=20, height=20), phong_material_grass_shadown)
        floor.rotate_x(-math.pi / 2)
        self.scene.add(floor)

    def update(self):
        #"""
        # view dynamic shadows -- need to increase shadow camera range
        self.directional_light.rotate_y(0.01337, False)
        #"""
        self.rig.update( self.input, self.delta_time)
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

