import arcpy
import os
import csv

class Toolbox(object):
    def __init__(self):
        self.label = "CASCADE Road Elevation Summary Toolbox"
        self.alias = "cascadeRoadElevation"
        self.tools = [RoadElevationSummary]

class RoadElevationSummary(object):
    def __init__(self):
        self.label = "Summarize Road Elevation by Domain"
        self.description = "Calculates the average elevation of NC-12 road points per domain using a DEM raster."

    def getParameterInfo(self):
        params = [
            arcpy.Parameter(
                displayName="Domain Polygons",
                name="domain_polygons",
                datatype="GPFeatureLayer",
                parameterType="Required",
                direction="Input"
            ),
            arcpy.Parameter(
                displayName="Road Points (NC-12)",
                name="road_points",
                datatype="GPFeatureLayer",
                parameterType="Required",
                direction="Input"
            ),
            arcpy.Parameter(
                displayName="DEM Raster",
                name="dem_raster",
                datatype="GPRasterLayer",
                parameterType="Required",
                direction="Input"
            ),
            arcpy.Parameter(
                displayName="Output Folder",
                name="output_folder",
                datatype="DEFolder",
                parameterType="Required",
                direction="Input"
            )
        ]
        return params

    def execute(self, parameters, messages):
        domain_polygons = parameters[0].valueAsText
        road_points = parameters[1].valueAsText
        dem_raster = parameters[2].valueAsText
        output_folder = parameters[3].valueAsText

        messages.addMessage("Extracting elevation values from DEM...")

        temp_points = os.path.join("in_memory", "temp_points")
        arcpy.sa.ExtractValuesToPoints(road_points, dem_raster, temp_points, interpolate_values="NONE")

        messages.addMessage("Performing spatial join with domains...")
        joined_fc = os.path.join("in_memory", "joined_fc")
        arcpy.analysis.SpatialJoin(temp_points, domain_polygons, joined_fc)

        messages.addMessage("Calculating summary statistics...")
        domain_elevations = {}
        with arcpy.da.SearchCursor(joined_fc, ["ID", "RASTERVALU"]) as cursor:
            for row in cursor:
                domain_id = row[0]
                elev = row[1]
                if elev is None:
                    continue
                if domain_id not in domain_elevations:
                    domain_elevations[domain_id] = []
                domain_elevations[domain_id].append(elev)

        output_csv = os.path.join(output_folder, "road_elevation_summary.csv")
        with open(output_csv, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["DomainID", "PointCount", "AverageElevation"])
            for domain_id, elevations in domain_elevations.items():
                avg_elev = sum(elevations) / len(elevations)
                writer.writerow([domain_id, len(elevations), round(avg_elev, 3)])

        messages.addMessage(f"Summary CSV written to: {output_csv}")
