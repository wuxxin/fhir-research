import unittest
import pandas as pd
from src.fhir_research.utils import filter_fhir_dataframe

class TestUtils(unittest.TestCase):

    def setUp(self):
        # Sample DataFrame mimicking structure from flatten_fhir_bundle
        data = {
            'id': ['obs1', 'obs2', 'obs3', 'obs4', 'obs5', 'obs6'],
            'effectiveDateTime': pd.to_datetime([
                '2023-01-01T10:00:00Z',
                '2023-01-01T10:05:00Z',
                '2023-01-02T11:00:00Z',
                '2023-01-02T11:05:00Z',
                '2023-01-03T12:00:00Z',
                '2023-01-03T12:05:00Z'
            ]),
            'code_coding_0_code': ['CODE1', 'CODE2', 'CODE1', 'CODE3', 'CODE2', 'CODE4'],
            'code_coding_0_display': ['Display1', 'Display2', 'Display1', 'Display3', 'Display2', 'Display4'],
            'valueQuantity_value': [10.0, 20.0, 12.0, 30.0, 22.0, 40.0],
            'valueQuantity_unit': ['mg/dL', 'mg/dL', 'mg/dL', 'U/L', 'mg/dL', 'U/L']
        }
        self.sample_df = pd.DataFrame(data)
        # Ensure effectiveDateTime is timezone-aware, matching typical FHIR output
        if not self.sample_df['effectiveDateTime'].dt.tz:
             self.sample_df['effectiveDateTime'] = self.sample_df['effectiveDateTime'].dt.tz_localize('UTC')


    def test_filter_fhir_dataframe_multiple_codes(self):
        """Test filtering with a list of codes."""
        filtered_df = filter_fhir_dataframe(
            self.sample_df,
            column_name="code_coding_0_code",
            codes=["CODE1", "CODE3"]
        )
        self.assertEqual(len(filtered_df), 3)
        self.assertTrue(all(filtered_df["code_coding_0_code"].isin(["CODE1", "CODE3"])))

        # Test that date and value columns are correctly processed (simple check)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(filtered_df['effectiveDateTime']))
        self.assertTrue(pd.api.types.is_numeric_dtype(filtered_df['valueQuantity_value']))


    def test_filter_fhir_dataframe_empty_codes_list(self):
        """Test filtering with an empty list of codes."""
        filtered_df = filter_fhir_dataframe(
            self.sample_df,
            column_name="code_coding_0_code",
            codes=[]
        )
        self.assertTrue(filtered_df.equals(self.sample_df))
        # Should be a copy
        self.assertNotEqual(id(filtered_df), id(self.sample_df))

    def test_filter_fhir_dataframe_none_codes(self):
        """Test filtering with codes=None."""
        filtered_df = filter_fhir_dataframe(
            self.sample_df,
            column_name="code_coding_0_code",
            codes=None
        )
        self.assertTrue(filtered_df.equals(self.sample_df))
        self.assertNotEqual(id(filtered_df), id(self.sample_df))

    def test_filter_fhir_dataframe_empty_column_name(self):
        """Test filtering with an empty column_name."""
        filtered_df = filter_fhir_dataframe(
            self.sample_df,
            column_name="",
            codes=["CODE1"]
        )
        self.assertTrue(filtered_df.equals(self.sample_df))
        self.assertNotEqual(id(filtered_df), id(self.sample_df))

    def test_filter_fhir_dataframe_non_existent_column(self):
        """Test filtering with a non-existent column name."""
        # According to current implementation, it prints a warning and returns a copy.
        filtered_df = filter_fhir_dataframe(
            self.sample_df,
            column_name="non_existent_column",
            codes=["CODE1"]
        )
        self.assertTrue(filtered_df.equals(self.sample_df))
        self.assertNotEqual(id(filtered_df), id(self.sample_df))

    def test_filter_fhir_dataframe_empty_input_df(self):
        """Test filtering with an empty input DataFrame."""
        empty_df = pd.DataFrame()
        filtered_df = filter_fhir_dataframe(
            empty_df,
            column_name="code_coding_0_code",
            codes=["CODE1"]
        )
        self.assertTrue(filtered_df.empty)

    def test_filter_fhir_dataframe_input_df_none(self):
        """Test filtering with None as input DataFrame."""
        filtered_df = filter_fhir_dataframe(
            None, # type: ignore
            column_name="code_coding_0_code",
            codes=["CODE1"]
        )
        self.assertTrue(filtered_df.empty)

    def test_filter_no_matching_codes(self):
        """Test filtering with codes that don't exist in the DataFrame."""
        filtered_df = filter_fhir_dataframe(
            self.sample_df,
            column_name="code_coding_0_code",
            codes=["NON_EXISTENT_CODE1", "NON_EXISTENT_CODE2"]
        )
        self.assertTrue(filtered_df.empty)
        self.assertEqual(len(filtered_df), 0)

if __name__ == '__main__':
    unittest.main()
