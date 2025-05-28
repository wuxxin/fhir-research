"""
FHIR Utilities Module
---------------------

This module provides functions to create and process FHIR resources,
specifically for generating patient data, lab observations, and bundling them.
It also includes a utility to flatten FHIR bundles into pandas DataFrames.

Core Functions:
    create_patient: Creates a FHIR Patient resource.
    create_observation: Creates a FHIR Observation resource for lab results.
    create_patient_lab_bundle: Creates a FHIR Bundle with a Patient and their
                               lab Observation resources.
    flatten_fhir_bundle: Flattens a FHIR Bundle dictionary into a pandas DataFrame.
"""

import datetime
import uuid
import pandas as pd

from fhir.resources.bundle import Bundle, BundleEntry
from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from fhir.resources.reference import Reference
from fhir.resources.humanname import HumanName
from fhir.resources.identifier import Identifier
from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.quantity import Quantity
from fhir.resources.meta import Meta


def create_patient(
    patient_id: str,
    family_name: str,
    given_name: str,
    birth_date: str,  # YYYY-MM-DD
    gender: str,
) -> Patient:
    """
    Creates a FHIR Patient resource.

    Args:
        patient_id (str): The unique ID for the patient.
        family_name (str): Patient's family name.
        given_name (str): Patient's given name.
        birth_date (str): Patient's birth date in 'YYYY-MM-DD' format.
        gender (str): Patient's gender (e.g., 'male', 'female', 'other', 'unknown').

    Returns:
        fhir.resources.patient.Patient: The FHIR Patient resource object.
    """
    patient = Patient.construct()
    patient.id = patient_id

    # Add Identifier
    patient_identifier = Identifier.construct(
        system="urn:ietf:rfc:3986",  # Using a generic system for example
        value=patient_id,
    )
    patient.identifier = [patient_identifier]

    # Create HumanName with Meta Profile
    human_name = HumanName.construct()
    human_name.use = "official"
    human_name.family = family_name
    human_name.given = [given_name]

    # Add Meta to HumanName
    # hn_meta = Meta.construct()
    # hn_meta.profile = ["http://fhir.de/StructureDefinition/humanname-de-basis"]
    # human_name.meta = hn_meta # This line caused the error
    patient.name = [human_name]

    patient.gender = gender
    try:
        patient.birthDate = datetime.date.fromisoformat(birth_date)
    except ValueError:
        raise ValueError("birth_date must be in YYYY-MM-DD format.")

    return patient


def create_observation(
    observation_id: str,
    patient_reference_str: str,
    effective_date_time: str,  # ISO 8601 format string
    code_system: str,
    code: str,
    code_display: str,
    value_quantity_value: float = None,
    value_quantity_unit: str = None,
    value_quantity_unit_system: str = "http://unitsofmeasure.org",
    value_quantity_unit_code: str = None,
    value_cc_system: str = None,
    value_cc_code: str = None,
    value_cc_display: str = None,
) -> Observation:
    """
    Creates a FHIR Observation resource, typically for a lab result.

    Args:
        observation_id (str): Unique ID for the observation.
        patient_reference_str (str): Reference string for the patient (e.g., "Patient/p1").
        effective_date_time (str): ISO 8601 datetime string for when the observation was made.
        code_system (str): System URL for the observation code (e.g., "http://loinc.org").
        code (str): The observation code itself (e.g., "2085-9").
        code_display (str): Display text for the observation code.
        value_quantity_value (float, optional): Numeric value for a Quantity-based observation.
        value_quantity_unit (str, optional): Unit for the quantity.
        value_quantity_unit_system (str, optional): System for the unit (default UCUM).
        value_quantity_unit_code (str, optional): UCUM code for the unit.
        value_cc_system (str, optional): System URL for a CodeableConcept-based observation value.
        value_cc_code (str, optional): Code for a CodeableConcept-based observation value.
        value_cc_display (str, optional): Display text for a CodeableConcept-based observation value.

    Returns:
        fhir.resources.observation.Observation: The FHIR Observation resource object.
    """
    observation = Observation.construct()
    observation.status = "final"  # Set status before id
    observation.id = observation_id

    # Category: Laboratory
    observation.category = [
        CodeableConcept.construct(
            coding=[
                Coding.construct(
                    system="http://terminology.hl7.org/CodeSystem/observation-category",
                    code="laboratory",
                    display="Laboratory",
                )
            ]
        )
    ]

    # Observation Code
    observation.code = CodeableConcept.construct(
        coding=[
            Coding.construct(
                system=code_system,
                code=code,
                display=code_display,
            )
        ]
    )

    # Subject (Patient Reference)
    observation.subject = Reference.construct(reference=patient_reference_str)

    # Effective DateTime
    try:
        # Attempt to parse as full datetime, assuming Z indicates UTC
        if "Z" in effective_date_time.upper():
            observation.effectiveDateTime = datetime.datetime.fromisoformat(
                effective_date_time.replace("Z", "+00:00")
            )
        # Attempt to parse as date if no time info, or if it's just date
        elif "T" not in effective_date_time:
            dt_obj = datetime.date.fromisoformat(effective_date_time)
            observation.effectiveDateTime = datetime.datetime.combine(
                dt_obj, datetime.time.min
            )  # Add midnight time
        else:  # General ISO format with time and potentially timezone
            observation.effectiveDateTime = datetime.datetime.fromisoformat(
                effective_date_time
            )

    except ValueError:
        raise ValueError(
            "effective_date_time must be a valid ISO 8601 string (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS[Z|+/-HH:MM])."
        )

    # Value Handling
    if value_quantity_value is not None and value_quantity_unit is not None:
        observation.valueQuantity = Quantity.construct(
            value=value_quantity_value,
            unit=value_quantity_unit,
            system=value_quantity_unit_system,
            code=value_quantity_unit_code
            if value_quantity_unit_code
            else value_quantity_unit,  # Fallback for code
        )
    elif value_cc_system is not None and value_cc_code is not None:
        observation.valueCodeableConcept = CodeableConcept.construct(
            coding=[
                Coding.construct(
                    system=value_cc_system, code=value_cc_code, display=value_cc_display
                )
            ]
        )
    # Else: no value is set, or other value[x] types could be added here.

    return observation


