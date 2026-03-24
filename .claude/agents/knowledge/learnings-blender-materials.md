# Blender Materials & Shading Learnings

Techniques discovered while working with flat-shaded materials, color palettes, and Blender material nodes. Updated by agents after each build.

---

## 1. **Flat material creation: use_nodes=False is the reliable pattern**
`mat.use_nodes = False` with `mat.diffuse_color = (r, g, b, 1.0)` gives perfect flat shading every time. No specular, no PBR. Create all materials upfront in one block so they're available by name everywhere. This is the doctrine-compliant approach for all architectural surfaces.

## 2. **Emission materials require node setup**
You cannot get emission with `use_nodes = False`. Create an Emission node + Material Output node manually. Strength=2.0 gives visible glow in EEVEE. Used for character sparks, tether lines, and window glow overlays.

## 3. **Translucent/transparent materials need Principled BSDF with blend_method**
For transparency (building cross-sections, TV screens), set `use_nodes = True`, use Principled BSDF with Alpha input (e.g., 0.85 for slight translucency, 0.15 for near-transparent shells), and set `material.blend_method = 'BLEND'`. Flat `use_nodes = False` materials do not support transparency in EEVEE.

## 4. **TV screen semi-transparency via mixed shaders**
A mix of transparent + emission shader with `blend_method = 'BLEND'` on the TV screen material lets miniature objects behind it remain visible. Good for "scene within scene" compositions.

## 5. **Color darkening for accent variants**
Simple `channel * 0.75` gives a natural darker shade for backpacks, shadows, or secondary elements. Works across all palette colors without needing separate hex definitions.

## 6. **Sun lamp warm color: RGB (1.0, 0.91, 0.78) approximates ~4500K**
Combined with the #F5F0EB world background, the scene reads as warm without being orange. This is the standard lighting color for the kitchen animation style.

## 7. **Fill light with shadow disabled prevents double-shadow artifacts**
Energy 0.8 (vs Sun at 3.0) gives about 25% fill ratio. Keeps the flat look while avoiding completely black shadow areas. Set `light.shadow_soft_size = 0` or disable shadow casting entirely on fill lights.

## 8. **Blue-tinted point light for cold atmosphere**
A POINT light with color (0.7, 0.85, 1.0) and energy=50 creates a convincing cold/frost effect (used in basement freezer). Localized color temperature shifts via point lights are more controllable than changing materials.

## 9. **Window glow via overlay planes beats material keyframing**
Creating emission-material planes slightly in front of dark window surfaces is simpler than animating material properties over time. Combined with hide/show keyframes for instant on/off control.

## 10. **Bezier curve as visible tether line**
A CURVE object with `bevel_depth=0.03` and an emission material (orange glow) creates a visible thin connection line between characters. The bevel depth controls line thickness in world units.

## 11. **Ground plane z-fighting prevention**
Multiple overlapping ground planes at slightly different Z heights (e.g., ground at -0.05, street at -0.04, garden at -0.04) prevents z-fighting. The 0.01 unit separation is invisible but eliminates flickering artifacts.

## 12. **Warm glow via sun energy animation**
Increasing sun energy from 3.0 to 4.5 during emotional moments creates a subtle warmth effect. A simple way to add mood without changing materials or adding lights.
