#!/usr/bin/python

################################################################################

def default_text():
    return '\n'.join([
        '-----------------------------------------------------------------------------------------------------------------------------',
        '      Item           Level        Part Number     Source Code      Unit Cost        Quantity         Costed           Cost     ',
        '-----------------------------------------------------------------------------------------------------------------------------',
        '       1               1             P-0001            1              1000             2               Y              2000     ',
        '       2               1             P-0002            1              1000             2               N               0       ',
        '       3                2            P-0003           120             2000             2               N               0       ',
        '       4                2            P-0004            11             1500             1               N               0       ',
        '       5                2            P-0005            78             100              1               N               0       ',
        '       6                2            P-0006           007             700              2               N               0       ',
        '       7                2            P-0007           007             700              2               Y              1400     ',
        '       8               1             P-0008            13             1000             1               N               0       ',
        '       9                2            P-0009            12             2000             1               Y              2000     ',
        '       10               2            P-0010            15             1500             3               N               0       ',
        '       11               2            P-0011            48             1000             1               N               0       ',
        '       12               2            P-0012            8               1               1               N               0       ',
        '       13               2            P-0013           007             700              1               N               0       ',
        '       14              1             P-0014            13             1000             2               N               0       ',
        '       15               2            P-0015           144             2000             1               N               0       ',
        '       16               2            P-0016            15             1500             1               N               0       ',
        '       17               2            P-0017            48             1000             1               N               0       ',
        '       18               2            P-0018            8               1               1               N               0       ',
        '       19               2            P-0019           007             700              1               N               0       ',
        '       20                3           P-0020           135             1000             1               N               0       ',
        '       21                3           P-0021           400              10              1               N               0       ',
        '       22                3           P-0022           600             2000             1               Y              2000     ',
        '       23               2            P-0023           007             800              1               Y              800      ',
        '       24              1             P-0024            12              1               5               Y               5       ',
        '       25              1             P-0025            12              1               5               Y               5       ',
        '       26              1             P-0026           145              90              1               N               0       ',
        '       27              1             P-0027           165             900              1               N               0       ',
        '-----------------------------------------------------------------------------------------------------------------------------',
        '     Totals                                                                            43              7              8210     ',
        '-----------------------------------------------------------------------------------------------------------------------------'
    ])

################################################################################

def custom_text():
    return '\n'.join([
        '--------------------------------------------------',
        '      Item        Part Number         Cost     ',
        '--------------------------------------------------',
        '       1             P-0001           2000     ',
        '       2             P-0002            0       ',
        '       3             P-0003            0       ',
        '       4             P-0004            0       ',
        '       5             P-0005            0       ',
        '       6             P-0006            0       ',
        '       7             P-0007           1400     ',
        '       8             P-0008            0       ',
        '       9             P-0009           2000     ',
        '       10            P-0010            0       ',
        '       11            P-0011            0       ',
        '       12            P-0012            0       ',
        '       13            P-0013            0       ',
        '       14            P-0014            0       ',
        '       15            P-0015            0       ',
        '       16            P-0016            0       ',
        '       17            P-0017            0       ',
        '       18            P-0018            0       ',
        '       19            P-0019            0       ',
        '       20            P-0020            0       ',
        '       21            P-0021            0       ',
        '       22            P-0022           2000     ',
        '       23            P-0023           800      ',
        '       24            P-0024            5       ',
        '       25            P-0025            5       ',
        '       26            P-0026            0       ',
        '       27            P-0027            0       ',
        '--------------------------------------------------',
        '     Totals                           8210     ',
        '--------------------------------------------------'
    ])

################################################################################

def custom_no_totals_text():
    return '\n'.join([
        '-----------------------------------',
        '      Item        Part Number  ',
        '-----------------------------------',
        '       1             P-0001    ',
        '       2             P-0002    ',
        '       3             P-0003    ',
        '       4             P-0004    ',
        '       5             P-0005    ',
        '       6             P-0006    ',
        '       7             P-0007    ',
        '       8             P-0008    ',
        '       9             P-0009    ',
        '       10            P-0010    ',
        '       11            P-0011    ',
        '       12            P-0012    ',
        '       13            P-0013    ',
        '       14            P-0014    ',
        '       15            P-0015    ',
        '       16            P-0016    ',
        '       17            P-0017    ',
        '       18            P-0018    ',
        '       19            P-0019    ',
        '       20            P-0020    ',
        '       21            P-0021    ',
        '       22            P-0022    ',
        '       23            P-0023    ',
        '       24            P-0024    ',
        '       25            P-0025    ',
        '       26            P-0026    ',
        '       27            P-0027    ',
        '-----------------------------------'
    ])