def create_patient_lab_bundle(patient_details: dict, lab_observations_details: list) -> Bundle:
    """
    Creates a FHIR Bundle containing a Patient resource and their lab Observation resources.

    Args:
        patient_details (dict): Dictionary with patient information. Expected keys:
            'id', 'family_name', 'given_name', 'birth_date', 'gender'.
            Example: {'id': "p1", 'family_name': "Doe", 'given_name': "John",
                      'birth_date': "1970-01-01", 'gender': "male"}
        lab_observations_details (list of dicts): A list of dictionaries, where each
            dictionary contains the parameters for the `create_observation` function.
            `patient_reference_str` will be automatically derived.
            Example for one lab observation dict:
            {
                'observation_id': "obs1",
                'effective_date_time': "2023-01-01T10:00:00Z",
                'code_system': "http://loinc.org",
                'code': "2085-9",
                'code_display': "Cholesterol in HDL",
                'value_quantity_value': 55.0,
                'value_quantity_unit': "mg/dL",
                'value_quantity_unit_code': "mg/dL" # UCUM code
            }

    Returns:
        fhir.resources.bundle.Bundle: The FHIR Bundle resource object.
    """
    bundle_entries = []

    # Create Patient Resource
    patient_resource = create_patient(
        patient_id=patient_details["id"],
        family_name=patient_details["family_name"],
        given_name=patient_details["given_name"],
        birth_date=patient_details["birth_date"],
        gender=patient_details["gender"],
    )
    patient_entry = BundleEntry.construct()
    # Use URN with resource ID for fullUrl, as per common practice for new resources in a bundle
    patient_entry.fullUrl = f"urn:uuid:{patient_resource.id}"
    patient_entry.resource = patient_resource
    bundle_entries.append(patient_entry)

    patient_reference_str = f"Patient/{patient_resource.id}"

    # Create Observation Resources
    for obs_detail in lab_observations_details:
        # Ensure patient_reference_str is passed correctly
        observation_resource = create_observation(
            patient_reference_str=patient_reference_str, **obs_detail
        )
        obs_entry = BundleEntry.construct()
        obs_entry.fullUrl = f"urn:uuid:{observation_resource.id}"
        obs_entry.resource = observation_resource
        bundle_entries.append(obs_entry)

    # Create Bundle
    bundle = Bundle.construct()
    bundle.type = "collection"
    bundle.id = str(uuid.uuid4())  # Assign a unique ID to the bundle itself
    bundle.timestamp = datetime.datetime.now(
        datetime.timezone.utc
    ).isoformat()  # Use timezone-aware UTC timestamp
    bundle.entry = bundle_entries

    return bundle


