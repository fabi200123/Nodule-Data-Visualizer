# HelpBreath - Python part of the application

Each of the folders in here correspond to a different aspect of the application.
In order to use this application you will need to have these requirements met:
- `Python3 version 3.9.2`
- python requirements installed 

In order to install the required packages for these scripts run the following command:
```bash
pip install -r requirements.py
```

## **Dash App**

Dash App folder corresponds to the Dash app that generates the Dashboard web page to visualize the CT Scans:
- 3D Nodule visualization
- 2D Slices with ROI (Region of Interest) 
- Nodule characteristics
- Graphs that shows nodule characteristics` evolution over time

To run this application, you will need to run this command:

```bash
python3 dash-app-dynamic.py
```

Another script that is in this folder is data extractor from the PDF. It is used to extract the field `Hemoleucograma completa` from the medical paper.

To run this script, you will need to run this command:
```bash
python3 pdf_extractor.py PACIENT_CNP PDF_FILE
```

This command needs 2 parameters:
- pacient's CNP from MongoDB
- path to the PDF file


## **Scripts for DICOM Conversion**

This folder contains the script to convert the DICOM images to NRRD images and to add the nodule characteristics retrieved using these images to MongoDB.
Besides this script, it contains a `modules` folder, which consists of the modules used inside the main script.

To run this script you will need to get inside the modules folder, the Precision-medicine-toolbox. To do this, after you are inside the `modules` folder you can run this command:
```bash 
git clone https://github.com/primakov/precision-medicine-toolbox/tree/master
```

After that, from the `Scripts_for_dicom_conversion`, you can run the script as follows:

```bash
python3 dicom_to_nrrd.py PACIENT_FOLDER
```

The parameter `PACIENT_FOLDER` reffers to the folder that contains the DICOM images of the pacient, stored inside a `dcms` folder.

## **Tests**

This folder contains the e2e tests for the Dash App.

In order to run those, you will need to run this command:
```bash
pytest .\dash_test.py
```