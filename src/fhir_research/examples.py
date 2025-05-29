from .utils import create_patient_lab_bundle


def fhir_bundle_marimo_max():
    "Generates a patient and 5 lab observations (4 HDL, 1 Blood-Sugar), returns a FHIR bundle"

    # Define Patient Data
    patient_details = {
        "id": "patient-example-01",
        "family_name": "Marimo",
        "given_name": "Max",
        "birth_date": "1974-01-01",
        "gender": "male",
    }

    # Define Observations Data
    lab_observations_details = [
        {
            "observation_id": "obs-marimo-01",
            "effective_date_time": "2020-01-15T09:00:00Z",
            "code_system": "http://loinc.org",
            "code": "2085-9",
            "code_display": "Cholesterol in HDL",
            "value_quantity_value": 60.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
        {
            "observation_id": "obs-marimo-02",
            "effective_date_time": "2020-01-15T09:05:00Z",  # Slightly different time
            "code_system": "http://loinc.org",
            "code": "2339-0",
            "code_display": "Glucose [Mass/volume] in Blood by Test strip",
            "value_quantity_value": 100.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
        {
            "observation_id": "obs-marimo-03",
            "effective_date_time": "2021-02-20T09:30:00Z",
            "code_system": "http://loinc.org",
            "code": "2085-9",
            "code_display": "Cholesterol in HDL",
            "value_quantity_value": 62.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
        {
            "observation_id": "obs-marimo-04",
            "effective_date_time": "2022-03-10T08:45:00Z",
            "code_system": "http://loinc.org",
            "code": "2085-9",
            "code_display": "Cholesterol in HDL",
            "value_quantity_value": 58.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
        {
            "observation_id": "obs-marimo-05",
            "effective_date_time": "2023-04-05T10:15:00Z",
            "code_system": "http://loinc.org",
            "code": "2085-9",
            "code_display": "Cholesterol in HDL",
            "value_quantity_value": 61.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
    ]

    # Generate FHIR Bundle
    fhir_bundle = create_patient_lab_bundle(
        patient_details=patient_details, lab_observations_details=lab_observations_details
    )

    return fhir_bundle
