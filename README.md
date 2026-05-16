# DRiVE Lab Repo - *not maintained*

Contains code to be used within the [University of Guelph DRiVE Lab](https://drivelab.uoguelph.ca/drive-lab/drive-lab-homepage/)

## Fast Export Purpose and Description

Project developed to bypass SCANeR Studio time-consuming export procedures. The tool allows researchers using SCANeR Studio to bypass the proprietary export procedures and instead collect data while drive simulations are running. Researchers set up the tool to collect their desired data, with the ability to select from a multitude of variables that SCANeR tracks. The scripting interface in SCANeR links the code in this repository, which processes the data collection. The primary function is to set up and perform the data collection.

## FastExport Manual

Access the [manual](fast-export-manual.pdf) for information on setting up the data collection preferences and the SCANeR Studio scripting interface

## Usage

[Export Confiugrator exe](exportconfigurator/export/export.exe) can be run locally on the user machine

## Python Version

***<span style="color:red">
    This project is developed and maintained to be executed with Python version 3.7.2 and no compatibility with later versions is guaranteed
</span>***

### Additional Usage Details

    This repo contains code and datasets for the University of Guelph DRiVE lab and integrations with SCANeR Studio. 
    A warning that some file names are hardcoded into the scripts, so they may not work unless they are present on the operating device.

    To open the configuration manager, run the export.exe

### Scenario Configuration

    In the Main script of the simulation, right click on the top line of the script. Navigate to "Insert Include".
    Then search for the file path "C:\OKTAL\SCANeRstudio_1.6\data\GUELPH_DATA_1.6\script\include" and select fastexport.inc.
    This will set up the simulation to record the data from the configuration file
