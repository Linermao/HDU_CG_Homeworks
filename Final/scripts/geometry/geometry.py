import OpenGL.GL as GL
import numpy as np
import math
from scripts.core.matrix import Matrix
import pywavefront


class Attribute:
    def __init__(self, data_type, data):
        # type of elements in data array: int | float | vec2 | vec3 | vec4
        self._data_type = data_type
        # array of data to be stored in buffer
        self._data = data
        # reference of available buffer from GPU
        self._buffer_ref = GL.glGenBuffers(1)
        # Upload data immediately
        self.upload_data()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    def upload_data(self):
        """ Upload the data to a GPU buffer """
        # Convert data to numpy array format; convert numbers to 32-bit floats
        data = np.array(self._data).astype(np.float32)
        # Select buffer used by the following functions
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._buffer_ref)
        # Store data in currently bound buffer
        GL.glBufferData(GL.GL_ARRAY_BUFFER, data.ravel(), GL.GL_STATIC_DRAW)

    def associate_variable(self, program_ref, variable_name):
        """ Associate variable in program with the buffer """
        # Get reference for program variable with given name
        variable_ref = GL.glGetAttribLocation(program_ref, variable_name)
        # If the program does not reference the variable, then exit
        if variable_ref != -1:
            # Select buffer used by the following functions
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._buffer_ref)
            # Specify how data will be read from the currently bound buffer into the specified variable
            if self._data_type == "int":
                GL.glVertexAttribPointer(variable_ref, 1, GL.GL_INT, False, 0, None)
            elif self._data_type == "float":
                GL.glVertexAttribPointer(variable_ref, 1, GL.GL_FLOAT, False, 0, None)
            elif self._data_type == "vec2":
                GL.glVertexAttribPointer(variable_ref, 2, GL.GL_FLOAT, False, 0, None)
            elif self._data_type == "vec3":
                GL.glVertexAttribPointer(variable_ref, 3, GL.GL_FLOAT, False, 0, None)
            elif self._data_type == "vec4":
                GL.glVertexAttribPointer(variable_ref, 4, GL.GL_FLOAT, False, 0, None)
            else:
                raise Exception(f'Attribute {variable_name} has unknown type {self._data_type}')
            # Indicate that data will be streamed to this variable
            GL.glEnableVertexAttribArray(variable_ref)

class Geometry:
    """ Stores attribute data and the total number of vertices """
    def __init__(self):
        # Store Attribute objects, indexed by name of associated variable in shader.
        # Shader variable associations set up later and stored in vertex array object in Mesh.
        self._attribute_dict = {}
        # number of vertices
        self._vertex_count = None

    @property
    def attribute_dict(self):
        return self._attribute_dict

    @property
    def vertex_count(self):
        return self._vertex_count

    def add_attribute(self, data_type, variable_name, data):
        attribute = Attribute(data_type, data)
        self._attribute_dict[variable_name] = attribute
        # Update the vertex count
        if variable_name == "vertexPosition":
            # Number of vertices may be calculated from
            # the length of any Attribute object's array of data
            self._vertex_count = len(data)

    def upload_data(self, variable_names=None):
        if not variable_names:
            variable_names = self._attribute_dict.keys()
        for variable_name in variable_names:
            self._attribute_dict[variable_name].upload_data()
            # Update the vertex count
            if variable_name == "vertexPosition":
                # Number of vertices may be calculated from
                # the length of any Attribute object's array of data
                self._vertex_count = len(self._attribute_dict[variable_name].data)

    def apply_matrix(self, matrix):
        """ Transform the data in an attribute using a matrix """
        old_position_data = self._attribute_dict["vertexPosition"].data
        new_position_data = []
        for old_pos in old_position_data:
            # Avoid changing list references
            new_pos = old_pos.copy()
            # Add the homogeneous fourth coordinate
            new_pos.append(1)
            # Multiply by matrix.
            # No need to transform new_pos to np.array.
            new_pos = matrix @ new_pos
            # Remove the homogeneous coordinate
            new_pos = list(new_pos[0:3])
            # Add to the new data list
            new_position_data.append(new_pos)
        self._attribute_dict["vertexPosition"].data = new_position_data
        # New data must be uploaded
        self._attribute_dict["vertexPosition"].upload_data()
        self._vertex_count = len(new_position_data)

        # Extract the rotation submatrix
        rotation_matrix = np.array(
            [matrix[0][0:3],
             matrix[1][0:3],
             matrix[2][0:3]]
        ).astype(float)

        old_vertex_normal_data = self._attribute_dict["vertexNormal"].data
        new_vertex_normal_data = []
        for old_normal in old_vertex_normal_data:
            # Avoid changing list references
            new_normal = old_normal.copy()
            new_normal = rotation_matrix @ new_normal
            new_vertex_normal_data.append(new_normal)
        self._attribute_dict["vertexNormal"].data = new_vertex_normal_data
        # New data must be uploaded
        self._attribute_dict["vertexNormal"].upload_data()

        old_face_normal_data = self._attribute_dict["faceNormal"].data
        new_face_normal_data = []
        for old_normal in old_face_normal_data:
            # Avoid changing list references
            new_normal = old_normal.copy()
            new_normal = rotation_matrix @ new_normal
            new_face_normal_data.append(new_normal)
        self._attribute_dict["faceNormal"].data = new_face_normal_data
        # New data must be uploaded
        self._attribute_dict["faceNormal"].upload_data()

    def merge(self, other_geometry):
        """
        Merge data from attributes of other geometry into this object.
        Requires both geometries to have attributes with same names.
        """
        for variable_name, attribute_instance in self._attribute_dict.items():
            attribute_instance.data.extend(other_geometry.attribute_dict[variable_name].data)
            # New data must be uploaded
            attribute_instance.upload_data()

