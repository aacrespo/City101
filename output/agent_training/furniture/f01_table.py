"""F1: Dining Table — 180x90x75cm, oak, LOG 300 (7 objects)"""
import rhinoscriptsyntax as rs

def box(x, y, z, L, W, H):
    pts = [(x,y,z),(x+L,y,z),(x+L,y+W,z),(x,y+W,z),
           (x,y,z+H),(x+L,y,z+H),(x+L,y+W,z+H),(x,y+W,z+H)]
    return rs.AddBox(pts)

def build_table(ox, oy, layer, table_L=180, table_W=90, table_H=75,
                top_thick=3, leg_sec=8, inset=6,
                stretcher_w=4, stretcher_h=6, stretcher_z=20):
    """Build a dining table at (ox, oy, 0) on the given layer."""
    rs.AddLayer(layer)
    leg_h = table_H - top_thick

    # Table top
    top = box(ox, oy, leg_h, table_L, table_W, top_thick)
    rs.ObjectLayer(top, layer)
    rs.ObjectName(top, "Table_Top")
    rs.SetUserText(top, "material", "oak")

    # 4 legs inset from edges
    leg_positions = [
        (ox + inset, oy + inset, "Table_Leg_01"),
        (ox + table_L - inset - leg_sec, oy + inset, "Table_Leg_02"),
        (ox + table_L - inset - leg_sec, oy + table_W - inset - leg_sec, "Table_Leg_03"),
        (ox + inset, oy + table_W - inset - leg_sec, "Table_Leg_04"),
    ]
    for lx, ly, name in leg_positions:
        leg = box(lx, ly, 0, leg_sec, leg_sec, leg_h)
        rs.ObjectLayer(leg, layer)
        rs.ObjectName(leg, name)
        rs.SetUserText(leg, "material", "oak")

    # 2 long stretchers connecting legs along X
    s_x = ox + inset + leg_sec
    s_len = table_L - 2 * inset - 2 * leg_sec
    s1_y = oy + inset + (leg_sec - stretcher_w) / 2.0
    s1 = box(s_x, s1_y, stretcher_z, s_len, stretcher_w, stretcher_h)
    rs.ObjectLayer(s1, layer)
    rs.ObjectName(s1, "Table_Stretcher_01")
    rs.SetUserText(s1, "material", "oak")

    s2_y = oy + table_W - inset - leg_sec + (leg_sec - stretcher_w) / 2.0
    s2 = box(s_x, s2_y, stretcher_z, s_len, stretcher_w, stretcher_h)
    rs.ObjectLayer(s2, layer)
    rs.ObjectName(s2, "Table_Stretcher_02")
    rs.SetUserText(s2, "material", "oak")

    print("Table built: 7 objects on {}".format(layer))

# --- Execute ---
if __name__ == "__main__" or True:
    build_table(600, 400, "Training::Furniture::F1_Table")
