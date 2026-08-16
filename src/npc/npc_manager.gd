## Keeps an ambient crowd alive in a ring around the player (PRD 06).
##
## Spawns on road points from streamed chunks, despawns when far behind,
## and hands NPCs wander targets so they follow the street network rather
## than drifting into fields.
class_name NPCManager
extends Node

const TARGET_COUNT := 28
const SPAWN_MIN := 30.0     # not right in the player's face
const SPAWN_MAX := 110.0
const DESPAWN_BEYOND := 170.0
const THINK_INTERVAL := 0.5

var _player: Node3D = null
var _streamer: WorldStreamer = null
var _think_left := 0.0


func setup(player: Node3D, streamer: WorldStreamer) -> void:
	_player = player
	_streamer = streamer


func _process(delta: float) -> void:
	if _player == null or _streamer == null or not _player.is_inside_tree():
		return
	_think_left -= delta
	if _think_left > 0.0:
		return
	_think_left = THINK_INTERVAL

	var pos := _player.global_position

	# Cull the far-behind (dead NPCs despawn on their own timer).
	var alive := 0
	for child in get_children():
		var npc := child as NPC
		if npc == null:
			continue
		if npc.global_position.distance_to(pos) > DESPAWN_BEYOND:
			npc.queue_free()
		else:
			alive += 1

	# Top up, a couple per think-tick to spread the cost.
	if alive < TARGET_COUNT:
		var points := _streamer.spawn_points_near(pos, SPAWN_MIN, SPAWN_MAX, 60)
		var to_spawn := mini(TARGET_COUNT - alive, 3)
		for _i in range(to_spawn):
			if points.is_empty():
				break
			var p: Vector3 = points.pick_random()
			var npc := NPC.new()
			npc.manager = self
			add_child(npc)
			npc.global_position = p + Vector3(0, 0.7, 0)


## A road point near the asker, so pedestrians follow streets.
func wander_target_near(from_pos: Vector3) -> Vector3:
	if _streamer == null:
		return Vector3.ZERO
	var points := _streamer.spawn_points_near(from_pos, 5.0, 60.0, 30)
	if points.is_empty():
		return Vector3.ZERO
	var p: Vector3 = points.pick_random()
	return p
