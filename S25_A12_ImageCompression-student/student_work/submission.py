# Isaac Lane
# CSCI 128 - Section K
# Assessment 12
# References: None
# Time: 3 hours

import helper_library as helper

def block_average(grid, x, y, width, height):
    new_grid = grid[y: y + height]

    for i, line in enumerate(new_grid):
        new_grid[i] = line[x: x + width]

    merged_values = []

    for val in new_grid[0][0]:
        merged_values.append(val)

    count = 1

    for i, line in enumerate(new_grid):
        for j, values in enumerate(line):
            if i == 0 and j == 0:
                continue
            else:
                count += 1
                for i, val in enumerate(values):
                    merged_values[i] = merged_values[i] + val


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
    if width <= threshold or height <= threshold:
        return create_compressed_block(block_average(grid, x, y, width, height), width, height)
    else:
        new_width = width // 2
        width2 = width - new_width
        new_height = height // 2
        height2 = height - new_height

        top_compressed_image = compress_image(grid, x, y, new_width, new_height, threshold)
        top_compressed_image = merge_lists(top_compressed_image, compress_image(grid, x + new_width, y, width2, new_height, threshold))

        bottom_compressed_image = compress_image(grid, x, y + new_height, new_width, height2, threshold)
        bottom_compressed_image = merge_lists(bottom_compressed_image, compress_image(grid, x + new_width, y + new_height, width2, height2, threshold))

        compressed_image = []
        for line in top_compressed_image:
            compressed_image.append(line)

        for line in bottom_compressed_image:
            compressed_image.append(line)

        return compressed_image

if __name__ == "__main__":
    image_file = input("IMAGE_FILENAME> ")
    threshold_num = int(input("COMPRESSION_THRESHOLD> "))

    image_list = helper.image_to_list(image_file)

    final_image = compress_image(image_list, 0, 0, len(image_list[0]), len(image_list), threshold_num)

    helper.output_image(final_image, "compressed_" + image_file)

    print(f"OUTPUT Width: {len(final_image[0])}")
    print(f"OUTPUT Height: {len(final_image)}")
    print(f"OUTPUT Threshold: {threshold_num}")