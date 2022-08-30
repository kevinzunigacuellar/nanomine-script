from pprint import pprint
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import re
import requests
import doxapy

NANOMINE_URL = "https://qa.materialsmine.org/api/graphql"

query = """query Query($input: imageExplorerInput!) {
  searchImages(input: $input) {
    images {
      file
      metaData {
        keywords
      }
    }
    totalItems
  }
}
"""

variables = {
    "input": {
        "search": "keyword",
        "searchValue": "nanocomposites"
    }
}


def lineal_path(bin_image):

    image = bin_img.transpose()  # rotate image
    # L = len(image)
    corr1 = np.zeros((len(image), 1))
    # print(corr1)
    corr2 = np.zeros((len(image), 1))
    # something = np.arange(, 1+- 1, - 1)
#     FC = FC * L
#     for ii in np.arange(1, L+1, 1).reshape(-1):
#         clm1 = image(:, ii)
#         clm2 = image(ii, :)
#         clm1 = bwlabel(clm1)
#         clm2 = bwlabel(clm2)
#         maxnum1 = np.amax(clm1)
#         maxnum2 = np.amax(clm2)
#         if maxnum1 > 0:
#             for jj in np.arange(1, maxnum1+1, 1).reshape(-1):
#                 cnt1 = sum(clm1 == jj)
#                 for kk in np.arange(1, cnt1+1, 1).reshape(-1):
#                     lcorr1[kk] = lcorr1(kk) + cnt1 - kk + 1
#         if maxnum2 > 0:
#             for jj in np.arange(1, maxnum2+1, 1).reshape(-1):
#                 cnt2 = sum(clm2 == jj)
#                 for kk in np.arange(1, cnt2+1, 1).reshape(-1):
#                     lcorr2[kk] = lcorr2(kk) + cnt2 - kk + 1

#     lcorr = (lcorr1 + lcorr2) / 2.0 / FC
#     return lcorr


def read_image(file):
    # checks if file is a url
    if is_url(file):
        img = requests.get(file, stream=True).raw
    else:
        img = file
    # open and converts image to numpy array
    return np.array(Image.open(img).convert('L'))


def request_image():
    res = requests.post(
        NANOMINE_URL, json={"query": query, "variables": variables})
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            res.status_code, query))


def is_url(name):
    url_pattern = re.compile(r"^https?://")
    return url_pattern.match(name) is not None


def binarize_image(img, binarization_type="sauvola", window_size=75, k=0.2):

    grayscale_image = read_image(img)
    binary_image = np.empty(grayscale_image.shape, grayscale_image.dtype)

    if binarization_type == "sauvola":
        print("Binarizing image with Sauvola binarization")
        sauvola = doxapy.Binarization(doxapy.Binarization.Algorithms.SAUVOLA)
        sauvola.initialize(grayscale_image)
        sauvola.to_binary(binary_image, {"window": window_size, "k": k})
        return binary_image

    elif binarization_type == "otsu":
        print("Binarizing image with Otsu binarization")
        otsu = doxapy.Binarization(doxapy.Binarization.Algorithms.OTSU)
        otsu.initialize(grayscale_image)
        otsu.to_binary(binary_image)
        return binary_image

    elif binarization_type == "niblack":
        print("Binarizing image with Niblack binarization")
        niblack = doxapy.Binarization(doxapy.Binarization.Algorithms.NIBLACK)
        niblack.initialize(grayscale_image)
        niblack.to_binary(
            binary_image, {"window": window_size, "k": k})  # k=0.01
        return binary_image

    elif binarization_type == "wolf":
        print("Binarizing image with Wolf binarization")
        wolf = doxapy.Binarization(doxapy.Binarization.Algorithms.WOLF)
        wolf.initialize(grayscale_image)
        wolf.to_binary(binary_image, {"window": window_size, "k": k})
        return binary_image

    elif binarization_type == "wan":
        print("Binarizing image with Wan binarization")
        wan = doxapy.Binarization(doxapy.Binarization.Algorithms.WAN)
        wan.initialize(grayscale_image)
        wan.to_binary(binary_image, {"window": window_size, "k": k})
        return binary_image
    else:
        raise Exception("Binarization type not recognized")


if __name__ == "__main__":
    img = "sample.png"
    # todo handle error if fails
    img_url = 'https://qa.materialsmine.org/api/files/59667d92e74a1d62877b8fb5'
    bin_img = binarize_image(img)
    # print(len(bin_img[0]))
    # lineal_path(bin_img)
    # step = 0.1
    # ex = np.arange(0, 5+step, step)
    # ex1 = np.linspace(0, 5, num=6)
    # pprint(ex1)
    Image.fromarray(bin_img).show()
