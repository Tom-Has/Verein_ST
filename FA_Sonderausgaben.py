import csv
import os
import datetime

import_file = "exported_data.csv"

if os.path.exists(export_file := f"FA_Meldung_{datetime.datetime.now().year - 1}.xml"):
    os.remove(export_file)

with open(import_file, newline='', encoding='utf-8') as imported:
    data = csv.DictReader(imported)

    if os.path.exists(export_file):
        os.remove(export_file)

    with open(export_file, "w", encoding="utf-8") as file:
        file.write('<SonderausgabenUebermittlung xmlns="https://finanzonline.bmf.gv.at/fon/ws/uebermittlungSonderausgaben">\n')
        file.write('\t<Info_Daten>\n')
        file.write('\t\t<Fastnr_Fon_Tn>123456789</Fastnr_Fon_Tn>\n')
        file.write('\t\t<Fastnr_Org>123456789</Fastnr_Org>\n')
        file.write('\t</Info_Daten>\n')
        file.write('\t<MessageSpec>\n')
        file.write('\t\t<MessageRefId>Paket1</MessageRefId>\n')
        file.write('\t\t<Timestamp>2026-01-01T00:00:00</Timestamp>\n')
        file.write('\t\t<Uebermittlungsart>KK</Uebermittlungsart>\n')
        file.write('\t\t<Zeitraum>2025</Zeitraum>\n')
        file.write('\t</MessageSpec>\n')

        for line in data:
            if line["gemeldet"].strip().lower() != "ja":
                vbpk = line.get("vbPK", "").strip()
                try:
                    betrag = float(line["Betrag"])
                except (ValueError, TypeError):
                    betrag = 0
                if vbpk and betrag > 0:
                    file.write('\t<Sonderausgaben Uebermittlungs_Typ="E">\n')
                    file.write(f'\t\t<RefNr>{line["Ref"].strip()}</RefNr>\n')
                    file.write(f'\t\t<Betrag>{betrag:.2f}</Betrag>\n')
                    file.write(f'\t\t<vbPK>{vbpk}</vbPK>\n')
                    file.write('\t</Sonderausgaben>\n')
        
        file.write('</SonderausgabenUebermittlung>\n')

"""
# Überreste des Originalskripts für pandas
base_df = pd.read_excel(path)
clean_df = base_df[
    (base_df["Gesamt\nSumme"] > 0) &
    (pd.isna(base_df["übermittelt"])) &
    (pd.notna(base_df["vbPK"]))
]
for index, row in clean_df.iterrows():
    print('\t<ns1:Sonderausgaben Uebermittlungs_Typ="E">\n')
    print('\t\t<ns1:RefNr>' + str(int(row["EinzahlerID"])) + '</ns1:RefNr>\n')
    print('\t\t<ns1:Betrag>' + str(int(row["Gesamt\nSumme"])) + '</ns1:Betrag>\n')
    print('\t\t<ns1:vbPK>' + row["vbPK"] + '</ns1:vbPK>\n')
    print('\t</ns1:Sonderausgaben>\n')
"""
