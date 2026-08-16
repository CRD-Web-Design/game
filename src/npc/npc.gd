## Ambient townsperson (PRD 06, vertical-slice version).
##
## Adults only, generated composites — per the PRD's hard constraints no
## child characters exist and no real person is depicted.
##
## Behaviour ladder: wander along road points -> flee from gunshots or
## injury -> down. Visuals are a capsule + head until the character pass.
class_name NPC
extends CharacterBody3D

const STATE_WANDER := 0
const STATE_FLEE := 1
const STATE_DEAD := 2

const WALK_SPEED := 1.4
const FLEE_SPEED := 5.2
const FLEE_TIME := 12.0
const GUNSHOT_PANIC_RADIUS := 45.0
const DESPAWN_AFTER_DEATH := 25.0

const JACKETS: Array[Color] = [
	Color(0.25, 0.28, 0.35), Color(0.4, 0.26, 0.24), Color(0.2, 0.34, 0.28),
	Color(0.5, 0.46, 0.4), Color(0.16, 0.16, 0.2), Color(0.55, 0.35, 0.2),
	Color(0.3, 0.4, 0.55), Color(0.6, 0.55, 0.35),
]
const SKINS: Array[Color] = [
	Color(0.87, 0.72, 0.6), Color(0.75, 0.57, 0.45),
	Color(0.55, 0.4, 0.3), Color(0.4, 0.28, 0.2),
]

var health := 100.0
var manager: Node = null  # NPCManager; duck-typed to avoid a cyclic class ref

var _state := STATE_WANDER
var _target := Vector3.ZERO
var _has_target := false
var _flee_from := Vector3.ZERO
var _flee_left := 0.0
var _idle_left := 0.0
var _stuck_left := 0.6


func _ready() -> void:
	add_to_group("npcs")

	var shape := CollisionShape3D.new()
	var capsule := CapsuleShape3D.new()
	capsule.radius = 0.3
	capsule.height = 1.75
	shape.shape = capsule
	shape.position = Vector3(0, 0.875, 0)
	add_child(shape)

	var body := MeshInstance3D.new()
	var body_mesh := CapsuleMesh.new()
	body_mesh.radius = 0.28
	body_mesh.height = 1.35
	body.mesh = body_mesh
	body.position = Vector3(0, 0.75, 0)
	var jacket := StandardMaterial3D.new()
	jacket.albedo_color = JACKETS[randi() % JACKETS.size()]
	body.material_override = jacket
	add_child(body)

	var head := MeshInstance3D.new()
	var head_mesh := SphereMesh.new()
	head_mesh.radius = 0.12
	head_mesh.height = 0.24
	head.mesh = head_mesh
	head.position = Vector3(0, 1.55, 0)
	var skin := StandardMaterial3D.new()
	skin.albedo_color = SKINS[randi() % SKINS.size()]
	head.material_override = skin
	add_child(head)

	_idle_left = randf_range(0.0, 2.0)


func _physics_process(delta: float) -> void:
	if _state == STATE_DEAD:
		return

	if not is_on_floor():
		velocity += get_gravity() * delta

	match _state:
		STATE_WANDER:
			_wander(delta)
		STATE_FLEE:
			_flee_tick(delta)

	move_and_slide()

	# Unstick: if we're trying to move but going nowhere, pick a new target.
	if _state != STATE_DEAD and _has_target:
		var horizontal := Vector2(velocity.x, velocity.z).length()
		if horizontal < 0.2:
			_stuck_left -= delta
			if _stuck_left <= 0.0:
				_has_target = false
				_stuck_left = 0.6
		else:
			_stuck_left = 0.6


func _wander(delta: float) -> void:
	if not _has_target:
		if _idle_left > 0.0:
			_idle_left -= delta
			velocity.x = 0.0
			velocity.z = 0.0
			return
		_pick_target()
		return
	_move_towards(_target, WALK_SPEED)
	if Vector2(_target.x - global_position.x, _target.z - global_position.z).length() < 1.5:
		_has_target = false
		_idle_left = randf_range(0.5, 4.0)


func _flee_tick(delta: float) -> void:
	_flee_left -= delta
	if _flee_left <= 0.0:
		_state = STATE_WANDER
		_has_target = false
		return
	var away := global_position - _flee_from
	away.y = 0.0
	if away.length_squared() < 0.01:
		away = Vector3(randf() - 0.5, 0.0, randf() - 0.5)
	var goal := global_position + away.normalized() * 10.0
	_move_towards(goal, FLEE_SPEED)


func _move_towards(goal: Vector3, speed: float) -> void:
	var dir := goal - global_position
	dir.y = 0.0
	if dir.length_squared() < 0.01:
		return
	dir = dir.normalized()
	velocity.x = dir.x * speed
	velocity.z = dir.z * speed
	# Face the way we're going.
	rotation.y = atan2(-dir.x, -dir.z)


func _pick_target() -> void:
	if manager != null and manager.has_method("wander_target_near"):
		var t: Vector3 = manager.call("wander_target_near", global_position)
		if t != Vector3.ZERO:
			_target = t
			_has_target = true
			return
	# Fallback: short random leg.
	var ang := randf() * TAU
	_target = global_position + Vector3(cos(ang), 0.0, sin(ang)) * randf_range(8.0, 20.0)
	_has_target = true


## Group broadcast from the weapon system.
func on_gunshot(at: Vector3) -> void:
	if _state == STATE_DEAD:
		return
	if global_position.distance_to(at) <= GUNSHOT_PANIC_RADIUS:
		_panic(at)


func take_damage(amount: float, from_pos: Vector3) -> void:
	if _state == STATE_DEAD:
		return
	health -= amount
	if health <= 0.0:
		_die()
	else:
		_panic(from_pos)


func _panic(from_pos: Vector3) -> void:
	_state = STATE_FLEE
	_flee_from = from_pos
	_flee_left = FLEE_TIME * randf_range(0.8, 1.2)


func _die() -> void:
	_state = STATE_DEAD
	velocity = Vector3.ZERO
	# Stop blocking bullets/movement, tip over, fade out later.
	for child in get_children():
		var col := child as CollisionShape3D
		if col != null:
			col.set_deferred("disabled", true)
	var tw := create_tween()
	tw.tween_property(self, "rotation:z", PI / 2.0, 0.35).set_ease(Tween.EASE_IN)
	var timer := get_tree().create_timer(DESPAWN_AFTER_DEATH)
	timer.timeout.connect(queue_free)
