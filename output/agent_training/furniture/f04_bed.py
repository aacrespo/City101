"""F4: Bed — Single 90x200cm, frame 30cm, headboard 90cm, LOG 300+350 (15 objects with slats)"""
import rhinoscriptsyntax as rs

def box(x, y, z, L, W, H):
    pts = [(x,y,z),(x+L,y,z),(x+L,y+W,z),(x,y+W,z),
           (x,y,z+H),(x+L,y,z+H),(x+L,y+W,z+H),(x,y+W,z+H)]
    return rs.AddBox(pts)

def build_bed(ox, oy, layer, mattress_w=90, mattress_l=200, frame_h=30,
              headboard_h=90, rail_t=3, leg_sec=6, mattress_t=20,
              clearance=0.5, slats=True, slat_count=5):
    """Build a bed at (ox, oy, 0) on the given layer."""
    rs.AddLayer(layer)

    frame_w = mattress_w + 2 * clearance
    frame_l = mattress_l + 2 * clearance
    outer_w = frame_w + 2 * rail_t
    outer_l = frame_l + 2 * rail_t
    objs = []

    # 4 corner posts
    for lx, ly, name in [
        (ox, oy, "Bed_Post_01"),
        (ox + outer_l - leg_sec, oy, "Bed_Post_02"),
        (ox + outer_l - leg_sec, oy + outer_w - leg_sec, "Bed_Post_03"),
        (ox, oy + outer_w - leg_sec, "Bed_Post_04")]:
        post = box(lx, ly, 0, leg_sec, leg_sec, frame_h)
        rs.ObjectLayer(post, layer)
        rs.ObjectName(post, name)
        rs.SetUserText(post, "material", "oak")
        objs.append(post)

    # 2 long side rails
    for i, ry in enumerate([oy, oy + outer_w - rail_t]):
        rail = box(ox + leg_sec, ry, 0, outer_l - 2 * leg_sec, rail_t, frame_h)
        rs.ObjectLayer(rail, layer)
        rs.ObjectName(rail, "Bed_SideRail_{:02d}".format(i + 1))
        rs.SetUserText(rail, "material", "oak")
        objs.append(rail)

    # Head rail + foot rail
    for rx, name in [(ox, "Bed_HeadRail"), (ox + outer_l - rail_t, "Bed_FootRail")]:
        rail = box(rx, oy + leg_sec, 0, rail_t, outer_w - 2 * leg_sec, frame_h)
        rs.ObjectLayer(rail, layer)
        rs.ObjectName(rail, name)
        rs.SetUserText(rail, "material", "oak")
        objs.append(rail)

    # Headboard (full outer width, from floor to headboard_h)
    hb = box(ox, oy, 0, rail_t, outer_w, headboard_h)
    rs.ObjectLayer(hb, layer)
    rs.ObjectName(hb, "Bed_Headboard")
    rs.SetUserText(hb, "material", "oak")
    objs.append(hb)

    # Slats (LOG 350): 7cm wide x 1.8cm thick, spanning between long rails
    if slats:
        slat_w = 7.0
        slat_t_h = 1.8
        spacing = (outer_l - 2 * rail_t - slat_count * slat_w) / (slat_count + 1)
        for i in range(slat_count):
            sx = ox + rail_t + spacing + i * (slat_w + spacing)
            slat = box(sx, oy + rail_t, frame_h - slat_t_h, slat_w, frame_w, slat_t_h)
            rs.ObjectLayer(slat, layer)
            rs.ObjectName(slat, "Bed_Slat_{:02d}".format(i + 1))
            rs.SetUserText(slat, "material", "spruce")
            objs.append(slat)

    # Mattress
    matt = box(ox + rail_t + clearance, oy + rail_t + clearance, frame_h,
               mattress_l, mattress_w, mattress_t)
    rs.ObjectLayer(matt, layer)
    rs.ObjectName(matt, "Bed_Mattress")
    rs.SetUserText(matt, "material", "mattress_fabric")
    objs.append(matt)

    return objs
