## Weapon system (PRD 05, vertical-slice version): four weapons, hitscan
## firing with spread/pellets, ammo + reload, recoil, muzzle flash, HUD.
##
## Sits under the player's Head camera so aim = view. Weapon data is inline
## for now; it migrates to .tres resources when the full arsenal lands.
class_name WeaponManager
extends Node3D

const DEFS: Array[Dictionary] = [
	{
		"name": "Fists", "damage": 25.0, "mag": -1, "cooldown": 0.45,
		"auto": false, "range": 1.9, "pellets": 1, "spread": 0.0,
		"reload": 0.0, "sound": "punch", "recoil": 0.0,
		"vm_size": Vector3.ZERO, "vm_color": Color(0, 0, 0),
	},
	{
		"name": "9mm Pistol", "damage": 34.0, "mag": 12, "cooldown": 0.16,
		"auto": false, "range": 300.0, "pellets": 1, "spread": 0.012,
		"reload": 1.4, "sound": "pistol", "recoil": 0.022,
		"vm_size": Vector3(0.05, 0.13, 0.24), "vm_color": Color(0.13, 0.13, 0.15),
	},
	{
		"name": "Pump Shotgun", "damage": 12.0, "mag": 6, "cooldown": 1.0,
		"auto": false, "range": 60.0, "pellets": 8, "spread": 0.045,
		"reload": 2.2, "sound": "shotgun", "recoil": 0.055,
		"vm_size": Vector3(0.055, 0.075, 0.72), "vm_color": Color(0.22, 0.14, 0.09),
	},
	{
		"name": "SMG", "damage": 22.0, "mag": 30, "cooldown": 0.09,
		"auto": true, "range": 200.0, "pellets": 1, "spread": 0.03,
		"reload": 1.8, "sound": "smg", "recoil": 0.014,
		"vm_size": Vector3(0.05, 0.12, 0.42), "vm_color": Color(0.1, 0.1, 0.12),
	},
]

const SOUNDS := {
	"pistol": preload("res://assets/sfx/pistol.wav"),
	"shotgun": preload("res://assets/sfx/shotgun.wav"),
	"smg": preload("res://assets/sfx/smg.wav"),
	"punch": preload("res://assets/sfx/punch.wav"),
	"reload": preload("res://assets/sfx/reload.wav"),
	"dryfire": preload("res://assets/sfx/dryfire.wav"),
	"hit": preload("res://assets/sfx/hit.wav"),
}

var current := 1  # start with the pistol so shooting works immediately

var _mag: Array[int] = []
var _cooldown_left := 0.0
var _reload_left := 0.0

var _cam: Camera3D = null
var _player: Player = null
var _viewmodel: MeshInstance3D = null
var _muzzle_light: OmniLight3D = null
var _audio: AudioStreamPlayer = null
var _audio_hit: AudioStreamPlayer = null
var _ammo_label: Label = null
var _vm_rest := Vector3(0.28, -0.22, -0.5)


func _ready() -> void:
	_cam = get_parent() as Camera3D
	_player = get_parent().get_parent() as Player
	for def in DEFS:
		var mag_size: int = def.get("mag", -1)
		_mag.append(mag_size)

	_viewmodel = MeshInstance3D.new()
	_viewmodel.position = _vm_rest
	add_child(_viewmodel)

	_muzzle_light = OmniLight3D.new()
	_muzzle_light.position = _vm_rest + Vector3(0, 0.05, -0.5)
	_muzzle_light.light_color = Color(1.0, 0.75, 0.4)
	_muzzle_light.light_energy = 0.0
	_muzzle_light.omni_range = 9.0
	add_child(_muzzle_light)

	_audio = AudioStreamPlayer.new()
	add_child(_audio)
	_audio_hit = AudioStreamPlayer.new()
	_audio_hit.volume_db = -6.0
	add_child(_audio_hit)

	_build_hud()
	_apply_weapon()


func _build_hud() -> void:
	var hud := CanvasLayer.new()
	hud.name = "WeaponHUD"
	add_child(hud)

	var crosshair := Label.new()
	crosshair.text = "+"
	crosshair.set_anchors_preset(Control.PRESET_CENTER)
	crosshair.add_theme_color_override("font_color", Color(1, 1, 1, 0.9))
	hud.add_child(crosshair)

	_ammo_label = Label.new()
	_ammo_label.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	_ammo_label.offset_left = -320.0
	_ammo_label.offset_top = -48.0
	_ammo_label.offset_right = -16.0
	_ammo_label.offset_bottom = -16.0
	_ammo_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_ammo_label.add_theme_color_override("font_color", Color(1, 1, 1, 0.85))
	_ammo_label.add_theme_color_override("font_outline_color", Color(0, 0, 0, 0.8))
	_ammo_label.add_theme_constant_override("outline_size", 4)
	hud.add_child(_ammo_label)


func _def() -> Dictionary:
	return DEFS[current]


func _apply_weapon() -> void:
	var size: Vector3 = _def().get("vm_size", Vector3.ZERO)
	if size == Vector3.ZERO:
		_viewmodel.visible = false
	else:
		_viewmodel.visible = true
		var box := BoxMesh.new()
		box.size = size
		_viewmodel.mesh = box
		var mat := StandardMaterial3D.new()
		mat.albedo_color = _def().get("vm_color", Color.BLACK)
		_viewmodel.material_override = mat
	_reload_left = 0.0


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("slot_1"):
		_switch(0)
	elif event.is_action_pressed("slot_2"):
		_switch(1)
	elif event.is_action_pressed("slot_3"):
		_switch(2)
	elif event.is_action_pressed("slot_4"):
		_switch(3)
	elif event.is_action_pressed("weapon_next"):
		_switch((current + 1) % DEFS.size())
	elif event.is_action_pressed("weapon_prev"):
		_switch((current - 1 + DEFS.size()) % DEFS.size())
	elif event.is_action_pressed("reload"):
		_start_reload()


