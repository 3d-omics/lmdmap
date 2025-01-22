
import argparse
import os
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from pyairtable import Table, Api

# Constants
WIDTH = 1000
HEIGHT = 1000
MEMBRANE_MICRON_WIDTH = 16000
MEMBRANE_MICRON_HEIGHT = 45000
MEMBRANE_PIXEL_WIDTH = 2180
MEMBRANE_PIXEL_HEIGHT = 5780
RESOLUTION_X = 7.4  # Manually corrected resolution
RESOLUTION_Y = MEMBRANE_MICRON_HEIGHT / MEMBRANE_PIXEL_HEIGHT

SLIDE_COORDS = [
    {"slide_tl": (250, 2212), "slide_br": (25660, 77470), "membrane_tl": (4962, 8698), "membrane_br": (21013, 53732)},
    {"slide_tl": (28983, 2004), "slide_br": (54565, 77541), "membrane_tl": (33689, 8698), "membrane_br": (49650, 53658)},
    {"slide_tl": (64978, 1938), "slide_br": (90644, 77372), "membrane_tl": (69768, 8658), "membrane_br": (85819, 53692)},
    {"slide_tl": (93780, 1946), "slide_br": (119690, 77465), "membrane_tl": (98718, 8682), "membrane_br": (114760, 53772)}
]

# Airtable configuration
BASE_ID = "appKakM1bnKSekwuW"
TABLE_NAME = "4-MSE-Info"

# Functions
def fetch_data_from_airtable(cryosection):
    api_key = os.getenv("AIRTABLE_API_KEY")
    if not api_key:
        raise ValueError("AIRTABLE_API_KEY environment variable is not set.")

    api = Api(api_key)
    table = api.table(BASE_ID, TABLE_NAME)
    records = table.all()

    # Extract and filter records by cryosection
    data = []
    for record in records:
        fields = record.get("fields", {})
        if fields.get("cryosection_text") == cryosection:
            xcoord = fields.get("Xcoord")
            ycoord = fields.get("Ycoord")
            size = fields.get("size")
            shape = fields.get("shape")

            # Handle cases where Xcoord or Ycoord is a list
            if isinstance(xcoord, list):
                xcoord = np.mean(xcoord)  # Calculate the average
            if isinstance(ycoord, list):
                ycoord = np.mean(ycoord)  # Calculate the average
            # Convert lists to strings if necessary
            if isinstance(size, list):
                size = ", ".join(map(str, size))
            if isinstance(shape, list):
                shape = ", ".join(map(str, shape))

            data.append({
                "ID": record.get("id"),
                "Xcoord": xcoord,
                "Ycoord": ycoord,
                "size": size,
                "shape": shape,
                "cryosection_text": fields.get("cryosection_text"),
                "SampleType": fields.get("SampleType")
            })

    return pd.DataFrame(data)

def determine_slide_position(mean_x):
    for i, coords in enumerate(SLIDE_COORDS):
        if coords["membrane_tl"][0] < mean_x < coords["membrane_br"][0]:
            return i + 1, coords["membrane_tl"], coords["membrane_br"]
    return None, None, None

def process_input_data(input_data, membrane_tl):
    input_data["Xcoord_pixel"] = (input_data["Xcoord"] - membrane_tl[0]) / RESOLUTION_X + 120
    input_data["Ycoord_pixel"] = (input_data["Ycoord"] - membrane_tl[1]) / RESOLUTION_Y
    return input_data

def crop_image(image_path, crop_ref_x, crop_ref_y):
    with Image.open(image_path) as img:
        cropped = img.crop((crop_ref_x, crop_ref_y, crop_ref_x + WIDTH, crop_ref_y + HEIGHT))
        return cropped

def draw_microsamples_on_image(image, microsamples):
    draw = ImageDraw.Draw(image)
    for _, row in microsamples.iterrows():
        draw.ellipse(
            [(row["Xcoord_pixel_crop"] - 2, row["Ycoord_pixel_crop"] - 2),
             (row["Xcoord_pixel_crop"] + 2, row["Ycoord_pixel_crop"] + 2)],
            fill="red"
        )
    return image

# Main script
def main():
    parser = argparse.ArgumentParser(description="Process cryosection data and images.")
    parser.add_argument(
        "-n", "--name", type=str, required=True,
        help="Cryosection identifier (required)."
    )
    parser.add_argument(
        "-i", "--image", type=str, required=True,
        help="Path to the overview image (required)."
    )
    parser.add_argument(
        "--draw-microsamples", action="store_true",
        help="Draw microsamples on the output cropped image (optional)."
    )
    args = parser.parse_args()

    cryosection = args.name
    overview_image = args.image
    draw_microsamples = args.draw_microsamples

    input_data = fetch_data_from_airtable(cryosection)

    if input_data.empty:
        raise ValueError(f"No data found for cryosection: {cryosection}")

    microsample_centroid = input_data[["Xcoord", "Ycoord"]].mean()
    slide_position, membrane_tl, membrane_br = determine_slide_position(microsample_centroid["Xcoord"])

    if slide_position is None:
        raise ValueError("Microsample is not within any slide's bounds.")

    input_data = process_input_data(input_data, membrane_tl)

    microsample_centroid_pixel = input_data[["Xcoord_pixel", "Ycoord_pixel"]].mean()
    crop_ref_x = round(microsample_centroid_pixel["Xcoord_pixel"] - WIDTH / 2)
    crop_ref_y = round(microsample_centroid_pixel["Ycoord_pixel"] - HEIGHT / 2)

    crop_ref_x = max(crop_ref_x, 20)
    crop_ref_y = max(crop_ref_y, 20)

    cropped_image = crop_image(overview_image, crop_ref_x, crop_ref_y)

    input_data["Xcoord_pixel_crop"] = round(input_data["Xcoord_pixel"] - crop_ref_x)
    input_data["Ycoord_pixel_crop"] = round(input_data["Ycoord_pixel"] - crop_ref_y)

    #Output csv
    output_csv_path = f"{cryosection}.csv"
    input_data.to_csv(output_csv_path, index=False)

    #Output unmarked cropped image
    output_image_path = f"{cryosection}.jpg"
    cropped_image.save(output_image_path)

    # Draw microsamples on the image if the flag is set
    if draw_microsamples:
        cropped_image = draw_microsamples_on_image(cropped_image, input_data)
        output_image_path = f"{cryosection}_marked.jpg"
        cropped_image.save(output_image_path)

    print(f"Processed images and data saved succesfully.")
