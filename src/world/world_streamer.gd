## Ring-based chunk streaming (PRD 03/08, M1 version).
##
## Loads chunks within LOAD_RADIUS of the target (the player), at most one
## per frame to avoid hitches; unloads beyond UNLOAD_RADIUS (hysteresis so
## chunks don't thrash at the boundary). Distances are measured on the
## ground plane to each chunk's AABB centre.
class_name WorldStreamer
extends Node3D

const LOAD_RADIUS := 450.0
const UNLOAD_RADIUS := 620.0

var _chunks_by_id: Dictionary = {}  # id -> manifest chunk dict
var _loaded: Dictionary = {}        # id -> Node3D
var _queue: Array[String] = []
var _target: Node3D = null


func setup(manifest: Dictionary, target: Node3D) -> void:
	_target = target
	for c in manifest.get("chunks", []):
		_chunks_by_id[str(c.get("id"))] = c


## Synchronously load everything around a point — used once at spawn so the
## player never drops through not-yet-loaded ground.
func force_load_at(pos: Vector3) -> void:
	_refresh_queue(pos)
	while not _queue.is_empty():
		_load_next()


func _process(_delta: float) -> void:
	if _target == null or not _target.is_inside_tree():
		return
	var pos := _target.global_position
	_refresh_queue(pos)
	if not _queue.is_empty():
		_load_next()
	_unload_one_far(pos)


func _chunk_dist(chunk: Dictionary, pos: Vector3) -> float:
	var aabb: Array = chunk.get("aabb", [])
	if aabb.size() != 6:
		return INF
	# Manifest AABB is pipeline-axes (x=east, y=north); Godot z = -north.
	var cx: float = (aabb[0] + aabb[3]) / 2.0
	var cz: float = -((aabb[1] + aabb[4]) / 2.0)
	return Vector2(pos.x - cx, pos.z - cz).length()


func _refresh_queue(pos: Vector3) -> void:
	_queue.clear()
	var candidates: Array = []
	for id in _chunks_by_id:
		if _loaded.has(id):
			continue
		var d := _chunk_dist(_chunks_by_id[id], pos)
		if d <= LOAD_RADIUS:
			candidates.append([d, id])
	candidates.sort()  # nearest first
	for c in candidates:
		_queue.append(str(c[1]))


func _load_next() -> void:
	if _queue.is_empty():
		return
	var id: String = _queue.pop_front()
	if _loaded.has(id):
		return
	var node := ChunkLoader.build_chunk(_chunks_by_id[id])
	add_child(node)
	_loaded[id] = node


func _unload_one_far(pos: Vector3) -> void:
	for id in _loaded:
		if _chunk_dist(_chunks_by_id[id], pos) > UNLOAD_RADIUS:
			var node: Node3D = _loaded[id]
			node.queue_free()
			_loaded.erase(id)
			return  # one per frame; erase-while-iterating is unsafe anyway


func loaded_count() -> int:
	return _loaded.size()


## Road points (in Godot coords) from LOADED chunks within a ring around pos.
## Used for NPC spawning and wander targets, so pedestrians stick to streets.
func spawn_points_near(pos: Vector3, r_min: float, r_max: float, max_n: int) -> Array[Vector3]:
	var out: Array[Vector3] = []
	for id in _loaded:
		var chunk: Dictionary = _chunks_by_id[id]
		var pts: Array = chunk.get("road_points", [])
		for p in pts:
			var arr: Array = p
			if arr.size() != 3:
				continue
			var v := Vector3(float(arr[0]), float(arr[2]) + 0.4, -float(arr[1]))
			var d := Vector2(v.x - pos.x, v.z - pos.z).length()
			if d >= r_min and d <= r_max:
				out.append(v)
				if out.size() >= max_n:
					return out
	return out
