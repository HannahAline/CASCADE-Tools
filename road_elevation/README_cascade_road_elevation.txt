CASCADE Road Elevation Tool
===========================

Author: Hannah A. Henry  
Email: hahenry@unc.edu  
ORCID: https://orcid.org/0000-0003-0767-8669  
GitHub: https://github.com/HannahAline  

Overview
--------
This ArcGIS Pro Python Toolbox calculates the average road elevation (e.g., NC-12) within each CASCADE model domain using a provided DEM raster. 
The tool supports long-term coastal geomorphology research and CASCADE model applications by quantifying how road elevations vary through time.

Toolbox Name:
    cascade_road_elevation_tool.pyt

Tool Name:
    Calculate Road Elevation by Domain

Functionality
-------------
The tool performs the following steps:
1. Extracts elevation values from a DEM raster at road point or line locations.
2. Performs a spatial join between road features and rectangular domain polygons.
3. Computes the number of sampled points and the average elevation for each domain, keyed by the "ID" field.
4. Outputs a summary CSV file with results for all domains.

Inputs
------
- **Domain Polygons (Feature Layer)**  
  Polygon layer with a unique "ID" field for each domain (e.g., 500 m x 1000 m grid cells).  

- **Road Features (Feature Layer)**  
  Point or line features representing the road alignment (e.g., NC-12).  

- **DEM Raster (Raster Layer)**  
  Digital Elevation Model used to extract elevation values.  

- **Output Folder (Folder)**  
  Directory where the summary CSV file will be saved.  

Outputs
-------
- **road_elevation_summary.csv**  
  A CSV file saved in the specified folder with the following fields:  
    - DomainID  
    - PointCount  
    - AverageElevation  

Example Workflow
----------------
Run this tool with annual DEMs to track changes in NC-12’s elevation across years. 
This analysis helps evaluate road vulnerability and adaptation strategies within the CASCADE modeling framework.

Citation and Reuse
------------------
If you use this tool in your research, please cite:

> Hannah A. Henry (2025). CASCADE Road Elevation Tool.  
> University of North Carolina at Chapel Hill.  
> GitHub: https://github.com/HannahAline  
> ORCID: https://orcid.org/0000-0003-0767-8669  

License
-------
This tool is open-source and freely available for academic and nonprofit use. 
Please contact the author for other licensing inquiries.


