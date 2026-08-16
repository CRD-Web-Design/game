## First-person player (M1): walk, sprint, jump, mouse look.
## F toggles noclip fly for map review; Esc releases the mouse, click recaptures.
##
## GDScript notes (compile-checked in CI): no `:=` inference from Variant
## expressions, and `as` casts instead of relying on `is` narrowing.
class_name Player
extends CharacterBody3D

const WALK_SPEED := 4.5
const SPRINT_SPEED := 7.5
const JUMP_VELOCITY := 4.8
const FLY_SPEED := 45.0
const FLY_FAST_MULTIPLIER := 4.0
const MOUSE_SENSITIVITY := 0.002
const ACCEL_GROUND := 10.0   # 1/s, exponential approach to target velocity
const ACCEL_AIR := 2.0

var fly_mode := false

var _yaw := 0.0
var _pitch := 0.0

@onready var head: Camera3D = $Head
@onready var body_shape: CollisionShape3D = $Collision
@onready var help_label: Label = $HUD/Help


func _ready() -> void:
	_yaw = rotation.y
	help_label.text = (
		"Click: capture mouse  ·  Esc: release  ·  WASD: move  ·  Shift: sprint\n"
		+ "Space: jump  ·  F: noclip fly (E/Q up/down)"
	)


func _unhandled_input(event: InputEvent) -> void:
	var mb := event as InputEventMouseButton
	if mb != null and mb.pressed and Input.mouse_mode != Input.MOUSE_MODE_CAPTURED:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
		return

	if event.is_action_pressed("ui_cancel"):
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
		return

	if event.is_action_pressed("toggle_fly"):
		fly_mode = not fly_mode
		body_shape.disabled = fly_mode
		velocity = Vector3.ZERO
		return

	var mm := event as InputEventMouseMotion
	if mm != null and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		_yaw -= mm.relative.x * MOUSE_SENSITIVITY
		_pitch = clampf(_pitch - mm.relative.y * MOUSE_SENSITIVITY, -PI / 2, PI / 2)
		rotation = Vector3(0.0, _yaw, 0.0)
		head.rotation = Vector3(_pitch, 0.0, 0.0)


func _physics_process(delta: float) -> void:
	var input2 := Input.get_vector("move_left", "move_right", "move_forward", "move_back")

	if fly_mode:
		_fly(input2, delta)
		return

	if not is_on_floor():
		velocity += get_gravity() * delta
	elif Input.is_action_just_pressed("jump"):
		velocity.y = JUMP_VELOCITY

	var speed := SPRINT_SPEED if Input.is_action_pressed("sprint") else WALK_SPEED
	var wish := (global_basis * Vector3(input2.x, 0.0, input2.y))
	wish.y = 0.0
	wish = wish.normalized() * speed if wish.length_squared() > 0.0 else Vector3.ZERO

	var accel := ACCEL_GROUND if is_on_floor() else ACCEL_AIR
	var horizontal := Vector3(velocity.x, 0.0, velocity.z)
	horizontal = horizontal.lerp(wish, 1.0 - exp(-accel * delta))
	velocity.x = horizontal.x
	velocity.z = horizontal.z

	move_and_slide()


func _fly(input2: Vector2, delta: float) -> void:
	var speed := FLY_SPEED * (FLY_FAST_MULTIPLIER if Input.is_action_pressed("sprint") else 1.0)
	# Full 3D flight along the view direction, plus world-space vertical keys.
	var dir := head.global_basis * Vector3(input2.x, 0.0, input2.y)
	dir.y += Input.get_action_strength("fly_up") - Input.get_action_strength("fly_down")
	velocity = dir.normalized() * speed if dir.length_squared() > 0.0 else Vector3.ZERO
	global_position += velocity * delta
