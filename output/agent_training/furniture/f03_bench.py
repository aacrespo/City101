"""F3: Bench — 120x35x45cm, oak, LOG 300 (3 objects)"""
import rhinoscriptsyntax as rs

def box(x, y, z, L, W, H):
    pts = [(x,y,z),(x+L,y,z),(x+L,y+W,z),(x,y+W,z),
           (x,y,z+H),(x+L,y,z+H),(x+L,y+W,z+H),(x,y+W,z+H)]
    return rs.AddBox(pts)

def build_bench(ox, oy, layer, bench_L=120, bench_W=35, bench_H=45,
                seat_thick=4, leg_thick=3, inset=10):
    """Build a bench at (ox, oy, 0) on the given layer."""
    rs.AddLayer(layer)
    leg_h = bench_H - seat_thick

    # Seat plank
    seat = box(ox, oy, leg_h, bench_L, bench_W, seat_thick)
    rs.ObjectLayer(seat, layer)
    rs.ObjectName(seat, "Bench_Seat")
    rs.SetUserText(seat, "material", "oak")

    # 2 slab legs inset from ends
    leg1 = box(ox + inset, oy, 0, leg_thick, bench_W, leg_h)
    rs.ObjectLayer(leg1, layer)
    rs.ObjectName(leg1, "Bench_Leg_01")
    rs.SetUserText(leg1, "material", "oak")

    leg2 = box(ox + bench_L - inset - leg_thick, oy, 0, leg_thick, bench_W, leg_h)
    rs.ObjectLayer(leg2, layer)
    rs.ObjectName(leg2, "Bench_Leg_02")
    rs.SetUserText(leg2, "material", "oak")

    print("Bench built: 3 objects on {}".format(layer))

# --- Execute ---
if __name__ == "__main__" or True:
    build_bench(600, 650, "Training::Furniture::F3_Bench")