def flatten_fhir_bundle(bundle_dict: dict) -> pd.DataFrame:
    """
    Flattens a FHIR Bundle dictionary into a pandas DataFrame.

    This function extracts resources from the bundle, flattens each one
    using a recursive helper function, and then combines them into a single
    DataFrame. Patient information is denormalized onto associated observations.

    Args:
        bundle_dict (dict): A FHIR Bundle resource represented as a Python dictionary
                            (e.g., after `bundle.as_json()`).

    Returns:
        pandas.DataFrame: A DataFrame containing the flattened bundle data.
    """

    def _flatten_resource(resource_dict, parent_key="", sep="_"):
        items = {}
        for k, v in resource_dict.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(_flatten_resource(v, new_key, sep=sep))
            elif isinstance(v, list):
                if v and isinstance(v[0], dict):
                    for i, item in enumerate(v):
                        items.update(_flatten_resource(item, f"{new_key}{sep}{i}", sep=sep))
                else:
                    items[new_key] = (
                        ", ".join(map(str, v)) if len(v) > 1 else (v[0] if v else None)
                    )
            else:
                items[new_key] = v
        return items

    if not bundle_dict or "entry" not in bundle_dict:
        return pd.DataFrame()

    resources = [
        entry["resource"] for entry in bundle_dict.get("entry", []) if "resource" in entry
    ]

    flattened_patients = []
    flattened_observations = []

    for resource in resources:
        resource_type = resource.get("resourceType")
        flat_resource = _flatten_resource(resource)

        original_entry = next(
            (
                e
                for e in bundle_dict.get("entry", [])
                if e.get("resource", {}).get("id") == resource.get("id")
            ),
            None,
        )
        if original_entry and "fullUrl" in original_entry:
            flat_resource["fullUrl"] = original_entry["fullUrl"]

        if resource_type == "Patient":
            flattened_patients.append(flat_resource)
        elif resource_type == "Observation":
            flattened_observations.append(flat_resource)

    df_patients = pd.DataFrame(flattened_patients)
    df_observations = pd.DataFrame(flattened_observations)

    if df_observations.empty:
        return df_patients if not df_patients.empty else pd.DataFrame()

    if df_patients.empty:
        return df_observations  # Or an empty DF if observations is also empty

    # Enhanced merging logic
    # Prefer matching Observation.subject.reference with Patient.fullUrl
    merged_df = pd.DataFrame()

    if "fullUrl" in df_patients.columns and "subject_reference" in df_observations.columns:
        merged_df = pd.merge(
            df_observations,
            df_patients.add_prefix("patient_"),  # Prefix patient columns to avoid clashes
            left_on="subject_reference",
            right_on="patient_fullUrl",
            how="left",
        )

    # Fallback or alternative: Match Observation.subject.reference (e.g., "Patient/id1")
    # with a constructed reference from patient ID if fullUrl merge was incomplete or not possible.
    # This assumes subject_reference might sometimes be "Patient/{id}" and patient_id is just "{id}"
    if (
        merged_df.empty
        or merged_df[[col for col in merged_df.columns if col.startswith("patient_")]]
        .isnull()
        .all()
        .all()
    ):
        if "id" in df_patients.columns and "subject_reference" in df_observations.columns:
            # Create a temporary reference column in df_patients
            df_patients_temp = df_patients.copy()
            df_patients_temp["temp_patient_ref"] = "Patient/" + df_patients_temp["id"].astype(
                str
            )

            current_suffixes = ("_obs", "_patient")  # Default suffixes if not specified

            merged_df = pd.merge(
                df_observations,
                df_patients_temp.add_prefix("patient_"),
                left_on="subject_reference",
                right_on="patient_temp_patient_ref",  # patient_id becomes patient_patient_id after prefix
                how="left",
                suffixes=current_suffixes,
            )
            # Clean up prefixed columns from df_patients if they were all NaNs from a failed previous merge attempt
            # This part is tricky; the goal is to avoid duplicate patient columns if one merge strategy worked partially
            # For simplicity, we'll assume the last merge is the definitive one if prior ones were empty or all NaNs.
            if "patient_temp_patient_ref" in merged_df.columns:
                merged_df = merged_df.drop(columns=["patient_temp_patient_ref"])

    # If still no patient info merged for some observations, ensure observation data is preserved
    if merged_df.empty and not df_observations.empty:
        merged_df = df_observations.copy()
        if (
            not df_patients.empty
        ):  # Add empty patient columns if patients exist but didn't merge
            for col in df_patients.columns:
                merged_df[f"patient_{col}"] = pd.NA
    elif not merged_df.empty and df_observations.shape[0] > merged_df.shape[0]:
        # This case implies some observations were dropped, which shouldn't happen with left merge
        # Potentially, if an obs had no patient match, it might be handled here if merge was inner
        pass  # Current logic uses left merge, so all observations should be kept.

    # Remove the temporary patient_id column if it exists from a previous version's logic
    if (
        "patient_id" in merged_df.columns and "id_obs" in merged_df.columns
    ):  # Example of a specific cleanup
        if "patient_id_patient" in merged_df.columns:  # if patient_id is from patient table
            pass  # keep it
        # This cleanup needs to be more robust based on actual column names post-merge

    return merged_df.reset_index(drop=True)
