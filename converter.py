
from math import floor

def build_converters(units_length, feet_length):
    units_per_foot = units_length / feet_length

    def ft_in_to_units(feet, inches = 0) -> float:
        feet += inches / 12
        return feet * units_per_foot

    def units_to_ft_in(units):
        total_feet = units / units_per_foot
        feet = floor(total_feet)
        inches = round((total_feet - feet) * 12)
        return int(feet), int(inches)

    return ft_in_to_units, units_to_ft_in
