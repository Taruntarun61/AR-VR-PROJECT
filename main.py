import os
import vtk
import pydicom
import numpy as np


def dicom_to_vtk(dicom_dir):
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(dicom_dir)
    reader.Update()

    # Get image data
    image_data = reader.GetOutput()
    print("DICOM Imagedata:", image_data)

    # Compute spacing
    spacing = image_data.GetSpacing()
    print("DICOM spacing:", spacing)

    # Compute dimensions
    dims = image_data.GetDimensions()
    print("DICOM dimensions:", dims)  # Print dimensions for debugging

    # Check if dimensions are not 3D
    if len(dims) != 3:
        raise ValueError("DICOM data is not in 3D")

    # Create a VTK image
    image_vtk = vtk.vtkImageData()
    image_vtk.SetDimensions(dims)
    image_vtk.SetSpacing(spacing)
    image_vtk.AllocateScalars(vtk.VTK_DOUBLE, 1)

    # Copy data from DICOM reader to VTK image
    image_vtk.DeepCopy(image_data)

    # Reslice image data
    reslice = vtk.vtkImageReslice()
    reslice.SetInputData(image_vtk)
    reslice.SetOutputDimensionality(3)
    reslice.SetResliceAxesDirectionCosines(1, 0, 0, 0, 1, 0, 0, 0, 1)
    reslice.SetInterpolationModeToLinear()
    reslice.Update()

    return reslice.GetOutput()


def create_mesh(image_data):
    contour = vtk.vtkMarchingCubes()
    contour.SetInputData(image_data)
    contour.SetValue(4, 4)
    contour.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(contour.GetOutput())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor


if __name__ == "__main__":
    # Path to DICOM directory
    dicom_dir = r'C:\Users\tarun\PycharmProjects\pyth\OneDrive_1_3-17-2024'

    # Convert DICOM to VTK image data
    image_data = dicom_to_vtk(dicom_dir)

    # Create 3D mesh
    mesh_actor = create_mesh(image_data)

    # Create renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(mesh_actor)

    # Create render window
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    # Create render window interactor
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # Start the interaction
    render_window.Render()
    render_window_interactor.Start()