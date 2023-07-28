
from math import floor, sqrt
from xml.dom import getDOMImplementation
from typing import Tuple, Union

import xml.dom


NS_URI = 'http://www.w3.org/2000/svg'


def set_attributes(element, attributes: dict, **kwargs):
    for key, value in attributes.items():
        if not isinstance(value, str):
            value = str(value)
        element.setAttribute(key, value)


def feet_inches_to_meters(feet: int, inches: int = 0):
    total_inches = feet * 12 + inches
    return total_inches / 39.37


def meters_to_feet_inches(meters: float) -> Tuple[int, int]:
    total_inches = meters * 39.37
    feet = total_inches // 12
    inches = round(total_inches % 12)
    return int(feet), int(inches)


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
            {
                'version': '1.0',
                'width': width,
                'height': height,
                'xmlns': NS_URI,
            },
        )
        return svg

    def draw_line(self, x1, y1, x2, y2, stroke=None):
        line = self.doc.createElement('line')
        set_attributes(
            line,
            {
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2,
                'stroke': stroke
            },
        )
        self.svg.appendChild(line)

    def draw_rect(self, x, y, width, height, stroke=None, fill='transparent'):
        rect = self.doc.createElement('rect')
        set_attributes(
            rect,
            {
                'x': x,
                'y': y,
                'width': width,
                'height': height,
                'stroke': stroke,
                'fill': fill,
            }
        )
        self.svg.appendChild(rect)


class MetersToUnitsConverter:
    def __init__(self, units_len, meters_len):
        self.units_per_meter = units_len / meters_len

    def __call__(self, *args, **kwargs):
        return args[0] * self.units_per_meter


def main():

    # size the drawing represents
    meters_width = feet_inches_to_meters(125)
    feet_height = feet_inches_to_meters(175)

    # width and height of images in units
    units_width = 400
    units_height = int((units_width * feet_height) / meters_width)
    print(f"{units_width=} {units_height=}")

    units_converter = MetersToUnitsConverter(units_width, meters_width)

    len_ne_side = feet_inches_to_meters(4, 8)  # side with gate by Scott & Melissa
    len_e_side = feet_inches_to_meters(55, 7)
    len_nw_side = feet_inches_to_meters(14)  # side with gate across driveway
    len_w_side = feet_inches_to_meters(114, 7)

    garage_s_wall = feet_inches_to_meters(26, 1)
    garage_w_wall = feet_inches_to_meters(32, 4)

    house_w_wall = feet_inches_to_meters(28, 3)
    house_s_wall = feet_inches_to_meters(30)

    overall_width = len_nw_side + house_s_wall + garage_s_wall + len_ne_side
    print(f"{overall_width = }")

    len_s_side = sqrt(
        overall_width ** 2 + (len_w_side - (len_e_side + garage_w_wall)) ** 2
    )
    print(f"{len_s_side = }")







    svg = Svg(units_width, units_height)

    nw_corner = (
        units_converter(feet_inches_to_meters(10)),
        units_converter(feet_inches_to_meters(10) + house_w_wall)
    )
    sw_corner = (
        nw_corner[0],
        nw_corner[1] + units_converter(len_w_side)
    )
    se_corner = (
        nw_corner[0] + units_converter(overall_width),
        nw_corner[1] + units_converter(garage_w_wall + len_e_side),
    )
    ne_corner = (
        se_corner[0],
        nw_corner[1] + units_converter(garage_w_wall),
    )
    house_sw_corner = (
        nw_corner[0] + units_converter(len_nw_side),
        nw_corner[1]
    )
    house_nw_corner = (
        house_sw_corner[0],
        house_sw_corner[1] - units_converter(house_w_wall)
    )
    house_backdoor_corner = (
        house_sw_corner[0] + units_converter(house_s_wall),
        house_sw_corner[1],
    )
    garage_se_corner = (
        ne_corner[0] - units_converter(len_ne_side),
        ne_corner[1],
    )

    svg.draw_line(*nw_corner, *sw_corner, 'black')
    svg.draw_line(*sw_corner, *se_corner, 'black')
    svg.draw_line(*se_corner, *ne_corner, 'black')
    svg.draw_line(*nw_corner, *house_sw_corner, 'black')
    svg.draw_line(*garage_se_corner, *ne_corner, 'black')

    svg.draw_rect(
        *house_nw_corner,
        units_converter(house_s_wall + garage_s_wall),
        units_converter(house_w_wall),
        'black',
        'black',
    )
    svg.draw_rect(
        *house_backdoor_corner,
        units_converter(garage_s_wall),
        units_converter(garage_w_wall),
        'black',
        'black',
    )

    # print(dir(xml.dom))

    with open('fence1.svg', 'w') as out_file:
        out_file.write(svg.doc.toprettyxml())


if __name__ == '__main__':
    main()


