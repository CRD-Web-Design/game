## Minimal runtime OBJ parser for mapgen grey-box output.
##
## Loads `v`/`f` records into an ArrayMesh (positions only; normals are
## generated). Exists so generated meshes need no editor import step and the
## pipeline can rebuild while the game runs. Replaced by glTF at M2.
class_name ObjLoader


static func load_mesh(path: String) -> ArrayMesh:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("ObjLoader: cannot open %s" % path)
		return null

	var verts := PackedVector3Array()
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)

	while not file.eof_reached():
		var line := file.get_line()
		if line.begins_with("v "):
			var p := line.split(" ", false)
			verts.append(Vector3(p[1].to_float(), p[2].to_float(), p[3].to_float()))
		elif line.begins_with("f "):
			var p := line.split(" ", false)
			# Fan-triangulate; indices may be v, v/vt, v/vt/vn or v//vn.
			var idx: Array[int] = []
			for k in range(1, p.size()):
				idx.append(p[k].get_slice("/", 0).to_int() - 1)
			for k in range(1, idx.size() - 1):
				st.add_vertex(verts[idx[0]])
				st.add_vertex(verts[idx[k]])
				st.add_vertex(verts[idx[k + 1]])

	st.generate_normals()
	return st.commit()
