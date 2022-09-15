from pprint import pprint
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import re
import requests
import random
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


def two_point_correlation(bin_image, radius=10):

    # get dimensions of image
    height, width = bin_image.shape

    # print dimensions of image
    print("Image dimensions: {}x{}".format(width, height))

    # generate random coordinate
    def generate_random_point():
        return random.randint(0, height - 1), random.randint(0, width - 1)

    def get_second_point(point):
        x, y = point
        x1_range = range(x - radius, x + radius + 1)
        print(x1_range)

    iteration_counter = 0
    same_color = 0

    trials = int(width * height/2)

    for i in range(trials):
        p1 = generate_radom_point()
        p2 = generate_radom_point()

        # prevent p1 and p2 from being the same point
        while (p1 == p2):
            p2 = generate_radom_point()

        [x1, y1] = p1
        [x2, y2] = p2

        if bin_image[x1, y1] == bin_image[x2, y2]:
            same_color += 1

        total += 1

    print("Total points: {}, same color {} \nThe probability is {}".format(
        total, same_color, same_color/total))


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
    # two_point_correlation(bin_img)
    Image.fromarray(bin_img).show()

    def get_second_point(point, radius=10):
        x, y = point
        x1_range = np.arange(x - radius, x + radius + 1, 1)
        x1_range = x1_range[x1_range >= 0]

    get_second_point((1, 1))
