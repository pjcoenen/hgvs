# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from nose.plugins.attrib import attr

from hgvs.exceptions import HGVSUnsupportedOperationError, HGVSInvalidVariantError, HGVSInvalidVariantError
import hgvs.dataproviders.uta
import hgvs.variantmapper
import hgvs.parser
import hgvs.normalizer

hdp = hgvs.dataproviders.uta.connect(mode="run", cache="tests/data/cache.hdp")


@attr(tags=["normalization"])
class Test_HGVSNormalizer(unittest.TestCase):
    """Tests for normalizer"""

    @classmethod
    def setUpClass(cls):
        cls.hp = hgvs.parser.Parser()
        cls.norm = hgvs.normalizer.Normalizer(hdp, shuffle_direction=3, cross_boundaries=True)
        cls.norm5 = hgvs.normalizer.Normalizer(hdp, shuffle_direction=5, cross_boundaries=True)
        cls.normc = hgvs.normalizer.Normalizer(hdp, shuffle_direction=3, cross_boundaries=False)
        cls.norm5c = hgvs.normalizer.Normalizer(hdp, shuffle_direction=5, cross_boundaries=False)

    def test_c_normalizer(self):
        """Test normalizer for variant type c."""
        #3' shuffling
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NM_000088.3:c.589_600inv"))),
                         "NM_000088.3:c.590_599inv")
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NM_001166478.1:c.31del"))),
                         "NM_001166478.1:c.35delT")
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NM_001166478.1:c.35_36insT"))),
                         "NM_001166478.1:c.35dupT")
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NM_001166478.1:c.36_37insTC"))),
                         "NM_001166478.1:c.36_37dupCT")
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NM_001166478.1:c.35_36dup"))),
                         "NM_001166478.1:c.36_37dupCT")
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NM_001166478.1:c.2_7delinsTTTAGA"))),
                         "NM_001166478.1:c.3_4delGAinsTT")
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NM_001166478.1:c.30_31insT"))),
                         "NM_001166478.1:c.35dupT")
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NM_001166478.1:c.59delG"))),
                         "NM_001166478.1:c.61delG")
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NM_001166478.1:c.36_37insTCTCTC"))),
                         "NM_001166478.1:c.37_38insCTCTCT")
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NM_000051.3:c.14_15insT"))),
                         "NM_000051.3:c.15dupT")

        #5' shuffling
        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant("NM_000088.3:c.589_600inv"))),
                         "NM_000088.3:c.590_599inv")
        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant("NM_001166478.1:c.34del"))),
                         "NM_001166478.1:c.31delT")
        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant("NM_001166478.1:c.35_36insT"))),
                         "NM_001166478.1:c.31dupT")
        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant("NM_001166478.1:c.36_37insTC"))),
                         "NM_001166478.1:c.35_36dupTC")
        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant("NM_001166478.1:c.35_36dup"))),
                         "NM_001166478.1:c.35_36dupTC")
        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant("NM_001166478.1:c.2_7delinsTTTAGA"))),
                         "NM_001166478.1:c.3_4delGAinsTT")
        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant("NM_001166478.1:c.30_31insT"))),
                         "NM_001166478.1:c.31dupT")
        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant("NM_001166478.1:c.61delG"))),
                         "NM_001166478.1:c.59delG")
        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant("NM_001166478.1:c.36_37insTCTCTC"))),
                         "NM_001166478.1:c.34_35insTCTCTC")
        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant("NM_000051.3:c.14_15insT"))),
                         "NM_000051.3:c.14dupT")

        #Around exon-intron boundary
        self.assertEqual(str(self.normc.normalize(self.hp.parse_hgvs_variant("NM_001166478.1:c.59delG"))),
                         "NM_001166478.1:c.60delG")
        self.assertEqual(str(self.norm5c.normalize(self.hp.parse_hgvs_variant("NM_001166478.1:c.61delG"))),
                         "NM_001166478.1:c.61delG")
        self.assertEqual(str(self.norm5c.normalize(self.hp.parse_hgvs_variant("NM_001110792.1:c.1030_1035del"))),
                         "NM_001110792.1:c.1029_1034delGAGCGG")
        with self.assertRaises(HGVSUnsupportedOperationError):
            self.normc.normalize(self.hp.parse_hgvs_variant("NM_001166478.1:c.59_61del"))

        #UTR variants
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NM_000051.3:c.-5_-4insA"))),
                         "NM_000051.3:c.-3dupA")
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NM_000051.3:c.-4_-3insAC"))),
                         "NM_000051.3:c.-3_-2dupAC")
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NM_000051.3:c.-2_-1insCA"))),
                         "NM_000051.3:c.-1_1dupCA")

        self.assertEqual(str(self.normc.normalize(self.hp.parse_hgvs_variant("NM_000051.3:c.-2_-1insCA"))),
                         "NM_000051.3:c.-1_1insAC")

        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant("NM_000051.3:c.-4_-3insA"))),
                         "NM_000051.3:c.-4dupA")
        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant("NM_000051.3:c.1_2insCA"))),
                         "NM_000051.3:c.-1_1dupCA")

        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NM_000051.3:c.*2_*3insT"))),
                         "NM_000051.3:c.*4dupT")
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NM_000051.3:c.9170_9171insAT"))),
                         "NM_000051.3:c.9171_*1dupAT")

        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant("NM_000051.3:c.*4_*5insT"))),
                         "NM_000051.3:c.*3dupT")
        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant("NM_000051.3:c.9171_*1insA"))),
                         "NM_000051.3:c.9171dupA")

        with self.assertRaises(HGVSInvalidVariantError):
            self.norm.normalize(self.hp.parse_hgvs_variant("NM_000059.3:c.7790delAAG"))

    def test_g_normalizer(self):
        """Test normalizer for variant type g."""
        #3' shuffling
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NC_000006.11:g.49917122_49917123insA"))),
                         "NC_000006.11:g.49917127dupA")
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NC_000006.11:g.49917121_49917122insGA"))),
                         "NC_000006.11:g.49917122_49917123dupGA")
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NC_000006.11:g.49917122_49917123dup"))),
                         "NC_000006.11:g.49917122_49917123dupGA")
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NC_000006.11:g.49917122_49917123dupGA"))),
                         "NC_000006.11:g.49917122_49917123dupGA")
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant("NC_000006.11:g.49917098delC"))),
                         "NC_000006.11:g.49917099delC")
        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant(
            "NC_000006.11:g.49917151_49917156delinsTCTAAA"))), "NC_000006.11:g.49917154_49917155delTCinsAA")

        #5' shuffling
        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant("NC_000006.11:g.49917122_49917123insA"))),
                         "NC_000006.11:g.49917123dupA")
        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant("NC_000006.11:g.49917121_49917122insGA"))),
                         "NC_000006.11:g.49917121_49917122dupAG")
        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant("NC_000006.11:g.49917122_49917123dup"))),
                         "NC_000006.11:g.49917121_49917122dupAG")
        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant("NC_000006.11:g.49917122_49917123dupGA"))),
                         "NC_000006.11:g.49917121_49917122dupAG")
        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant("NC_000006.11:g.49917099delC"))),
                         "NC_000006.11:g.49917098delC")
        self.assertEqual(str(self.norm5.normalize(self.hp.parse_hgvs_variant(
            "NC_000006.11:g.49917151_49917156delinsTCTAAA"))), "NC_000006.11:g.49917154_49917155delTCinsAA")

        self.assertEqual(str(self.norm.normalize(self.hp.parse_hgvs_variant(
            "NC_000009.11:g.36233991_36233992delCAinsTG"))), "NC_000009.11:g.36233991_36233992inv")
        with self.assertRaises(HGVSInvalidVariantError):
            self.norm.normalize(self.hp.parse_hgvs_variant("NG_032871.1:g.32476_53457delinsAATTAAGGTATA"))

        with self.assertRaises(HGVSInvalidVariantError):
            self.norm.normalize(self.hp.parse_hgvs_variant("NG_032871.1:g.32476_53457delinsAATTAAGGTATA"))

if __name__ == "__main__":
    unittest.main()

# <LICENSE>
# Copyright 2015 HGVS Contributors (https://bitbucket.org/biocommons/hgvs)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# </LICENSE>
