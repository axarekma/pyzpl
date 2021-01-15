# int version, type, lens_units, source_units, source_multiplier;
# int i_data[50];
# double d_data[50];
import struct
import numpy as np

import matplotlib.pyplot as plt

TYPE = {1: "Detector Rectangle", 2: "Color", 3: "Polar", 4: " Volume objects"}
LENS_UNITS = {0: "mm", 1: "cm", 2: "in", 3: "M"}
SOURCE_UNITS = {0: "Watt", 1: "Lumen", 2: "Joule"}
SOURCE_MULTIPLIER = {}


def i_data_NSC_DETE(i_data):
    return {
        "nx": i_data[0],
        "ny": i_data[1],
        "rays_spatial": i_data[2],
        "rays_angular": i_data[3],
    }


def coherent_irradiance(image_data, tol=1e-5):
    retval = image_data[:, :, 2] ** 2 + image_data[:, :, 3] ** 2
    retval /= np.sum(retval)
    retval *= np.sum(image_data[:, :, 0])
    return retval


def coherent_phase(image_data):
    return np.arctan2(image_data[:, :, 2], image_data[:, :, 3])


def incoherent_irradiance(image_data):
    return image_data[:, :, 0]


def read_ddr(filename):
    input_image = open(filename, "rb")

    header0 = input_image.read(5 * 4)
    header1 = input_image.read(50 * 4)
    dummy = input_image.read(4)
    header2 = input_image.read(50 * 8)
    rtm = input_image.read(1 * 4)

    # print("header0")
    # print(header0)
    # print(struct.unpack("=" + "i" * 5, header0))
    # print("header1")
    # print(header1)
    # print(struct.unpack("=" + "l" * 50, header1))
    # print("header2")
    # print(header2)
    # print(struct.unpack("=" + "d" * 50, header2))

    # print("Ray Trace Method")
    # print(rtm)
    # print(struct.unpack("=" + "i", rtm))

    # current = input_image.tell()
    # input_image.seek(0, 2)
    # eof = input_image.tell()
    # print(f"cu {current} eof {eof} size {eof-current}")
    # print(f"{(eof-current)/8} doubles")
    # print(f"{(eof-current)/(8*5)} pixels ({512*512})")

    # print("first pixel")
    # pixel0 = input_image.read(5 * 8)
    # print(pixel0)
    # print(struct.unpack("=" + "d" * 5, pixel0))

    # return

    iheader = i_data_NSC_DETE(struct.unpack("=" + "i" * 50, header1))
    nx, ny = iheader["nx"], iheader["ny"]
    data_size = 5 * iheader["nx"] * iheader["ny"]
    imtype = "f8"

    image_data = np.fromfile(file=input_image, dtype=imtype, count=data_size).reshape(
        (ny, nx, 5)
    )

    # plt.figure(figsize=(15, 3))
    # for i in range(5):
    #     # print(np.sum(image_data[:, :, i]))
    #     plt.subplot(1, 5, i + 1)
    #     plt.imshow(image_data[:, :, i])
    # plt.show()

    # print(f"Version: {version}")
    # print(f"dtype: {TYPE[dtype]}")
    # print(f"lens_units: {LENS_UNITS[lens_units]}")
    # print(f"source_units: {SOURCE_UNITS[source_units]}")
    # print(f"source_multiplier: {source_multiplier}")

    return image_data


if __name__ == "__main__":

    folder = "c:\\Users\\Axel\\Documents\\Zemax\\Samples\\"
    read_ddr(folder + "_test_macro.DDR")
    read_ddr(folder + "_test_manual.DDR")

    # arr = np.array([11, 12, 13, 14, 15, 21, 22, 23, 24, 25, 31, 32, 33, 34, 35])
    # print(arr)
    # arr_reshape = arr.reshape((3, 5))
    # print(arr_reshape)

