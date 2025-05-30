def extract_polyline_path(tile_map, object_layer_name="Path", object_name="enemy_path"):
    """
    Extracts a polyline path from a Tiled object layer by name.
    Works even when pytiled_parser objects can't be imported directly.
    
    Args:
        tile_map: The loaded tilemap from arcade.load_tilemap().
        object_layer_name (str): The name of the object layer.
        object_name (str): The name of the polyline object.

    Returns:
        List of (x, y) points if found, otherwise an empty list.
    """
    object_layer = tile_map.object_lists.get(object_layer_name, [])
    for obj in object_layer:
        if obj.name == object_name and obj.shape and type(obj.shape).__name__ == "Polyline":
            return obj.shape.points
    return []
