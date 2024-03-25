import os
import pydicom
import numpy as np
import SimpleITK as sitk

def load_dicom_series(directory):
    """
    Load a DICOM series from a directory.
    """
    reader = sitk.ImageSeriesReader()
    dicom_files = reader.GetGDCMSeriesFileNames(directory)
    reader.SetFileNames(dicom_files)
    image = reader.Execute()
    return image

def region_growing_segmentation(image):
    """
    Perform region growing segmentation on the input image.
    """
    # Define seed point (you may need to adjust this)
    seed_point = (100, 100, 10)  # Example seed point (x, y, z)

    # Apply region growing segmentation
    segmented_image = sitk.ConnectedThreshold(image, seedList=[seed_point], lower=0, upper=2000)

    return segmented_image

def save_segmentation(segmentation, output_directory):
    """
    Save the segmented image.
    """
    sitk.WriteImage(segmentation, os.path.join(output_directory, "segmented_image.dcm"))

if __name__ == "__main__":
    # Directory containing DICOM files
    dicom_directory =r'C:\Users\tarun\PycharmProjects\pyth\project.vvcx\case2\case2'

    # Load DICOM series
    dicom_image = load_dicom_series(dicom_directory)

    # Segment the image using region growing
    segmented_image = region_growing_segmentation(dicom_image)

    # Save the segmented image
    output_directory = "output"
    os.makedirs(output_directory, exist_ok=True)
    save_segmentation(segmented_image, output_directory)


