from scripts.core.object3d import Object3D

class Light(Object3D):
    AMBIENT = 1
    DIRECTIONAL = 2
    POINT = 3

    def __init__(self, light_type=0):
        super().__init__()
        self._light_type = light_type
        self._color = [1, 1, 1]
        self._attenuation = [1, 0, 0]

    @property
    def light_type(self):
        return self._light_type

    @property
    def color(self):
        return self._color

    @property
    def attenuation(self):
        return self._attenuation

class AmbientLight(Light):
    def __init__(self, color=(1, 1, 1)):
        super().__init__(Light.AMBIENT)
        self._color = color

class DirectionalLight(Light):
    def __init__(self, color=(1, 1, 1), direction=(0, -1, 0)):
        super().__init__(Light.DIRECTIONAL)
        self._color = color
        self.set_direction(direction)

class PointLight(Light):
    def __init__(self,
                 color=(1, 1, 1),
                 position=(0, 0, 0),
                 attenuation=(1, 0, 0.1)
                 ):
        super().__init__(Light.POINT)
        self._color = color
        self._attenuation = attenuation
        self.set_position(position)

