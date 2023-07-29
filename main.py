
from math import atan, cos, floor, sin
from math import degrees as radians_to_degrees
from math import radians as degrees_to_radians
from xml.dom import getDOMImplementation

from measurements import \
    ft_in_to_units, \
    garage_s_wall, \
    garage_w_wall, \
    garage_se_corner, \
    house_backdoor_corner, \
    house_nw_corner, \
    house_w_wall, \
    house_s_wall, \
    house_sw_corner, \
    ne_corner, \
    nw_corner, \
    se_corner, \
    southern_fence_angle_degrees, \
    sw_corner, \
    units_height, \
    units_width


NS_URI = 'http://www.w3.org/2000/svg'

DEFAULT_ATTRIBUTES = {
    'stroke': 'black',
    'stroke-width': 2,
    'fill': 'transparent',
}


dashed_stroke = {
    'stroke-dasharray': '5,5',
}


def set_attributes(element, **kwargs):
    all_attributes = DEFAULT_ATTRIBUTES.copy()
    all_attributes.update(kwargs)

    for key, value in all_attributes.items():
        if not isinstance(value, str):
            value = str(value)
        element.setAttribute(key, value)


class Svg:

    def __init__(self, width, height):
        self.doc = self.create_document()
        self.svg = self.create_svg(self.doc, width, height)

    @staticmethod
    def create_document():
        dom = getDOMImplementation()
        doc_type = dom.createDocumentType('svg', 'publicId', 'systemId')
        return dom.createDocument(NS_URI, 'svg', doc_type)

    @staticmethod
    def create_svg(doc, width, height):
        svg = doc.documentElement
        set_attributes(
            svg,
            version='1.0',
            width=width,
            height=height,
            xmlns=NS_URI,
        )
        return svg

    def draw_line(self, x1, y1, x2, y2, **kwargs):
        line = self.doc.createElement('line')
        set_attributes(
            line,
            x1=x1, y1=y1,
            x2=x2, y2=y2,
            **kwargs,
        )
        self.svg.appendChild(line)

    def draw_line_point_direction_distance(self, x1, y1, degrees, distance, **kwargs):
        radians = degrees_to_radians(degrees)
        delta_x = cos(radians) * distance
        delta_y = -1.0 * sin(radians) * distance
        self.draw_line(x1, y1, x1 + delta_x, y1 + delta_y, **kwargs)

    def draw_rect(self, x, y, width, height, **kwargs):
        rect = self.doc.createElement('rect')
        set_attributes(
            rect,
            x=x,
            y=y,
            width=width,
            height=height,
            **kwargs,
        )
        self.svg.appendChild(rect)


def draw_extant_fence_line(svg: Svg, **kwargs):
    svg.draw_line(*nw_corner, *sw_corner, **kwargs)
    svg.draw_line(*sw_corner, *se_corner, **kwargs)
    svg.draw_line(*se_corner, *ne_corner, **kwargs)
    svg.draw_line(*nw_corner, *house_sw_corner, **kwargs)
    svg.draw_line(*garage_se_corner, *ne_corner, **kwargs)


def draw_neighbors_fences(svg: Svg, **kwargs):
    kwargs.update(dashed_stroke)
    corners_and_angles = {
        nw_corner: [180],
        ne_corner: [90],
        se_corner: [southern_fence_angle_degrees, 270],
        sw_corner: [southern_fence_angle_degrees + 180, 270],
    }
    twelve_ft_in_units = ft_in_to_units(12)
    for corner, angles in corners_and_angles.items():
        for angle in angles:
            svg.draw_line_point_direction_distance(
                *corner,
                angle,
                twelve_ft_in_units,
                **kwargs,
            )


def draw_house(svg):
    svg.draw_rect(
        *house_nw_corner,
        house_s_wall + garage_s_wall,
        house_w_wall,
        fill='black'
    )
    svg.draw_rect(
        *house_backdoor_corner,
        garage_s_wall,
        garage_w_wall,
        fill='black',
    )


def replace_existing():
    svg = Svg(units_width, units_height)

    draw_extant_fence_line(svg)
    draw_neighbors_fences(svg)
    draw_house(svg)

    with open('replace_existing.svg', 'w') as out_file:
        out_file.write(svg.doc.toprettyxml())


def build_inside():
    svg = Svg(units_width, units_height)

    draw_extant_fence_line(svg, **dashed_stroke)
    draw_neighbors_fences(svg)
    draw_house(svg)

    offset = ft_in_to_units(2)
    inner_nw_corner = (
        nw_corner[0] + offset,
        nw_corner[1],
    )
    inner_sw_corner = (
        sw_corner[0] + offset,
        sw_corner[1] - offset
    )
    inner_se_corner = (
        se_corner[0] - offset,
        se_corner[1] - offset,
    )
    inner_ne_corner = (
        ne_corner[0] - offset,
        ne_corner[1]
    )

    svg.draw_line(*inner_nw_corner, *house_sw_corner)
    svg.draw_line(*inner_nw_corner, *inner_sw_corner)
    svg.draw_line(*inner_sw_corner, *inner_se_corner)
    svg.draw_line(*inner_se_corner, *inner_ne_corner)
    svg.draw_line(*inner_ne_corner, *garage_se_corner)

    with open("build_inside.svg", 'w') as out_file:
        out_file.write(svg.doc.toprettyxml())


def main():
    replace_existing()
    build_inside()


if __name__ == '__main__':
    main()
