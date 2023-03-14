import xmltodict
import pandas as pd

def xml_to_dataframe(file_path):
    with open(file_path) as f:
        xml_data = f.read()

    xml_dict = xmltodict.parse(xml_data)
    asgn_rpt_list = xml_dict['FIXML']['AsgnRpt']
    if isinstance(asgn_rpt_list, dict):
        asgn_rpt_list = [asgn_rpt_list]

    df_list = []
    for asgn_rpt in asgn_rpt_list:
        row_dict = {'RptID': asgn_rpt['@RptID'], 'BizDt': asgn_rpt['@BizDt'], 'Ccy': asgn_rpt['@Ccy'], 'SetSesID': asgn_rpt['@SetSesID'], 'UndSetPx': asgn_rpt['@UndSetPx'], 'AsgnMeth': asgn_rpt['@AsgnMeth']}
        pty_list = asgn_rpt.get('Pty', [])
        if isinstance(pty_list, dict):
            pty_list = [pty_list]
        row_dict.update({'Pty{}_ID'.format(i+1): pty['@ID'] for i, pty in enumerate(pty_list)})
        row_dict.update({'Pty{}_R'.format(i+1): pty['@R'] for i, pty in enumerate(pty_list)})
        instrmt = asgn_rpt.get('Instrmt', {})
        row_dict.update({'Instrmt_ID': instrmt.get('@ID', ''), 'SecTyp': instrmt.get('@SecTyp', ''), 'MMY': instrmt.get('@MMY', ''), 'Exch': instrmt.get('@Exch', ''), 'StrkPx': instrmt.get('@StrkPx', ''), 'PutCall': instrmt.get('@PutCall', ''), 'Fctr': instrmt.get('@Fctr', ''), 'PCFctr': instrmt.get('@PCFctr', '')})
        undly = asgn_rpt.get('Undly', {})
        row_dict.update({'Undly_ID': undly.get('@ID', ''), 'Undly_SecTyp': undly.get('@SecTyp', ''), 'Undly_MMY': undly.get('@MMY', ''), 'Undly_Exch': undly.get('@Exch', '')})
        qty_list = asgn_rpt.get('Qty', [])
        if isinstance(qty_list, dict):
            qty_list = [qty_list]
        row_dict.update({'Qty{}_Short'.format(i+1): qty['@Short'] for i, qty in enumerate(qty_list)})
        row_dict.update({'Qty{}_Typ'.format(i+1): qty['@Typ'] for i, qty in enumerate(qty_list)})
        df_list.append(row_dict)

    df = pd.DataFrame(df_list)
    return df
