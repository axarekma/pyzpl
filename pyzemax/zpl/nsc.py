from .nscobjects import set_position, set_parameter, set_property
import subprocess
import sys
from pathlib import Path
import os


def clear_macro_lines():
    return [
        "! this part is used to clear the NSC editor",
        "totalobjNum = NOBJ(1)",
        "for i, totalobjNum, 1, -1",
        "    DELETEOBJECT 1, i",
        "next",
    ]


def insert_object():
    return ["INSERTOBJECT 1,1"]


class NSC:
    def __init__(self, polarization=1,executable = "c:\\Program Files\\Zemax OpticStudio\\OpticStudio.exe"):
        self.executable = None
        if os.path.exists(executable):
            self.executable = executable
        else:
            print(f'OpticStudio.exe not found at {executable}')
            print('Please specify executable path in constructor NSC(executable="path to OpticStudio.exe")')

        self.lines = ["! NCXT NSC Generator Macro", "! Axel EKman", ""]
        self.objects = []

        self.reset = True
        self.split = 1
        self.scatter = 1
        self.usepolar = 1

    def run(self, fname=None, wait=True):
        if fname is None:
            py_path = Path(Path(os.getcwd()))
            fname = py_path / "__temp.zpl"
            print(f'Saving at ', fname)

        self.save(fname)
        os_arg = [self.executable, f"-zpl={fname}"]
        # print(os_arg)
        process = subprocess.Popen(os_arg)
        if wait:
            if process.wait() != 0:
                print("There was an error")
            print("Process finished")

        return process

    def __str__(self):
        return "\n".join(self.lines)

    def add(self, obj):
        self.objects.append(obj)

    def nstr(self):
        surf = 1  # non-sequential
        source = 0  # 0 is all
        ignore_errors = 1
        self.lines.append(
            f"NSTR {surf}, {source}, {self.split}, {self.scatter}, {self.usepolar}, {ignore_errors}, 0, 1"
        )
        # self.lines.append(f"NSTR surf, source, split, scatter, usepolar, ignore_errors, random_seed, save, savefilename, filter, zrd_format

    def print(self, msg):
        self.lines.append(f'PRINT "{msg}"')

    def object_index(self, classtype):
        return [i for i, obj in enumerate(self.objects) if isinstance(obj, classtype)]

    def initialize_objects(self):
        self.clear_editor()
        self.lines += ["", "!Insert objects"]
        for obj in self.objects:
            self.lines += insert_object()

        self.lines += ["", "!Set Object parameters"]
        for i, obj in enumerate(self.objects):
            self.lines += obj.lines(i + 1)
            self.lines.append("")

    def clear_editor(self):
        self.lines += clear_macro_lines()

    def clear(self):
        self.lines = ["! NCXT NSC Generator Macro", "! Axel EKman", ""]

    def update(self):
        self.lines.append("UPDATE ALL")

    def set_position(self, index, position):
        old_position = self.objects[index].position
        self.objects[index].position = position

        index_change = [
            i for i, p in enumerate(zip(old_position, position)) if p[0] != p[1]
        ]

        for i in index_change:
            self.lines.append(set_position(1, index + 1, i + 1, position[i]))

    def set_parameter(self, index, parameter, value):
        # TODO check if changed
        self.lines.append(set_parameter(1, index + 1, parameter, value))

    def set_property(self, index, parameter):
        pass
        # TODO

    def clear_detectors(self):
        self.lines.append("temp = NSDD(1,0,0,0)")

    def savedetector(self, index, fname):
        self.lines.append(f'SAVEDETECTOR 1, {index+1}, "{fname}"')

    def save(self, path):
        with open(path, "w") as outfile:
            outlines = [line + "\n" for line in self.lines]
            outfile.writelines(outlines)

