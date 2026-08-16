## Entry point (M1): stream the generated town around a first-person player.
extends Node3D

const PLAYER_SCENE: PackedScene = preload("res://src/player/player.tscn")

@onready var streamer: WorldStreamer = $WorldStreamer


func _ready() -> void:
	var manifest := ChunkLoader.load_manifest()
	if manifest.is_empty():
		push_warning(
			"No generated map found. Run the pipeline first:\n"
			+ "  pip install -e tools/mapgen[dev]\n"
			+ "  mapgen build --config tools/mapgen/atherton.toml --fixture\n"
			+ "then restart. (Real data: see tools/mapgen/README.md)"
		)
		return

	var spawn := _spawn_point(manifest)
	var player := PLAYER_SCENE.instantiate() as Player

	streamer.setup(manifest, player)
	streamer.force_load_at(spawn)  # ground exists before the player drops in

	player.position = spawn
	add_child(player)

	var npc_manager := NPCManager.new()
	npc_manager.name = "NPCManager"
	add_child(npc_manager)
	npc_manager.setup(player, streamer)

	var chunks: Array = manifest.get("chunks", [])
	print("Atherton: spawned at %s — %d/%d chunks in, streaming the rest (%s)" % [
		str(spawn), streamer.loaded_count(), chunks.size(),
		str(manifest.get("generator", "?")),
	])


## Spawn in the densest chunk — with real data that is Market Street.
func _spawn_point(manifest: Dictionary) -> Vector3:
	var chunks: Array = manifest.get("chunks", [])
	var best: Dictionary = {}
	var best_n := -1
	for c in chunks:
		var n: int = c.get("n_buildings", 0)
		if n > best_n:
			best_n = n
			best = c
	var aabb: Array = best.get("aabb", [])
	if aabb.size() != 6:
		return Vector3(0.0, 100.0, 0.0)
	# Manifest AABB is pipeline-axes (x=east, y=north, z=up);
	# Godot position is (east, up, -north). See tools/mapgen meshio.py.
	var cx: float = (aabb[0] + aabb[3]) / 2.0
	var cy: float = (aabb[1] + aabb[4]) / 2.0
	var top: float = aabb[5]
	return Vector3(cx, top + 2.0, -cy)
