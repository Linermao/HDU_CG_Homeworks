import OpenGL.GL as GL
from scripts.mesh import Mesh
from scripts.geometry.geometry import Geometry
from scripts.material.basic import BasicMaterial


class LineMaterial(BasicMaterial):
    def __init__(self, vertex_shader_code=None, fragment_shader_code=None, property_dict=None, use_vertex_colors=True):
        super().__init__(vertex_shader_code, fragment_shader_code, use_vertex_colors)
        # Render vertices as continuous line by default
        self._setting_dict["drawStyle"] = GL.GL_LINE_STRIP
        # Set the line thickness
        self._setting_dict["lineWidth"] = 1
        # line type: "connected" | "loop" | "segments"
        self._setting_dict["lineType"] = "connected"
        self.set_properties(property_dict)

    def update_render_settings(self):
        GL.glLineWidth(self._setting_dict["lineWidth"])
        if self._setting_dict["lineType"] == "connected":
            self._setting_dict["drawStyle"] = GL.GL_LINE_STRIP
        elif self._setting_dict["lineType"] == "loop":
            self._setting_dict["drawStyle"] = GL.GL_LINE_LOOP
        elif self._setting_dict["lineType"] == "segments":
            self._setting_dict["drawStyle"] = GL.GL_LINES
        else:
            raise Exception("Unknown LineMaterial draw style")

class GridHelper(Mesh):
    def __init__(self, size=10, divisions=10, grid_color=(0, 0, 0), center_color=(0.5, 0.5, 0.5), line_width=1):
        geometry = Geometry()
        position_data = []
        color_data = []
        # Create range of values
        values = []
        delta_size = size / divisions
        for n in range(divisions + 1):
            values.append(-size / 2 + n * delta_size)
        # Add vertical lines
        for x in values:
            position_data.append([x, -size / 2, 0])
            position_data.append([x, size / 2, 0])
            if x == 0:
                color_data.append(center_color)
                color_data.append(center_color)
            else:
                color_data.append(grid_color)
                color_data.append(grid_color)
        # Add horizontal lines
        for y in values:
            position_data.append([-size / 2, y, 0])
            position_data.append([size / 2, y, 0])
            if y == 0:
                color_data.append(center_color)
                color_data.append(center_color)
            else:
                color_data.append(grid_color)
                color_data.append(grid_color)
        geometry.add_attribute("vec3", "vertexPosition", position_data)
        geometry.add_attribute("vec3", "vertexColor", color_data)
        material = LineMaterial(
            property_dict = {
                "useVertexColors": 1,
                "lineWidth": line_width,
                "lineType": "segments"
            }
        )
        # Initialize the mesh
        super().__init__(geometry, material)
