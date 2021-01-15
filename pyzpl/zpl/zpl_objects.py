OBJECT_DICTIONARY = {
    "Sphere": "NSC_SPHE",
    "Source Rectangle": "NSC_SRCR",
    "Source Gaussian": "NSC_SGAU",
    "Detector Rectangle": "NSC_DETE",
    "CAD Part: STEP/IGES/SAT": "NSC_IMPT",
    "Cylinder Volume": "NSC_CBLK",
}


def object_types(arg):
    values = [v for v in OBJECT_DICTIONARY.values()]

    if arg in values:
        return arg

    retval = OBJECT_DICTIONARY.get(arg, None)
    if retval is None:
        raise ValueError("Could not find %s in object types", arg)
    return retval
