"""
Generate Example FHIR Data and Flatten
--------------------------------------

This script uses refactored functions from the `fhir_utils` module to:
1. Define example patient and lab observation data using new dictionary structures.
2. Generate a FHIR Bundle containing these data using `create_patient_lab_bundle`.
3. Print the generated FHIR Bundle in JSON format.
4. Flatten the FHIR Bundle into a pandas DataFrame using `flatten_fhir_bundle`.
5. Print the resulting DataFrame.
"""

import json

# Assuming the script is run from the project root, 'src' should be discoverable.
from src.medical_data_science.fhir_utils import (
    create_patient_lab_bundle,
    flatten_fhir_bundle,
)

def main():
    """Main function to generate and process FHIR data."""

    # 1. Define Patient Data
    patient_details = {
        'id': "patient-example-01",
        'family_name': "Mustermann",
        'given_name': "Max",
        'birth_date': "1973-01-01",  # Assuming 50 years old as of 2023-01-01
        'gender': "male"
    }
    print(f"Using Patient Details: {patient_details}\n")

    # 2. Define Lab Observations Data
    lab_observations_details = [
        {
            'observation_id': "hdl-obs-01",
            'effective_date_time': "2020-01-01T10:00:00Z",
            'code_system': "http://loinc.org",
            'code': "2085-9",
            'code_display': "Cholesterol in HDL [Mass/volume] in Serum or Plasma",
            'value_quantity_value': 55.0,
            'value_quantity_unit': "mg/dL",
            'value_quantity_unit_code': "mg/dL" 
        },
        {
            'observation_id': "glucose-obs-01",
            'effective_date_time': "2020-01-01T10:05:00Z", # Slightly different time
            'code_system': "http://loinc.org",
            'code': "2339-0",
            'code_display': "Glucose [Mass/volume] in Blood by Test strip",
            'value_quantity_value': 100.0,
            'value_quantity_unit': "mg/dL",
            'value_quantity_unit_code': "mg/dL"
        },
        {
            'observation_id': "hdl-obs-02",
            'effective_date_time': "2021-01-01T10:30:00Z",
            'code_system': "http://loinc.org",
            'code': "2085-9",
            'code_display': "Cholesterol in HDL [Mass/volume] in Serum or Plasma",
            'value_quantity_value': 58.0,
            'value_quantity_unit': "mg/dL",
            'value_quantity_unit_code': "mg/dL"
        },
        {
            'observation_id': "hdl-obs-03",
            'effective_date_time': "2022-01-01T11:00:00Z",
            'code_system': "http://loinc.org",
            'code': "2085-9",
            'code_display': "Cholesterol in HDL [Mass/volume] in Serum or Plasma",
            'value_quantity_value': 52.0,
            'value_quantity_unit': "mg/dL",
            'value_quantity_unit_code': "mg/dL"
        }
    ]
    print(f"Using {len(lab_observations_details)} Lab Observation Details.\n")

    # 3. Generate FHIR Bundle
    print("Generating FHIR Bundle...")
    fhir_bundle = create_patient_lab_bundle(
        patient_details=patient_details,
        lab_observations_details=lab_observations_details
    )
    print("FHIR Bundle generated.\n")

    # 4. Print the FHIR Bundle
    bundle_json = fhir_bundle.as_json() # fhir.resources model has as_json()
    print("--- Generated FHIR Bundle (JSON) ---")
    print(json.dumps(bundle_json, indent=2))
    print("--- End of FHIR Bundle ---\n")

    # 5. Flatten Bundle to DataFrame
    print("Flattening FHIR Bundle to DataFrame...")
    # The flatten_fhir_bundle function expects a dictionary
    flattened_df = flatten_fhir_bundle(bundle_json)
    print("DataFrame generated.\n")

    # 6. Print the DataFrame
    print("--- Flattened DataFrame ---")
    if flattened_df is not None and not flattened_df.empty:
        print(flattened_df.to_string())
    else:
        print("DataFrame is empty or None.")
    print("--- End of DataFrame ---")

if __name__ == "__main__":
    main()