class ParametricGeometry(Geometry):
    """
    Parametric geometry defined by
    (x, y, z) = surface_function(u, v),
    where u and v are the parameters
    """
    def __init__(self,
                 u_start, u_end, u_resolution,
                 v_start, v_end, v_resolution,
                 surface_function):
        super().__init__()
        # Generate set of points on function
        delta_u = (u_end - u_start) / u_resolution
        delta_v = (v_end - v_start) / v_resolution

        position_list = []
        texture_position_list = []
        vertex_normal_list = []
        for u_index in range(u_resolution + 1):
            xyz_list = []
            uv_list = []
            n_list = []
            for v_index in range(v_resolution + 1):
                # 3D vertex coordinates
                u = u_start + u_index * delta_u
                v = v_start + v_index * delta_v
                p = surface_function(u, v)
                xyz_list.append(p)
                # 3D normal coordinates
                p1 = surface_function(u + delta_u/1e3, v)
                p2 = surface_function(u, v + delta_v/1e3)
                normal_vector = self.calculate_normal(p, p1, p2)
                n_list.append(normal_vector)
                # 2D texture coordinates
                u_texture = u_index / u_resolution
                v_texture = v_index / v_resolution
                uv_list.append([u_texture, v_texture])
            position_list.append(xyz_list)
            vertex_normal_list.append(n_list)
            texture_position_list.append(uv_list)

        # Store vertex data
        position_data = []
        color_data = []
        uv_data = []
        # default vertex colors
        c1, c2, c3 = [1, 0, 0], [0, 1, 0], [0, 0, 1]
        c4, c5, c6 = [0, 1, 1], [1, 0, 1], [1, 1, 0]
        vertex_normal_data = []
        face_normal_data = []

        # Group vertex data into triangles.
        # Note: .copy() is necessary to avoid storing references.
        # position_data will be also copied in apply_matrix() in the Geometry class.
        for i_index in range(u_resolution):
            for j_index in range(v_resolution):
                # position data
                p_a = position_list[i_index + 0][j_index + 0]
                p_b = position_list[i_index + 1][j_index + 0]
                p_c = position_list[i_index + 1][j_index + 1]
                p_d = position_list[i_index + 0][j_index + 1]
                position_data += [p_a.copy(), p_b.copy(), p_c.copy(),
                                  p_a.copy(), p_c.copy(), p_d.copy()]
                # color data
                color_data += [c1, c2, c3,
                               c4, c5, c6]
                # uv data of texture coordinates
                uv_a = texture_position_list[i_index + 0][j_index + 0]
                uv_b = texture_position_list[i_index + 1][j_index + 0]
                uv_c = texture_position_list[i_index + 1][j_index + 1]
                uv_d = texture_position_list[i_index + 0][j_index + 1]
                uv_data += [uv_a, uv_b, uv_c,
                            uv_a, uv_c, uv_d]
                # vertex normal vectors
                n_a = vertex_normal_list[i_index + 0][j_index + 0]
                n_b = vertex_normal_list[i_index + 1][j_index + 0]
                n_c = vertex_normal_list[i_index + 1][j_index + 1]
                n_d = vertex_normal_list[i_index + 0][j_index + 1]
                vertex_normal_data += [n_a.copy(), n_b.copy(), n_c.copy(),
                                       n_a.copy(), n_c.copy(), n_d.copy()]
                # face normal vectors
                fn0 = self.calculate_normal(p_a, p_b, p_c)
                fn1 = self.calculate_normal(p_a, p_c, p_d)
                face_normal_data += [fn0.copy(), fn0.copy(), fn0.copy(),
                                     fn1.copy(), fn1.copy(), fn1.copy()]

        self.add_attribute("vec3", "vertexPosition", position_data)
        self.add_attribute("vec3", "vertexColor", color_data)
        self.add_attribute("vec2", "vertexUV", uv_data)
        self.add_attribute("vec3", "vertexNormal", vertex_normal_data)
        self.add_attribute("vec3", "faceNormal", face_normal_data)

    @staticmethod
    def calculate_normal(p0, p1, p2):
        v1 = np.array(p1) - np.array(p0)
        v2 = np.array(p2) - np.array(p0)
        orthogonal_vector = np.cross(v1, v2)
        norm = np.linalg.norm(orthogonal_vector)
        normal_vector = orthogonal_vector / norm if norm > 1e-6 \
            else np.array(p0) / np.linalg.norm(p0)
        return normal_vector

