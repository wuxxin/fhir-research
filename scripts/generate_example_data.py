"""
Generate Example FHIR Data and Flatten
--------------------------------------

This script uses functions from the `fhir_utils` module to:
1. Define example patient and HDL observation data.
2. Generate a FHIR Bundle containing these data.
3. Print the generated FHIR Bundle in JSON format.
4. Flatten the FHIR Bundle into a pandas DataFrame.
5. Print the resulting DataFrame.
"""

import json
from datetime import datetime, timedelta, date

# Assuming the script is run from the project root, 'src' should be discoverable.
# If not, sys.path adjustments might be needed, but typically not for this structure.
from src.medical_data_science.fhir_utils import (
    create_patient_hdl_observation,
    flatten_fhir_bundle,
)

def main():
    """Main function to generate and process FHIR data."""

    # 1. Define Patient Data
    patient_id = "patient-example-01"
    patient_family_name = "Mustermann"
    patient_given_name = "Max"
    
    # Calculate patient_birth_date: 50 years before 2023-01-01
    reference_date_for_age = date(2023, 1, 1)
    patient_birth_date_dt = reference_date_for_age - timedelta(days=50 * 365.25) # Approximate 50 years
    patient_birth_date = patient_birth_date_dt.strftime("%Y-%m-%d") # Format as YYYY-MM-DD

    patient_gender = "male"

    print(f"Calculated Patient Birth Date: {patient_birth_date}\n")

    # 2. Define HDL Observations Data
    hdl_observations_data = [
        {
            "value": 55.0,
            "effective_date_time": "2020-01-01T10:00:00Z",
            "observation_id": "hdl-obs-01",
        },
        {
            "value": 58.0,
            "effective_date_time": "2021-01-01T10:30:00Z",
            "observation_id": "hdl-obs-02",
        },
        {
            "value": 52.0,
            "effective_date_time": "2022-01-01T11:00:00Z",
            "observation_id": "hdl-obs-03",
        },
    ]

    # 3. Generate FHIR Bundle
    print("Generating FHIR Bundle...")
    fhir_bundle = create_patient_hdl_observation(
        patient_id=patient_id,
        patient_family_name=patient_family_name,
        patient_given_name=patient_given_name,
        patient_birth_date=patient_birth_date,
        patient_gender=patient_gender,
        hdl_observations=hdl_observations_data,
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
    if not flattened_df.empty:
        print(flattened_df.to_string())
    else:
        print("DataFrame is empty.")
    print("--- End of DataFrame ---")

if __name__ == "__main__":
    main()
