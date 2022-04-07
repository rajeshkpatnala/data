# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" A Script to process USA Census PEP monthly population data
    from the datasets in provided local path.
    Typical usage:
    1. python3 preprocess.py
    2. python3 preprocess.py -i input_data
"""
import os
import re
import argparse

import numpy as np
import pandas as pd

pd.set_option("display.max_columns", None)


def _extract_year(val: str) -> tuple:
    """
    This Methods returns true,year from the value contains year.
    Otherwise false,''

    Arguments:
        val (str) : A string value contains data below format
                    yyyy or yyyy [1] or .MM 1
    Returns:
        res (tuple) : Tuple with boolean value and year value or None
    """
    val = str(val).strip().split(' ', maxsplit=1)[0]
    if val.isnumeric() and len(val) == 4:
        return True, val
    return False, None


def _return_year(col: str) -> str:
    """
    This Methods returns year value if col contains year.
    Otherwise pandas NA value.

    Arguments:
        col (str) : A string value contains data below format
                    yyyy or yyyy [1] or .MM 1
    Returns:
        res (str) : String value with year yyyy or pandas NA value
    """
    res, out = _extract_year(col)
    if res:
        return out
    return pd.NA


def _return_month(col: str) -> str:
    """
    This Methods returns month and date value if col contains month, date.
    Otherwise pandas NA value.

    Arguments:
        col (str) : A string value contains data below format
                    yyyy or yyyy [1] or .MM 1
    Returns:
        res (str) : String value with month mm or pandas NA value
    """
    res = _extract_year(col)
    if res[0]:
        return pd.NA
    return col


def _sum_cols(col: pd.Series) -> pd.Series:
    """
    This method concats two DataFrame column values
    with space in-between.

    Arguments:
        col[0] (Series) : DataFrame Column of dtype str
        col[1] (Series) : DataFrame Column of dtype str

    Returns:
        res (Series) : Concatenated DataFrame Columns
    """
    res = col[0]
    if col[1] is None:
        return res
    res = col[0] + ' ' + col[1]
    return res


def _year_range(col: pd.Series) -> str:
    """
    This method returns year range from the dataframe
    column.

    Arguments:
        col (Series) : DataFrame Column of dtype str

    Returns:
        year_range (str) : String of Concatenated max and min year values
    """
    year_range = None
    max_year = max(pd.to_datetime(col, errors='coerce').dt.year)
    min_year = min(pd.to_datetime(col, errors='coerce').dt.year)
    year_range = str(max_year) + '-' + str(min_year)
    return year_range


class CensusUSACountryPopulation:
    """
    CensusUSACountryPopulation class provides methods
    to load the data into dataframes, process, cleans
    dataframes and finally creates single cleaned csv
    file.
    Also provides methods to generate MCF and TMCF
    Files using pre-defined templates.
    """

    def __init__(self, input_files: list, csv_file_path: str,
                 mcf_file_path: str, tmcf_file_path: str) -> None:
        self.input_files = input_files
        self.cleaned_csv_file_path = csv_file_path
        self.mcf_file_path = mcf_file_path
        self.tmcf_file_path = tmcf_file_path
        self.df = None
        self.file_name = None
        self.scaling_factor = 1

    def _load_data(self, file: str) -> pd.DataFrame:
        """
        This Methods loads the data into pandas Dataframe
        using the provided file path and Returns the Dataframe.

        Arguments:
            file (str) : String of Dataset File Path
        Returns:
            df (DataFrame) : DataFrame with loaded dataset
        """
        df = None
        self.file_name = os.path.basename(file)
        if ".xls" in file:
            df = pd.read_excel(file)

        elif ".txt" in file:
            skip_rows_txt = 17
            self.file_name = self.file_name.replace(".txt", ".xlsx")
            cols = [
                "Year and Month", "Date", "Resident Population",
                "Resident Population Plus Armed Forces Overseas",
                "Civilian Population",
                "Civilian NonInstitutionalized Population"
            ]
            df = pd.read_table(file,
                               index_col=False,
                               delim_whitespace=True,
                               engine='python',
                               skiprows=skip_rows_txt,
                               names=cols)
        return df

    def _clean_txt_file(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        This method cleans the dataframe loaded from a txt file format.
        Also, Performs transformations on the data.

        Arguments:
            df (DataFrame) : DataFrame of txt dataset

        Returns:
            df (DataFrame) : Transformed DataFrame for txt dataset.
        """
        # Scaling factor for txt file : 1000
        self.scaling_factor = 1000
        df['Year and Month'] = df[['Year and Month', 'Date']].apply(_sum_cols,
                                                                    axis=1)
        df.drop(columns=['Date'], inplace=True)
        for col in df.columns:
            df[col] = df[col].str.replace(",", "")
        idx = df[df['Resident Population'] == "(census)"].index

        resident_population = 1
        resident_population_plus_armed_forces_overseas = 2
        civilian_population = 3
        civilian_noninstitutionalized_population = 4

        # Moving the row data left upto one index value.
        df.iloc[idx, resident_population] = df.iloc[idx][
            "Resident Population Plus Armed Forces Overseas"]
        df.iloc[idx, resident_population_plus_armed_forces_overseas] = df.iloc[
            idx]["Civilian Population"]
        df.iloc[idx, civilian_population] = df.iloc[idx][
            "Civilian NonInstitutionalized Population"]
        df.iloc[idx, civilian_noninstitutionalized_population] = np.NAN

        return df

    def _transform_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        This method transforms Dataframe into cleaned DF.
        Also, It Creates new columns, remove duplicates,
        Standaradize headers to SV's, Mulitply with
        scaling factor.

        Arguments:
            df (DataFrame) : DataFrame

        Returns:
            df (DataFrame) : DataFrame.
        """
        final_cols = [col for col in df.columns if 'year' not in col.lower()]

        df['Year'] = df['Year and Month'].apply(_return_year).fillna(
            method='ffill', limit=12)
        df['Month'] = df['Year and Month'].apply(_return_month)
        df.dropna(subset=['Year', 'Month'], inplace=True)

        # Creating new Date Column and Final Date format is yyyy-mm
        df['Date'] = df['Year'] + df['Month']
        df['Date'] = df['Date'].str.replace(".", "").str.replace(
            " ", "").str.replace("*", "")
        df['Date'] = pd.to_datetime(df['Date'],
                                    format='%Y%B%d',
                                    errors="coerce")
        df.dropna(subset=['Date'], inplace=True)
        df['Date'] = df['Date'].dt.strftime('%Y-%m')
        df.drop_duplicates(subset=['Date'], inplace=True)

        # Deriving new SV Count_Person_InArmedForcesOverseas as
        # subtracting Resident Population from
        # Resident Population Plus Armed Forces Overseas
        df['Count_Person_InUSArmedForcesOverseas'] = df[
            'Resident Population Plus Armed Forces Overseas'].astype(
                'int') - df['Resident Population'].astype('int')
        computed_cols = ["Date", "Count_Person_InUSArmedForcesOverseas"]

        # Selecting Coumputed and Final Columns from the DF.
        df = df[computed_cols + final_cols]

        # Renaming DF Headers with ref to SV's Naming Standards.
        final_cols_list = ["Count_Person_" + col\
                        .replace("Population ", "")\
                        .replace("Population", "")\
                        .replace(" Plus ", "Or")\
                        .replace("Armed Forces Overseas", \
                            "InUSArmedForcesOverseas")\
                        .replace("Household", \
                                "ResidesInHousehold")\
                        .replace("Resident", "USResident")\
                        .replace("Noninstitutionalized", \
                            "NonInstitutionalized")\
                        .strip()\
                        .replace(" ", "_")\
                        .replace("__", "_")\
                        for col in final_cols]

        final_cols_list = computed_cols + final_cols_list
        df.columns = final_cols_list

        # Multiplying the data with scaling factor.
        for col in final_cols_list:
            if "count" in col.lower():
                if self.scaling_factor != 1:
                    df[col] = df[col].astype(
                        'float', errors="ignore").multiply(self.scaling_factor)
                df[col] = df[col].astype('Int64', errors="ignore")
        self.scaling_factor = 1

        # Creating Location column with default value country/USA.
        # as the dataset is all about USA country level only.
        df.insert(1, "Location", "country/USA", True)
        df.insert(0, 'date_range', _year_range(df['Date']), True)
        return df

    def _transform_data(self, file: str, df: pd.DataFrame) -> None:
        """
        This method calls the required functions to transform
        the dataframe and saves the final cleaned data in
        CSV file format.

        Arguments:
            file (str) : Dataset File Path

        Returns:
            df (DataFrame) : DataFrame.
        """

        # Finding the Dir Path
        file_dir = os.path.dirname(self.cleaned_csv_file_path)
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)

        # Cleaning txt file if file is in txt format
        if ".txt" in file:
            df = self._clean_txt_file(df)

        df = self._transform_df(df)

        keep_value = "first"
        if self.df is None:
            self.df = df
        else:
            self.df = self.df.append(df, ignore_index=True)

        self.df.sort_values(by=['Date', 'date_range'],
                            ascending=False,
                            inplace=True)
        self.df.drop_duplicates("Date", keep=keep_value, inplace=True)
        self.df.drop(['date_range'], axis=1, inplace=True)
        self.df.to_csv(self.cleaned_csv_file_path, index=False)

    def process(self):
        """
        This is main method to iterate on each file,
        calls defined methods to clean, generate final
        cleaned CSV file, MCF file and TMCF file.
        """
        for file in self.input_files:
            df = self._load_data(file)
            self._transform_data(file, df)
        self._generate_mcf(self.df.columns)
        self._generate_tmcf(self.df.columns)

    def _generate_mcf(self, df_cols: list) -> None:
        """
        This method generates MCF file w.r.t
        dataframe headers and defined MCF template

        Arguments:
            df_cols (list) : List of DataFrame Columns

        Returns:
            None
        """
        mcf_template = """Node: dcid:{}
