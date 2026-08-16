## Builds chunk nodes from the mapgen manifest (assets/generated/manifest.json).
##
## Layers -> textured triplanar materials (world-space mapping, so the
## generated meshes need no UVs). Walkable layers get trimesh collision.
## POIs (pubs/shops) get signage, and enterable ones interior light + props.
class_name ChunkLoader

const GENERATED_DIR := "res://assets/generated"

static var _materials := {}


static func _texture_material(tex_path: String, scale: float, rough: float) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	var tex := load(tex_path) as Texture2D
	if tex != null:
		m.albedo_texture = tex
	m.uv1_triplanar = true
	m.uv1_scale = Vector3(scale, scale, scale)
	m.roughness = rough
	return m


static func _material(layer: String) -> StandardMaterial3D:
	if _materials.has(layer):
		return _materials[layer]
	var m: StandardMaterial3D
	match layer:
		"terrain":
			m = _texture_material("res://assets/textures/grass.png", 0.12, 1.0)
		"roads":
			m = _texture_material("res://assets/textures/tarmac.png", 0.2, 0.95)
		"walls":
			m = _texture_material("res://assets/textures/brick.png", 0.3, 0.9)
		"roofs":
			m = _texture_material("res://assets/textures/slate.png", 0.28, 0.85)
		"floors":
			m = _texture_material("res://assets/textures/planks.png", 0.35, 0.8)
		_:
			m = StandardMaterial3D.new()
			m.albedo_color = Color(0.8, 0.2, 0.8)  # unknown layer: loud
	_materials[layer] = m
	return m


static func load_manifest() -> Dictionary:
	var path := GENERATED_DIR.path_join("manifest.json")
	if not FileAccess.file_exists(path):
		return {}
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(path))
	return parsed if parsed is Dictionary else {}


## Manifest coords are pipeline-axes (x=east, y=north, z=up);
## Godot is (east, up, -north).
static func to_godot(x: float, y: float, z: float) -> Vector3:
	return Vector3(x, z, -y)


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
		# Roads deliberately have no collision: ribbons float 5 cm over the
		# terrain the player stands on; doubled surfaces cause jitter.
		if layer != "roads":
			var body := StaticBody3D.new()
			body.name = layer + "_col"
			var shape := CollisionShape3D.new()
			shape.shape = mesh.create_trimesh_shape()
			body.add_child(shape)
			mi.add_child(body)

	var pois: Array = chunk.get("pois", [])
	for poi in pois:
		_dress_poi(node, poi)
	return node


static func _dress_poi(parent: Node3D, poi: Dictionary) -> void:
	var kind := str(poi.get("kind", ""))
	var poi_name := str(poi.get("name", ""))
	var cx: float = poi.get("x", 0.0)
	var cy: float = poi.get("y", 0.0)
	var ground: float = poi.get("ground", 0.0)
	var enterable: bool = poi.get("enterable", false)

	# Sign above the door (or centroid), named places only.
	if poi_name != "":
		var sign_pos := to_godot(cx, cy, ground + 4.2)
		var door = poi.get("door")
		if door is Array and (door as Array).size() == 2:
			var d: Array = door
			sign_pos = to_godot(float(d[0]), float(d[1]), ground + 3.2)
		var label := Label3D.new()
		label.text = poi_name
		label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		label.font_size = 96
		label.pixel_size = 0.008
		label.modulate = Color(1.0, 0.85, 0.5) if kind == "pub" else Color(0.95, 0.95, 1.0)
		label.outline_size = 24
		label.position = sign_pos
		parent.add_child(label)

	if not enterable:
		return

	# Warm interior light so the doorway reads from the street.
	var light := OmniLight3D.new()
	light.position = to_godot(cx, cy, ground + 2.3)
	light.light_color = Color(1.0, 0.85, 0.6)
	light.light_energy = 1.4
	light.omni_range = 8.0
	light.shadow_enabled = false
	parent.add_child(light)

	# Grey-box furniture: pubs get a bar and a couple of tables, shops a counter.
	if kind == "pub":
		_add_prop(parent, to_godot(cx - 1.5, cy - 1.0, ground), Vector3(2.6, 1.1, 0.6),
				Color(0.32, 0.2, 0.12))
		_add_prop(parent, to_godot(cx + 1.6, cy + 1.2, ground), Vector3(0.9, 0.75, 0.9),
				Color(0.4, 0.28, 0.16))
		_add_prop(parent, to_godot(cx + 0.2, cy + 2.4, ground), Vector3(0.9, 0.75, 0.9),
				Color(0.4, 0.28, 0.16))
	else:
		_add_prop(parent, to_godot(cx, cy - 0.8, ground), Vector3(2.2, 0.95, 0.7),
				Color(0.5, 0.45, 0.4))


static func _add_prop(parent: Node3D, base_pos: Vector3, size: Vector3, color: Color) -> void:
	var body := StaticBody3D.new()
	body.position = base_pos + Vector3(0, size.y / 2.0 + 0.05, 0)

	var mi := MeshInstance3D.new()
	var box := BoxMesh.new()
	box.size = size
	mi.mesh = box
	var mat := StandardMaterial3D.new()
	mat.albedo_color = color
	mat.roughness = 0.8
	mi.material_override = mat
	body.add_child(mi)

	var shape := CollisionShape3D.new()
	var box_shape := BoxShape3D.new()
	box_shape.size = size
	shape.shape = box_shape
	body.add_child(shape)

	parent.add_child(body)
