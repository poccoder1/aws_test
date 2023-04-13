import xml.etree.ElementTree as ET
import csv

# Parse XML file
tree = ET.parse('input.xml')
root = tree.getroot()

# Extract header information
report_name = root.attrib['name']
exch_name = root.find('.//exchNam').text
rpt_cod = root.find('.//rptCod').text

# Create CSV file
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write header row
    writer.writerow(['Report Name', 'Exchange Name', 'Report Code', 'Member Legal Name', 'Member ID',
                     'Account Type Name', 'Liquidation Group Name', 'Current Market Component Name',
                     'Market Risk Aggr T', 'Market Risk Aggr T-1', 'LiquAdj Component Name', 'LiquAdj Value'])

    # Loop through reportNameGrp elements
    for cm_rc in root.findall('.//reportNameGrp/*'):

        # Extract member legal name and ID
        memb_lgl_nam = cm_rc.find('.//membLglNam').text
        memb_id = cm_rc.find('.//membId').text

        # Loop through acctTyGrp elements
        for acct_ty_grp in cm_rc.findall('.//acctTyGrp'):

            # Extract account type name
            acct_ty_name = acct_ty_grp.attrib['Name']

            # Loop through LiquidationGrp elements
            for liq_grp in acct_ty_grp.findall('.//LiquidationGrp'):

                # Extract Liquidation group name
                liq_grp_name = liq_grp.attrib['Name']

                # Loop through currMarComp elements
                for curr_mar_comp in liq_grp.findall('.//currMarComp'):

                    # Extract current market component name
                    curr_mar_comp_name = curr_mar_comp.attrib['Name']

                    # Extract MarketRisk_Aggr_T and MarketRisk_Aggr_T-1 values
                    mkt_risk_aggr_t = curr_mar_comp.find('.//MarketRisk_Aggr_T').text
                    mkt_risk_aggr_t_1 = curr_mar_comp.find('.//MarketRisk_Aggr_T-1').text

                    # Loop through LiquAdj elements
                    for liq_adj in curr_mar_comp.findall('.//LiquAdj'):

                        # Extract LiquAdj component name and value
                        liq_adj_comp_name = liq_adj.get('component', '')
                        liq_adj_val = liq_adj.text

                        # Write row to CSV file
                        writer.writerow([report_name, exch_name, rpt_cod, memb_lgl_nam, memb_id,
                                         acct_ty_name, liq_grp_name, curr_mar_comp_name,
                                         mkt_risk_aggr_t, mkt_risk_aggr_t_1, liq_adj_comp_name, liq_adj_val])