class BoxGeometry(Geometry):
    def __init__(self, width=1, height=1, depth=1):
        super().__init__()
        # vertices
        p0 = [-width / 2, -height / 2, -depth / 2]
        p1 = [width / 2, -height / 2, -depth / 2]
        p2 = [-width / 2, height / 2, -depth / 2]
        p3 = [width / 2, height / 2, -depth / 2]
        p4 = [-width / 2, -height / 2, depth / 2]
        p5 = [width / 2, -height / 2, depth / 2]
        p6 = [-width / 2, height / 2, depth / 2]
        p7 = [width / 2, height / 2, depth / 2]
        # colors for faces in order:
        # x+, x-, y+, y-, z+, z-
        c1, c2 = [1, 0.5, 0.5], [0.5, 0, 0]
        c3, c4 = [0.5, 1, 0.5], [0, 0.5, 0]
        c5, c6 = [0.5, 0.5, 1], [0, 0, 0.5]
        # texture coordinates
        t0, t1, t2, t3 = [0, 0], [1, 0], [0, 1], [1, 1]
        # Each side consists of two triangles
        position_data = [p5, p1, p3, p5, p3, p7,
                         p0, p4, p6, p0, p6, p2,
                         p6, p7, p3, p6, p3, p2,
                         p0, p1, p5, p0, p5, p4,
                         p4, p5, p7, p4, p7, p6,
                         p1, p0, p2, p1, p2, p3]
        color_data = [c1] * 6 + [c2] * 6 + [c3] * 6 \
                   + [c4] * 6 + [c5] * 6 + [c6] * 6
        uv_data = [t0, t1, t3, t0, t3, t2] * 6
        self.add_attribute("vec3", "vertexPosition", position_data)
        self.add_attribute("vec3", "vertexColor", color_data)
        self.add_attribute("vec2", "vertexUV", uv_data)
        # normal vectors for x+, x-, y+, y-, z+, z-
        n1, n2 = [1, 0, 0], [-1, 0, 0]
        n3, n4 = [0, 1, 0], [0, -1, 0]
        n5, n6 = [0, 0, 1], [0, 0, -1]
        normal_data = [n1]*6 + [n2]*6 + [n3]*6 + [n4]*6 + [n5]*6 + [n6]*6
        self.add_attribute("vec3", "vertexNormal", normal_data)
        self.add_attribute("vec3", "faceNormal", normal_data)