typeOf: dcs:StatisticalVariable
populationType: dcs:Person{}{}{}
statType: dcs:measuredValue
measuredProperty: dcs:count
"""
        mcf = ""
        for col in df_cols:
            residence = ""
            status = ""
            armedf = ""
            if col.lower() in ["date", "location"]:
                continue
            if re.findall('Resident', col):
                residence = "\nresidentStatus"
                status = ": dcs:USResident"
            if re.findall('ArmedForces', col):
                residence = "\nresidentStatus"
                if len(status) == 0:
                    status = ": dcs:InUSArmedForcesOverseas"
                else:
                    status = ": dcs:USResident__InUSArmedForcesOverseas"
            if re.findall('Resides', col):
                if re.findall('Household', col):
                    residence = "\nresidenceType"
                    status = ": dcs:Household"
            if re.findall('NonInstitutionalized', col):
                residence = "\ninstitutionalization"
                status = ": dcs:USC_NonInstitutionalized"
            if re.findall('Civilian', col):
                armedf = "\narmedForcesStatus: dcs:Civilian"
            if re.findall('Count_Person_InUSArmedForcesOverseas', col):
                armedf = "\narmedForcesStatus: dcs:InArmedForces"
            mcf = mcf + mcf_template.format(col, residence, status,
                                            armedf) + "\n"

        # Writing Genereated MCF to local path.
        with open(self.mcf_file_path, 'w+', encoding='utf-8') as f_out:
            f_out.write(mcf.rstrip('\n'))

    def _generate_tmcf(self, df_cols: list) -> None:
        """
        This method generates TMCF file w.r.t
        dataframe headers and defined TMCF template

        Arguments:
            df_cols (list) : List of DataFrame Columns

        Returns:
            None
        """
        tmcf_template = """Node: E:USA_Population_Count->E{}
