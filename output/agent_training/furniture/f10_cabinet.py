"""F10: Simple Cabinet — 60x40x80cm, oak, 2 doors, 1 shelf, LOG 300 (9 objects)"""
import rhinoscriptsyntax as rs

def box(x, y, z, L, W, H):
    pts = [(x,y,z),(x+L,y,z),(x+L,y+W,z),(x,y+W,z),
           (x,y,z+H),(x+L,y,z+H),(x+L,y+W,z+H),(x,y+W,z+H)]
    return rs.AddBox(pts)

def build_cabinet(ox, oy, layer, width=60, depth=40, height=80,
                  door_count=2, shelf_count=1, board_t=1.8, back_t=0.6,
                  plinth_h=8, plinth_inset=3):
    """Build a simple cabinet at (ox, oy, 0) on the given layer."""
    rs.AddLayer(layer)

    inner_w = width - 2 * board_t    # 56.4
    inner_h = height - plinth_h - 2 * board_t  # 68.4
    objs = []

    # Plinth
    plinth = box(ox + plinth_inset, oy + plinth_inset, 0,
                 width - 2 * plinth_inset, depth - 2 * plinth_inset, plinth_h)
    rs.ObjectLayer(plinth, layer)
    rs.ObjectName(plinth, "Cabinet_Plinth")
    rs.SetUserText(plinth, "material", "oak")
    objs.append(plinth)

    # Bottom board
    bottom = box(ox, oy, plinth_h, width, depth, board_t)
    rs.ObjectLayer(bottom, layer)
    rs.ObjectName(bottom, "Cabinet_Bottom")
    rs.SetUserText(bottom, "material", "oak")
    objs.append(bottom)

    # 2 side panels
    for i, sx in enumerate([ox, ox + width - board_t]):
        side = box(sx, oy, plinth_h + board_t, board_t, depth, inner_h)
        rs.ObjectLayer(side, layer)
        rs.ObjectName(side, "Cabinet_Side_{:02d}".format(i + 1))
        rs.SetUserText(side, "material", "oak")
        objs.append(side)

    # Top board
    top = box(ox, oy, height - board_t, width, depth, board_t)
    rs.ObjectLayer(top, layer)
    rs.ObjectName(top, "Cabinet_Top")
    rs.SetUserText(top, "material", "oak")
    objs.append(top)

    # Internal shelves
    for i in range(shelf_count):
        sz = plinth_h + board_t + (i + 1) * inner_h / (shelf_count + 1)
        shelf = box(ox + board_t, oy, sz, inner_w, depth, board_t)
        rs.ObjectLayer(shelf, layer)
        rs.ObjectName(shelf, "Cabinet_Shelf_{:02d}".format(i + 1))
        rs.SetUserText(shelf, "material", "oak")
        objs.append(shelf)

    # Back panel
    back = box(ox, oy + depth - back_t, plinth_h, width, back_t, height - plinth_h)
    rs.ObjectLayer(back, layer)
    rs.ObjectName(back, "Cabinet_Back")
    rs.SetUserText(back, "material", "plywood")
    objs.append(back)

    # Doors (28.2cm wide each for 2 doors)
    door_w = inner_w / door_count
    for i in range(door_count):
        dx = ox + board_t + i * door_w
        door = box(dx, oy - 0.1, plinth_h + board_t, door_w, board_t, inner_h)
        rs.ObjectLayer(door, layer)
        rs.ObjectName(door, "Cabinet_Door_{:02d}".format(i + 1))
        rs.SetUserText(door, "material", "oak")
        objs.append(door)

    return objs
