import pandas as pd


def generate_new_df_with_transformed_column(df: pd.DataFrame, column_name: str, transformation):
    """
    Generate a new DataFrame with a transformed column.

    This function takes a pandas DataFrame, applies a specified transformation
    to a specified column, and returns a new DataFrame containing the transformed
    column alongside all other original columns, excluding the specified column.

    Args:
        df: original dataframe
        column_name: name of the column to transform
        transformation: function that transforms specified column

    Returns:
        a new dataframe with transformed column
    """
    df_column_transformed = df[column_name].apply(transformation)
    df_transformed = pd.concat(
        [df_column_transformed.rename(column_name), df.drop(columns=[column_name])], axis=1)
    return df_transformed
