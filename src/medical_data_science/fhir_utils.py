"""
FHIR Utilities Module
---------------------

This module provides functions to create and process FHIR resources,
specifically for patient data and associated HDL observations.

Functions:
    create_patient_hdl_observation: Creates a FHIR Bundle with a Patient
                                      and their HDL Observation resources.
    flatten_fhir_bundle: Flattens a FHIR Bundle dictionary into a pandas DataFrame.
"""
import datetime
import uuid
import pandas as pd

from fhir.resources.bundle import Bundle, BundleEntry
from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from fhir.resources.fhirreference import FHIRReference
from fhir.resources.humanname import HumanName
from fhir.resources.identifier import Identifier
from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.quantity import Quantity
from fhir.resources.meta import Meta


def create_patient_hdl_observation(
    patient_id: str,
    patient_family_name: str,
    patient_given_name: str,
    patient_birth_date: str,  # YYYY-MM-DD
    patient_gender: str,
    hdl_observations: list[dict]
) -> Bundle:
    """
    Creates a FHIR Bundle containing a Patient resource and their HDL Observation resources.

    Args:
        patient_id (str): The ID for the patient.
        patient_family_name (str): Patient's family name.
        patient_given_name (str): Patient's given name.
        patient_birth_date (str): Patient's birth date in 'YYYY-MM-DD' format.
        patient_gender (str): Patient's gender (e.g., 'male', 'female', 'other').
        hdl_observations (list of dicts): A list where each dict contains:
            - 'value' (float): The HDL value.
            - 'effective_date_time' (str): Observation date 'YYYY-MM-DDTHH:MM:SSZ' or 'YYYY-MM-DD'.
            - 'observation_id' (str): A unique ID for this observation.

    Returns:
        fhir.resources.bundle.Bundle: The FHIR Bundle resource object.
    """
    bundle_entries = []

    # --- Create Patient Resource ---
    patient = Patient.construct()
    patient.id = patient_id
    
    # Meta and Profile for HumanName - fhir.resources may not support meta on sub-elements directly.
    # We will create HumanName correctly. Conceptual conformance to the profile is noted.
    # If direct meta profiling for HumanName was supported, it would look like:
    # hn_meta = Meta.construct()
    # hn_meta.profile = ['http://fhir.de/StructureDefinition/humanname-de-basis']
    # human_name.meta = hn_meta
    # For now, we focus on correct HumanName structure.

    human_name = HumanName.construct()
    human_name.use = "official"
    human_name.family = patient_family_name
    human_name.given = [patient_given_name]
    # If HumanName could have its own meta:
    # human_name.meta = Meta.construct(profile=['http://fhir.de/StructureDefinition/humanname-de-basis'])
    patient.name = [human_name]

    patient.identifier = [
        Identifier.construct(
            system="urn:ietf:rfc:3986", value=f"urn:uuid:{patient_id}"
        )
    ]
    patient.gender = patient_gender
    patient.birthDate = datetime.date.fromisoformat(patient_birth_date)

    patient_entry = BundleEntry.construct()
    patient_entry.fullUrl = f"urn:uuid:{patient.id}" # Using URN for new resource
    patient_entry.resource = patient
    bundle_entries.append(patient_entry)

    # --- Create Observation Resources ---
    for obs_data in hdl_observations:
        observation = Observation.construct()
        observation.id = obs_data["observation_id"]
        observation.status = "final"

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

        observation.code = CodeableConcept.construct(
            coding=[
                Coding.construct(
                    system="http://loinc.org",
                    code="2085-9",
                    display="Cholesterol in HDL [Mass/volume] in Serum or Plasma",
                )
            ]
        )

        observation.subject = FHIRReference.construct(
            reference=f"urn:uuid:{patient_id}" # Reference patient by its fullUrl in the bundle
        )
        
        # Ensure effectiveDateTime is correctly formatted
        effective_date_time_str = obs_data["effective_date_time"]
        try:
            # Try parsing as full datetime
            observation.effectiveDateTime = datetime.datetime.fromisoformat(effective_date_time_str.replace('Z', '+00:00'))
        except ValueError:
            # Fallback to parsing as date if time is not included
            observation.effectiveDateTime = datetime.datetime.combine(
                datetime.date.fromisoformat(effective_date_time_str),
                datetime.time.min # Default to midnight
            )


        observation.valueQuantity = Quantity.construct(
            value=obs_data["value"],
            unit="mg/dL",
            system="http://unitsofmeasure.org",
            code="mg/dL",
        )

        obs_entry = BundleEntry.construct()
        obs_entry.fullUrl = f"urn:uuid:{observation.id}"
        obs_entry.resource = observation
        bundle_entries.append(obs_entry)

    # --- Create Bundle ---
    bundle = Bundle.construct()
    bundle.type = "collection"
    bundle.id = str(uuid.uuid4()) # Assign a unique ID to the bundle itself
    bundle.timestamp = datetime.datetime.utcnow().isoformat() + "Z"
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
                # If the list contains dictionaries, flatten them
                if v and isinstance(v[0], dict):
                    for i, item in enumerate(v):
                        items.update(_flatten_resource(item, f"{new_key}{sep}{i}", sep=sep))
                # If the list contains simple types, join them or handle as needed
                # For simplicity, we'll join by comma or just take the first if one item
                else:
                    items[new_key] = ', '.join(map(str, v)) if len(v) > 1 else (v[0] if v else None)
            else:
                items[new_key] = v
        return items

    if not bundle_dict or "entry" not in bundle_dict:
        return pd.DataFrame()

    resources = [entry["resource"] for entry in bundle_dict.get("entry", []) if "resource" in entry]

    flattened_patients = []
    flattened_observations = []

    for resource in resources:
        resource_type = resource.get("resourceType")
        flat_resource = _flatten_resource(resource)
        
        # Add fullUrl if present in the original entry, as it's useful for joins
        # Search for this resource in the original bundle_dict to get its fullUrl
        original_entry = next((e for e in bundle_dict.get("entry", []) if e.get("resource", {}).get("id") == resource.get("id")), None)
        if original_entry and "fullUrl" in original_entry:
            flat_resource["fullUrl"] = original_entry["fullUrl"]
        
        if resource_type == "Patient":
            flattened_patients.append(flat_resource)
        elif resource_type == "Observation":
            flattened_observations.append(flat_resource)
        # Other resource types could be handled here if needed

    df_patients = pd.DataFrame(flattened_patients)
    df_observations = pd.DataFrame(flattened_observations)

    if df_observations.empty:
        return df_patients # Or an empty DF if patients is also empty

    if df_patients.empty:
        return df_observations # Or an empty DF if observations is also empty

    # Merge observations with patient data
    # The subject reference in Observation is like "Patient/patient-id" or "urn:uuid:patient-id"
    # We need to match this with Patient's fullUrl or derive the ID
    
    # Adjust patient DataFrame to have a common key for merging
    # If patient fullUrl is like "urn:uuid:some-id", use that.
    # If it's relative like "Patient/some-id", construct that form.
    if "fullUrl" in df_patients.columns:
         # Ensure 'subject_reference' column exists in df_observations
        if "subject_reference" not in df_observations.columns and "subject_display" in df_observations.columns : # subject_reference might not always be present.
             df_observations["subject_reference"] = df_observations["subject_display"].apply(lambda x: x if isinstance(x,str) else "" )


        if "subject_reference" in df_observations.columns:
            # Attempt merge on fullUrl and subject_reference
            merged_df = pd.merge(
                df_observations,
                df_patients,
                left_on="subject_reference",
                right_on="fullUrl",
                how="left",
                suffixes=("_obs", "_patient"),
            )
            # Fallback or alternative merge strategy if IDs are used directly
            if "id_patient" in df_patients.columns and "subject_reference" in df_observations.columns:
                 # Check if 'id_patient' column exists, if not, create it from 'id'
                if 'id_patient' not in df_patients.columns and 'id' in df_patients.columns:
                    df_patients = df_patients.rename(columns={'id': 'id_patient'})

                df_observations["subject_id_ref"] = df_observations["subject_reference"].apply(
                    lambda x: x.split("/")[-1] if isinstance(x, str) and "/" in x else (x.split(":")[-1] if isinstance(x, str) and ":" in x else x)
                )
                if not merged_df[df_patients.columns.difference(df_observations.columns).tolist()].isnull().all().all(): # if previous merge was successful skip this
                    merged_df = pd.merge(
                        df_observations,
                        df_patients.add_prefix("patient_"), # Add prefix to avoid column name clashes
                        left_on="subject_id_ref",
                        right_on="patient_id_patient", #after prefixing this is the new name
                        how="left",
                        suffixes=("_obs", ""), # Keep obs suffix for clarity, patient columns are already prefixed
                    )
                    if "subject_id_ref" in merged_df.columns: # drop helper column
                        merged_df = merged_df.drop(columns=["subject_id_ref"])

        else: # If subject_reference is missing in observations, can't merge effectively
            merged_df = df_observations
            for col in df_patients.columns: # Add empty patient columns if any patient exists
                 if not df_patients.empty:
                    merged_df[f"patient_{col}"] = pd.NA
    else: # If no fullUrl on patients, or other issue
        merged_df = df_observations
        # Add empty patient columns if any patient exists
        if not df_patients.empty:
            for col in df_patients.columns:
                 merged_df[f"patient_{col}"] = pd.NA
                 
    return merged_df
