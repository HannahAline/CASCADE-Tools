# CASCADE Tools

Custom ArcGIS Python Toolboxes for preprocessing datasets for the **CASCADE** (Coastal Adaptation to Storms, Climate Change, and Sea Level Rise) barrier island model.  
These tools automate critical steps in preparing high-resolution elevation and shoreline datasets, ensuring standardized and reproducible workflows for barrier island geomorphology research.

Developed by [Hannah A. Henry](https://orcid.org/0000-0003-0767-8669), Ph.D. Student, University of North Carolina at Chapel Hill.  
GitHub: [HannahAline](https://github.com/HannahAline)

---

## Available Toolboxes

### [Clip and Resample Tool](clip_resample/README.txt)  
**Toolbox:** `cascade_clip_resample_tool.pyt`  
- Clips DEM rasters to the extent of each CASCADE model domain.  
- Resamples rasters to a user-defined resolution.  
- Produces per-domain elevation datasets for downstream modeling.  

---

### [Domain Dune Offset Tool](dune_offset/README.txt)  
**Toolbox:** `cascade_domain_dune_offset_tool.pyt`  
- Calculates distance between dune crest and an offshore datum line (offsets) for each domain.  
- Uses an offshore datum line, transects, and dune crest features.  
- Generates CSV outputs required for CASCADE overwash and dune evolution modules.  

---

### [Road Elevation Tool](road_elevation/README.txt)  
**Toolbox:** `cascade_road_elevation_tool.pyt`  
- Extracts DEM elevations at road features (e.g., NC-12 on Hatteras Island).  
- Computes number of road points and mean elevation per domain.  
- Supports temporal analysis of infrastructure vulnerability.  

---

## Usage
Each toolbox is packaged as an ArcGIS Pro Python Toolbox (`.pyt`).  
Open in ArcGIS Pro → configure input datasets → run the tool → review CSV or raster outputs.  

Detailed usage instructions, input/output definitions, and example workflows are provided in the `README.txt` files within each subdirectory.  

---

## Citation
If you use these tools in research or publications, please cite:

> Hannah A. Henry (2025). *CASCADE Tools: ArcGIS Python Toolboxes for Barrier Island Modeling*.  
> University of North Carolina at Chapel Hill.  
> GitHub: [https://github.com/HannahAline/CASCADE-Tools](https://github.com/HannahAline/CASCADE-Tools)  
> ORCID: [https://orcid.org/0000-0003-0767-8669](https://orcid.org/0000-0003-0767-8669)

---

## License
These tools are open-source and freely available for academic and nonprofit use.  
Please contact the author regarding licensing for other applications.
