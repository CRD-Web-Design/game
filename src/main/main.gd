## M0 entry point: load the generated grey-box town and drop a fly camera on it.
extends Node3D

@onready var camera: Camera3D = $FlyCamera


func _ready() -> void:
	var manifest := ChunkLoader.load_manifest()
	if manifest.is_empty():
		push_warning(
			"No generated map found. Run the pipeline first:\n"
			+ "  pip install -e tools/mapgen[dev]\n"
			+ "  mapgen build --config tools/mapgen/atherton.toml --fixture\n"
			+ "then restart. (Real data: see docs/reference/data-sources-and-licences.md)"
		)
		return

	var chunks: Array = manifest.get("chunks", [])
	for chunk in chunks:
		add_child(ChunkLoader.build_chunk(chunk))
	print("Atherton grey-box: %d chunks loaded (%s)" % [chunks.size(), manifest.get("generator", "?")])

	_frame_camera(chunks)


## Start the camera above the most built-up chunk, looking across the town.
func _frame_camera(chunks: Array) -> void:
	var best: Dictionary = {}
	for c in chunks:
		if c.get("layers", {}).has("buildings"):
			best = c
			break
	if best.is_empty() and not chunks.is_empty():
		best = chunks[0]
	if best.is_empty():
		return
	var aabb: Array = best.get("aabb", [])
	if aabb.size() != 6:
		return
	# Manifest AABB is in pipeline axes (x=east, y=north, z=up);
	# Godot position is (east, up, -north). See tools/mapgen meshio.py.
	# Explicit float types: `:=` cannot infer from untyped-Array elements.
	var cx: float = (aabb[0] + aabb[3]) / 2.0
	var cy: float = (aabb[1] + aabb[4]) / 2.0
	var top: float = aabb[5]
	camera.position = Vector3(cx, top + 120.0, -(cy - 180.0))
	camera.look_at(Vector3(cx, top, -cy))
