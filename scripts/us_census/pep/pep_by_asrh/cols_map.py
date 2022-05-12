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
This file has various metadata dictionaries and methods
that useful in resolving the dataset fields and also
to derive new SV's
"""
_cols_dict = {
    "UNIVERSE":
        "Universe",
    "MONTH":
        "Month",
    "YEAR":
        "Year",
    "AGE":
        "Age",
    "TOT_POP":
        "Total_Population",
    "TOT_MALE":
        "Male",
    "TOT_FEMALE":
        "Female",
    "WA_MALE":
        "Male_WhiteAlone",
    "WA_FEMALE":
        "Female_WhiteAlone",
    "BA_MALE":
        "Male_BlackOrAfricanAmericanAlone",
    "BA_FEMALE":
        "Female_BlackOrAfricanAmericanAlone",
    "IA_MALE":
        "Male_AmericanIndianAndAlaskaNativeAlone",
    "IA_FEMALE":
        "Female_AmericanIndianAndAlaskaNativeAlone",
    "AA_MALE":
        "Male_AsianAlone",
    "AA_FEMALE":
        "Female_AsianAlone",
    "NA_MALE":
        "Male_NativeHawaiianAndOtherPacificIslanderAlone",
    "NA_FEMALE":
        "Female_NativeHawaiianAndOtherPacificIslanderAlone",
    "TOM_MALE":
        "Male_TwoOrMoreRaces",
    "TOM_FEMALE":
        "Female_TwoOrMoreRaces",
    "WAC_MALE":
        "Male_WhiteAloneOrInCombinationWithOneOrMoreOtherRaces",
    "WAC_FEMALE":
        "Female_WhiteAloneOrInCombinationWithOneOrMoreOtherRaces",
    "BAC_MALE":
        "Male_BlackOrAfricanAmericanAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "BAC_FEMALE":
        "Female_BlackOrAfricanAmericanAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "IAC_MALE":
        "Male_AmericanIndianAndAlaskaNativeAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "IAC_FEMALE":
        "Female_AmericanIndianAndAlaskaNativeAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "AAC_MALE":
        "Male_AsianAloneOrInCombinationWithOneOrMoreOtherRaces",
    "AAC_FEMALE":
        "Female_AsianAloneOrInCombinationWithOneOrMoreOtherRaces",
    "NAC_MALE":
        "Male_NativeHawaiianAndOtherPacificIslanderAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "NAC_FEMALE":
        "Female_NativeHawaiianAndOtherPacificIslanderAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "NH_MALE":
        "Male_NotHispanicOrLatino",
    "NH_FEMALE":
        "Female_NotHispanicOrLatino",
    "NHWA_MALE":
        "Male_WhiteAloneNotHispanicOrLatino",
    "NHWA_FEMALE":
        "Female_WhiteAloneNotHispanicOrLatino",
    "NHBA_MALE":
        "Male_NotHispanicOrLatino_BlackOrAfricanAmericanAlone",
    "NHBA_FEMALE":
        "Female_NotHispanicOrLatino_BlackOrAfricanAmericanAlone",
    "NHIA_MALE":
        "Male_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
    "NHIA_FEMALE":
        "Female_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
    "NHAA_MALE":
        "Male_NotHispanicOrLatino_AsianAlone",
    "NHAA_FEMALE":
        "Female_NotHispanicOrLatino_AsianAlone",
    "NHNA_MALE":
        "Male_NotHispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone",
    "NHNA_FEMALE":
        "Female_NotHispanicOrLatino_NativeHawaiianAnd" + \
            "OtherPacificIslanderAlone",
    "NHTOM_MALE":
        "Male_NotHispanicOrLatino_TwoOrMoreRaces",
    "NHTOM_FEMALE":
        "Female_NotHispanicOrLatino_TwoOrMoreRaces",
    "NHWAC_MALE":
        "Male_NotHispanicOrLatino_" + \
            "WhiteAloneOrInCombinationWithOneOrMoreOtherRaces",
    "NHWAC_FEMALE":
        "Female_NotHispanicOrLatino_" + \
            "WhiteAloneOrInCombinationWithOneOrMoreOtherRaces",
    "NHBAC_MALE":
        "Male_NotHispanicOrLatino_BlackOrAfricanAmericanAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "NHBAC_FEMALE":
        "Female_NotHispanicOrLatino_BlackOrAfricanAmericanAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "NHIAC_MALE":
        "Male_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "NHIAC_FEMALE":
        "Female_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "NHAAC_MALE":
        "Male_NotHispanicOrLatino_AsianAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "NHAAC_FEMALE":
        "Female_NotHispanicOrLatino_AsianAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "NHNAC_MALE":
        "Male_NotHispanicOrLatino_" + \
            "NativeHawaiianAndOtherPacificIslanderAlone" + \
                "OrInCombinationWithOneOrMoreOtherRaces",
    "NHNAC_FEMALE":
        "Female_NotHispanicOrLatino_" + \
            "NativeHawaiianAndOtherPacificIslanderAlone" + \
                "OrInCombinationWithOneOrMoreOtherRaces",
    "H_MALE":
        "Male_HispanicOrLatino",
    "H_FEMALE":
        "Female_HispanicOrLatino",
    "HWA_MALE":
        "Male_HispanicOrLatino_WhiteAlone",
    "HWA_FEMALE":
        "Female_HispanicOrLatino_WhiteAlone",
    "HBA_MALE":
        "Male_HispanicOrLatino_BlackOrAfricanAmericanAlone",
    "HBA_FEMALE":
        "Female_HispanicOrLatino_BlackOrAfricanAmericanAlone",
    "HIA_MALE":
        "Male_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
    "HIA_FEMALE":
        "Female_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
    "HAA_MALE":
        "Male_HispanicOrLatino_AsianAlone",
    "HAA_FEMALE":
        "Female_HispanicOrLatino_AsianAlone",
    "HNA_MALE":
        "Male_HispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone",
    "HNA_FEMALE":
        "Female_HispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone",
    "HTOM_MALE":
        "Male_HispanicOrLatino_TwoOrMoreRaces",
    "HTOM_FEMALE":
        "Female_HispanicOrLatino_TwoOrMoreRaces",
    "HWAC_MALE":
        "Male_HispanicOrLatino_WhiteAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "HWAC_FEMALE":
        "Female_HispanicOrLatino_WhiteAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "HBAC_MALE":
        "Male_HispanicOrLatino_BlackOrAfricanAmericanAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "HIAC_MALE":
        "Male_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "HIAC_FEMALE":
        "Female_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "HAAC_MALE":
        "Male_HispanicOrLatino_AsianAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "HAAC_FEMALE":
        "Female_HispanicOrLatino_AsianAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "HNAC_MALE":
        "Male_HispanicOrLatino_" + \
            "NativeHawaiianAndOtherPacificIslanderAlone" + \
                "OrInCombinationWithOneOrMoreOtherRaces",
    "HNAC_FEMALE":
        "Female_HispanicOrLatino_" + \
            "NativeHawaiianAndOtherPacificIslanderAlone" + \
                "OrInCombinationWithOneOrMoreOtherRaces",
    "HBAC_FEMALE":
        "Female_HispanicOrLatino_BlackOrAfricanAmericanAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
    "SUMLEV":
        "SUMLEV",
    "STATE":
        "STATE",
    "COUNTY":
        "COUNTY",
    "STNAME":
        "STNAME",
    "CTYNAME":
        "CTYNAME",
    "AGEGRP":
        "AGEGRP"
}


def get_cols_dict() -> dict:
    return _cols_dict


_nationals_1980_1999_hispanic_cols = {
    "Male_HispanicOrLatino_WhiteAlone_computed": [
        "White_Male_Population", "Male_WhiteAloneNotHispanicOrLatino"
    ],
    "Female_HispanicOrLatino_WhiteAlone_computed": [
        "White_Female_Population", "Female_WhiteAloneNotHispanicOrLatino"
    ],
    "Male_HispanicOrLatino_Black_computed": [
        "Black_Male_Population", "Male_NotHispanicOrLatino_Black"
    ],
    "Female_HispanicOrLatino_Black_computed": [
        "Black_Female_Population", "Female_NotHispanicOrLatino_Black"
    ],
    "Male_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed": [
        "Male_AsianOrPacificIslander",
        "Male_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone"
    ],
    "Female_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed": [
        "Female_AsianOrPacificIslander",
        "Female_NotHispanicOrLatino_AsianOrPacificIslander"
    ],
    "Male_HispanicOrLatino_AsianOrPacificIslander_computed": [
        "Male_AsianOrPacificIslander",
        "Male_NotHispanicOrLatino_AsianOrPacificIslander"
    ],
    "Female_HispanicOrLatino_AsianOrPacificIslander_computed": [
        "Female_AsianOrPacificIslander",
        "Female_NotHispanicOrLatino_AsianOrPacificIslander"
    ]
}
_nationals_1980_1999_derived_cols = {
    "Male_NotHispanicOrLatino_computed": [
        "Male_WhiteAloneNotHispanicOrLatino", "Male_NotHispanicOrLatino_Black",
        "Male_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_NotHispanicOrLatino_AsianOrPacificIslander"
    ],
    "Female_NotHispanicOrLatino_computed": [
        "Female_WhiteAloneNotHispanicOrLatino",
        "Female_NotHispanicOrLatino_Black",
        "Female_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_NotHispanicOrLatino_AsianOrPacificIslander"
    ],
    "Male_HispanicOrLatino_computed": [
        "Male_HispanicOrLatino_WhiteAlone_computed",
        "Male_HispanicOrLatino_Black_computed",
        "Male_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed",
        "Male_HispanicOrLatino_AsianOrPacificIslander_computed"
    ],
    "Female_HispanicOrLatino_computed": [
        "Female_HispanicOrLatino_WhiteAlone_computed",
        "Female_HispanicOrLatino_Black_computed",
        "Female_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed",
        "Female_HispanicOrLatino_AsianOrPacificIslander_computed"
    ],
    "WhiteAloneNotHispanicOrLatino_computed": [
        "Male_WhiteAloneNotHispanicOrLatino",
        "Female_WhiteAloneNotHispanicOrLatino"
    ],
    "NotHispanicOrLatino_Black_computed": [
        "Male_NotHispanicOrLatino_Black", "Female_NotHispanicOrLatino_Black"
    ],
    "HispanicOrLatino_WhiteAlone_computed": [
        "Male_HispanicOrLatino_WhiteAlone_computed",
        "Female_HispanicOrLatino_WhiteAlone_computed"
    ],
    "HispanicOrLatino_Black_computed": [
        "Male_HispanicOrLatino_Black_computed",
        "Female_HispanicOrLatino_Black_computed"
    ],
    "NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed": [
        "Male_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone"
    ],
    "HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed": [
        "Male_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed",
        "Female_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed"
    ],
    "NotHispanicOrLatino_AsianOrPacificIslander_computed": [
        "Male_HispanicOrLatino_AsianOrPacificIslander_computed",
        "Female_HispanicOrLatino_AsianOrPacificIslander_computed"
    ],
    "HispanicOrLatino_AsianOrPacificIslander_computed": [
        "Male_HispanicOrLatino_AsianOrPacificIslander_computed",
        "Female_HispanicOrLatino_AsianOrPacificIslander_computed"
    ],
    "HispanicOrLatino_computed": [
        "Male_HispanicOrLatino_WhiteAlone_computed",
        "Male_HispanicOrLatino_Black_computed",
        "Male_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed",
        "Male_HispanicOrLatino_AsianOrPacificIslander_computed",
        "Female_HispanicOrLatino_WhiteAlone_computed",
        "Female_HispanicOrLatino_Black_computed",
        "Female_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed",
        "Female_HispanicOrLatino_AsianOrPacificIslander_computed"
    ],
    "NotHispanicOrLatino_computed": [
        "Male_WhiteAloneNotHispanicOrLatino", "Male_NotHispanicOrLatino_Black",
        "Male_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_NotHispanicOrLatino_AsianOrPacificIslander",
        "Female_WhiteAloneNotHispanicOrLatino",
        "Female_NotHispanicOrLatino_Black",
        "Female_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_NotHispanicOrLatino_AsianOrPacificIslander"
    ]
}

_nationals_2000_2009_dict = {
    "HispanicOrLatino_WhiteAlone_computed": [
        "Female_HispanicOrLatino_WhiteAlone",
        "Male_HispanicOrLatino_WhiteAlone"
    ],
    "HispanicOrLatino_BlackOrAfricanAmericanAlone_computed": [
        "Female_HispanicOrLatino_BlackOrAfricanAmericanAlone",
        "Male_HispanicOrLatino_BlackOrAfricanAmericanAlone"
    ],
    "HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed": [
        "Female_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone"
    ],
    "HispanicOrLatino_AsianAlone_computed": [
        "Female_HispanicOrLatino_AsianAlone",
        "Male_HispanicOrLatino_AsianAlone"
    ],
    "HispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone_computed": [
        "Female_HispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone",
        "Male_HispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone"
    ],
    "HispanicOrLatino_TwoOrMoreRaces_computed": [
        "Male_HispanicOrLatino_TwoOrMoreRaces",
        "Female_HispanicOrLatino_TwoOrMoreRaces"
    ],
    "WhiteAloneNotHispanicOrLatino_computed": [
        "Female_WhiteAloneNotHispanicOrLatino",
        "Male_WhiteAloneNotHispanicOrLatino"
    ],
    "NotHispanicOrLatino_BlackOrAfricanAmericanAlone_computed": [
        "Female_NotHispanicOrLatino_BlackOrAfricanAmericanAlone",
        "Male_NotHispanicOrLatino_BlackOrAfricanAmericanAlone"
    ],
    "NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed": [
        "Female_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone"
    ],
    "NotHispanicOrLatino_AsianAlone_computed": [
        "Female_NotHispanicOrLatino_AsianAlone",
        "Male_NotHispanicOrLatino_AsianAlone"
    ],
    "NotHispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone_computed": [
        "Female_NotHispanicOrLatino_" + \
            "NativeHawaiianAndOtherPacificIslanderAlone",
        "Male_NotHispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone"
    ],
    "NotHispanicOrLatino_TwoOrMoreRaces_computed": [
        "Male_NotHispanicOrLatino_TwoOrMoreRaces",
        "Female_NotHispanicOrLatino_TwoOrMoreRaces"
    ],
    "HispanicOrLatino_computed": [
        "Male_HispanicOrLatino", "Female_HispanicOrLatino"
    ],
    "NotHispanicOrLatino_computed": [
        "Male_NotHispanicOrLatino", "Female_NotHispanicOrLatino"
    ]
}

_state_2010_2020_hispanic_dict = {
    "HispanicOrLatino_WhiteAlone_computed": [
        "Female_HispanicOrLatino_WhiteAlone",
        "Male_HispanicOrLatino_WhiteAlone"
    ],
    "HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed": [
        "Female_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone"
    ],
    "HispanicOrLatino_AsianAlone_computed": [
        "Female_HispanicOrLatino_AsianAlone",
        "Male_HispanicOrLatino_AsianAlone"
    ],
    "HispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone_computed": [
        "Female_HispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone",
        "Male_HispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone"
    ],
    "HispanicOrLatino_TwoOrMoreRaces_computed": [
        "Male_HispanicOrLatino_TwoOrMoreRaces",
        "Female_HispanicOrLatino_TwoOrMoreRaces"
    ],
    "WhiteAloneNotHispanicOrLatino_computed": [
        "Female_WhiteAloneNotHispanicOrLatino",
        "Male_WhiteAloneNotHispanicOrLatino"
    ],
    "NotHispanicOrLatino_BlackOrAfricanAmericanAlone_computed": [
        "Female_NotHispanicOrLatino_BlackOrAfricanAmericanAlone",
        "Male_NotHispanicOrLatino_BlackOrAfricanAmericanAlone"
    ],
    "NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed": [
        "Female_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone"
    ],
    "NotHispanicOrLatino_AsianAlone_computed": [
        "Female_NotHispanicOrLatino_AsianAlone",
        "Male_NotHispanicOrLatino_AsianAlone"
    ],
    "NotHispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone_computed": [
        "Female_NotHispanicOrLatino_" + \
            "NativeHawaiianAndOtherPacificIslanderAlone",
        "Male_NotHispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone"
    ],
    "NotHispanicOrLatino_TwoOrMoreRaces_computed": [
        "Male_NotHispanicOrLatino_TwoOrMoreRaces",
        "Female_NotHispanicOrLatino_TwoOrMoreRaces"
    ],
    "Male_NotHispanicOrLatino_computed": [
        "Male_WhiteAloneNotHispanicOrLatino",
        "Male_NotHispanicOrLatino_BlackOrAfricanAmericanAlone",
        "Male_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_NotHispanicOrLatino_AsianAlone",
        "Male_NotHispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone",
        "Male_NotHispanicOrLatino_TwoOrMoreRaces"
    ],
    "Female_NotHispanicOrLatino_computed": [
        "Female_WhiteAloneNotHispanicOrLatino",
        "Female_NotHispanicOrLatino_BlackOrAfricanAmericanAlone",
        "Female_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_NotHispanicOrLatino_AsianAlone",
        "Female_NotHispanicOrLatino_" + \
            "NativeHawaiianAndOtherPacificIslanderAlone",
        "Female_NotHispanicOrLatino_TwoOrMoreRaces"
    ],
    "Male_HispanicOrLatino_computed": [
        "Male_HispanicOrLatino_WhiteAlone",
        "Male_HispanicOrLatino_BlackOrAfricanAmericanAlone",
        "Male_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_HispanicOrLatino_AsianAlone",
        "Male_HispanicOrLatino_" + \
            "NativeHawaiianAndOtherPacificIslanderAlone",
        "Male_HispanicOrLatino_TwoOrMoreRaces"
    ],
    "Female_HispanicOrLatino_computed": [
        "Female_HispanicOrLatino_WhiteAlone",
        "Female_HispanicOrLatino_BlackOrAfricanAmericanAlone",
        "Female_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_HispanicOrLatino_AsianAlone",
        "Female_HispanicOrLatino_" + \
            "NativeHawaiianAndOtherPacificIslanderAlone",
        "Female_HispanicOrLatino_TwoOrMoreRaces"
    ]
}
_state_2010_2020_total_dict = {
    "HispanicOrLatino_computed": [
        "Male_HispanicOrLatino_computed", "Female_HispanicOrLatino_computed"
    ],
    "NotHispanicOrLatino_computed": [
        "Male_NotHispanicOrLatino_computed",
        "Female_NotHispanicOrLatino_computed"
    ]
}

_nationals_2010_2021_dict = {
    "WhiteAloneNotHispanicOrLatino_computed": [
        "Male_WhiteAloneNotHispanicOrLatino",
        "Female_WhiteAloneNotHispanicOrLatino"
    ],
    "NotHispanicOrLatino_BlackOrAfricanAmericanAlone_computed": [
        "Male_NotHispanicOrLatino_BlackOrAfricanAmericanAlone",
        "Female_NotHispanicOrLatino_BlackOrAfricanAmericanAlone"
    ],
    "NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed": [
        "Male_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone"
    ],
    "NotHispanicOrLatino_AsianAlone_computed": [
        "Male_NotHispanicOrLatino_AsianAlone",
        "Female_NotHispanicOrLatino_AsianAlone"
    ],
    "NotHispanicOrLatino_" + \
            "NativeHawaiianAndOtherPacificIslanderAlone_computed": [
        "Male_NotHispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone",
        "Female_NotHispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone"
    ],
    "NotHispanicOrLatino_TwoOrMoreRaces_computed": [
        "Male_NotHispanicOrLatino_TwoOrMoreRaces",
        "Female_NotHispanicOrLatino_TwoOrMoreRaces"
    ],
    "NotHispanicOrLatino_" + \
            "WhiteAloneOrInCombinationWithOneOrMoreOtherRaces_computed": [
        "Male_NotHispanicOrLatino_" + \
            "WhiteAloneOrInCombinationWithOneOrMoreOtherRaces",
        "Female_NotHispanicOrLatino_" + \
            "WhiteAloneOrInCombinationWithOneOrMoreOtherRaces"
    ],
    "NotHispanicOrLatino_" + \
            "BlackOrAfricanAmericanAlone" + \
                "OrInCombinationWithOneOrMoreOtherRaces_computed":
        [
            "Male_NotHispanicOrLatino_" + \
                "BlackOrAfricanAmericanAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces",
            "Female_NotHispanicOrLatino_" + \
                "BlackOrAfricanAmericanAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces"
        ],
    "NotHispanicOrLatino_" + \
            "AmericanIndianAndAlaskaNativeAlone" + \
                "OrInCombinationWithOneOrMoreOtherRaces_computed":
        [
            "Male_NotHispanicOrLatino_" + \
                "AmericanIndianAndAlaskaNativeAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces",
            "Female_NotHispanicOrLatino_" + \
                "AmericanIndianAndAlaskaNativeAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces"
        ],
    "NotHispanicOrLatino_" + \
            "AsianAloneOrInCombinationWithOneOrMoreOtherRaces_computed": [
        "Male_NotHispanicOrLatino_" + \
            "AsianAloneOrInCombinationWithOneOrMoreOtherRaces",
        "Female_NotHispanicOrLatino_" + \
            "AsianAloneOrInCombinationWithOneOrMoreOtherRaces"
    ],
    "NotHispanicOrLatino_" + \
            "NativeHawaiianAndOtherPacificIslanderAlone" + \
                "OrInCombinationWithOneOrMoreOtherRaces_computed":
        [
            "Male_NotHispanicOrLatino_" + \
                "NativeHawaiianAndOtherPacificIslanderAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces",
            "Female_NotHispanicOrLatino_" + \
                "NativeHawaiianAndOtherPacificIslanderAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces"
        ],
    "HispanicOrLatino_WhiteAlone_computed": [
        "Male_HispanicOrLatino_WhiteAlone",
        "Female_HispanicOrLatino_WhiteAlone"
    ],
    "HispanicOrLatino_BlackOrAfricanAmericanAlone_computed": [
        "Male_HispanicOrLatino_BlackOrAfricanAmericanAlone",
        "Female_HispanicOrLatino_BlackOrAfricanAmericanAlone"
    ],
    "HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed": [
        "Male_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone"
    ],
    "HispanicOrLatino_AsianAlone_computed": [
        "Male_HispanicOrLatino_AsianAlone",
        "Female_HispanicOrLatino_AsianAlone"
    ],
    "HispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone_computed": [
        "Male_HispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone",
        "Female_HispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone"
    ],
    "HispanicOrLatino_TwoOrMoreRaces_computed": [
        "Male_HispanicOrLatino_TwoOrMoreRaces",
        "Female_HispanicOrLatino_TwoOrMoreRaces"
    ],
    "HispanicOrLatino_" + \
            "WhiteAloneOrInCombinationWithOneOrMoreOtherRaces_computed": [
        "Male_HispanicOrLatino_" + \
            "WhiteAloneOrInCombinationWithOneOrMoreOtherRaces",
        "Female_HispanicOrLatino_" + \
            "WhiteAloneOrInCombinationWithOneOrMoreOtherRaces"
    ],
    "HispanicOrLatino_" + \
            "BlackOrAfricanAmericanAlone" + \
                "OrInCombinationWithOneOrMoreOtherRaces_computed":
        [
            "Male_HispanicOrLatino_" + \
                "BlackOrAfricanAmericanAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces",
            "Female_HispanicOrLatino_" + \
                "BlackOrAfricanAmericanAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces"
        ],
    "HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone" + \
        "OrInCombinationWithOneOrMoreOtherRaces_computed":
        [
            "Male_HispanicOrLatino_" + \
                "AmericanIndianAndAlaskaNativeAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces",
            "Female_HispanicOrLatino_" + \
                "AmericanIndianAndAlaskaNativeAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces"
        ],
    "HispanicOrLatino_" + \
            "AsianAloneOrInCombinationWithOneOrMoreOtherRaces_computed": [
        "Male_HispanicOrLatino_AsianAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
        "Female_HispanicOrLatino_AsianAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces"
    ],
    "HispanicOrLatino_NativeHawaiianAndOther" + \
        "PacificIslanderAloneOrInCombinationWithOneOrMoreOtherRaces_computed":
        [
            "Male_HispanicOrLatino_NativeHawaiianAndOther" + \
                "PacificIslanderAloneOrInCombinationWithOneOrMoreOtherRaces",
            "Female_HispanicOrLatino_NativeHawaiianAndOther" + \
                "PacificIslanderAloneOrInCombinationWithOneOrMoreOtherRaces"
        ]
}

_county_2000_2009_dict = {
    "HispanicOrLatino_WhiteAlone_computed": [
        "Female_HispanicOrLatino_WhiteAlone", "Male_HispanicOrLatino_WhiteAlone"
    ],
    "HispanicOrLatino_BlackOrAfricanAmericanAlone_computed": [
        "Female_HispanicOrLatino_BlackOrAfricanAmericanAlone",
        "Male_HispanicOrLatino_BlackOrAfricanAmericanAlone"
    ],
    "HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed": [
        "Female_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone"
    ],
    "HispanicOrLatino_AsianAlone_computed": [
        "Female_HispanicOrLatino_AsianAlone", "Male_HispanicOrLatino_AsianAlone"
    ],
    "HispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone_computed": [
        "Female_HispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone",
        "Male_HispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone"
    ],
    "HispanicOrLatino_TwoOrMoreRaces_computed": [
        "Male_HispanicOrLatino_TwoOrMoreRaces",
        "Female_HispanicOrLatino_TwoOrMoreRaces"
    ],
    "WhiteAloneNotHispanicOrLatino_computed": [
        "Female_WhiteAloneNotHispanicOrLatino",
        "Male_WhiteAloneNotHispanicOrLatino"
    ],
    "NotHispanicOrLatino_BlackOrAfricanAmericanAlone_computed": [
        "Female_NotHispanicOrLatino_BlackOrAfricanAmericanAlone",
        "Male_NotHispanicOrLatino_BlackOrAfricanAmericanAlone"
    ],
    "NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed": [
        "Female_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone"
    ],
    "NotHispanicOrLatino_AsianAlone_computed": [
        "Female_NotHispanicOrLatino_AsianAlone",
        "Male_NotHispanicOrLatino_AsianAlone"
    ],
    "NotHispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone_computed": [
        "Female_NotHispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone",
        "Male_NotHispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone"
    ],
    "NotHispanicOrLatino_TwoOrMoreRaces_computed": [
        "Male_NotHispanicOrLatino_TwoOrMoreRaces",
        "Female_NotHispanicOrLatino_TwoOrMoreRaces"
    ],
    "HispanicOrLatino_computed": [
        "Male_HispanicOrLatino", "Female_HispanicOrLatino"
    ],
    "NotHispanicOrLatino_computed": [
        "Male_NotHispanicOrLatino", "Female_NotHispanicOrLatino"
    ]
}

_county_2010_2020_dict = {
    "WhiteAloneNotHispanicOrLatino_computed": [
        "Male_WhiteAloneNotHispanicOrLatino",
        "Female_WhiteAloneNotHispanicOrLatino"
    ],
    "NotHispanicOrLatino_BlackOrAfricanAmericanAlone_computed": [
        "Male_NotHispanicOrLatino_BlackOrAfricanAmericanAlone",
        "Female_NotHispanicOrLatino_BlackOrAfricanAmericanAlone"
    ],
    "NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed": [
        "Male_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone"
    ],
    "NotHispanicOrLatino_AsianAlone_computed": [
        "Male_NotHispanicOrLatino_AsianAlone",
        "Female_NotHispanicOrLatino_AsianAlone"
    ],
    "NotHispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone_computed": [
        "Male_NotHispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone",
        "Female_NotHispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone"
    ],
    "NotHispanicOrLatino_TwoOrMoreRaces_computed": [
        "Male_NotHispanicOrLatino_TwoOrMoreRaces",
        "Female_NotHispanicOrLatino_TwoOrMoreRaces"
    ],
    "NotHispanicOrLatino_WhiteAloneOrInCombinationWithOneOrMoreOtherRaces" + \
            "_computed": [
        "Male_NotHispanicOrLatino_" + \
            "WhiteAloneOrInCombinationWithOneOrMoreOtherRaces",
        "Female_NotHispanicOrLatino_" + \
            "WhiteAloneOrInCombinationWithOneOrMoreOtherRaces"
    ],
    "NotHispanicOrLatino_" + \
            "BlackOrAfricanAmericanAlone" + \
                "OrInCombinationWithOneOrMoreOtherRaces_computed":
        [
            "Male_NotHispanicOrLatino_" + \
                "BlackOrAfricanAmericanAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces",
            "Female_NotHispanicOrLatino_" + \
                "BlackOrAfricanAmericanAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces"
        ],
    "NotHispanicOrLatino_" + \
            "AmericanIndianAndAlaskaNativeAlone" + \
                "OrInCombinationWithOneOrMoreOtherRaces" + \
                    "_computed":
        [
            "Male_NotHispanicOrLatino_" + \
                "AmericanIndianAndAlaskaNativeAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces",
            "Female_NotHispanicOrLatino_" + \
                "AmericanIndianAndAlaskaNativeAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces"
        ],
    "NotHispanicOrLatino_" + \
            "AsianAloneOrInCombinationWithOneOrMoreOtherRaces_computed": [
        "Male_NotHispanicOrLatino_" + \
            "AsianAloneOrInCombinationWithOneOrMoreOtherRaces",
        "Female_NotHispanicOrLatino_" + \
            "AsianAloneOrInCombinationWithOneOrMoreOtherRaces"
    ],
    "NotHispanicOrLatino_" + \
            "NativeHawaiianAndOtherPacificIslanderAlone" + \
                "OrInCombinationWithOneOrMoreOtherRaces_computed":
        [
            "Male_NotHispanicOrLatino_" + \
                "NativeHawaiianAndOtherPacificIslanderAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces",
            "Female_NotHispanicOrLatino_" + \
                "NativeHawaiianAndOtherPacificIslanderAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces"
        ],
    "HispanicOrLatino_WhiteAlone_computed": [
        "Male_HispanicOrLatino_WhiteAlone",
        "Female_HispanicOrLatino_WhiteAlone"
    ],
    "HispanicOrLatino_BlackOrAfricanAmericanAlone_computed": [
        "Male_HispanicOrLatino_BlackOrAfricanAmericanAlone",
        "Female_HispanicOrLatino_BlackOrAfricanAmericanAlone"
    ],
    "HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed": [
        "Male_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone"
    ],
    "HispanicOrLatino_AsianAlone_computed": [
        "Male_HispanicOrLatino_AsianAlone",
        "Female_HispanicOrLatino_AsianAlone"
    ],
    "HispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone_computed": [
        "Male_HispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone",
        "Female_HispanicOrLatino_NativeHawaiianAndOtherPacificIslanderAlone"
    ],
    "HispanicOrLatino_TwoOrMoreRaces_computed": [
        "Male_HispanicOrLatino_TwoOrMoreRaces",
        "Female_HispanicOrLatino_TwoOrMoreRaces"
    ],
    "HispanicOrLatino_WhiteAloneOrInCombinationWithOneOrMoreOtherRaces" + \
            "_computed": [
        "Male_HispanicOrLatino_" + \
            "WhiteAloneOrInCombinationWithOneOrMoreOtherRaces",
        "Female_HispanicOrLatino_" + \
            "WhiteAloneOrInCombinationWithOneOrMoreOtherRaces"
    ],
    "HispanicOrLatino_" + \
            "BlackOrAfricanAmericanAlone" + \
                "OrInCombinationWithOneOrMoreOtherRaces_computed":
        [
            "Male_HispanicOrLatino_" + \
                "BlackOrAfricanAmericanAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces",
            "Female_HispanicOrLatino_" + \
                "BlackOrAfricanAmericanAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces"
        ],
    "HispanicOrLatino_" + \
            "AmericanIndianAndAlaskaNativeAlone" + \
                "OrInCombinationWithOneOrMoreOtherRaces_computed":
        [
            "Male_HispanicOrLatino_" + \
                "AmericanIndianAndAlaskaNativeAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces",
            "Female_HispanicOrLatino_" + \
                "AmericanIndianAndAlaskaNativeAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces"
        ],
    "HispanicOrLatino_AsianAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces_computed": [
        "Male_HispanicOrLatino_AsianAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces",
        "Female_HispanicOrLatino_AsianAlone" + \
            "OrInCombinationWithOneOrMoreOtherRaces"
    ],
    "HispanicOrLatino_" + \
            "NativeHawaiianAndOtherPacificIslanderAlone" + \
                "OrInCombinationWithOneOrMoreOtherRaces_computed":
        [
            "Male_HispanicOrLatino_" + \
                "NativeHawaiianAndOtherPacificIslanderAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces",
            "Female_HispanicOrLatino_" + \
                "NativeHawaiianAndOtherPacificIslanderAlone" + \
                    "OrInCombinationWithOneOrMoreOtherRaces"
        ]
}

_county_1900_1999_dict = {
    "NotHispanicOrLatino_White_computed": [
        "Male_NotHispanicOrLatino_White", "Female_NotHispanicOrLatino_White"
    ],
    "HispanicOrLatino_White_computed": [
        "Male_HispanicOrLatino_White", "Female_HispanicOrLatino_White"
    ],
    "HispanicOrLatino_computed": [
        "Male_HispanicOrLatino", "Female_HispanicOrLatino"
    ]
}

_state_1980_1989_dict = {
    "NotHispanicOrLatino_Black_computed": [
        "Female_NotHispanicOrLatino_Black", "Male_NotHispanicOrLatino_Black"
    ],
    "NotHispanicOrLatino_White_computed": [
        "Female_NotHispanicOrLatino_White", "Male_NotHispanicOrLatino_White"
    ],
    "NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed": [
        "Female_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone"
    ],
    "NotHispanicOrLatino_AsianOrPacificIslander_computed": [
        "Female_NotHispanicOrLatino_AsianOrPacificIslander",
        "Male_NotHispanicOrLatino_AsianOrPacificIslander"
    ],
    "Female_NotHispanicOrLatino_computed": [
        "Female_NotHispanicOrLatino_Black", "Female_NotHispanicOrLatino_White",
        "Female_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_NotHispanicOrLatino_AsianOrPacificIslander"
    ],
    "Male_NotHispanicOrLatino_computed": [
        "Male_NotHispanicOrLatino_Black", "Male_NotHispanicOrLatino_White",
        "Male_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_NotHispanicOrLatino_AsianOrPacificIslander"
    ],
    "HispanicOrLatino_Black_computed": [
        "Female_HispanicOrLatino_Black", "Male_HispanicOrLatino_Black"
    ],
    "HispanicOrLatino_White_computed": [
        "Female_HispanicOrLatino_White", "Male_HispanicOrLatino_White"
    ],
    "HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed": [
        "Female_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone"
    ],
    "HispanicOrLatino_AsianOrPacificIslander_computed": [
        "Female_HispanicOrLatino_AsianOrPacificIslander",
        "Male_HispanicOrLatino_AsianOrPacificIslander"
    ],
    "Female_HispanicOrLatino_computed": [
        "Female_HispanicOrLatino_Black", "Female_HispanicOrLatino_White",
        "Female_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_HispanicOrLatino_AsianOrPacificIslander"
    ],
    "Male_HispanicOrLatino_computed": [
        "Male_HispanicOrLatino_Black", "Male_HispanicOrLatino_White",
        "Male_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_HispanicOrLatino_AsianOrPacificIslander"
    ]
}

_state_1990_1999_dict = {
    "Male_NotHispanicOrLatino_computed": [
        "Male_WhiteAloneNotHispanicOrLatino", "Male_NotHispanicOrLatino_Black",
        "Male_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_NotHispanicOrLatino_AsianOrPacificIslander"
    ],
    "Female_NotHispanicOrLatino_computed": [
        "Female_WhiteAloneNotHispanicOrLatino",
        "Female_NotHispanicOrLatino_Black",
        "Female_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_NotHispanicOrLatino_AsianOrPacificIslander"
    ],
    "Male_HispanicOrLatino_computed": [
        "Male_HispanicOrLatino_WhiteAlone", "Male_HispanicOrLatino_Black",
        "Male_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_HispanicOrLatino_AsianOrPacificIslander"
    ],
    "Female_HispanicOrLatino_computed": [
        "Female_HispanicOrLatino_WhiteAlone", "Female_HispanicOrLatino_Black",
        "Female_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_HispanicOrLatino_AsianOrPacificIslander"
    ],
    "WhiteAloneNotHispanicOrLatino_computed": [
        "Male_WhiteAloneNotHispanicOrLatino",
        "Female_WhiteAloneNotHispanicOrLatino"
    ],
    "NotHispanicOrLatino_Black_computed": [
        "Male_NotHispanicOrLatino_Black", "Female_NotHispanicOrLatino_Black"
    ],
    "HispanicOrLatino_WhiteAlone_computed": [
        "Male_HispanicOrLatino_WhiteAlone", "Female_HispanicOrLatino_WhiteAlone"
    ],
    "HispanicOrLatino_Black_computed": [
        "Male_HispanicOrLatino_Black", "Female_HispanicOrLatino_Black"
    ],
    "NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed": [
        "Male_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone"
    ],
    "HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone_computed": [
        "Male_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone"
    ],
    "NotHispanicOrLatino_AsianOrPacificIslander_computed": [
        "Male_HispanicOrLatino_AsianOrPacificIslander",
        "Female_HispanicOrLatino_AsianOrPacificIslander"
    ],
    "HispanicOrLatino_AsianOrPacificIslander_computed": [
        "Male_HispanicOrLatino_AsianOrPacificIslander",
        "Female_HispanicOrLatino_AsianOrPacificIslander"
    ],
    "HispanicOrLatino_computed": [
        "Male_HispanicOrLatino_WhiteAlone", "Male_HispanicOrLatino_Black",
        "Male_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_HispanicOrLatino_AsianOrPacificIslander",
        "Female_HispanicOrLatino_WhiteAlone", "Female_HispanicOrLatino_Black",
        "Female_HispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_HispanicOrLatino_AsianOrPacificIslander"
    ],
    "NotHispanicOrLatino_computed": [
        "Male_WhiteAloneNotHispanicOrLatino", "Male_NotHispanicOrLatino_Black",
        "Male_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Male_NotHispanicOrLatino_AsianOrPacificIslander",
        "Female_WhiteAloneNotHispanicOrLatino",
        "Female_NotHispanicOrLatino_Black",
        "Female_NotHispanicOrLatino_AmericanIndianAndAlaskaNativeAlone",
        "Female_NotHispanicOrLatino_AsianOrPacificIslander"
    ]
}


def _state_1990_1999():
    return _state_1990_1999_dict


def _state_1980_1989():
    return _state_1980_1989_dict


def _county_1900_1999():
    return _county_1900_1999_dict


def _county_2010_2020():
    return _county_2010_2020_dict


def _county_2000_2009():
    return _county_2000_2009_dict


def _nationals_2010_2021():
    return _nationals_2010_2021_dict


def _get_state_2010_2020(dict_name):
    if dict_name == "derived":
        return _state_2010_2020_hispanic_dict
    return _state_2010_2020_total_dict


def _get_nationals_2000_2009():
    return _nationals_2000_2009_dict


def _get_nationals_1980_1999(dict_name):
    if dict_name == "hispanic":
        return _nationals_1980_1999_hispanic_cols
    return _nationals_1980_1999_derived_cols