################################################################################

def default_xml():
    return '\n'.join([
        '<xml>',
        '<parts>',
        '<part><level>1</level><part_number>P-0001</part_number><source_code>1</source_code><unit_cost>1000</unit_cost><quantity>2</quantity><costed>Y</costed><cost>2000</cost></part>',
        '<part><level>1</level><part_number>P-0002</part_number><source_code>1</source_code><unit_cost>1000</unit_cost><quantity>2</quantity><costed>N</costed><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0003</part_number><source_code>120</source_code><unit_cost>2000</unit_cost><quantity>2</quantity><costed>N</costed><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0004</part_number><source_code>11</source_code><unit_cost>1500</unit_cost><quantity>1</quantity><costed>N</costed><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0005</part_number><source_code>78</source_code><unit_cost>100</unit_cost><quantity>1</quantity><costed>N</costed><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0006</part_number><source_code>007</source_code><unit_cost>700</unit_cost><quantity>2</quantity><costed>N</costed><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0007</part_number><source_code>007</source_code><unit_cost>700</unit_cost><quantity>2</quantity><costed>Y</costed><cost>1400</cost></part>',
        '<part><level>1</level><part_number>P-0008</part_number><source_code>13</source_code><unit_cost>1000</unit_cost><quantity>1</quantity><costed>N</costed><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0009</part_number><source_code>12</source_code><unit_cost>2000</unit_cost><quantity>1</quantity><costed>Y</costed><cost>2000</cost></part>',
        '<part><level>2</level><part_number>P-0010</part_number><source_code>15</source_code><unit_cost>1500</unit_cost><quantity>3</quantity><costed>N</costed><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0011</part_number><source_code>48</source_code><unit_cost>1000</unit_cost><quantity>1</quantity><costed>N</costed><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0012</part_number><source_code>8</source_code><unit_cost>1</unit_cost><quantity>1</quantity><costed>N</costed><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0013</part_number><source_code>007</source_code><unit_cost>700</unit_cost><quantity>1</quantity><costed>N</costed><cost>0</cost></part>',
        '<part><level>1</level><part_number>P-0014</part_number><source_code>13</source_code><unit_cost>1000</unit_cost><quantity>2</quantity><costed>N</costed><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0015</part_number><source_code>144</source_code><unit_cost>2000</unit_cost><quantity>1</quantity><costed>N</costed><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0016</part_number><source_code>15</source_code><unit_cost>1500</unit_cost><quantity>1</quantity><costed>N</costed><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0017</part_number><source_code>48</source_code><unit_cost>1000</unit_cost><quantity>1</quantity><costed>N</costed><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0018</part_number><source_code>8</source_code><unit_cost>1</unit_cost><quantity>1</quantity><costed>N</costed><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0019</part_number><source_code>007</source_code><unit_cost>700</unit_cost><quantity>1</quantity><costed>N</costed><cost>0</cost></part>',
        '<part><level>3</level><part_number>P-0020</part_number><source_code>135</source_code><unit_cost>1000</unit_cost><quantity>1</quantity><costed>N</costed><cost>0</cost></part>',
        '<part><level>3</level><part_number>P-0021</part_number><source_code>400</source_code><unit_cost>10</unit_cost><quantity>1</quantity><costed>N</costed><cost>0</cost></part>',
        '<part><level>3</level><part_number>P-0022</part_number><source_code>600</source_code><unit_cost>2000</unit_cost><quantity>1</quantity><costed>Y</costed><cost>2000</cost></part>',
        '<part><level>2</level><part_number>P-0023</part_number><source_code>007</source_code><unit_cost>800</unit_cost><quantity>1</quantity><costed>Y</costed><cost>800</cost></part>',
        '<part><level>1</level><part_number>P-0024</part_number><source_code>12</source_code><unit_cost>1</unit_cost><quantity>5</quantity><costed>Y</costed><cost>5</cost></part>',
        '<part><level>1</level><part_number>P-0025</part_number><source_code>12</source_code><unit_cost>1</unit_cost><quantity>5</quantity><costed>Y</costed><cost>5</cost></part>',
        '<part><level>1</level><part_number>P-0026</part_number><source_code>145</source_code><unit_cost>90</unit_cost><quantity>1</quantity><costed>N</costed><cost>0</cost></part>',
        '<part><level>1</level><part_number>P-0027</part_number><source_code>165</source_code><unit_cost>900</unit_cost><quantity>1</quantity><costed>N</costed><cost>0</cost></part>',
        '</parts>',
        '<totals><quantity>43</quantity><costed>7</costed><cost>8210</cost></totals>',
        '</xml>'
    ])

