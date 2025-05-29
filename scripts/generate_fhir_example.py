"""
Generate Example FHIR Data and Flatten
"""

from fhir_research.utils import flatten_fhir_bundle, filter_fhir_dataframe
from fhir_research.examples import fhir_bundle_marimo_max


def main():
    fhir_bundle = fhir_bundle_marimo_max()
    bundle_json_str = fhir_bundle.model_dump_json(indent=2)
    bundle_dict = fhir_bundle.model_dump()
    df_full = flatten_fhir_bundle(bundle_dict)
    df_subset = filter_fhir_dataframe(df_full, "code_coding_0_code", "2085-9")

    print("--- FHIR Bundle (JSON) ---")
    print(bundle_json_str)
    print("--- End of FHIR Bundle (JSON) ---")

    print("--- Full DataFrame ---")
    if df_full is not None and not df_full.empty:
        print(df_full.to_string())
    else:
        print("DataFrame is empty or None.")
    print("--- End of Full DataFrame ---")

    print("--- Filtered DataFrame ---")
    if df_subset is not None and not df_subset.empty:
        print(df_subset.to_string())
    else:
        print("DataFrame is empty or None.")
    print("--- End of Filtered DataFrame ---")


if __name__ == "__main__":
    main()
