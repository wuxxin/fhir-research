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


def fhir_bundle_german_lab_example():
    """Generates a FHIR bundle for Hans Schmidt with German lab observations."""

    # Define Patient Data
    patient_details = {
        "id": "patient-example-02",
        "family_name": "Schmidt",
        "given_name": "Hans",
        "birth_date": "1978-05-15",
        "gender": "male",
    }

    # Define Observations Data
    # Set 1: All lab parameters present
    lab_observations_set1 = [
        {
            "observation_id": "obs-schmidt-01",
            "effective_date_time": "2022-05-20T07:30:00Z",
            "code_system": "http://loinc.org",
            "code": "2324-2",
            "code_display": "Gamma glutamyl transferase",
            "value_quantity_value": 45.0,
            "value_quantity_unit": "U/L",
            "value_quantity_unit_code": "U/L",
        },
        {
            "observation_id": "obs-schmidt-02",
            "effective_date_time": "2022-05-20T07:30:00Z",
            "code_system": "http://loinc.org",
            "code": "1558-6",
            "code_display": "Glucose^fasting",
            "value_quantity_value": 90.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
        {
            "observation_id": "obs-schmidt-03",
            "effective_date_time": "2022-05-20T07:30:00Z",
            "code_system": "http://loinc.org",
            "code": "2093-3",
            "code_display": "Cholesterol",
            "value_quantity_value": 200.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
        {
            "observation_id": "obs-schmidt-04",
            "effective_date_time": "2022-05-20T07:30:00Z",
            "code_system": "http://loinc.org",
            "code": "2085-9",
            "code_display": "Cholesterol in HDL",
            "value_quantity_value": 50.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
        {
            "observation_id": "obs-schmidt-05",
            "effective_date_time": "2022-05-20T07:30:00Z",
            "code_system": "http://loinc.org",
            "code": "2089-1",
            "code_display": "Cholesterol in LDL",
            "value_quantity_value": 130.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
        {
            "observation_id": "obs-schmidt-06",
            "effective_date_time": "2022-05-20T07:30:00Z",
            "code_system": "http://loinc.org",
            "code": "9830-1",
            "code_display": "Cholesterol.total/Cholesterol in HDL",
            "value_quantity_value": 4.0,
            "value_quantity_unit": "ratio",
            "value_quantity_unit_code": "{ratio}", # UCUM code for ratio
        },
        {
            "observation_id": "obs-schmidt-07",
            "effective_date_time": "2022-05-20T07:30:00Z",
            "code_system": "http://loinc.org",
            "code": "2571-8",
            "code_display": "Triglyceride",
            "value_quantity_value": 150.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
    ]

    # Set 2: Triglyceride missing, other values slightly different
    lab_observations_set2 = [
        {
            "observation_id": "obs-schmidt-08",
            "effective_date_time": "2023-08-10T08:00:00Z",
            "code_system": "http://loinc.org",
            "code": "2324-2",
            "code_display": "Gamma glutamyl transferase",
            "value_quantity_value": 48.0,
            "value_quantity_unit": "U/L",
            "value_quantity_unit_code": "U/L",
        },
        {
            "observation_id": "obs-schmidt-09",
            "effective_date_time": "2023-08-10T08:00:00Z",
            "code_system": "http://loinc.org",
            "code": "1558-6",
            "code_display": "Glucose^fasting",
            "value_quantity_value": 95.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
        {
            "observation_id": "obs-schmidt-10",
            "effective_date_time": "2023-08-10T08:00:00Z",
            "code_system": "http://loinc.org",
            "code": "2093-3",
            "code_display": "Cholesterol",
            "value_quantity_value": 210.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
        {
            "observation_id": "obs-schmidt-11",
            "effective_date_time": "2023-08-10T08:00:00Z",
            "code_system": "http://loinc.org",
            "code": "2085-9",
            "code_display": "Cholesterol in HDL",
            "value_quantity_value": 52.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
        {
            "observation_id": "obs-schmidt-12",
            "effective_date_time": "2023-08-10T08:00:00Z",
            "code_system": "http://loinc.org",
            "code": "2089-1",
            "code_display": "Cholesterol in LDL",
            "value_quantity_value": 135.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
        {
            "observation_id": "obs-schmidt-13",
            "effective_date_time": "2023-08-10T08:00:00Z",
            "code_system": "http://loinc.org",
            "code": "9830-1",
            "code_display": "Cholesterol.total/Cholesterol in HDL",
            "value_quantity_value": 4.04, # 210 / 52 = 4.038...
            "value_quantity_unit": "ratio",
            "value_quantity_unit_code": "{ratio}", # UCUM code for ratio
        },
        # Triglyceride (LOINC "2571-8") is intentionally omitted here
    ]

    # Set 3: LDL-Cholesterin missing, other values varied
    lab_observations_set3 = [
        {
            "observation_id": "obs-schmidt-14",
            "effective_date_time": "2024-01-15T09:00:00Z",
            "code_system": "http://loinc.org",
            "code": "2324-2", # Gamma-GT
            "code_display": "Gamma glutamyl transferase",
            "value_quantity_value": 50.0,
            "value_quantity_unit": "U/L",
            "value_quantity_unit_code": "U/L",
        },
        {
            "observation_id": "obs-schmidt-15",
            "effective_date_time": "2024-01-15T09:00:00Z",
            "code_system": "http://loinc.org",
            "code": "1558-6", # Glukose
            "code_display": "Glucose^fasting",
            "value_quantity_value": 92.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
        {
            "observation_id": "obs-schmidt-16",
            "effective_date_time": "2024-01-15T09:00:00Z",
            "code_system": "http://loinc.org",
            "code": "2093-3", # Cholesterin
            "code_display": "Cholesterol",
            "value_quantity_value": 190.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
        {
            "observation_id": "obs-schmidt-17",
            "effective_date_time": "2024-01-15T09:00:00Z",
            "code_system": "http://loinc.org",
            "code": "2085-9", # HDL-Cholesterin
            "code_display": "Cholesterol in HDL",
            "value_quantity_value": 55.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
        # LDL-Cholesterin (LOINC "2089-1") is intentionally omitted here
        {
            "observation_id": "obs-schmidt-18",
            "effective_date_time": "2024-01-15T09:00:00Z",
            "code_system": "http://loinc.org",
            "code": "9830-1", # Cholesterin/HDL-Chol.-Ratio
            "code_display": "Cholesterol.total/Cholesterol in HDL",
            "value_quantity_value": 3.45, # 190 / 55 = 3.45
            "value_quantity_unit": "ratio",
            "value_quantity_unit_code": "{ratio}",
        },
        {
            "observation_id": "obs-schmidt-19",
            "effective_date_time": "2024-01-15T09:00:00Z",
            "code_system": "http://loinc.org",
            "code": "2571-8", # Triglyceride
            "code_display": "Triglyceride",
            "value_quantity_value": 140.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
    ]

    # Set 4: Gamma-GT missing, other values varied
    lab_observations_set4 = [
        # Gamma-GT (LOINC "2324-2") is intentionally omitted here
        {
            "observation_id": "obs-schmidt-20",
            "effective_date_time": "2024-07-20T09:30:00Z",
            "code_system": "http://loinc.org",
            "code": "1558-6", # Glukose
            "code_display": "Glucose^fasting",
            "value_quantity_value": 88.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
        {
            "observation_id": "obs-schmidt-21",
            "effective_date_time": "2024-07-20T09:30:00Z",
            "code_system": "http://loinc.org",
            "code": "2093-3", # Cholesterin
            "code_display": "Cholesterol",
            "value_quantity_value": 195.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
        {
            "observation_id": "obs-schmidt-22",
            "effective_date_time": "2024-07-20T09:30:00Z",
            "code_system": "http://loinc.org",
            "code": "2085-9", # HDL-Cholesterin
            "code_display": "Cholesterol in HDL",
            "value_quantity_value": 53.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
        {
            "observation_id": "obs-schmidt-23",
            "effective_date_time": "2024-07-20T09:30:00Z",
            "code_system": "http://loinc.org",
            "code": "2089-1", # LDL-Cholesterin
            "code_display": "Cholesterol in LDL",
            "value_quantity_value": 125.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
        {
            "observation_id": "obs-schmidt-24",
            "effective_date_time": "2024-07-20T09:30:00Z",
            "code_system": "http://loinc.org",
            "code": "9830-1", # Cholesterin/HDL-Chol.-Ratio
            "code_display": "Cholesterol.total/Cholesterol in HDL",
            "value_quantity_value": 3.68, # 195 / 53 = 3.679...
            "value_quantity_unit": "ratio",
            "value_quantity_unit_code": "{ratio}",
        },
        {
            "observation_id": "obs-schmidt-25",
            "effective_date_time": "2024-07-20T09:30:00Z",
            "code_system": "http://loinc.org",
            "code": "2571-8", # Triglyceride
            "code_display": "Triglyceride",
            "value_quantity_value": 145.0,
            "value_quantity_unit": "mg/dL",
            "value_quantity_unit_code": "mg/dL",
        },
    ]

    all_lab_observations = lab_observations_set1 + lab_observations_set2 + lab_observations_set3 + lab_observations_set4

    # Generate FHIR Bundle
    fhir_bundle = create_patient_lab_bundle(
        patient_details=patient_details, lab_observations_details=all_lab_observations
    )

    return fhir_bundle