################################################################################

def custom_xml():
    return '\n'.join([
        '<xml>',
        '<parts>',
        '<part><level>1</level><part_number>P-0001</part_number><cost>2000</cost></part>',
        '<part><level>1</level><part_number>P-0002</part_number><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0003</part_number><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0004</part_number><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0005</part_number><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0006</part_number><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0007</part_number><cost>1400</cost></part>',
        '<part><level>1</level><part_number>P-0008</part_number><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0009</part_number><cost>2000</cost></part>',
        '<part><level>2</level><part_number>P-0010</part_number><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0011</part_number><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0012</part_number><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0013</part_number><cost>0</cost></part>',
        '<part><level>1</level><part_number>P-0014</part_number><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0015</part_number><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0016</part_number><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0017</part_number><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0018</part_number><cost>0</cost></part>',
        '<part><level>2</level><part_number>P-0019</part_number><cost>0</cost></part>',
        '<part><level>3</level><part_number>P-0020</part_number><cost>0</cost></part>',
        '<part><level>3</level><part_number>P-0021</part_number><cost>0</cost></part>',
        '<part><level>3</level><part_number>P-0022</part_number><cost>2000</cost></part>',
        '<part><level>2</level><part_number>P-0023</part_number><cost>800</cost></part>',
        '<part><level>1</level><part_number>P-0024</part_number><cost>5</cost></part>',
        '<part><level>1</level><part_number>P-0025</part_number><cost>5</cost></part>',
        '<part><level>1</level><part_number>P-0026</part_number><cost>0</cost></part>',
        '<part><level>1</level><part_number>P-0027</part_number><cost>0</cost></part>',
        '</parts>',
        '<totals><cost>8210</cost></totals>',
        '</xml>'
    ])

################################################################################

def custom_no_totals_xml():
    return '\n'.join([
        '<xml>',
        '<parts>',
        '<part><level>1</level><part_number>P-0001</part_number></part>',
        '<part><level>1</level><part_number>P-0002</part_number></part>',
        '<part><level>2</level><part_number>P-0003</part_number></part>',
        '<part><level>2</level><part_number>P-0004</part_number></part>',
        '<part><level>2</level><part_number>P-0005</part_number></part>',
        '<part><level>2</level><part_number>P-0006</part_number></part>',
        '<part><level>2</level><part_number>P-0007</part_number></part>',
        '<part><level>1</level><part_number>P-0008</part_number></part>',
        '<part><level>2</level><part_number>P-0009</part_number></part>',
        '<part><level>2</level><part_number>P-0010</part_number></part>',
        '<part><level>2</level><part_number>P-0011</part_number></part>',
        '<part><level>2</level><part_number>P-0012</part_number></part>',
        '<part><level>2</level><part_number>P-0013</part_number></part>',
        '<part><level>1</level><part_number>P-0014</part_number></part>',
        '<part><level>2</level><part_number>P-0015</part_number></part>',
        '<part><level>2</level><part_number>P-0016</part_number></part>',
        '<part><level>2</level><part_number>P-0017</part_number></part>',
        '<part><level>2</level><part_number>P-0018</part_number></part>',
        '<part><level>2</level><part_number>P-0019</part_number></part>',
        '<part><level>3</level><part_number>P-0020</part_number></part>',
        '<part><level>3</level><part_number>P-0021</part_number></part>',
        '<part><level>3</level><part_number>P-0022</part_number></part>',
        '<part><level>2</level><part_number>P-0023</part_number></part>',
        '<part><level>1</level><part_number>P-0024</part_number></part>',
        '<part><level>1</level><part_number>P-0025</part_number></part>',
        '<part><level>1</level><part_number>P-0026</part_number></part>',
        '<part><level>1</level><part_number>P-0027</part_number></part>',
        '</parts>',
        '</xml>'
    ])

################################################################################


