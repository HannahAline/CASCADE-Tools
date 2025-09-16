import arcpy
import os
import csv

class Toolbox(object):
    def __init__(self):
        self.label = "Clip and Resample Barrier Domains"
        self.alias = "clipresample"
        self.tools = [ClipAndResample]

class ClipAndResample(object):
    def __init__(self):
        self.label = "Clip and Resample Domains"
        self.description = (
            "Clips a LiDAR raster to each domain polygon and resamples it to 10m resolution. "
            "Each domain's outputs are organized into individual subfolders named by domain ID. "
            "A summary CSV is generated to validate all output files and assist with reproducibility."
        )
        self.canRunInBackground = False

    def getParameterInfo(self):
        params = []

        in_raster = arcpy.Parameter(
            displayName="Input LiDAR Raster",
            name="in_raster",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input"
        )
        params.append(in_raster)

        in_domains = arcpy.Parameter(
            displayName="Domain Polygon Layer",
            name="in_domains",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        )
        params.append(in_domains)

        out_folder = arcpy.Parameter(
            displayName="Base Output Folder",
            name="out_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Output"
        )
        params.append(out_folder)

        return params

    def execute(self, parameters, messages):
        lidar_raster = parameters[0].valueAsText
        domains_fc = parameters[1].valueAsText
        base_output_folder = parameters[2].valueAsText

        arcpy.env.overwriteOutput = True

        if not os.path.exists(base_output_folder):
            os.makedirs(base_output_folder)

        arcpy.AddMessage("Starting domain processing...")

        # Prepare summary CSV
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_csv = os.path.join(base_output_folder, f"domain_processing_summary_{timestamp}.csv")
        csv_fields = ["Domain_ID", "Clip_Path", "Resample_Path", "Status"]
        with open(summary_csv, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_fields)

            with arcpy.da.SearchCursor(domains_fc, ['OID@', 'ID']) as cursor:
                for oid, domain_id in cursor:
                    try:
                        arcpy.AddMessage(f"Processing domain ID {domain_id}...")
                        domain_folder = os.path.join(base_output_folder, f"domain_{domain_id}")
                        if not os.path.exists(domain_folder):
                            os.makedirs(domain_folder)

                        temp_layer = "domain_layer"
                        arcpy.MakeFeatureLayer_management(domains_fc, temp_layer)
                        arcpy.management.SelectLayerByAttribute(
                            in_layer_or_view=temp_layer,
                            selection_type="NEW_SELECTION",
                            where_clause=f"OBJECTID = {oid}"
                        )

                        clip_output = os.path.join(domain_folder, f"clip_domain_{domain_id}.tif")
                        resample_output = os.path.join(domain_folder, f"resampled_domain_{domain_id}.tif")

                        arcpy.management.Clip(
                            in_raster=lidar_raster,
                            rectangle="",
                            out_raster=clip_output,
                            in_template_dataset=temp_layer,
                            nodata_value="-9999",
                            clipping_geometry="ClippingGeometry",
                            maintain_clipping_extent="MAINTAIN_EXTENT"
                        )

                        arcpy.management.Resample(
                            in_raster=clip_output,
                            out_raster=resample_output,
                            cell_size="10 10",
                            resampling_type="BILINEAR"
                        )

                        writer.writerow([domain_id, clip_output, resample_output, "Success"])
                    except Exception as e:
                        arcpy.AddError(f"Failed domain ID {domain_id}: {str(e)}")
                        writer.writerow([domain_id, "", "", f"Failed: {str(e)}"])

        arcpy.AddMessage("✅ All domains processed. Summary CSV saved at: " + summary_csv)
