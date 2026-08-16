## Free-fly debug camera for grey-box review (M0/M1).
## RMB (hold): capture mouse and look. WASD move, E/Q up/down, Shift fast.
extends Camera3D

@export var speed := 30.0
@export var fast_multiplier := 6.0
@export var mouse_sensitivity := 0.002

var _yaw := 0.0
var _pitch := 0.0


func _ready() -> void:
	_yaw = rotation.y
	_pitch = rotation.x


func _unhandled_input(event: InputEvent) -> void:
	# `as` casts, not `is` checks: GDScript does not narrow types after `is`,
	# so member access on the InputEvent-typed param is a compile error.
	var mb := event as InputEventMouseButton
	if mb != null and mb.button_index == MOUSE_BUTTON_RIGHT:
		Input.mouse_mode = (
			Input.MOUSE_MODE_CAPTURED if mb.pressed else Input.MOUSE_MODE_VISIBLE
		)
		return
	var mm := event as InputEventMouseMotion
	if mm != null and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		_yaw -= mm.relative.x * mouse_sensitivity
		_pitch = clampf(_pitch - mm.relative.y * mouse_sensitivity, -PI / 2, PI / 2)
		rotation = Vector3(_pitch, _yaw, 0.0)


func _process(delta: float) -> void:
	var dir := Vector3.ZERO
	dir += Vector3.FORWARD * Input.get_action_strength("fly_forward")
	dir += Vector3.BACK * Input.get_action_strength("fly_back")
	dir += Vector3.LEFT * Input.get_action_strength("fly_left")
	dir += Vector3.RIGHT * Input.get_action_strength("fly_right")
	var v := speed * (fast_multiplier if Input.is_action_pressed("fly_fast") else 1.0)
	# Horizontal movement follows the camera; vertical is world-space.
	var motion := (global_basis * dir) * v * delta
	motion.y += (Input.get_action_strength("fly_up") - Input.get_action_strength("fly_down")) * v * delta
	global_position += motion
