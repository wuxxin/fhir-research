import unittest
from fhir.resources.bundle import Bundle
from fhir.resources.patient import Patient
from fhir.resources.observation import Observation

from src.fhir_research.examples import fhir_bundle_german_lab_example

class TestExamples(unittest.TestCase):

    def test_fhir_bundle_german_lab_example_structure(self):
        """Test the basic structure and patient details of the German lab example bundle."""
        bundle = fhir_bundle_german_lab_example()

        self.assertIsInstance(bundle, Bundle)
        self.assertEqual(bundle.type, "collection")
        self.assertIsNotNone(bundle.entry)
        self.assertTrue(len(bundle.entry) > 0) # Should have patient + observations

        patient_entries = [e for e in bundle.entry if e.resource and e.resource.get_resource_type() == "Patient"]
        self.assertEqual(len(patient_entries), 1)

        patient_resource = patient_entries[0].resource
        self.assertIsInstance(patient_resource, Patient)
        self.assertEqual(patient_resource.id, "patient-example-02")

        self.assertTrue(len(patient_resource.name) > 0)
        self.assertEqual(patient_resource.name[0].family, "Schmidt")
        self.assertEqual(patient_resource.name[0].given[0], "Hans")
        self.assertEqual(str(patient_resource.birthDate), "1978-05-15")
        self.assertEqual(patient_resource.gender, "male")

    def test_fhir_bundle_german_lab_example_observations(self):
        """Test the presence and content of observations in the German lab example bundle."""
        bundle = fhir_bundle_german_lab_example()

        observations = [e.resource for e in bundle.entry if e.resource and e.resource.get_resource_type() == "Observation"]
        self.assertEqual(len(observations), 25) # 7 + 6 + 6 + 6 = 25 observations

        # Define expected LOINC codes for each set
        # Set 1: All 7 parameters
        loincs_set1 = ["2324-2", "1558-6", "2093-3", "2085-9", "2089-1", "9830-1", "2571-8"]
        # Set 2: Triglyceride ("2571-8") missing (6 parameters)
        loincs_set2 = ["2324-2", "1558-6", "2093-3", "2085-9", "2089-1", "9830-1"]
        # Set 3: LDL-Cholesterin ("2089-1") missing (6 parameters)
        loincs_set3 = ["2324-2", "1558-6", "2093-3", "2085-9", "9830-1", "2571-8"]
        # Set 4: Gamma-GT ("2324-2") missing (6 parameters)
        loincs_set4 = ["1558-6", "2093-3", "2085-9", "2089-1", "9830-1", "2571-8"]

        # Group observations by effectiveDateTime to distinguish sets
        observations_by_date = {}
        for obs in observations:
            self.assertIsInstance(obs, Observation)
            date_str = str(obs.effectiveDateTime.date()) # Use date part for grouping
            if date_str not in observations_by_date:
                observations_by_date[date_str] = []
            observations_by_date[date_str].append(obs)

        self.assertIn("2022-05-20", observations_by_date)
        self.assertIn("2023-08-10", observations_by_date)
        self.assertIn("2024-01-15", observations_by_date)
        self.assertIn("2024-07-20", observations_by_date)

        # Check observations for Set 1 ("2022-05-20")
        obs_set1_list = observations_by_date["2022-05-20"]
        self.assertEqual(len(obs_set1_list), len(loincs_set1))
        present_loincs_s1 = [obs.code.coding[0].code for obs in obs_set1_list]
        for loinc in loincs_set1:
            self.assertIn(loinc, present_loincs_s1)

        # Check observations for Set 2 ("2023-08-10")
        obs_set2_list = observations_by_date["2023-08-10"]
        self.assertEqual(len(obs_set2_list), len(loincs_set2))
        present_loincs_s2 = [obs.code.coding[0].code for obs in obs_set2_list]
        for loinc in loincs_set2:
            self.assertIn(loinc, present_loincs_s2)
        self.assertNotIn("2571-8", present_loincs_s2) # Triglyceride missing

        # Check observations for Set 3 ("2024-01-15")
        obs_set3_list = observations_by_date["2024-01-15"]
        self.assertEqual(len(obs_set3_list), len(loincs_set3))
        present_loincs_s3 = [obs.code.coding[0].code for obs in obs_set3_list]
        for loinc in loincs_set3:
            self.assertIn(loinc, present_loincs_s3)
        self.assertNotIn("2089-1", present_loincs_s3) # LDL-Cholesterin missing

        # Check observations for Set 4 ("2024-07-20")
        obs_set4_list = observations_by_date["2024-07-20"]
        self.assertEqual(len(obs_set4_list), len(loincs_set4))
        present_loincs_s4 = [obs.code.coding[0].code for obs in obs_set4_list]
        for loinc in loincs_set4:
            self.assertIn(loinc, present_loincs_s4)
        self.assertNotIn("2324-2", present_loincs_s4) # Gamma-GT missing

        # Check some observation details (e.g. first observation for Schmidt from set 1)
        schmidt_obs1 = next((obs for obs in obs_set1_list if obs.id == "obs-schmidt-01"), None)
        self.assertIsNotNone(schmidt_obs1)
        self.assertEqual(schmidt_obs1.code.coding[0].code, "2324-2") # Gamma-GT
        self.assertEqual(schmidt_obs1.valueQuantity.value, 45.0)
        self.assertEqual(schmidt_obs1.valueQuantity.unit, "U/L")


if __name__ == '__main__':
    unittest.main()