class RectangleGeometry(Geometry):
    def __init__(self, width=1, height=1, position=(0, 0), alignment=(0.5, 0.5)):
        super().__init__()
        # vertices
        # p2 - p3
        # |  /  |
        # p0 - p1
        # p0 = [-width/2, -height/2, 0]
        # p1 = [ width/2, -height/2, 0]
        # p2 = [-width/2,  height/2, 0]
        # p3 = [ width/2,  height/2, 0]
        x, y = position
        a, b = alignment
        p0 = [x + (-a) * width, y + (-b) * height, 0]
        p1 = [x + (1 - a) * width, y + (-b) * height, 0]
        p2 = [x + (-a) * width, y + (1 - b) * height, 0]
        p3 = [x + (1 - a) * width, y + (1 - b) * height, 0]
        # colors
        c0, c1, c2, c3 = [1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1]
        # texture coordinates
        t0, t1, t2, t3 = [0, 0], [1, 0], [0, 1], [1, 1]
        # triangles p0-p1-p3 and p0-p3-p2
        # p2 - p3
        # |  /  |
        # p0 - p1
        position_data = [p0, p1, p3, p0, p3, p2]
        color_data = [c0, c1, c3, c0, c3, c2]
        # color_data = [c0, c0, c0, c1, c1, c1]
        uv_data = [t0, t1, t3, t0, t3, t2]
        self.add_attribute("vec3", "vertexPosition", position_data)
        self.add_attribute("vec3", "vertexColor", color_data)
        self.add_attribute("vec2", "vertexUV", uv_data)
        normal_data = [[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]]
        self.add_attribute("vec3", "vertexNormal", normal_data)
        self.add_attribute("vec3", "faceNormal", normal_data)

class EllipsoidGeometry(ParametricGeometry):
    def __init__(self, width=1, height=1, depth=1, theta_segments=16, phi_segments=32):
        def surface_function(u, v):
            # [x, y, z] = surface_function(u, v)
            # Here,
            # x = width / 2 * sin(theta) * cos(phi),
            # y = height / 2 * sin(theta) * sin(phi),
            # z = depth / 2 * cos(theta),
            # where 0 <= theta < pi, 0 <= phi < 2*pi.
            # Then, u = phi / (2*pi), v = (1 - theta/pi).
            # Then, phi = 2 * pi * u, theta = (1 - v)*pi.
            phi = 2 * math.pi * u
            theta = (1 - v) * math.pi
            return [width / 2 * math.sin(theta) * math.cos(phi),
                    height / 2 * math.sin(theta) * math.sin(phi),
                    depth / 2 * math.cos(theta)]

        super().__init__(u_start=0,
                         u_end=1,
                         u_resolution=phi_segments,
                         v_start=0,
                         v_end=1,
                         v_resolution=theta_segments,
                         surface_function=surface_function)
        # Rotate the ellipsoid around the x-axis on -90 degrees.
        # The vertices and normals will be recalculated.
        self.apply_matrix(Matrix.make_rotation_x(-math.pi/2))

class SphereGeometry(EllipsoidGeometry):
    def __init__(self, radius=1, theta_segments=16, phi_segments=32):
        super().__init__(2*radius, 2*radius, 2*radius, theta_segments, phi_segments)


class OBJGeometry(Geometry):
    def __init__(self, size=1.0):
        super().__init__()
        model = pywavefront.Wavefront('./model/satellite_obj.obj', create_materials=True, collect_faces=True)
        vertices = model.vertices
        faces = []
        for mesh in model.mesh_list:
            faces.extend(mesh.faces)

        position_data = []
        normal_data = []
        uv_data = []
        material_data = []

        for face in faces:
            for vertex_index in face:
                vertex = vertices[vertex_index]
                position_data.append(vertex[:3])
                if len(vertex) >= 6:
                    normal_data.append(vertex[3:6])
                if len(vertex) == 8:
                    uv_data.append(vertex[6:8])
                
                # Assuming one material per face (basic handling)
                material = model.mesh_list[0].materials[0]
                color = material.diffuse if material and hasattr(material, 'diffuse') else [1, 1, 1]
                material_data.append(color)

        if not normal_data:
            normal_data = [[0.5, 0.5, 0.5]] * len(position_data)
        if not uv_data:
            uv_data = [[0.5, 0.5]] * len(position_data)

        position_data_p = np.array(position_data)
        position_data_p *= size
        position_data = position_data_p.tolist()

        self.add_attribute("vec3", "vertexPosition", position_data)
        self.add_attribute("vec3", "vertexNormal", normal_data)
        self.add_attribute("vec2", "vertexUV", uv_data)
        self.add_attribute("vec3", "vertexColor", material_data)
