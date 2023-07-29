
from math import atan, sqrt
from math import degrees as radians_to_degrees

from converter import build_converters

# size the drawing represents
feet_width = 125
feet_height = 175

# width and height of images in units
units_width = 400
units_height = int((units_width * feet_height) / feet_width)
print(f"{units_width=} {units_height=}")

ft_in_to_units, units_to_ft_in = build_converters(units_width, feet_width)

len_ne_side = ft_in_to_units(4, 8)  # side with gate by Scott & Melissa
len_e_side = ft_in_to_units(55, 7)
len_nw_side = ft_in_to_units(14)  # side with gate across driveway
len_w_side = ft_in_to_units(114, 7)

garage_s_wall = ft_in_to_units(26, 1)
garage_w_wall = ft_in_to_units(32, 4)

house_w_wall = ft_in_to_units(28, 3)
house_s_wall = ft_in_to_units(30)

overall_width = len_nw_side + house_s_wall + garage_s_wall + len_ne_side
print(f"overall_width={units_to_ft_in(overall_width)}")

len_s_side = sqrt(
    overall_width ** 2 + (len_w_side - (len_e_side + garage_w_wall)) ** 2
)
print(f"len_s_side={units_to_ft_in(len_s_side)}")

nw_corner = (
    ft_in_to_units(20),
    ft_in_to_units(10) + house_w_wall
)
sw_corner = (
    nw_corner[0],
    nw_corner[1] + len_w_side
)
se_corner = (
    nw_corner[0] + overall_width,
    nw_corner[1] + garage_w_wall + len_e_side,
)
ne_corner = (
    se_corner[0],
    nw_corner[1] + garage_w_wall,
)

delta_x = se_corner[0] - sw_corner[0]
delta_y = -1.0 * (se_corner[1] - sw_corner[1])
southern_fence_angle_degrees = round(
    radians_to_degrees(
        atan(delta_y / delta_x)
    ),
    2,
)
print(f"{southern_fence_angle_degrees = }")

house_sw_corner = (
    nw_corner[0] + len_nw_side,
    nw_corner[1]
)
house_nw_corner = (
    house_sw_corner[0],
    house_sw_corner[1] - house_w_wall
)
house_backdoor_corner = (
    house_sw_corner[0] + house_s_wall,
    house_sw_corner[1],
)
garage_se_corner = (
    ne_corner[0] - len_ne_side,
    ne_corner[1],
)
