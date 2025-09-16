CASCADE Clip and Resample Tool
==============================

Author: Hannah A. Henry  
Email: hahenry@unc.edu  
ORCID: https://orcid.org/0000-0003-0767-8669  
GitHub: https://github.com/HannahAline  

Overview
--------
This ArcGIS Pro Python Toolbox clips and resamples DEM rasters to the boundaries of CASCADE model domains. 
The tool ensures that each domain has a standardized elevation dataset with consistent extent and resolution, 
serving as a preprocessing step for downstream CASCADE analyses.

Toolbox Name:
    cascade_clip_resample_tool.pyt

Tool Name:
    Clip and Resample DEMs by Domain

Functionality
-------------
The tool performs the following steps:
1. Clips input DEM raster(s) to the extent of each domain polygon.  
2. Resamples clipped rasters to a user-specified resolution.  
3. Saves each processed DEM into per-domain subfolders with standardized filenames.  

Inputs
------
- **Domain Polygons (Feature Layer)**  
  Polygon layer with a unique "ID" field for each rectangular domain.  

- **Input DEM (Raster Layer)**  
  Digital Elevation Model to be clipped and resampled.  

- **Target Resolution (Numeric)**  
  Desired raster cell size (e.g., 5 m, 10 m).  

- **Output Folder (Folder)**  
  Directory where clipped and resampled rasters will be saved.  

Outputs
-------
- **Clipped and Resampled DEMs**  
  GeoTIFF files saved in per-domain subfolders.  
  Filenames follow the convention: `domain_<ID>_resampled.tif`.  

Example Workflow
----------------
Run this tool as the first preprocessing step for CASCADE.  
Outputs can be passed directly into the `cascade_export_npy` tool to generate NumPy array inputs for CASCADE simulations.

Citation and Reuse
------------------
If you use this tool in your research, please cite:

> Hannah A. Henry (2025). CASCADE Clip and Resample Tool.  
> University of North Carolina at Chapel Hill.  
> GitHub: https://github.com/HannahAline  
> ORCID: https://orcid.org/0000-0003-0767-8669  

License
-------
This tool is open-source and freely available for academic and nonprofit use. 
Please contact the author for other licensing inquiries.