func _switch(index: int) -> void:
	if index == current:
		return
	current = index
	_apply_weapon()


func _process(delta: float) -> void:
	_cooldown_left = maxf(0.0, _cooldown_left - delta)
	if _reload_left > 0.0:
		_reload_left = maxf(0.0, _reload_left - delta)
		if _reload_left == 0.0:
			var mag_size: int = _def().get("mag", -1)
			_mag[current] = mag_size

	# Viewmodel recovers from recoil kick.
	_viewmodel.position = _viewmodel.position.lerp(_vm_rest, 1.0 - exp(-14.0 * delta))

	_update_hud()

	if Input.mouse_mode != Input.MOUSE_MODE_CAPTURED:
		return
	var auto: bool = _def().get("auto", false)
	if auto and Input.is_action_pressed("fire"):
		_try_fire()
	elif not auto and Input.is_action_just_pressed("fire"):
		_try_fire()


func _update_hud() -> void:
	if _ammo_label == null:
		return
	var def := _def()
	var mag_size: int = def.get("mag", -1)
	var text: String = str(def.get("name", "?"))
	if mag_size > 0:
		if _reload_left > 0.0:
			text += "   reloading..."
		else:
			text += "   %d / %d" % [_mag[current], mag_size]
	_ammo_label.text = text


func _start_reload() -> void:
	var def := _def()
	var mag_size: int = def.get("mag", -1)
	var reload_time: float = def.get("reload", 0.0)
	if mag_size <= 0 or _mag[current] == mag_size or _reload_left > 0.0:
		return
	_reload_left = reload_time
	_audio.stream = SOUNDS["reload"]
	_audio.play()


func _try_fire() -> void:
	if _cooldown_left > 0.0 or _reload_left > 0.0 or _cam == null:
		return
	var def := _def()
	var mag_size: int = def.get("mag", -1)
	if mag_size > 0 and _mag[current] <= 0:
		_audio.stream = SOUNDS["dryfire"]
		_audio.play()
		_cooldown_left = 0.3
		return

	_cooldown_left = def.get("cooldown", 0.3)
	if mag_size > 0:
		_mag[current] -= 1

	_audio.stream = SOUNDS[str(def.get("sound", "punch"))]
	_audio.play()

	var pellets: int = def.get("pellets", 1)
	var hit_something := false
	for _p in range(pellets):
		if _fire_ray(def):
			hit_something = true
	if hit_something:
		_audio_hit.stream = SOUNDS["hit"]
		_audio_hit.play()

	# Feedback: recoil + muzzle flash + viewmodel kick.
	var recoil: float = def.get("recoil", 0.0)
	if _player != null and recoil > 0.0:
		_player.add_recoil(recoil * randf_range(0.8, 1.2))
	if recoil > 0.0:
		_muzzle_light.light_energy = 3.0
		var tw := create_tween()
		tw.tween_property(_muzzle_light, "light_energy", 0.0, 0.07)
	_viewmodel.position = _vm_rest + Vector3(0, 0.015, 0.06)

	# NPCs react to the bang, not the bullet.
	get_tree().call_group("npcs", "on_gunshot", _cam.global_position)


func _fire_ray(def: Dictionary) -> bool:
	var spread: float = def.get("spread", 0.0)
	var max_range: float = def.get("range", 100.0)
	var damage: float = def.get("damage", 10.0)

	var origin := _cam.global_position
	var dir := -_cam.global_basis.z
	if spread > 0.0:
		dir = dir.rotated(_cam.global_basis.x, randf_range(-spread, spread))
		dir = dir.rotated(_cam.global_basis.y, randf_range(-spread, spread))

	var query := PhysicsRayQueryParameters3D.create(origin, origin + dir * max_range)
	if _player != null:
		query.exclude = [_player.get_rid()]
	var hit := get_world_3d().direct_space_state.intersect_ray(query)
	if hit.is_empty():
		return false

	var collider: Object = hit.get("collider")
	var hit_pos: Vector3 = hit.get("position", Vector3.ZERO)
	_spawn_impact(hit_pos)
	if collider != null and collider.has_method("take_damage"):
		collider.call("take_damage", damage, origin)
		return true
	return false


## Brief glowing spark at the impact point.
func _spawn_impact(at: Vector3) -> void:
	var spark := MeshInstance3D.new()
	var sphere := SphereMesh.new()
	sphere.radius = 0.03
	sphere.height = 0.06
	spark.mesh = sphere
	var mat := StandardMaterial3D.new()
	mat.emission_enabled = true
	mat.emission = Color(1.0, 0.7, 0.3)
	mat.emission_energy_multiplier = 4.0
	mat.albedo_color = Color(0.3, 0.2, 0.1)
	spark.material_override = mat
	get_tree().current_scene.add_child(spark)
	spark.global_position = at
	var tw := spark.create_tween()
	tw.tween_property(spark, "scale", Vector3.ONE * 0.05, 0.18)
	tw.tween_callback(spark.queue_free)
