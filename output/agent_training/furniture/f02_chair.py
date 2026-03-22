"""F2: Chair — 45x50x85cm, seat height 45cm, oak, LOG 300 (7 objects)"""
import rhinoscriptsyntax as rs

def box(x, y, z, L, W, H):
    pts = [(x,y,z),(x+L,y,z),(x+L,y+W,z),(x,y+W,z),
           (x,y,z+H),(x+L,y,z+H),(x+L,y+W,z+H),(x,y+W,z+H)]
    return rs.AddBox(pts)

def build_chair(ox, oy, layer, chair_W=45, chair_D=50, chair_H=85,
                seat_h=45, seat_thick=2, leg_sec=3.5,
                rail_w=3, rail_d=2):
    """Build a chair at (ox, oy, 0) on the given layer."""
    rs.AddLayer(layer)
    seat_z = seat_h - seat_thick

    # Seat
    seat = box(ox, oy, seat_z, chair_W, chair_D, seat_thick)
    rs.ObjectLayer(seat, layer)
    rs.ObjectName(seat, "Chair_Seat")
    rs.SetUserText(seat, "material", "oak")

    # Front legs (to seat height)
    fl = box(ox, oy, 0, leg_sec, leg_sec, seat_z)
    rs.ObjectLayer(fl, layer)
    rs.ObjectName(fl, "Chair_Leg_01")
    rs.SetUserText(fl, "material", "oak")

    fr = box(ox + chair_W - leg_sec, oy, 0, leg_sec, leg_sec, seat_z)
    rs.ObjectLayer(fr, layer)
    rs.ObjectName(fr, "Chair_Leg_02")
    rs.SetUserText(fr, "material", "oak")

    # Back legs (to full chair height)
    bl = box(ox, oy + chair_D - leg_sec, 0, leg_sec, leg_sec, chair_H)
    rs.ObjectLayer(bl, layer)
    rs.ObjectName(bl, "Chair_Leg_03")
    rs.SetUserText(bl, "material", "oak")

    br = box(ox + chair_W - leg_sec, oy + chair_D - leg_sec, 0, leg_sec, leg_sec, chair_H)
    rs.ObjectLayer(br, layer)
    rs.ObjectName(br, "Chair_Leg_04")
    rs.SetUserText(br, "material", "oak")

    # Back rails connecting back legs
    rail_x = ox + leg_sec
    rail_len = chair_W - 2 * leg_sec
    rail_y = oy + chair_D - leg_sec

    # Top rail at z=82 (top at 82, so bottom at 79)
    rt = box(rail_x, rail_y, 82 - rail_w, rail_len, rail_d, rail_w)
    rs.ObjectLayer(rt, layer)
    rs.ObjectName(rt, "Chair_Rail_Top")
    rs.SetUserText(rt, "material", "oak")

    # Mid rail at z=60
    rm = box(rail_x, rail_y, 60 - rail_w, rail_len, rail_d, rail_w)
    rs.ObjectLayer(rm, layer)
    rs.ObjectName(rm, "Chair_Rail_Mid")
    rs.SetUserText(rm, "material", "oak")

    print("Chair built: 7 objects on {}".format(layer))

# --- Execute ---
if __name__ == "__main__" or True:
    build_chair(600, 550, "Training::Furniture::F2_Chair")
