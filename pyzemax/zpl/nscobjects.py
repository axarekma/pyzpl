"""NSC object wrapper
parameters :
https://osphotonics.wordpress.com/2015/05/07/zemax-programming-language-3-10-non-sequential-components/

"""

from .zpl_objects import object_types


def set_position(surf, obj, code, val):
    if isinstance(val, float):
        return f"SETNSCPOSITION {surf}, {obj}, {code}, {val:.4g}"
    return f"SETNSCPOSITION {surf}, {obj}, {code}, {val}"


def set_property(surf, obj, code, face, val):
    if isinstance(val, float):
        return f"SETNSCPROPERTY {surf}, {obj}, {code}, {face}, {val:.4g}"
    return f"SETNSCPROPERTY {surf}, {obj}, {code}, {face}, {val}"


def set_parameter(surf, obj, par, val):
    if isinstance(val, float):
        return f"SETNSCPARAMETER {surf}, {obj}, {par}, {val:.4g}"
    return f"SETNSCPARAMETER {surf}, {obj}, {par}, {val}"


class NSCObject:
    def __init__(self, objtype, position, parameters=[], properties=[]):
        self.objtype = object_types(objtype)
        self.position = position
        self.parameters = parameters
        self.properties = properties

    def __str__(self):
        return "\n".join(self.lines("obj"))

    def lines(self, ind):
        lines = []
        lines.append(set_property(1, ind, 0, 0, f'"{self.objtype}"'))
        for i, p in enumerate(self.position):
            lines.append(set_position(1, ind, i + 1, p))

        for p in self.parameters:
            lines.append(set_parameter(1, ind, p[0], p[1]))

        for p in self.properties:
            lines.append(set_property(1, ind, p[0], 0, p[1]))

        return lines


class NSCDetector(NSCObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NSCSource(NSCObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


"""
TODO parameters in common for sources
1: # Layout Rays: Defines how many random rays to launch from the source when creating layout plots.
2: # Analysis Rays: Defines how many random rays to launch from the source when performing analysis.
3: Power (units): Power is the total power over the defined range of the source. The power units are specified by the system source units. See “Source Units” for details.
4: Wavenumber: The wavenumber to use when tracing random rays. Zero means polychromatic; which chooses ray wavelengths randomly with the weighting defined on the wavelength data editor.
5: Color #: The pen color to use when drawing rays from this source. If zero, the default color will be chosen. The other parameters have source type specific meanings as described in the follow sections.
"""

