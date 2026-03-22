"""F7: Bookshelf — 80x30x120cm, oak, 4 shelves (incl top/bottom), LOG 300 (7 objects)"""
import rhinoscriptsyntax as rs

def box(x, y, z, L, W, H):
    pts = [(x,y,z),(x+L,y,z),(x+L,y+W,z),(x,y+W,z),
           (x,y,z+H),(x+L,y,z+H),(x+L,y+W,z+H),(x,y+W,z+H)]
    return rs.AddBox(pts)

def build_bookshelf(ox, oy, layer, width=80, depth=30, height=120,
                    shelf_count=4, board_t=1.8, back_t=0.6, back_panel=True):
    """Build a bookshelf at (ox, oy, 0) on the given layer."""
    rs.AddLayer(layer)

    inner_w = width - 2 * board_t  # 76.4
    objs = []

    # 2 side panels (full height)
    for i, sx in enumerate([ox, ox + width - board_t]):
        side = box(sx, oy, 0, board_t, depth, height)
        rs.ObjectLayer(side, layer)
        rs.ObjectName(side, "Bookshelf_Side_{:02d}".format(i + 1))
        rs.SetUserText(side, "material", "oak")
        objs.append(side)

    # Shelves evenly spaced (including top and bottom)
    for i in range(shelf_count):
        sz = i * (height - board_t) / (shelf_count - 1)
        shelf = box(ox + board_t, oy, sz, inner_w, depth, board_t)
        rs.ObjectLayer(shelf, layer)
        rs.ObjectName(shelf, "Bookshelf_Shelf_{:02d}".format(i + 1))
        rs.SetUserText(shelf, "material", "oak")
        objs.append(shelf)

    # Back panel
    if back_panel:
        back = box(ox, oy + depth - back_t, 0, width, back_t, height)
        rs.ObjectLayer(back, layer)
        rs.ObjectName(back, "Bookshelf_Back")
        rs.SetUserText(back, "material", "plywood")
        objs.append(back)

    return objs
