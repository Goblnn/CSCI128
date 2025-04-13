# Isaac Lane
# CSCI 128 - Section K
# Assessment 12
# References: None
# Time: 1 hour

import helper_library as helper

def block_average(grid, x, y, width, height):
    new_grid = grid[y: y + height]
    print(new_grid)

    for i, line in enumerate(new_grid):
        new_grid[i] = line[x: x + width]
    print(new_grid)

    merged_values = new_grid[0][0]

    count = 1

    for i, line in enumerate(new_grid):
        for j, values in enumerate(line):
            if i == 0 and j == 0:
                continue
            else:
                count += 1
                merged_values[0] = (merged_values[0] + values[0])
                merged_values[1] = (merged_values[1] + values[1])
                merged_values[2] = (merged_values[2] + values[2])

    merged_values[0] = merged_values[0] // count
    merged_values[1] = merged_values[1] // count
    merged_values[2] = merged_values[2] // count

    return merged_values

def create_compressed_block(avg_color, width, height):
    new_lst = []

    for i in range(height):
        new_lst.append([])
        for j in range(width):
            new_lst[i].append(avg_color)

    return new_lst

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