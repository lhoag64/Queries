import logging
from   collections                  import OrderedDict
from   summary.summary.summarydata  import SummaryData

#----------------------------------------------------------------------
class StdData(SummaryData):

  #--------------------------------------------------------------------
  def __init__(self,item,itemDict,nameDict,objNameDict):

    super().__init__(item,itemDict,nameDict,objNameDict)

    #logging.debug('ITEMS')
    #for item in itemDict:
    #  logging.debug(item)

    #logging.debug('NAMES')
    #for name in nameDict:
    #  logging.debug(name)

    title      = 'Summary Statement'
    regionList = self.regionList
    period     = self.period
    region     = self.regionList[0]
    prefix     = 'MATRIX.' + region + '.' + period + '.'

    #------------------------------------------------------------------
    # TODO: MAKE LIKE MATRIX
    #  TITLE
    #  ROW-DATA-HDR
    #  COL-DATA-HDR
    #  TBL-DATA 
    #------------------------------------------------------------------
    self.title = self._calcTitleText(title,regionList,period)

    hdrDict          = OrderedDict()
    hdrDict['TITLE'] = OrderedDict()
    rows = 1
    cols = 1
    data = [[None for col in range(cols)] for row in range(rows)]
    data[0][0] = self.title
    hdrDict['TITLE']['DATA'   ] = data
    hdrDict['TITLE']['ROWS'   ] = rows
    hdrDict['TITLE']['COLS'   ] = cols
    hdrDict['TITLE']['MERGED' ] = [(0,0,1,3)]
    hdrDict['TITLE']['HGT'    ] = [(0,52)]
    hdrDict['TITLE']['FMT'    ] = self.fmt1a
    hdrDict['ROWS'] = rows
    hdrDict['COLS'] = cols

    #------------------------------------------------------------------
    hrsDict          = OrderedDict()
    hrsDict['TITLE'] = OrderedDict()
    rows = 1
    cols = 3
    data = [['' for col in range(cols)] for row in range(rows)]
    data[0][0] = 'Hours'
    data[0][1] = 'Hours'
    data[0][2] = 'As a % Contracted'
    hrsDict['TITLE']['DATA'  ] = data
    hrsDict['TITLE']['ROWS'  ] = rows
    hrsDict['TITLE']['COLS'  ] = cols
    hrsDict['TITLE']['BORDER'] = [(0,0,rows,cols,'medium')]
    fmt = [[self.fmt2b for col in range(cols)] for row in range(rows)]
    fmt[0][0] = self.fmt2a
    hrsDict['TITLE']['FMT'   ] = fmt

    conHrs = prefix + 'UTL_OT.X.TBL_DATA.CONTRACTED.RANGE'
    totHrs = prefix + 'UTL_CF.X.TBL_DATA.TOTAL_TIME.RANGE'
    addHrs = prefix + 'UTL_OT.X.TBL_DATA.ADDITIONAL.RANGE'
    hc     = prefix + 'FAE_WH.X.ROW_COMP_TBL.' + region + '_HEADCOUNT.RANGE'

    conRange = self.objNameDict[conHrs]
    totRange = self.objNameDict[totHrs]
    addRange = self.objNameDict[addHrs]
    hcRange  = self.objNameDict[hc    ]

    conHrs = '=SUM(' + conRange[1] + '.' + conHrs + ')'
    totHrs = '=SUM(' + totRange[1] + '.' + totHrs + ')'
    addHrs = '=SUM(' + addRange[1] + '.' + addHrs + ')'
    hc     = '=AVERAGE(' + hcRange[1]  + '.' + hc + ')'

    hrsDict['DATA'] = OrderedDict()
    rows = 4
    cols = 3
    data = [['' for col in range(cols)] for row in range(rows)]
    data[0][0] = 'Contracted Number of Hours'
    data[1][0] = 'Total Hours Booked'
    data[2][0] = 'Additional Hours Worked over Contracted'
    data[3][0] = 'Number of Heads'
    data[0][1] = conHrs
    data[1][1] = totHrs
    data[2][1] = addHrs
    data[3][1] = hc
    hrsDict['DATA']['DATA'  ] = data
    hrsDict['DATA']['ROWS'  ] = rows
    hrsDict['DATA']['COLS'  ] = cols
    hrsDict['DATA']['BORDER'] = [(0,0,rows,cols,'medium')]
    fmt = [[self.fmt2f for col in range(cols)] for row in range(rows)]
    fmt[0][0] = self.fmt2c
    fmt[1][0] = self.fmt2c
    fmt[2][0] = self.fmt2c
    fmt[3][0] = self.fmt2c
    hrsDict['DATA']['FMT'   ] = fmt

    hrsDict['ROWS'] = hrsDict['TITLE']['ROWS'] + hrsDict['DATA']['ROWS']
    hrsDict['COLS'] = hrsDict['TITLE']['COLS'] + hrsDict['DATA']['COLS']

    #------------------------------------------------------------------
    actSDict          = OrderedDict()
    actSDict['TITLE'] = OrderedDict()
    rows = 1
    cols = 3
    data = [['' for col in range(cols)] for row in range(rows)]
    data[0][0] = 'Activity (Summary - Average Across Period)'
    data[0][1] = 'Hours'
    data[0][2] = 'Percentage %'
    actSDict['TITLE']['DATA'  ] = data
    actSDict['TITLE']['ROWS'  ] = rows
    actSDict['TITLE']['COLS'  ] = cols
    actSDict['TITLE']['BORDER'] = [(0,0,rows,cols,'medium')]
    fmt = [[self.fmt2b for col in range(cols)] for row in range(rows)]
    fmt[0][0] = self.fmt2a
    actSDict['TITLE']['FMT'   ] = fmt

    utlCf = prefix + 'UTL_CF.X.ROW_COMP_TBL.UTILISATION_AS_A_PCT.RANGE'
    utlPs = prefix + 'UTL_PS.X.ROW_COMP_TBL.UTILISATION_AS_A_PCT.RANGE'
    utlDt = prefix + 'UTL_DT.X.ROW_COMP_TBL.UTILISATION_AS_A_PCT.RANGE'
    utlLs = prefix + 'UTL_LS.X.ROW_COMP_TBL.UTILISATION_AS_A_PCT.RANGE'

    utlCfRange = self.objNameDict[utlCf]
    utlPsRange = self.objNameDict[utlPs]
    utlDtRange = self.objNameDict[utlDt]
    utlLsRange = self.objNameDict[utlLs]

    utlCf = '=AVERAGE(' + utlCfRange[1] + '.' + utlCf + ')'
    utlPs = '=AVERAGE(' + utlPsRange[1] + '.' + utlPs + ')'
    utlDt = '=AVERAGE(' + utlDtRange[1] + '.' + utlDt + ')'
    utlLs = '=AVERAGE(' + utlLsRange[1] + '.' + utlLs + ')'

    actSDict['DATA'] = OrderedDict()
    rows = 4
    cols = 3
    data = [[None for col in range(cols)] for row in range(rows)]
    data[0][0] = 'Utilisation (Customer Funded Works)'
    data[1][0] = 'Utilisation (Pre-Sales Work)'
    data[2][0] = 'Utilisation (Downtime, Exc Leave and Sickness)'
    data[3][0] = 'Utilisation (Leave and Sickness)'
    data[0][1] = utlCf
    data[1][1] = utlPs
    data[2][1] = utlDt
    data[3][1] = utlLs
    data[0][2] = ''
    data[1][2] = ''
    data[2][2] = ''
    data[3][2] = ''
    actSDict['DATA']['DATA'  ] = data
    actSDict['DATA']['ROWS'  ] = rows
    actSDict['DATA']['COLS'  ] = cols
    actSDict['DATA']['BORDER'] = [(0,0,rows,cols,'medium')]
    fmt = [['' for col in range(cols)] for row in range(rows)]
    fmt[0][0] = self.fmt4; fmt[0][1] = self.fmt4b; fmt[0][2] = self.fmt3b
    fmt[1][0] = self.fmt5; fmt[1][1] = self.fmt5b; fmt[1][2] = self.fmt5b
    fmt[2][0] = self.fmt6; fmt[2][1] = self.fmt6b; fmt[2][2] = self.fmt6b
    fmt[3][0] = self.fmt7; fmt[3][1] = self.fmt7b; fmt[3][2] = self.fmt7b
    actSDict['DATA']['FMT'   ] = fmt

    actSDict['ROWS'] = actSDict['TITLE']['ROWS'] + actSDict['DATA']['ROWS']
    actSDict['COLS'] = actSDict['TITLE']['COLS'] + actSDict['DATA']['COLS']

    #------------------------------------------------------------------
    actDDict          = OrderedDict()
    actDDict['TITLE'] = OrderedDict()
    rows = 1
    cols = 3
    data = [[None for col in range(cols)] for row in range(rows)]
    data[0][0] = 'Activity (Detailed)'
    data[0][1] = 'Hours'
    data[0][2] = 'As a % of Total'
    actDDict['TITLE']['DATA'  ] = data
    actDDict['TITLE']['ROWS'  ] = rows
    actDDict['TITLE']['COLS'  ] = cols
    actDDict['TITLE']['BORDER'] = [(0,0,rows,cols,'medium')]
    fmt = [[self.fmt2b for col in range(cols)] for row in range(rows)]
    fmt[0][0] = self.fmt2a
    actDDict['TITLE']['FMT'   ] = fmt

    act = [0.0 for row in range(16)]
    act[ 0] = prefix + 'ACTIVITY.X.TBL_DATA.SUPPORT_AGREEMENT_SOFTWARE_10.RANGE'
    act[ 1] = prefix + 'ACTIVITY.X.TBL_DATA.SUPPORT_AGREEMENT_HARDWARE_11.RANGE'
    act[ 2] = prefix + 'ACTIVITY.X.TBL_DATA.POST_SALES_SUPPORT_SW_CUSTOMER_FUNDED_14.RANGE'
    act[ 3] = prefix + 'ACTIVITY.X.TBL_DATA.POST_SALES_SUPPORT_HW_CUSTOMER_FUNDED_15.RANGE'
    act[ 4] = prefix + 'ACTIVITY.X.TBL_DATA.NRE_CUSTOMER_FUNDED_16.RANGE'
    act[ 5] = prefix + 'ACTIVITY.X.TBL_DATA.TRAINING_PROVIDING_NON_CUSTOMER_SPECIFIC_17.RANGE'
    act[ 6] = prefix + 'ACTIVITY.X.TBL_DATA.TRAINING_PROVIDING_CUSTOMER_SPECIFIC_18.RANGE'
    act[ 7] = prefix + 'ACTIVITY.X.TBL_DATA.POST_SALES_SUPPORT_WARRANTY_PERIOD_23.RANGE'
    act[ 8] = prefix + 'ACTIVITY.X.TBL_DATA.PRE_SALES_SUPPORT_12.RANGE'
    act[ 9] = prefix + 'ACTIVITY.X.TBL_DATA.POST_SALES_SUPPORT_NON_CONTRACT_13.RANGE'
    act[10] = prefix + 'ACTIVITY.X.TBL_DATA.TRAINING_RECEIVING_NON_CUSTOMER_SPECIFIC_19.RANGE'
    act[11] = prefix + 'ACTIVITY.X.TBL_DATA.TRAINING_RECEIVING_CUSTOMER_SPECIFIC_20.RANGE'
    act[12] = prefix + 'ACTIVITY.X.TBL_DATA.INTERNAL_BUSINESS_MEETING_21.RANGE'
    act[13] = prefix + 'ACTIVITY.X.TBL_DATA.PROFESSIONAL_SERVICES_22.RANGE'
    act[14] = prefix + 'UTL_DT.X.TBL_DATA.FOR.RANGE'
    act[15] = prefix + 'UTL_LS.X.TBL_DATA.FOR.RANGE'

    rng = [0.0 for row in range(16)]
    rng[ 0] = self.objNameDict[act[ 0]]
    rng[ 1] = self.objNameDict[act[ 1]]
    rng[ 2] = self.objNameDict[act[ 2]]
    rng[ 3] = self.objNameDict[act[ 3]]
    rng[ 4] = self.objNameDict[act[ 4]]
    rng[ 5] = self.objNameDict[act[ 5]]
    rng[ 6] = self.objNameDict[act[ 6]]
    rng[ 7] = self.objNameDict[act[ 7]]
    rng[ 8] = self.objNameDict[act[ 8]]
    rng[ 9] = self.objNameDict[act[ 9]]
    rng[10] = self.objNameDict[act[10]]
    rng[11] = self.objNameDict[act[11]]
    rng[12] = self.objNameDict[act[12]]
    rng[13] = self.objNameDict[act[13]]
    rng[14] = self.objNameDict[act[14]]
    rng[15] = self.objNameDict[act[15]]

    act[ 0] = '=SUM(' + rng[ 0][1] + '.' + act[ 0] + ')'
    act[ 1] = '=SUM(' + rng[ 1][1] + '.' + act[ 1] + ')'
    act[ 2] = '=SUM(' + rng[ 2][1] + '.' + act[ 2] + ')'
    act[ 3] = '=SUM(' + rng[ 3][1] + '.' + act[ 3] + ')'
    act[ 4] = '=SUM(' + rng[ 4][1] + '.' + act[ 4] + ')'
    act[ 5] = '=SUM(' + rng[ 5][1] + '.' + act[ 5] + ')'
    act[ 6] = '=SUM(' + rng[ 6][1] + '.' + act[ 6] + ')'
    act[ 7] = '=SUM(' + rng[ 7][1] + '.' + act[ 7] + ')'
    act[ 8] = '=SUM(' + rng[ 8][1] + '.' + act[ 8] + ')'
    act[ 9] = '=SUM(' + rng[ 9][1] + '.' + act[ 9] + ')'
    act[10] = '=SUM(' + rng[10][1] + '.' + act[10] + ')'
    act[11] = '=SUM(' + rng[11][1] + '.' + act[11] + ')'
    act[12] = '=SUM(' + rng[12][1] + '.' + act[12] + ')'
    act[13] = '=SUM(' + rng[13][1] + '.' + act[13] + ')'
    act[14] = '=SUM(' + rng[14][1] + '.' + act[14] + ')'
    act[15] = '=SUM(' + rng[15][1] + '.' + act[15] + ')'

    actDDict['DATA'] = OrderedDict()
    rows = 16
    cols =  3
    data = [['' for col in range(cols)] for row in range(rows)]
    data[ 0][0] = 'Support Agreement (Software)'
    data[ 1][0] = 'Support Agreement (Hardware)'
    data[ 2][0] = 'Post-Sales Support (Software - Customer Funded)'
    data[ 3][0] = 'Post-Sales Support (Hardware - Customer Funded)'
    data[ 4][0] = 'NRE (Customer Funded)'
    data[ 5][0] = 'Training - Providing - Non-Customer Specific'
    data[ 6][0] = 'Training - Providing - Customer Spectific'
    data[ 7][0] = 'Post-Sales Support (Warrant Period)'
    data[ 8][0] = 'Pre-Sales Support'
    data[ 9][0] = 'Post-Sales Support (Non Contract)'
    data[10][0] = 'Training - Receiving - Non-Customer Specific'
    data[11][0] = 'Training - Receiving - Customer Specific'
    data[12][0] = 'Internal Business Meeting'
    data[13][0] = 'Professional Services'
    data[14][0] = 'Downtime (Exc Leave and Sickness)'
    data[15][0] = 'Leave and Sickness'
    data[ 0][1] = act[ 0]
    data[ 1][1] = act[ 1]
    data[ 2][1] = act[ 2]
    data[ 3][1] = act[ 3]
    data[ 4][1] = act[ 4]
    data[ 5][1] = act[ 5]
    data[ 6][1] = act[ 6]
    data[ 7][1] = act[ 7]
    data[ 8][1] = act[ 8]
    data[ 9][1] = act[ 9]
    data[10][1] = act[10]
    data[11][1] = act[11]
    data[12][1] = act[12]
    data[13][1] = act[13]
    data[14][1] = act[14]
    data[15][1] = act[15]
    data[ 0][2] = '=D20/SUM(D20:D27)*100'
    data[ 1][2] = '=D21/SUM(D20:D27)*100'
    data[ 2][2] = '=D22/SUM(D20:D27)*100'
    data[ 3][2] = '=D23/SUM(D20:D27)*100'
    data[ 4][2] = '=D24/SUM(D20:D27)*100'
    data[ 5][2] = '=D25/SUM(D20:D27)*100'
    data[ 6][2] = '=D26/SUM(D20:D27)*100'
    data[ 7][2] = '=D27/SUM(D20:D27)*100'
    data[ 8][2] = '=D28/SUM(D28:D33)*100'
    data[ 9][2] = '=D29/SUM(D28:D33)*100'
    data[10][2] = '=D30/SUM(D28:D33)*100'
    data[11][2] = '=D31/SUM(D28:D33)*100'
    data[12][2] = '=D32/SUM(D28:D33)*100'
    data[13][2] = '=D33/SUM(D28:D33)*100'
    data[14][2] = '=D34/D34*100'
    data[15][2] = '=D35/D35*100'
    actDDict['DATA']['DATA'  ] = data
    actDDict['DATA']['ROWS'  ] = rows
    actDDict['DATA']['COLS'  ] = cols
    actDDict['DATA']['BORDER'] = [(0,0,rows,cols,'medium')]
    fmt = [['' for col in range(cols)] for row in range(rows)]
    fmt[ 0][0] = self.fmt4; fmt[ 0][1] = self.fmt4b; fmt[ 0][2] = self.fmt4b
    fmt[ 1][0] = self.fmt4; fmt[ 1][1] = self.fmt4b; fmt[ 1][2] = self.fmt4b
    fmt[ 2][0] = self.fmt4; fmt[ 2][1] = self.fmt4b; fmt[ 2][2] = self.fmt4b
    fmt[ 3][0] = self.fmt4; fmt[ 3][1] = self.fmt4b; fmt[ 3][2] = self.fmt4b
    fmt[ 4][0] = self.fmt4; fmt[ 4][1] = self.fmt4b; fmt[ 4][2] = self.fmt4b
    fmt[ 5][0] = self.fmt4; fmt[ 5][1] = self.fmt4b; fmt[ 5][2] = self.fmt4b
    fmt[ 6][0] = self.fmt4; fmt[ 6][1] = self.fmt4b; fmt[ 6][2] = self.fmt4b
    fmt[ 7][0] = self.fmt4; fmt[ 7][1] = self.fmt4b; fmt[ 7][2] = self.fmt4b
    fmt[ 8][0] = self.fmt5; fmt[ 8][1] = self.fmt5b; fmt[ 8][2] = self.fmt5b
    fmt[ 9][0] = self.fmt5; fmt[ 9][1] = self.fmt5b; fmt[ 9][2] = self.fmt5b
    fmt[10][0] = self.fmt5; fmt[10][1] = self.fmt5b; fmt[10][2] = self.fmt5b
    fmt[11][0] = self.fmt5; fmt[11][1] = self.fmt5b; fmt[11][2] = self.fmt5b
    fmt[12][0] = self.fmt5; fmt[12][1] = self.fmt5b; fmt[12][2] = self.fmt5b
    fmt[13][0] = self.fmt5; fmt[13][1] = self.fmt5b; fmt[13][2] = self.fmt5b
    fmt[14][0] = self.fmt6; fmt[14][1] = self.fmt6b; fmt[14][2] = self.fmt6b
    fmt[15][0] = self.fmt7; fmt[15][1] = self.fmt7b; fmt[15][2] = self.fmt7b
    actDDict['DATA']['FMT'   ] = fmt

    actDDict['ROWS'] = actDDict['TITLE']['ROWS'] + actDDict['DATA']['ROWS']
    actDDict['COLS'] = actDDict['TITLE']['COLS'] + actDDict['DATA']['COLS']

    #------------------------------------------------------------------
    gkaDict          = OrderedDict()
    gkaDict['TITLE'] = OrderedDict()
    rows = 1
    cols = 3
    data = [['' for col in range(cols)] for row in range(rows)]
    data[0][0] = 'Customer Split'
    data[0][1] = 'Hours'
    data[0][2] = 'As a % of Total'
    gkaDict['TITLE']['DATA'  ] = data
    gkaDict['TITLE']['ROWS'  ] = rows
    gkaDict['TITLE']['COLS'  ] = cols
    gkaDict['TITLE']['BORDER'] = [(0,0,rows,cols,'medium')]
    fmt = [[self.fmt2b for col in range(cols)] for row in range(rows)]
    fmt[0][0] = self.fmt2a
    gkaDict['TITLE']['FMT'   ] = fmt

    gka = [0.0 for row in range(9)]
    gka[ 0] = prefix + 'GKA.X.TBL_DATA.ERICSSON.RANGE'
    gka[ 1] = prefix + 'GKA.X.TBL_DATA.NOKIA.RANGE'
    gka[ 2] = prefix + 'GKA.X.TBL_DATA.ALCATEL_LUCENT.RANGE'
    gka[ 3] = prefix + 'GKA.X.TBL_DATA.NOKIA_ALU_COMBINED.RANGE'
    gka[ 4] = prefix + 'GKA.X.TBL_DATA.ALL_OTHERS.RANGE'
    gka[ 5] = prefix + 'GKA.X.TBL_DATA.COBHAM.RANGE'
    gka[ 6] = prefix + 'GKA.X.TBL_DATA.TRAINING_TECHNICAL_NON_CUSTOMER_SPECIFIC.RANGE'
    gka[ 7] = prefix + 'GKA.X.TBL_DATA.OTHER.RANGE'
    gka[ 8] = prefix + 'ACTIVITY.X.TBL_DATA.OTHER_OVERHEAD_LEAVE_ETC.RANGE'

    rng = [0.0 for row in range(9)]
    rng[ 0] = self.objNameDict[gka[ 0]]
    rng[ 1] = self.objNameDict[gka[ 1]]
    rng[ 2] = self.objNameDict[gka[ 2]]
    rng[ 3] = self.objNameDict[gka[ 3]]
    rng[ 4] = self.objNameDict[gka[ 4]]
    rng[ 5] = self.objNameDict[gka[ 5]]
    rng[ 6] = self.objNameDict[gka[ 6]]
    rng[ 7] = self.objNameDict[gka[ 7]]
    rng[ 8] = self.objNameDict[gka[ 8]]

    gka[ 0] = '=SUM(' + rng[ 0][1] + '.' + gka[ 0] + ')'
    gka[ 1] = '=SUM(' + rng[ 1][1] + '.' + gka[ 1] + ')'
    gka[ 2] = '=SUM(' + rng[ 2][1] + '.' + gka[ 2] + ')'
    gka[ 3] = '=SUM(' + rng[ 3][1] + '.' + gka[ 3] + ')'
    gka[ 4] = '=SUM(' + rng[ 4][1] + '.' + gka[ 4] + ')'
    gka[ 5] = '=SUM(' + rng[ 5][1] + '.' + gka[ 5] + ')'
    gka[ 6] = '=SUM(' + rng[ 6][1] + '.' + gka[ 6] + ')'
    gka[ 7] = '=SUM(' + rng[ 7][1] + '.' + gka[ 7] + ')'
    gka[ 8] = '=SUM(' + rng[ 8][1] + '.' + gka[ 8] + ')'

    gkaDict['DATA'] = OrderedDict()
    rows =  9
    cols =  3
    data = [['' for col in range(cols)] for row in range(rows)]
    data[ 0][0] = 'Ericsson'
    data[ 1][0] = 'Nokia'
    data[ 2][0] = 'Alcatel-Lucent'
    data[ 3][0] = 'Nokia/ALU Combined'
    data[ 4][0] = 'Sum of All Others Customers'
    data[ 5][0] = 'Cobham'
    data[ 6][0] = 'Technical Training - All Types'
    data[ 7][0] = 'Unspecified Customer'
    data[ 8][0] = 'Other (Leave, Overhead, etc.)'
    data[ 0][1] = gka[ 0]
    data[ 1][1] = gka[ 1]
    data[ 2][1] = gka[ 2]
    data[ 3][1] = gka[ 3]
    data[ 4][1] = gka[ 4]
    data[ 5][1] = gka[ 5]
    data[ 6][1] = gka[ 6]
    data[ 7][1] = gka[ 7]
    data[ 8][1] = gka[ 8]
    data[ 0][2] = '=D36/(SUM(D36:D38)+SUM(D40:D43))*100'
    data[ 1][2] = '=D37/(SUM(D36:D38)+SUM(D40:D43))*100'
    data[ 2][2] = '=D38/(SUM(D36:D38)+SUM(D40:D43))*100'
    data[ 3][2] = '=(D37+D38)/(SUM(D36:D38)+SUM(D40:D43))*100'
    data[ 4][2] = '=D40/(SUM(D36:D38)+SUM(D40:D43))*100'
    data[ 5][2] = '=D41/(SUM(D36:D38)+SUM(D40:D43))*100'
    data[ 6][2] = '=D42/(SUM(D36:D38)+SUM(D40:D43))*100'
    data[ 7][2] = '=D43/(SUM(D36:D38)+SUM(D40:D43))*100'
    data[ 8][2] = '=D44/D44*100'
    gkaDict['DATA']['DATA'  ] = data
    gkaDict['DATA']['ROWS'  ] = rows
    gkaDict['DATA']['COLS'  ] = cols
    gkaDict['DATA']['BORDER'] = [(0,0,rows,cols,'medium')]
    fmt = [[self.fmt2f for col in range(cols)] for row in range(rows)]
    fmt[ 0][0] = self.fmt2c
    fmt[ 1][0] = self.fmt2c
    fmt[ 2][0] = self.fmt2c
    fmt[ 3][0] = self.fmt2c
    fmt[ 4][0] = self.fmt2c
    fmt[ 5][0] = self.fmt2c
    fmt[ 6][0] = self.fmt2c
    fmt[ 7][0] = self.fmt2c
    fmt[ 8][0] = self.fmt2c
    gkaDict['DATA']['FMT'   ] = fmt

    gkaDict['ROWS'] = gkaDict['TITLE']['ROWS'] + gkaDict['DATA']['ROWS']
    gkaDict['COLS'] = gkaDict['TITLE']['COLS'] + gkaDict['DATA']['COLS']

    #------------------------------------------------------------------
    cfsDict          = OrderedDict()
    cfsDict['TITLE'] = OrderedDict()
    rows = 1
    cols = 3
    data = [['' for col in range(cols)] for row in range(rows)]
    data[0][0] = 'Financial Spend on Support Agreements (Period - Loaded Labour Hours)'
    data[0][1] = 'Cost'
    data[0][2] = 'Income'
    cfsDict['TITLE']['DATA'  ] = data
    cfsDict['TITLE']['ROWS'  ] = rows
    cfsDict['TITLE']['COLS'  ] = cols
    cfsDict['TITLE']['BORDER'] = [(0,0,rows,cols,'medium')]
    fmt = [[self.fmt2b for col in range(cols)] for row in range(rows)]
    fmt[0][0] = self.fmt2a
    cfsDict['TITLE']['FMT'   ] = fmt

    cfsDict['DATA'] = OrderedDict()
    rows =  6
    cols =  3
    data = [['TBC' for col in range(cols)] for row in range(rows)]
    data[ 0][0] = 'Ericsson'
    data[ 1][0] = 'Nokia'
    data[ 2][0] = 'Alcatel-Lucent'
    data[ 3][0] = 'Cobham'
    data[ 4][0] = 'Unspecified Customer'
    data[ 5][0] = 'Other (Leave, Overhead, etc.)'
    cfsDict['DATA']['DATA'  ] = data
    cfsDict['DATA']['ROWS'  ] = rows
    cfsDict['DATA']['COLS'  ] = cols
    cfsDict['DATA']['BORDER'] = [(0,0,rows,cols,'medium')]
    fmt = [[self.fmt4b for col in range(cols)] for row in range(rows)]
    fmt[ 0][0] = self.fmt4
    fmt[ 1][0] = self.fmt4
    fmt[ 2][0] = self.fmt4
    fmt[ 3][0] = self.fmt4
    fmt[ 4][0] = self.fmt4
    fmt[ 5][0] = self.fmt4
    cfsDict['DATA']['FMT'   ] = fmt

    cfsDict['ROWS'] = cfsDict['TITLE']['ROWS'] + cfsDict['DATA']['ROWS']
    cfsDict['COLS'] = cfsDict['TITLE']['COLS'] + cfsDict['DATA']['COLS']

    #------------------------------------------------------------------
    sfsDict          = OrderedDict()
    sfsDict['TITLE'] = OrderedDict()
    rows = 1
    cols = 3
    data = [['' for col in range(cols)] for row in range(rows)]
    data[0][0] = 'Financial Spend on Pre-Sales and Non-CF Support (Period - Loaded Labour Hours)'
    data[0][1] = 'Cost'
    data[0][2] = 'Income'
    sfsDict['TITLE']['DATA'] = data
    sfsDict['TITLE']['ROWS'] = rows
    sfsDict['TITLE']['COLS'] = cols
    sfsDict['TITLE']['BORDER'] = [(0,0,rows,cols,'medium')]
    fmt = [[self.fmt2b for col in range(cols)] for row in range(rows)]
    fmt[0][0] = self.fmt2a
    sfsDict['TITLE']['FMT'   ] = fmt

    sfsDict['DATA'] = OrderedDict()
    rows =  5
    cols =  3
    data = [['TBC' for col in range(cols)] for row in range(rows)]
    data[ 0][0] = 'Pre-Sales Support'
    data[ 1][0] = 'Post-Sales Support (No Contract)'
    data[ 2][0] = 'Training - Receiving - Non-Customer Specific'
    data[ 3][0] = 'Training - Receiving - Customer Specific'
    data[ 4][0] = 'Professional Services'
    sfsDict['DATA']['DATA'  ] = data
    sfsDict['DATA']['ROWS'  ] = rows
    sfsDict['DATA']['COLS'  ] = cols
    sfsDict['DATA']['BORDER'] = [(0,0,rows,cols,'medium')]
    fmt = [[self.fmt5b for col in range(cols)] for row in range(rows)]
    fmt[ 0][0] = self.fmt5
    fmt[ 1][0] = self.fmt5
    fmt[ 2][0] = self.fmt5
    fmt[ 3][0] = self.fmt5
    fmt[ 4][0] = self.fmt5
    sfsDict['DATA']['FMT'   ] = fmt

    sfsDict['ROWS'] = sfsDict['TITLE']['ROWS'] + sfsDict['DATA']['ROWS']
    sfsDict['COLS'] = sfsDict['TITLE']['COLS'] + sfsDict['DATA']['COLS']

    #------------------------------------------------------------------
    ltsDict          = OrderedDict()
    ltsDict['TITLE'] = OrderedDict()
    rows = 1
    cols = 3
    data = [['' for col in range(cols)] for row in range(rows)]
    data[0][0] = 'Labour, Travel, and Standby'
    data[0][1] = 'Hours'
    data[0][2] = 'As a % of Total'
    ltsDict['TITLE']['DATA'] = data
    ltsDict['TITLE']['ROWS'] = rows
    ltsDict['TITLE']['COLS'] = cols
    ltsDict['TITLE']['BORDER'] = [(0,0,rows,cols,'medium')]
    fmt = [[self.fmt2b for col in range(cols)] for row in range(rows)]
    fmt[0][0] = self.fmt2a
    ltsDict['TITLE']['FMT'   ] = fmt

    lts = [0.0 for row in range(3)]
    lts[ 0] = prefix + 'LTS.X.TBL_DATA.LABOUR.RANGE'
    lts[ 1] = prefix + 'LTS.X.TBL_DATA.TRAVEL.RANGE'
    lts[ 2] = prefix + 'LTS.X.TBL_DATA.STAND_BY.RANGE'

    rng = [0.0 for row in range(3)]
    rng[ 0] = self.objNameDict[lts[ 0]]
    rng[ 1] = self.objNameDict[lts[ 1]]
    rng[ 2] = self.objNameDict[lts[ 2]]

    lts[ 0] = '=SUM(' + rng[ 0][1] + '.' + lts[ 0] + ')'
    lts[ 1] = '=SUM(' + rng[ 1][1] + '.' + lts[ 1] + ')'
    lts[ 2] = '=SUM(' + rng[ 2][1] + '.' + lts[ 2] + ')'

    ltsDict['DATA'] = OrderedDict()
    rows =  3
    cols =  3
    data = [['' for col in range(cols)] for row in range(rows)]
    data[ 0][0] = 'Labour Hours'
    data[ 1][0] = 'Travel Hours'
    data[ 2][0] = 'Standby Hours'
    data[ 0][1] = lts[0]
    data[ 1][1] = lts[1]
    data[ 2][1] = lts[2]
    data[ 0][2] = '=D62/SUM(D62:D64)*100'
    data[ 1][2] = '=D63/SUM(D62:D64)*100'
    data[ 2][2] = '=D64/SUM(D62:D64)*100'
    ltsDict['DATA']['DATA'  ] = data
    ltsDict['DATA']['ROWS'  ] = rows
    ltsDict['DATA']['COLS'  ] = cols
    ltsDict['DATA']['BORDER'] = [(0,0,rows,cols,'medium')]
    fmt = [[self.fmt3b for col in range(cols)] for row in range(rows)]
    fmt[ 0][0] = self.fmt3
    fmt[ 1][0] = self.fmt3
    fmt[ 2][0] = self.fmt3
    ltsDict['DATA']['FMT'   ] = fmt

    ltsDict['ROWS'] = ltsDict['TITLE']['ROWS'] + ltsDict['DATA']['ROWS']
    ltsDict['COLS'] = ltsDict['TITLE']['COLS'] + ltsDict['DATA']['COLS']

    #------------------------------------------------------------------
    rows  = 1
    rows += hdrDict['ROWS']  + 1
    rows += hrsDict['ROWS']  + 1
    rows += actSDict['ROWS'] + 1
    rows += actDDict['ROWS'] + 1
    rows += gkaDict['ROWS']  + 1
    rows += cfsDict['ROWS']  + 1
    rows += sfsDict['ROWS']  + 1
    rows += ltsDict['ROWS']  + 1
    rows += 1
    cols = 5

    self.tbl                   = OrderedDict()
    self.tbl['HDR']            = hdrDict
    self.tbl['TBL']            = OrderedDict()
    self.tbl['TBL']['HOURS'  ] = hrsDict
    self.tbl['TBL']['ACT-SUM'] = actSDict
    self.tbl['TBL']['ACT-DET'] = actDDict
    self.tbl['TBL']['GKA-DET'] = gkaDict
    self.tbl['TBL']['CFS-DET'] = cfsDict
    self.tbl['TBL']['SFS-DET'] = sfsDict
    self.tbl['TBL']['LTS-DET'] = ltsDict
    self.tbl['ROWS'] = rows
    self.tbl['COLS'] = cols
    self.tbl['COL-WID'] = [10,70,20,20,10]
