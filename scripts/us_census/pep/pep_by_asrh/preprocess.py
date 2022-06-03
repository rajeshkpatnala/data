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
"""
This Python Script Load the datasets, cleans it
and generates cleaned csv, MCF, TMCF file.
"""
import os

from copy import deepcopy
import pandas as pd

from absl import app
from absl import flags
from cols_map import _get_mapper_cols_dict

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

FLAGS = flags.FLAGS
default_input_path = os.path.dirname(
    os.path.abspath(__file__)) + os.sep + "input_data"
flags.DEFINE_string("input_path", default_input_path, "Import Data File's List")


def _convert_to_int(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        df[col] = df[col].astype("int", errors='ignore')
    return df


def _derive_cols(df: pd.DataFrame, derived_cols: dict) -> pd.DataFrame:
    """Derive new columns using DataFrame and derived_cols dict
    Args:
        df (pd.DataFrame): Input DataFrame loaded with data.
        derived_cols (dict): derived_cols dict
       where key represents dervied col and values represents existing columns.

    Returns:
        pd.DataFrame: DataFrame
    """
    for dsv, sv in derived_cols.items():
        df[dsv] = df.loc[:, sv].apply(pd.to_numeric,
                                      errors='coerce').sum(axis=1)
    return df


def _get_age_grp(age_grp: enumerate) -> str:
    """
    Returns Age Groups using age_grp index as below.
    0: ""
    1: 0To4
    2: 5To9
    3: 10To14
    ...
    ...
    18: 85
    Args:
        age_grp (int): Age Group Bucket Index

    Returns:
        str: Age Bucket Value
    """
    if age_grp == 0:
        return ""
    if age_grp == 18:
        return "85OrMore"
    start = 5 * (age_grp - 1)
    end = 5 * (age_grp) - 1
    return f"{start}To{end}"


def _get_age_grp_county_2000_2009(age_grp: enumerate) -> str:
    """
    Returns Age Groups using age_grp index as below,
    applies for country between years 2000 to 2009.
    0: "0"
    1: 1To4
    2: 5To9
    3: 10To14
    ...
    ...
    18: 85To89
    Args:
        age_grp (int): Age Group Bucket Index

    Returns:
        str: Age Bucket Value
    """
    if age_grp == 0:
        return "0"
    if age_grp == 1:
        return "1To4"
    if age_grp == 18:
        return "85OrMore"
    start = 5 * (age_grp - 1)
    end = 5 * (age_grp) - 1
    return f"{start}To{end}"


def _add_measurement_method(df: pd.DataFrame, src_col: str,
                            tgt_col: str) -> pd.DataFrame:
    """Adds Measurement Method either CensusPEPSurvey or
    dcAggregate/CensusPEPSurvey to tgt_col column.
    Args:
        df (pd.DataFrame): Input DataFrame
        src_col (str): SV Column Name
        tgt_col (str): Measurement Method Column

    Returns:
        pd.DataFrame: DataFrame with New Columns
    """
    df[tgt_col] = df[src_col].str.split("_").str[-1]
    df[tgt_col] = df[tgt_col].str.replace(r"^(?!computed).*",
                                          "dcs:CensusPEPSurvey",
                                          regex=True)
    df[tgt_col] = df[tgt_col].str.replace('computed',
                                          "dcs:dcAggregate/CensusPEPSurvey",
                                          regex=False)

    # Dervied SV's has '_computed' as part of the name,
    # to differentiate them with source generated SV's
    # Removing '_computed' in the SV's names.
    df[src_col] = df[src_col].str.replace("_computed", "")
    return df


def _load_df(path: str,
             file_format: str,
             header: str = None,
             skip_rows: int = None,
             encoding: str = "UTF-8") -> pd.DataFrame:
    """
    Returns the DataFrame using input path and config.
    Args:
        path (str): Input File Path
        file_format (str): Input File Format [csv, txt, xls, xlsx]
        header (str, optional): Input Dataset Header Row Line Number.
        DataFrame will consider header value and make it as header.
        Defaults to None.
        skip_rows (int, optional): Skip Rows Value for txt files.
        This is helpful to skip initial rows in txt file.Defaults to None.
        encoding (str, optional): Input File Encoding while
        loading data into DataFrame.Defaults to None.

    Returns:
        df (pd.DataFrame): Dataframe of input file
    """
    df = None
    if file_format.lower() == "csv":
        df = pd.read_csv(path, header=header, encoding=encoding)
    elif file_format.lower() == "txt":
        df = pd.read_table(path,
                           index_col=False,
                           delim_whitespace=True,
                           engine='python',
                           header=header,
                           skiprows=skip_rows,
                           encoding=encoding)
    elif file_format.lower() in ["xls", "xlsx"]:
        df = pd.read_excel(path, header=header)
    df = _convert_to_int(df)
    return df


def _unpivot_df(df: pd.DataFrame,
                id_col: list,
                data_cols: list,
                default_col="SV") -> pd.DataFrame:
    """
    Unpivot a DataFrame from wide to long format

    Before Transpose,

    df:
    Year    Location   HispaicOrLatino_Male  HispaicOrLatino_Female
    1999    geoId/01   14890                  15678
    1999    geoId/02   13452                  11980

    id_col: ["Year", "Location"]
    data_cols: ["HispaicOrLatino_Male", "HispaicOrLatino_Female"]
    default_col: "SV"

    Result df:
    Year    Location   SV                       Count_Person
    1999    geoId/01   HispaicOrLatino_Male     14890
    1999    geoId/02   HispaicOrLatino_Male     13452
    1999    geoId/01   HispaicOrLatino_Female   15678
    1999    geoId/02   HispaicOrLatino_Female   11980

    Args:
        df (pd.DataFrame): Dataframe with cleaned data
        common_col (list): Dataframe Column list
        data_cols (list): Dataframe Column list

    Returns:
        pd.DataFrame: Dataframe
    """
    res_df = pd.DataFrame()
    res_df = pd.melt(df,
                     id_vars=id_col,
                     value_vars=data_cols,
                     var_name=default_col,
                     value_name='Count_Person')
    # for col in data_cols:
    #     cols = common_col + [col]  # col have the population data,
    #     tmp_df = df[cols]
    #     # Renaming Col value with 'Count_Person' to
    #     # align with DataCommons Standarads
    #     tmp_df.columns = common_col + ["Count_Person"]
    #     tmp_df[default_col] = col
    #     res_df = pd.concat([res_df, tmp_df])
    return res_df


def _create_sv(desc: str, age: str) -> str:
    # Age 85 and 100
    if age in {100, 85}:
        return f"Count_Person_{age}OrMoreYears_{desc}"
    return f"Count_Person_{age}Years_{desc}"


def _process_nationals_1980_1989(file_path: str) -> pd.DataFrame:
    """
    Returns the Cleaned DataFrame consists
    national data for the year 1980-1989.

    Args:
        file_path (str): Input File Path

    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    data_df = _load_df(file_path, "txt", header=None, skip_rows=1)
    # Extracting Year from the file name and adding '7' to it
    # to filter the dataframe as it provides
    # population estimates for april(4) and july(7) month.
    yr = '7' + os.path.basename(file_path)[1:3]
    # col at index 1 in DataFrame contains date values, example as below
    # 488, 488100,788,788100 where 4 or 7 represents month, 88 represents year,
    # 100 represents age.
    yr_100 = yr + '100'
    yr, yr_100 = int(yr), int(yr_100)
    # Age is at index 2 column, but for age 100, it is present in index 1
    # column as 788100, so filtering that row separately
    # and loading it to another DataFrame yr_100_df
    yr_100_df = data_df[data_df[1] == yr_100].iloc[:, 1:].reset_index(drop=True)
    data_df = data_df[data_df[1] == yr].iloc[:, 1:].reset_index(drop=True)
    cols = [
        "Year", "Age", "Total_Population", "Total_Male_Population",
        "Total_Female_Population", "Male_WhiteAlone_Population",
        "Female_WhiteAlone_Population",
        "Male_BlackOrAfricanAmericanAlone_Population",
        "Female_BlackOrAfricanAmericanAlone_Population",
        "Male_AmericanIndianAndAlaskaNativeAlone",
        "Female_AmericanIndianAndAlaskaNativeAlone",
        "Male_AsianOrPacificIslander", "Female_AsianOrPacificIslander",
        "Male_HispanicOrLatino", "Female_HispanicOrLatino",
        "Male_WhiteAloneNotHispanicOrLatino",
        "Female_WhiteAloneNotHispanicOrLatino",
        "Male_NotHispanicOrLatino_BlackOrAfricanAmericanAlone",
        "Female_NotHispanicOrLatino_BlackOrAfricanAmericanAlone",
        "Male_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_NotHispanicOrLatino_AsianOrPacificIslander",
        "Female_NotHispanicOrLatino_AsianOrPacificIslander"
    ]
    hispanic_cols = _get_mapper_cols_dict("nationals_1980_1999_hispanic")
    derived_cols = _get_mapper_cols_dict("nationals_1980_1999_derived")
    data_df.columns = cols
    # Appending yr_100_df to
    if yr_100_df.shape[0] > 0:
        yr_100_df.insert(0, 0, yr)
        yr_100_df[1] = 100
        yr_100_df = yr_100_df.drop(columns=[23])
        yr_100_df.columns = cols
        data_df = pd.concat([data_df, yr_100_df]).reset_index(drop=True)
    # Type casting dataframe values to int.
    data_df = _convert_to_int(data_df)
    # Creating Year Column
    data_df["Year"] = "19" + data_df["Year"].astype('str').str[-2:]
    # Deriving Columns for HispanicOrLatino Origin
    for dsv, sv in hispanic_cols.items():
        data_df[sv[1:]] = -data_df[sv[1:]]
        data_df[dsv] = data_df.loc[:, sv].sum(axis=1)
        data_df[sv[1:]] = -data_df[sv[1:]]
        cols.append(dsv)
    # Deriving New Columns
    data_df = _derive_cols(data_df, derived_cols)
    cols = cols + list(derived_cols.keys())
    f_cols = [val for val in cols if "Hispanic" in val]
    data_df = _unpivot_df(data_df, ["Year", "Age"], f_cols)
    # Creating SV's name using SV, Age Column
    data_df["SV"] = data_df.apply(lambda row: _create_sv(row.SV, row.Age),
                                  axis=1)
    data_df["SV"] = data_df["SV"].str.replace("85OrMore", "85")
    data_df["Location"] = "country/USA"
    final_cols = [
        "Year", "Location", "SV", "Measurement_Method", "Count_Person"
    ]
    # Deriving Measurement Method for the SV's
    data_df = _add_measurement_method(data_df, "SV", "Measurement_Method")
    return data_df[final_cols]


def _process_state_1990_1999(file_path):
    """
    Returns the Cleaned DataFrame consists
    state data for the year 1990-1999.

    Args:
        file_path (str): Input File Path

    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    df = _load_df(file_path, "txt", header=None, skip_rows=15)
    cols = [
        "Year", "Location", "Age", "Male_WhiteAloneNotHispanicOrLatino",
        "Female_WhiteAloneNotHispanicOrLatino",
        "Male_NotHispanicOrLatino_BlackOrAfricanAmericanAlone",
        "Female_NotHispanicOrLatino_BlackOrAfricanAmericanAlone",
        "Male_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_NotHispanicOrLatino_AsianOrPacificIslander",
        "Female_NotHispanicOrLatino_AsianOrPacificIslander",
        "Male_HispanicOrLatino_WhiteAlone",
        "Female_HispanicOrLatino_WhiteAlone",
        "Male_HispanicOrLatino_BlackOrAfricanAmericanAlone",
        "Female_HispanicOrLatino_BlackOrAfricanAmericanAlone",
        "Male_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_HispanicOrLatino_AsianOrPacificIslander",
        "Female_HispanicOrLatino_AsianOrPacificIslander"
    ]
    df.columns = cols
    derived_cols = _get_mapper_cols_dict("state_1990_1999")
    # Deriving New Columns
    df = _derive_cols(df, derived_cols)

    cols = cols + list(derived_cols.keys())
    # Adding Leading Zeros for State's Fips Code.
    df["Location"] = df["Location"].astype('str').str.pad(width=2,
                                                          side="left",
                                                          fillchar="0")
    # Creating GeoId's using Fips Code
    df["Location"] = "geoId/" + df["Location"]
    f_cols = [val for val in cols if "Hispanic" in val]
    df = _unpivot_df(df, ["Year", "Location", "Age"], f_cols)
    df["SV"] = df.apply(lambda row: _create_sv(row.SV, row.Age), axis=1)
    final_cols = [
        "Year", "Location", "SV", "Measurement_Method", "Count_Person"
    ]
    df = df.reset_index(drop=True)
    # Deriving Measurement Method for the SV's
    df = _add_measurement_method(df, "SV", "Measurement_Method")
    return df[final_cols]


def _process_nationals_2000_2009(file_path: str) -> pd.DataFrame:
    """
    Returns the Cleaned DataFrame consists
    nationals data for the year 2000-2009.

    Args:
        file_path (str): Input File Path

    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    df = _load_df(file_path, "csv", header=0)
    # Considering Month = 7(July) and Skipping Age:999(Total Age)
    # Skipping Year: 2010
    df = df[(df["MONTH"] == 7) & (df["AGE"] != 999) &
            (df["YEAR"] != 2010)].reset_index(drop=True)
    cols = list(df.columns)
    # Mapping Dataset Headers to its FullForm
    cols_dict = _get_mapper_cols_dict("header_mappers")
    for idx, val in enumerate(cols):
        cols[idx] = cols_dict.get(val, val)
    df.columns = cols
    derived_cols = _get_mapper_cols_dict("nationals_2000_2009")
    # Deriving New Columns
    df = _derive_cols(df, derived_cols)
    cols = cols + list(derived_cols.keys())
    f_cols = [val for val in cols if "Hispanic" in val]
    df = _unpivot_df(df, ["Year", "Age"], f_cols)
    # Creating SV's name using SV, Age Columns
    df["SV"] = df.apply(lambda row: _create_sv(row.SV, row.Age), axis=1)
    df["Location"] = "country/USA"
    final_cols = [
        "Year", "Location", "SV", "Measurement_Method", "Count_Person"
    ]
    df = df.reset_index(drop=True)
    # Deriving Measurement Method for the SV's
    df = _add_measurement_method(df, "SV", "Measurement_Method")
    return df[final_cols]


def _process_state_2010_2020(file_path: str) -> pd.DataFrame:
    """
    Returns the Cleaned DataFrame consists
    state data for the year 2010-2020.

    Args:
        file_path (str): Input File Path

    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    df = _load_df(file_path, "csv", header=0)
    # SKipping Sex: 0, Origin: 0 which represents Total Count
    df = df[(df["SEX"] != 0) & (df["ORIGIN"] != 0)].reset_index(drop=True)

    # Creating GeoId's for State FIPS Code
    df["STATE"] = "geoId/" + df["STATE"].astype("str").str.pad(
        width=2, side="left", fillchar="0")
    gender_dict = {1: "Male", 2: "Female"}
    origin_dict = {1: "NotHispanicOrLatino", 2: "HispanicOrLatino"}
    race_dict = {
        1: "WhiteAlone",
        2: "BlackOrAfricanAmericanAlone",
        3: "AmericanIndianAndAlaskaNativeAlone",
        4: "AsianAlone",
        5: "NativeHawaiianAndOtherPacificIslanderAlone",
        6: "TwoOrMoreRaces"
    }
    df["SEX"] = df["SEX"].map(gender_dict)
    df["ORIGIN"] = df["ORIGIN"].map(origin_dict)
    df["RACE"] = df["RACE"].map(race_dict)
    df["SV"] = df["SEX"] + '_' + df["ORIGIN"] + '_' + df["RACE"]
    df["SV"] = df["SV"].str.replace("NotHispanicOrLatino_WhiteAlone",
                                    "WhiteAloneNotHispanicOrLatino")
    req_cols = list(df.columns)
    req_cols = [req_cols[3]] + [req_cols[-1]] + [
        req_cols[8]
    ] + req_cols[11:21] + [req_cols[-2]]
    pop_cols = [val for val in req_cols if "POPESTIMATE" in val]
    # Deriving New Columns
    df[pop_cols] = df[pop_cols].apply(pd.to_numeric, errors='coerce')
    derived_cols = _get_mapper_cols_dict("state_2010_2020_hispanic")
    for dsv, sv in derived_cols.items():
        tmp_derived_cols_df = df[df["SV"].isin(sv)][req_cols].reset_index(
            drop=True)
        tmp_derived_cols_df['SV'] = dsv
        tmp_derived_cols_df = tmp_derived_cols_df.groupby(
            ['STATE', 'SV', 'AGE']).sum().reset_index()
        df = df.append(tmp_derived_cols_df)
    # Deriving New Columns
    derived_cols = _get_mapper_cols_dict("state_2010_2020_total")
    for dsv, sv in derived_cols.items():
        tmp_derived_cols_df = df[df["SV"].isin(sv)][req_cols].reset_index(
            drop=True)
        tmp_derived_cols_df['SV'] = dsv
        tmp_derived_cols_df = tmp_derived_cols_df.groupby(
            ['STATE', 'SV', 'AGE']).sum().reset_index()
        df = df.append(tmp_derived_cols_df)
    # Creating SV's name using SV, Age Column

    df["SV"] = df.apply(lambda row: _create_sv(row.SV, row.AGE), axis=1)
    df = df[req_cols]
    req_cols = [
        col.replace("POPESTIMATE", "").replace("STATE", "Location")
        for col in req_cols
    ]
    df.columns = req_cols
    df = _unpivot_df(df, req_cols[:2], req_cols[3:], default_col="Year")
    f_cols = ["Year", "Location", "SV", "Measurement_Method", "Count_Person"]
    df["Count_Person"] = df["Count_Person"].astype("int")
    # Deriving Measurement Method for the SV's
    df = _add_measurement_method(df, "SV", "Measurement_Method")
    return df[f_cols]


def _process_nationals_2010_2021(file_path: str) -> pd.DataFrame:
    """
    Returns the Cleaned DataFrame consists
    natioanls data for the year 2010-2021.

    Args:
        file_path (str): Input File Path

    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    df = _load_df(file_path, "csv", header=0)
    # Considering Month = 7(July) and Skipping Age:999(Total Age)
    df = df[(df["AGE"] != 999) & (df["MONTH"] == 7)].reset_index(drop=True)
    cols_dict = _get_mapper_cols_dict("header_mappers")
    df.columns = df.columns.map(cols_dict)
    cols = df.columns.to_list()
    derived_cols = _get_mapper_cols_dict("nationals_2010_2021")
    # Deriving New Columns
    df = _derive_cols(df, derived_cols)
    cols = cols + list(derived_cols.keys())
    cols = ["Year", "Age"] + [col for col in cols if "Hispanic" in col]
    df = df[cols]
    df = _unpivot_df(df, ["Year", "Age"], cols[2:])
    # Creating SV's name using SV, Age Column
    df["SV"] = df.apply(lambda row: _create_sv(row.SV, row.Age), axis=1)
    df["SV"] = df["SV"].str.replace("85OrMore", "85")
    df["Location"] = "country/USA"
    df = df.drop(columns=["Age"])
    final_cols = [
        "Year", "Location", "SV", "Measurement_Method", "Count_Person"
    ]
    # Deriving Measurement Method for the SV's
    df = _add_measurement_method(df, "SV", "Measurement_Method")
    return df[final_cols]


def _process_state_1980_1989(file_path: str) -> str:
    """
    Returns the Cleaned DataFrame consists
    state data for the year 1980-1989.

    Args:
        file_path (str): Input File Path

    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    df = _load_df(file_path, "txt", header=None)
    df[0] = df[0].astype('str').str.pad(width=5, side="left", fillchar="0")
    start, end = 0, 4
    pop_cols = []
    while True:
        age = f"{start}To{end}"
        if start == 85:
            pop_cols.append("85OrMore")
            break
        pop_cols.append(age)
        start += 5
        end += 5
    df.columns = [0] + pop_cols
    # Creating GeoId's for State FIPS Code
    # Sample df[0]: 06212
    # df[0]: geoId(0,1)_Year(2)_Race(3)_Sex(4)
    df["Location"] = "geoId/" + df[0].str[:2]
    df["Year"] = "198" + df[0].str[2]
    df["Race"] = df[0].str[3]
    df["Sex"] = df[0].str[4]
    gender_dict = {'1': "Male", '2': "Female"}
    race_dict = {
        '1': "WhiteAloneNotHispanicOrLatino",
        '2': "NotHispanicOrLatino_BlackOrAfricanAmericanAlone",
        '3': "NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        '4': "NotHispanicOrLatino_AsianOrPacificIslander",
        '5': "HispanicOrLatino_WhiteAlone",
        '6': "HispanicOrLatino_BlackOrAfricanAmericanAlone",
        '7': "HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        '8': "HispanicOrLatino_AsianOrPacificIslander",
    }
    df["Race"] = df["Race"].map(race_dict)
    df["Sex"] = df["Sex"].map(gender_dict)
    df = df.drop(columns=[0])
    df["SV"] = df["Sex"] + "_" + df["Race"]
    # Deriving New Columns
    df[pop_cols] = df[pop_cols].apply(pd.to_numeric, errors='coerce')
    derived_cols = _get_mapper_cols_dict("state_1980_1989")
    df = df[["Year", "Location", "SV"] + pop_cols]
    for dsv, sv in derived_cols.items():
        tmp_derived_cols_df = df[df["SV"].isin(sv)].reset_index(drop=True)
        tmp_derived_cols_df['SV'] = dsv
        tmp_derived_cols_df = tmp_derived_cols_df.groupby(
            ['Year', 'Location', 'SV']).sum().reset_index()
        df = df.append(tmp_derived_cols_df)
    df = _unpivot_df(df, ["Year", "Location", "SV"],
                     pop_cols,
                     default_col="Age")
    # Creating SV's name using SV, Age Column
    df["SV"] = df.apply(lambda row: _create_sv(row.SV, row.Age), axis=1)
    # Deriving Measurement Method for the SV's
    df = _add_measurement_method(df, "SV", "Measurement_Method")
    df = df[["Year", "Location", "SV", "Measurement_Method", "Count_Person"]]
    return df


def _process_state_2000_2010(file_path: str) -> pd.DataFrame:
    """
    Returns the Cleaned DataFrame consists
    state data for the year 2000-2010.

    Args:
        file_path (str): Input File Path

    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    df = _load_df(file_path, "csv", header=0)
    df = df.drop(columns=["POPESTIMATE2010"])
    df = df[(df["STATE"] != 0)].reset_index(drop=True)
    df = df.reset_index()
    derived_cols_df = pd.DataFrame()
    gender_dict = {0: "empty", 1: "Male", 2: "Female"}
    origin_dict = {1: "NotHispanicOrLatino", 2: "HispanicOrLatino"}
    race_dict = {
        0: "empty",
        1: "WhiteAlone",
        2: "BlackOrAfricanAmericanAlone",
        3: "AmericanIndianAndAlaskaNativeAlone",
        4: "AsianAlone",
        5: "NativeHawaiianAndOtherPacificIslanderAlone",
        6: "TwoOrMoreRaces"
    }
    # Deriving New Columns
    for origin in [1, 2]:
        derived_cols_df = pd.concat([
            derived_cols_df, df[(df["ORIGIN"] == origin) & (df["SEX"] == 0) &
                                (df["RACE"] == 0) & (df["AGEGRP"] != 0)]
        ],
                                    ignore_index=True)
        for sex in [0, 1, 2]:
            if sex == 0:
                for race in [1, 2, 3, 4, 5, 6]:
                    derived_cols_df = pd.concat([
                        derived_cols_df,
                        df[(df["ORIGIN"] == origin) & (df["SEX"] == 0) &
                           (df["RACE"] == race) & (df["AGEGRP"] != 0)]
                    ],
                                                ignore_index=True)
            else:
                derived_cols_df = pd.concat([
                    derived_cols_df, df[(df["ORIGIN"] == origin) &
                                        (df["SEX"] == sex) & (df["RACE"] == 0) &
                                        (df["AGEGRP"] != 0)]
                ],
                                            ignore_index=True)
    df = df[(df["SEX"] != 0) & (df["RACE"] != 0) & (df["ORIGIN"] != 0) &
            (df["AGEGRP"] != 0)].reset_index(drop=True)
    df = pd.concat([df, derived_cols_df], ignore_index=True)
    df["RACE"] = df["RACE"].map(race_dict)
    df["ORIGIN"] = df["ORIGIN"].map(origin_dict)
    df["SEX"] = df["SEX"].map(gender_dict)
    df["SV"] = df["SEX"] + "_" + df["ORIGIN"] + "_" + df["RACE"]
    df["SV"] = df["SV"].str.replace("NotHispanicOrLatino_WhiteAlone",
                                    "WhiteAloneNotHispanicOrLatino")
    df["SV"] = df["SV"].str.replace("empty_", "").str.replace("_empty", "")
    df["Location"] = "geoId/" + df["STATE"].astype('str').str.pad(
        width=2, side="left", fillchar="0")
    cols = df.columns.to_list()
    # Creating Age Groups
    df["Age"] = df["AGEGRP"].apply(_get_age_grp)
    df["SV"] = df.apply(lambda row: _create_sv(row.SV, row.Age), axis=1)
    cols = ["Location", "SV"
           ] + [col for col in cols if col.startswith("POPESTIMATE")]
    df = df[cols]
    cols = [col.replace("POPESTIMATE", "") for col in cols]
    df.columns = cols
    df = _unpivot_df(df, cols[:2], cols[2:], default_col="Year")
    df = df[["Year", "Location", "SV", "Count_Person"]]
    # Deriving Measurement Method for the SV's
    df = _add_measurement_method(df, "SV", "Measurement_Method")
    return df[["Year", "Location", "SV", "Measurement_Method", "Count_Person"]]


def _process_county_1990_1999(file_path: str) -> pd.DataFrame:
    """
    Returns the Cleaned DataFrame consists
    county data for the year 1990-1999.

    Args:
        file_path (str): Input File Path.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    final_data = []
    # Reading txt file and filtering required rows
    prev_origin_race_cat = None
    curr_origin_race_cat = None
    data = []
    skipped_rows = []
    with open(file_path, "r", encoding="latin-1") as file:
        for lines in file.readlines():
            lines = lines.split(" ")
            lines = [line.strip() for line in lines if line.strip().isnumeric()]
            if len(lines) == 21:
                data.append(lines)
                if prev_origin_race_cat is None:
                    prev_origin_race_cat = lines[2]
                elif curr_origin_race_cat is None:
                    curr_origin_race_cat = lines[2]
                if len(data) == 2:
                    # Row level aggregation is calculated
                    # thru pairs (1,2), (3,4) and (11,12)
                    # Dervied SV's are below
                    # WhiteAloneNotHispanicOrLatino: 1 + 2
                    # HispanicOrLatino_WhiteAlone: 3 + 4
                    # HispanicOrLatino: 11 + 12
                    # Few rows were dropped due to unreadable characters,
                    # aggregation can be performed only when the pairs
                    # are available
                    if [prev_origin_race_cat,
                            curr_origin_race_cat] in [['1', '2'], ['3', '4'],
                                                      ['11', '12']]:
                        final_data = final_data + data
                        data = []
                        prev_origin_race_cat = None
                        curr_origin_race_cat = None
                    else:
                        skipped_rows.append(data.pop(0))
                        prev_origin_race_cat = curr_origin_race_cat
                        curr_origin_race_cat = None
    df = pd.DataFrame(final_data)
    skipped_df = pd.DataFrame(skipped_rows)
    pop_cols = [
        "0To4", "5To9", "10To14", "15To19", "20To24", "25To29", "30To34",
        "35To39", "40To44", "45To49", "50To54", "55To59", "60To64", "65To69",
        "70To74", "75To79", "80To84", "85OrMore"
    ]
    df.columns = ["Year", "Location", "SV"] + pop_cols
    skipped_df.columns = ["Year", "Location", "SV"] + pop_cols
    sv_dict = {
        '1': "Male_WhiteAloneNotHispanicOrLatino",
        '2': "Female_WhiteAloneNotHispanicOrLatino",
        '3': "Male_HispanicOrLatino_WhiteAlone",
        '4': "Female_HispanicOrLatino_WhiteAlone",
        '5': "Male_BlackOrAfricanAmericanAlone",
        '6': "Female_BlackOrAfricanAmericanAlone",
        '7': "Male_AmericanIndianAndAlaskaNativeAlone",
        '8': "Female_AmericanIndianAndAlaskaNativeAlone",
        '9': "Male_AsianOrPacificIslander",
        '10': "Female_AsianOrPacificIslander",
        '11': "Male_HispanicOrLatino",
        '12': "Female_HispanicOrLatino"
    }
    # Removing SV's from 5 to 10 as they are not part of origin
    # HispanicOrlatino (or) NotHispanicOrLatino
    df = df[~df["SV"].isin(["5", "6", "7", "8", "9", "10"])].reset_index(
        drop=True)
    skipped_df = skipped_df[~skipped_df["SV"].
                            isin(["5", "6", "7", "8", "9", "10"])].reset_index(
                                drop=True)
    df["SV"] = df["SV"].map(sv_dict)
    skipped_df["SV"] = skipped_df["SV"].map(sv_dict)
    derived_cols = _get_mapper_cols_dict("county_1900_1999")
    df[pop_cols] = df[pop_cols].apply(pd.to_numeric, errors='coerce')
    data = None
    for dsv, sv in derived_cols.items():
        data = df[df["SV"].isin(sv)].reset_index(drop=True)
        data["SV"] = dsv
        data = data.groupby(['Year', 'Location', "SV"]).sum().reset_index()
        df = pd.concat([df, data])
    df = pd.concat([df, skipped_df])
    df = df.dropna()
    df = _unpivot_df(df, ["Year", "Location", "SV"],
                     pop_cols,
                     default_col="Age")
    # Creating SV's name using SV, Age Column
    df["SV"] = df.apply(lambda row: _create_sv(row.SV, row.Age), axis=1)
    # Creating GeoId's for State FIPS Code
    df["Location"] = "geoId/" + df["Location"].astype("str").str.pad(
        width=5, side="left", fillchar="0")
    # Deriving Measurement Method for the SV's
    df = _add_measurement_method(df, "SV", "Measurement_Method")
    df = df[["Year", "Location", "SV", "Measurement_Method", "Count_Person"]]
    return df


def _process_county_2000_2009(file_path: str) -> pd.DataFrame:
    """
    Returns the Cleaned DataFrame consists
    county data for the year 2000-2009.

    Args:
        file_path (str): Input File Path

    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    df = _load_df(file_path, "csv", header=0, encoding="latin-1")
    # Skipping Below Year Values
    # 1 = 4/1/2000 resident population estimates base
    # 12 = 4/1/2010 resident 2010 Census population
    # 13 = 7/1/2010 resident population estimate
    df = df[(~df["YEAR"].isin([1, 12, 13])) &
            (df["AGEGRP"] != 99)].reset_index(drop=True)
    df["YEAR"] = 1998 + df["YEAR"]
    cols = list(df.columns)
    # Mapping Dataset Headers to its FullForm
    cols_dict = _get_mapper_cols_dict("header_mappers")
    for idx, val in enumerate(cols):
        cols[idx] = cols_dict.get(val, val)
    df.columns = cols
    df["STATE"] = df["STATE"].astype("str").str.pad(width=2,
                                                    side="left",
                                                    fillchar="0")
    df["COUNTY"] = df["COUNTY"].astype("str").str.pad(width=3,
                                                      side="left",
                                                      fillchar="0")
    df["Location"] = "geoId/" + df["STATE"] + df["COUNTY"]
    # Deriving New Columns
    derived_cols = _get_mapper_cols_dict("county_2000_2009")
    df = _derive_cols(df, derived_cols)
    cols = cols + list(derived_cols.keys())
    df["Age"] = df["AGEGRP"].apply(_get_age_grp_county_2000_2009)
    f_cols = [val for val in cols if "Hispanic" in val]
    df = _unpivot_df(df, ["Year", "Location", "Age"], f_cols)
    # Creating SV's name using SV, Age Column
    df["SV"] = df.apply(lambda row: _create_sv(row.SV, row.Age), axis=1)
    # Deriving Measurement Method for the SV's
    f_cols = ["Year", "Location", "SV", "Measurement_Method", "Count_Person"]
    df = _add_measurement_method(df, "SV", "Measurement_Method")
    return df[f_cols]


def _process_county_2010_2020(file_path: str) -> pd.DataFrame():
    """
    Returns the Cleaned DataFrame consists
    county data for the year 2010-2020.

    Args:
        file_path (str): Input File Path

    Returns:
        pd.DataFrame: Cleaned DataFrame
    """

    df = _load_df(file_path, "csv", header=0, encoding='latin-1')
    df = df[(~df["YEAR"].isin([1, 2, 13])) &
            (df["AGEGRP"] != 0)].reset_index(drop=True)
    df["YEAR"] = df["YEAR"].astype('str').str.replace("14", "13").astype("int")
    df["YEAR"] = 2007 + df["YEAR"]
    # Mapping Dataset Headers to its FullForm
    cols_dict = _get_mapper_cols_dict("header_mappers")
    cols = df.columns.to_list()
    for idx, val in enumerate(cols):
        cols[idx] = cols_dict.get(val, val)
    df.columns = cols
    df["STATE"] = df["STATE"].astype("str").str.pad(width=2,
                                                    side="left",
                                                    fillchar="0")
    df["COUNTY"] = df["COUNTY"].astype("str").str.pad(width=3,
                                                      side="left",
                                                      fillchar="0")
    df["Location"] = "geoId/" + df["STATE"] + df["COUNTY"]
    # Deriving New Columns
    derived_cols = _get_mapper_cols_dict("county_2010_2020")
    df = _derive_cols(df, derived_cols)
    cols = cols + list(derived_cols.keys())
    f_cols = [val for val in cols if "Hispanic" in val]
    df["Age"] = df["AGEGRP"].apply(_get_age_grp)
    df["Age"] = df["Age"].str.replace("85To89", "85")
    df = _unpivot_df(df, ["Year", "Location", "Age"], f_cols)
    # Creating SV's name using SV, Age Column
    df["SV"] = df.apply(lambda row: _create_sv(row.SV, row.Age), axis=1)
    f_cols = ["Year", "Location", "SV", "Measurement_Method", "Count_Person"]
    # Deriving Measurement Method for the SV's
    df = _add_measurement_method(df, "SV", "Measurement_Method")
    return df[f_cols]


def _derive_nationals(df: pd.DataFrame) -> pd.DataFrame:
    df["Location"] = "country/USA"
    df = df.groupby(by=["Year", "Location", "SV", "Measurement_Method"]).agg({
        'Count_Person': 'sum'
    }).reset_index()
    return df


class USCensusPEPByASRH:
    """
    This Class has requried methods to generate Cleaned CSV,
    MCF and TMCF Files.
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

    def _generate_mcf(self, sv_list) -> None:
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
populationType: dcs:Person{}{}{}{}
statType: dcs:measuredValue
measuredProperty: dcs:count
"""
        final_mcf_template = ""
        for sv in sv_list:
            if "Total" in sv:
                continue
            age = ''
            enthnicity = ''
            gender = ''
            race = ''
            sv_prop = sv.split("_")
            for prop in sv_prop:
                if prop in ["Count", "Person"]:
                    continue
                if "Years" in prop:
                    if "OrMoreYears" in prop:
                        age = "\nage: [" + prop.replace("OrMoreYears",
                                                        "") + " - Years]" + "\n"
                    elif "To" in prop:
                        age = "\nage: [" + prop.replace("Years", "").replace(
                            "To", " ") + " Years]" + "\n"
                    else:
                        age = "\nage: [Years " + prop.replace("Years",
                                                              "") + "]" + "\n"
                elif "Male" in prop or "Female" in prop:
                    gender = "gender: dcs:" + prop
                else:

                    if "race" in race:
                        race = race.strip() + "__" + prop + "\n"
                    else:
                        race = "race: dcs:" + prop + "\n"
            if gender == "":
                race = race.strip()
            final_mcf_template += mcf_template.format(sv, age, enthnicity, race,
                                                      gender) + "\n"
        # Writing Genereated MCF to local path.
        with open(self.mcf_file_path, 'w+', encoding='utf-8') as f_out:
            f_out.write(final_mcf_template.rstrip('\n'))

    def _generate_tmcf(self) -> None:
        """
        This method generates TMCF file w.r.t
        dataframe headers and defined TMCF template.
        Arguments:
            df_cols (list) : List of DataFrame Columns
        Returns:
            None
        """
        tmcf_template = """Node: E:USA_Population_ASRH->E0
typeOf: dcs:StatVarObservation
variableMeasured: C:USA_Population_ASRH->SV
measurementMethod: C:USA_Population_ASRH->Measurement_Method
observationAbout: C:USA_Population_ASRH->Location
observationDate: C:USA_Population_ASRH->Year
observationPeriod: \"P1Y\"
value: C:USA_Population_ASRH->Count_Person 
"""

        # Writing Genereated TMCF to local path.
        with open(self.tmcf_file_path, 'w+', encoding='utf-8') as f_out:
            f_out.write(tmcf_template.rstrip('\n'))

    def process(self):
        """
        This Method calls the required methods to generate cleaned CSV,
        MCF, and TMCF file
        """
        data_df = pd.DataFrame(columns=[[
            "Year", "Location", "SV", "Measurement_Method", "Count_Person"
        ]])
        # Creating Output Directory
        output_path = os.path.dirname(self.cleaned_csv_file_path)
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        sv_list = []
        f_names = []
        data_df.to_csv(self.cleaned_csv_file_path, index=False)
        for file_path in self.input_files:
            data_df = None
            f_names.append(file_path)
            if "sasr" in file_path:
                data_df = _process_state_1990_1999(file_path)
                if "sasrh" in file_path:
                    nat_df = _derive_nationals(deepcopy(data_df))
                    data_df = pd.concat([data_df, nat_df], axis=0)
            elif "st-est00int-alldata" in file_path:
                data_df = _process_state_2000_2010(file_path)
            elif "SC-EST2020-ALLDATA6" in file_path:
                data_df = _process_state_2010_2020(file_path)
            elif "st_int_asrh" in file_path:
                data_df = _process_state_1980_1989(file_path)
            elif "CQI.TXT" in file_path:
                data_df = _process_nationals_1980_1989(file_path)
            elif "us-est00int-alldata" in file_path:
                data_df = _process_nationals_2000_2009(file_path)
            elif "NC-EST" in file_path:
                data_df = _process_nationals_2010_2021(file_path)
            elif "casrh" in file_path:
                data_df = _process_county_1990_1999(file_path)
            elif "co-est00int-alldata" in file_path:
                data_df = _process_county_2000_2009(file_path)
            elif "CC-EST2020" in file_path:
                data_df = _process_county_2010_2020(file_path)

            data_df = _convert_to_int(data_df)
            data_df.to_csv(self.cleaned_csv_file_path,
                           mode="a",
                           header=False,
                           index=False)
            sv_list += data_df["SV"].to_list()
        sv_list = list(set(sv_list))
        sv_list.sort()
        self._generate_mcf(sv_list)
        self._generate_tmcf()


def main(_):
    input_path = FLAGS.input_path
    ip_files = os.listdir(input_path)
    ip_files = [input_path + os.sep + file for file in ip_files]
    data_file_path = os.path.dirname(
        os.path.abspath(__file__)) + os.sep + "output"
    if not os.path.exists(data_file_path):
        os.mkdir(data_file_path)
    # Defining Output Files
    cleaned_csv_path = data_file_path + os.sep + "USA_Population_ASRH.csv"
    mcf_path = data_file_path + os.sep + "USA_Population_ASRH.mcf"
    tmcf_path = data_file_path + os.sep + "USA_Population_ASRH.tmcf"
    loader = USCensusPEPByASRH(ip_files, cleaned_csv_path, mcf_path, tmcf_path)
    loader.process()


if __name__ == "__main__":
    app.run(main)