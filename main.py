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


# def linearpath(image):  # image is a binary image

#     image = rot90(image)
#     L = len(image)
#     lcorr1 = np.zeros((L, 1))
#     lcorr2 = np.zeros((L, 1))
#     FC = np.arange(L, 1+- 1, - 1)
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


def binarize_image(img, binarization_type="sauvola"):

    grayscale_image = read_image(img)
    binary_image = np.empty(grayscale_image.shape, grayscale_image.dtype)

    if binarization_type == "sauvola":
        sauvola = doxapy.Binarization(doxapy.Binarization.Algorithms.SAUVOLA)
        sauvola.initialize(grayscale_image)
        sauvola.to_binary(binary_image, {"window": 75, "k": 0.2})
        return binary_image

    elif binarization_type == "otsu":
        otsu = doxapy.Binarization(doxapy.Binarization.Algorithms.OTSU)
        otsu.initialize(grayscale_image)
        otsu.to_binary(binary_image)
        return binary_image

    elif binarization_type == "niblack":
        niblack = doxapy.Binarization(doxapy.Binarization.Algorithms.NIBLACK)
        niblack.initialize(grayscale_image)
        niblack.to_binary(binary_image, {"window": 75, "k": 0.01})
        return binary_image

    elif binarization_type == "wolf":
        wolf = doxapy.Binarization(doxapy.Binarization.Algorithms.WOLF)
        wolf.initialize(grayscale_image)
        wolf.to_binary(binary_image, {"window": 75, "k": 0.2})
        return binary_image

    elif binarization_type == "wan":
        wan = doxapy.Binarization(doxapy.Binarization.Algorithms.WAN)
        wan.initialize(grayscale_image)
        wan.to_binary(binary_image, {"window": 75, "k": 0.2})
        return binary_image
    else:
        raise Exception("Binarization type not recognized")


if __name__ == "__main__":
    img = "sample.png"
    img_url = 'https://qa.materialsmine.org/api/files/59667d92e74a1d62877b8fb5'
    bin_img = binarize_image(img_url, binarization_type="wan")
    Image.fromarray(bin_img).show()
