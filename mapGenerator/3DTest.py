from pywavefront import Wavefront

# Load the source OBJ file
source_file_path = "cube.obj"
source_mesh = Wavefront(source_file_path)

# Create a new mesh for the imported file
imported_mesh = Wavefront("empty.obj")

# Add the vertices and faces from the source mesh to the imported mesh
imported_mesh.vertices.extend(source_mesh.vertices)
imported_mesh.normals.extend(source_mesh.normals)
imported_mesh.texcoords.extend(source_mesh.texcoords)
imported_mesh.faces.extend(source_mesh.faces)

# Set the position of the imported mesh
x = 10.0
y = 0.0
z = 5.0
for vertex in imported_mesh.vertices:
    vertex[0] += x
    vertex[1] += y
    vertex[2] += z

# Save the modified mesh to a new OBJ file
output_file_path = "output.obj"
imported_mesh.save(output_file_path)

print("OBJ file successfully created:", output_file_path)