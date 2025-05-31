# FHIR Profiles

- **Patient Data**: Uses the core FHIR Patient resource.
    - `Patient.name` conforms to `http://fhir.de/StructureDefinition/humanname-de-basis`
    - `Patient.address` conforms to `http://fhir.de/StructureDefinition/address-de-basis`
- **HDL Cholesterol Observation**: Uses the core FHIR Observation resource
    - Category: `laboratory`
    - Code: LOINC `2085-9` ("Cholesterol in HDL [Mass/volume] in Serum or Plasma")
    - Units: `mg/dL` (UCUM code `mg/dL`)
