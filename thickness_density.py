from tqdm import tqdm
import os
import numpy as np
import csv
import click
import tifffile
from glob import glob


@click.command()
@click.argument("input_folder",
                type=click.Path(
                    exists=True,
                    file_okay=False))
@click.argument("output_filename", type=click.Path())
@click.option("--height_map_left", type=click.Path(exists=True))
@click.option("--height_map_right", type=click.Path(exists=True))
def main(input_folder, output_filename, height_map_left, height_map_right):
    input_filenames = sorted(glob(os.path.join(input_folder, "*.tif")))
    height_map_left = tifffile.imread(height_map_left)
    height_map_right = tifffile.imread(height_map_right)
    print(tifffile.imread(input_filenames[0]).shape)
    total_thickness = tifffile.imread(input_filenames[0]).shape[1] 
    thickness = (
        height_map_right -
        height_map_left
    )
    white_pixels = np.zeros(len(input_filenames))
    total_pixels = np.zeros(len(input_filenames))
    for i, input_filename in enumerate(tqdm(input_filenames)):
        input_file = tifffile.imread(input_filename).astype(np.bool)
        mask = np.zeros_like(input_file)
        for j, _ in enumerate(mask):
            mask[j, :int(height_map_left[i, j])] = 1
            mask[j, int(height_map_right[i, j]):] = 1
        masked = np.ma.masked_array(input_file, mask=mask)
        white_pixels[i] = np.sum(masked)
        total_pixels[i] = np.sum(1 - mask)
    with open(output_filename, "w") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["thickness", "thickness_sd", "density"])
        t = np.mean(thickness)
        t_sd = np.std(thickness)
        d = 1 - np.sum(white_pixels) / np.sum(total_pixels)
        writer.writerow([t, t_sd, d])


if __name__ == "__main__":
    main()