typeOf: dcs:StatVarObservation
variableMeasured: dcs:{}
measurementMethod: dcs:{}
observationAbout: C:USA_Population_Count->Location
observationDate: C:USA_Population_Count->Date
observationPeriod: \"P1M\"
value: C:USA_Population_Count->{} 
"""
        i = 0
        measure = ""
        tmcf = ""
        for col in df_cols:
            if col.lower() in ["date", "location"]:
                continue
            if re.findall('Count_Person_InUSArmedForcesOverseas', col):
                measure = "dcAggregate/CensusPEPSurvey"
            else:
                measure = "CensusPEPSurvey"
            tmcf = tmcf + tmcf_template.format(i, col, measure, col) + "\n"
            i = i + 1

        # Writing Genereated TMCF to local path.
        with open(self.tmcf_file_path, 'w+', encoding='utf-8') as f_out:
            f_out.write(tmcf.rstrip('\n'))


if __name__ == "__main__":

    HEADER = 1
    SKIP_ROWS = 1
    SKIP_ROWS_TXT = 17

    parser = argparse.ArgumentParser()
    #Adding optional argument
    default_input_path = os.path.dirname(
        os.path.abspath(__file__)) + os.sep + "input_data"
    parser.add_argument("-i",
                        "--input_data",
                        default=default_input_path,
                        help="Json file with Dataset URLS")

    # Read arguments from command line
    args = parser.parse_args()
    input_path = args.input_data

    ip_files = os.listdir(input_path)
    ip_files = [input_path + os.sep + file for file in ip_files]

    #Defining Output file names
    data_file_path = os.path.dirname(
        os.path.abspath(__file__)) + os.sep + "output"
    cleaned_csv_path = data_file_path + os.sep + "USA_Population_Count.csv"
    mcf_path = data_file_path + os.sep + "USA_Population_Count.mcf"
    tmcf_path = data_file_path + os.sep + "USA_Population_Count.tmcf"

    #print(os.path.dirname(cleaned_csv_path))

    loader = CensusUSACountryPopulation(ip_files, cleaned_csv_path, mcf_path,
                                        tmcf_path)

    loader.process()
