import pandas as pd
from config.rules import get_theoretical_charge


class DataProcessor:
    """
    Processes data for resource summary reports.
    """

    @staticmethod
    def validate_dataframe(df, required_columns):
        """
        Validate that a DataFrame has the required columns.

        Args:
            df (pandas.DataFrame): The DataFrame to validate
            required_columns (list): List of required column names

        Returns:
            tuple: (bool, list) - Success status and list of missing columns
        """
        available_columns = df.columns.tolist()
        missing_columns = [col for col in required_columns if col not in available_columns]

        return len(missing_columns) == 0, missing_columns

    @staticmethod
    def create_connection_dict(deployments_df, column_name):
        """
        Create a lookup dictionary for a specific column by project name.

        Args:
            deployments_df (pandas.DataFrame): The deployments DataFrame
            column_name (str): The column to extract values from

        Returns:
            dict: Mapping of project names to column values
        """
        result_dict = {}

        if column_name in deployments_df.columns:
            for _, row in deployments_df.iterrows():
                project_name = row['Nom']
                if not pd.isna(row.get(column_name, pd.NA)):
                    result_dict[project_name] = row[column_name]

        return result_dict

    @staticmethod
    def calculate_charge_jh(df):
        """
        Calculate Charge JH (Soumise / 8).

        Args:
            df (pandas.DataFrame): The DataFrame with Soumise (h) column

        Returns:
            pandas.DataFrame: DataFrame with added Charge JH column
        """
        df_copy = df.copy()
        df_copy['Charge JH'] = df_copy['Soumise (h)'] / 8
        return df_copy

    @staticmethod
    def calculate_theoretical_charge(connection_level, project_phase):
        """
        Calculate the theoretical charge based on connection level and project phase.

        Args:
            connection_level (str): The connection level
            project_phase (str): The project phase

        Returns:
            float: The theoretical charge value
        """
        return get_theoretical_charge(connection_level, project_phase)

    # @staticmethod
    # def format_resource_summary(pivot_df, connection_dict, phase_dict):
    #     """
    #     Format the resource summary with hierarchical structure.
    #
    #     Args:
    #         pivot_df (pandas.DataFrame): The pivot table DataFrame
    #         connection_dict (dict): Dictionary of connection levels by project
    #         phase_dict (dict): Dictionary of project phases by project
    #
    #     Returns:
    #         pandas.DataFrame: The formatted resource summary
    #     """
    #     # Create output DataFrame with all required columns
    #     result_df = pd.DataFrame(columns=[
    #         'Resource/ PROJET', 'Charge JH', 'Somme de Charge JH',
    #         'Niveau de connexion', 'Phase du projet', 'Charge Theorique'
    #     ])
    #
    #     current_resource = None
    #     row_index = 0
    #
    #     # Sort by resource first, then by project
    #     pivot_df = pivot_df.sort_values(['Ressource', 'Projet'])
    #
    #     for _, row in pivot_df.iterrows():
    #         resource = row['Ressource']
    #         project = row['Projet']
    #         charge = row['Charge JH']
    #
    #         # If this is a new resource, add the resource row
    #         if resource != current_resource:
    #             result_df.loc[row_index, 'Resource/ PROJET'] = resource
    #             resource_charge = pivot_df[pivot_df['Ressource'] == resource]['Charge JH'].sum()
    #             result_df.loc[row_index, 'Somme de Charge JH'] = resource_charge
    #             row_index += 1
    #             current_resource = resource
    #
    #         # Look up connection level and project phase for this project
    #         connection_level = connection_dict.get(project, '')
    #         project_phase = phase_dict.get(project, '')
    #
    #         # Calculate theoretical charge if both values are available
    #         theoretical_charge = None
    #         if connection_level and project_phase:
    #             theoretical_charge = DataProcessor.calculate_theoretical_charge(connection_level, project_phase)
    #
    #         # Add the project row indented under the resource
    #         result_df.loc[row_index, 'Resource/ PROJET'] = f"    {project}"
    #         result_df.loc[row_index, 'Charge JH'] = charge
    #         result_df.loc[row_index, 'Niveau de connexion'] = connection_level
    #         result_df.loc[row_index, 'Phase du projet'] = project_phase
    #
    #         if theoretical_charge is not None:
    #             result_df.loc[row_index, 'Charge Theorique'] = theoretical_charge
    #
    #         row_index += 1
    #
    #     return result_df
    @staticmethod
    def format_resource_summary(pivot_df, connection_dict, phase_dict):
        """
        Format the resource summary with hierarchical structure.

        Args:
            pivot_df (pandas.DataFrame): The pivot table DataFrame
            connection_dict (dict): Dictionary of connection levels by project
            phase_dict (dict): Dictionary of project phases by project

        Returns:
            pandas.DataFrame: The formatted resource summary
        """
        # Create output DataFrame with all required columns
        result_df = pd.DataFrame(columns=[
            'Resource/ PROJET', 'Charge JH', 'Somme de Charge JH',
            'Niveau de connexion', 'Phase du projet', 'Charge Theorique', 'Ecart'
        ])

        current_resource = None
        row_index = 0

        # Sort by resource first, then by project
        pivot_df = pivot_df.sort_values(['Ressource', 'Projet'])

        for _, row in pivot_df.iterrows():
            resource = row['Ressource']
            project = row['Projet']
            charge = row['Charge JH']

            # If this is a new resource, add the resource row
            if resource != current_resource:
                result_df.loc[row_index, 'Resource/ PROJET'] = resource
                resource_charge = pivot_df[pivot_df['Ressource'] == resource]['Charge JH'].sum()
                result_df.loc[row_index, 'Somme de Charge JH'] = resource_charge
                row_index += 1
                current_resource = resource

            # Look up connection level and project phase for this project
            connection_level = connection_dict.get(project, '')
            project_phase = phase_dict.get(project, '')

            # Calculate theoretical charge if both values are available
            theoretical_charge = None
            if connection_level and project_phase:
                theoretical_charge = DataProcessor.calculate_theoretical_charge(connection_level, project_phase)

            # Add the project row indented under the resource
            result_df.loc[row_index, 'Resource/ PROJET'] = f"    {project}"
            result_df.loc[row_index, 'Charge JH'] = charge
            result_df.loc[row_index, 'Niveau de connexion'] = connection_level
            result_df.loc[row_index, 'Phase du projet'] = project_phase

            if theoretical_charge is not None:
                result_df.loc[row_index, 'Charge Theorique'] = theoretical_charge
                # Calculate Ecart (Charge Theorique - Charge JH)
                result_df.loc[row_index, 'Ecart'] = theoretical_charge - charge

            row_index += 1

        return result_df