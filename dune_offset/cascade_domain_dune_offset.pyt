
# -*- coding: utf-8 -*-
import arcpy
import os
import csv

class Toolbox(object):
    def __init__(self):
        self.label = "CASCADE Domain Offset Tool"
        self.alias = "cascade_offset"
        self.tools = [DomainOffsetCalculator]

class DomainOffsetCalculator(object):
    def __init__(self):
        self.label = "Calculate Domain Offset (Revised)"
        self.description = "Calculates average offset from transect-dune intersections for each domain using multiple transects per domain."

    def getParameterInfo(self):
        params = [
            arcpy.Parameter(
                displayName="Domains (Polygon)",
                name="domains",
                datatype="GPFeatureLayer",
                parameterType="Required",
                direction="Input"
            ),
            arcpy.Parameter(
                displayName="Transects (Line)",
                name="transects",
                datatype="GPFeatureLayer",
                parameterType="Required",
                direction="Input"
            ),
            arcpy.Parameter(
                displayName="Dune Line (Line)",
                name="duneline",
                datatype="GPFeatureLayer",
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
        domains_fc = parameters[0].valueAsText
        transects_fc = parameters[1].valueAsText
        dune_fc = parameters[2].valueAsText
        output_folder = parameters[3].valueAsText

        arcpy.env.overwriteOutput = True
        out_csv_path = os.path.join(output_folder, "domain_offsets.csv")

        # Prepare CSV
        with open(out_csv_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Domain_ID", "Transect_LineID", "Offset_Distance"])

            with arcpy.da.SearchCursor(domains_fc, ["SHAPE@", "ID"]) as domain_cursor:
                for domain_row in domain_cursor:
                    domain_geom = domain_row[0]
                    domain_id = domain_row[1]

                    # Create domain-specific folder
                    domain_folder = os.path.join(output_folder, f"domain_{domain_id}")
                    os.makedirs(domain_folder, exist_ok=True)

                    # Select transects intersecting the domain
                    domain_transects = arcpy.management.SelectLayerByLocation(
                        transects_fc, "INTERSECT", domain_geom, selection_type="NEW_SELECTION"
                    )

                    # For each transect, find intersection with dune
                    with arcpy.da.SearchCursor(domain_transects, ["SHAPE@", "LineID"]) as tran_cursor:
                        for tran in tran_cursor:
                            tran_geom, line_id = tran

                            intersect_points = arcpy.analysis.Intersect(
                                [tran_geom, dune_fc],
                                os.path.join("in_memory", f"int_{domain_id}_{line_id}"),
                                output_type="POINT"
                            )

                            point_count = int(arcpy.management.GetCount(intersect_points)[0])
                            if point_count > 0:
                                # Get distance from start of transect to intersection point
                                with arcpy.da.SearchCursor(intersect_points, ["SHAPE@"]) as p_cursor:
                                    for p in p_cursor:
                                        intersect_point = p[0]
                                        offset = tran_geom.measureOnLine(intersect_point)
                                        writer.writerow([domain_id, line_id, offset])

        arcpy.AddMessage(f"CSV output saved to: {out_csv_path}")
