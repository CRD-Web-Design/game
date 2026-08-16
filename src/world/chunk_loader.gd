## Builds chunk nodes from the mapgen manifest (assets/generated/manifest.json).
##
## M0: loads every chunk up front — the fixture town is tiny. The ring-
## streaming system specified in PRD 03/08 replaces the load-all loop at M1.
class_name ChunkLoader

const GENERATED_DIR := "res://assets/generated"

# Grey-box layer palette (PRD 09 comes much later; grey is the point at M0).
static var _materials := {}


static func _material(layer: String) -> StandardMaterial3D:
	if _materials.has(layer):
		return _materials[layer]
	var m := StandardMaterial3D.new()
	match layer:
		"terrain":
			m.albedo_color = Color(0.38, 0.42, 0.34)
		"roads":
			m.albedo_color = Color(0.22, 0.22, 0.24)
		"buildings":
			m.albedo_color = Color(0.65, 0.63, 0.60)
		_:
			m.albedo_color = Color(0.8, 0.2, 0.8)  # unknown layer: loud
	_materials[layer] = m
	return m


static func load_manifest() -> Dictionary:
	var path := GENERATED_DIR.path_join("manifest.json")
	if not FileAccess.file_exists(path):
		return {}
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(path))
	return parsed if parsed is Dictionary else {}


static func build_chunk(chunk: Dictionary) -> Node3D:
	var node := Node3D.new()
	node.name = str(chunk.get("id", "chunk"))
	var layers: Dictionary = chunk.get("layers", {})
	for layer in layers:
		var mesh := ObjLoader.load_mesh(GENERATED_DIR.path_join(layers[layer]))
		if mesh == null:
			continue
		var mi := MeshInstance3D.new()
		mi.name = layer
		mi.mesh = mesh
		mi.material_override = _material(layer)
		node.add_child(mi)
		# Walkable layers get trimesh collision. Roads deliberately don't:
		# ribbons float 5 cm above the terrain the player already stands on,
		# and doubled surfaces make CharacterBody3D jitter.
		if layer == "terrain" or layer == "buildings":
			var body := StaticBody3D.new()
			body.name = layer + "_col"
			var shape := CollisionShape3D.new()
			shape.shape = mesh.create_trimesh_shape()
			body.add_child(shape)
			mi.add_child(body)
	return node
