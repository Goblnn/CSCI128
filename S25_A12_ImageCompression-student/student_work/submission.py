# Isaac Lane
# CSCI 128 - Section K
# Assessment 12
# References: None
# Time: 1 hour

import helper_library as helper

def block_average(grid, x, y, width, height):


def create_compressed_block(avg_color, width, height):


def merge_lists(lst1, lst2):
    new_lst = []

    for i in range(len(lst1)):
        new_lst.append([])
        for char in lst1[i]:
            new_lst[i].append(char)

    for i in range(len(lst2)):
        for char in lst2[i]:
            new_lst[i].append(char)

    return new_lst

def compress_image(grid, x, y, width, height, threshold):
    rgb_values = []
    return rgb_values


if __name__ == "__main__":
    image_file = input("IMAGE_FILENAME> ")
    threshold_num = int(input("COMPRESSIOn_THRESHOLD> "))

    image_list = helper.image_to_list(image_file)

    final_image = compress_image(image_list, 0, 0, len(image_list), len(image_list[1]), threshold_num)

    helper.output_image(final_image, image_file)