import arcade

def load_map_and_path(map_path: str, tile_scaling: float):
    tile_map = arcade.load_tilemap(map_path, scaling=tile_scaling)
    scene = arcade.Scene()

    # Add all tile layers to the scene
    for layer_name, sprite_list in tile_map.sprite_lists.items():
        scene.add_sprite_list(name=layer_name, sprite_list=sprite_list)
        print(f"[DEBUG] Added tile layer to scene: {layer_name}")

    spawn_point = (0, 0)
    enemy_path = []

    path_layer = tile_map.object_lists.get("Path", [])
    print(f"[DEBUG] Path layer contains {len(path_layer)} objects.")

    for obj in path_layer:
        print(f"[DEBUG] Object raw data: name='{obj.name}', type='{obj.type}', shape={getattr(obj, 'shape', None)}, x={getattr(obj, 'x', None)}, y={getattr(obj, 'y', None)}")

        if obj.name and obj.name.strip().lower() == "starting point":
            shape = getattr(obj, "shape", None)
            if isinstance(shape, list) and len(shape) == 4:
                # Calculate center of rectangle
                xs = [point[0] for point in shape]
                ys = [point[1] for point in shape]
                center_x = sum(xs) / 4
                center_y = sum(ys) / 4
                spawn_point = (center_x, center_y)
                print(f"[DEBUG] Rectangle 'starting point' center: {spawn_point}")
            else:
                print(f"[WARNING] Unrecognized shape for 'starting point': {shape}")

        elif obj.name and obj.name.strip().lower() == "path":
            shape = getattr(obj, "shape", None)
            if isinstance(shape, list) and shape:
                enemy_path = shape
                print(f"[DEBUG] Path to follow: {enemy_path}")
            else:
                print("[WARNING] Path object has no valid shape")

    return tile_map, scene, spawn_point, enemy_path
