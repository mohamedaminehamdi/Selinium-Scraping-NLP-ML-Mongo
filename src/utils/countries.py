import json
import os
import sys
from typing import Final
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'utils'))
sys.path.append(parent_dir)

from my_utils import write_output_to_file


country_fr_to_en1: Final[dict] = {
  "Afghanistan": {
    "FR": "Afghanistan"
  },
  "Albania": {
    "FR": "Albanie"
  },
  "Algeria": {
    "FR": "Algérie"
  },
  "Andorra": {
    "FR": "Andorre"
  },
  "Angola": {
    "FR": "Angola"
  },
  "Antigua and Barbuda": {
    "FR": "Antigua-et-Barbuda"
  },
  "Argentina": {
    "FR": "Argentine"
  },
  "Armenia": {
    "FR": "Arménie"
  },
  "Australia": {
    "FR": "Australie"
  },
  "Austria": {
    "FR": "Autriche"
  },
  "Azerbaijan": {
    "FR": "Azerbaïdjan"
  },
  "Bahamas": {
    "FR": "Bahamas"
  },
  "Bahrain": {
    "FR": "Bahreïn"
  },
  "Bangladesh": {
    "FR": "Bangladesh"
  },
  "Barbados": {
    "FR": "Barbade"
  },
  "Belarus": {
    "FR": "Biélorussie"
  },
  "Belgium": {
    "FR": "Belgique"
  },
  "Belize": {
    "FR": "Belize"
  },
  "Benin": {
    "FR": "Bénin"
  },
  "Bhutan": {
    "FR": "Bhoutan"
  },
  "Bolivia": {
    "FR": "Bolivie"
  },
  "Bosnia and Herzegovina": {
    "FR": "Bosnie-Herzégovine"
  },
  "Botswana": {
    "FR": "Botswana"
  },
  "Brazil": {
    "FR": "Brésil"
  },
  "Brunei": {
    "FR": "Brunéi Darussalam"
  },
  "Bulgaria": {
    "FR": "Bulgarie"
  },
  "Burkina Faso": {
    "FR": "Burkina Faso"
  },
  "Burundi": {
    "FR": "Burundi"
  },
  "Cabo Verde": {
    "FR": "Cap-Vert"
  },
  "Cambodia": {
    "FR": "Cambodge"
  },
  "Cameroon": {
    "FR": "Cameroun"
  },
  "Canada": {
    "FR": "Canada"
  },
  "Central African Republic": {
    "FR": "République centrafricaine"
  },
  "Chad": {
    "FR": "Tchad"
  },
  "Chile": {
    "FR": "Chili"
  },
  "China": {
    "FR": "Chine"
  },
  "Colombia": {
    "FR": "Colombie"
  },
  "Comoros": {
    "FR": "Comores"
  },
  "Congo (Congo-Brazzaville)": {
    "FR": "Congo (République du Congo)"
  },
  "Costa Rica": {
    "FR": "Costa Rica"
  },
  "Croatia": {
    "FR": "Croatie"
  },
  "Cuba": {
    "FR": "Cuba"
  },
  "Cyprus": {
    "FR": "Chypre"
  },
  "Czechia (Czech Republic)": {
    "FR": "Tchéquie (République tchèque)"
  },
  "Denmark": {
    "FR": "Danemark"
  },
  "Djibouti": {
    "FR": "Djibouti"
  },
  "Dominica": {
    "FR": "Dominique"
  },
  "Dominican Republic": {
    "FR": "République dominicaine"
  },
  "Ecuador": {
    "FR": "Équateur"
  },
  "Egypt": {
    "FR": "Égypte"
  },
  "El Salvador": {
    "FR": "Salvador"
  },
  "Equatorial Guinea": {
    "FR": "Guinée équatoriale"
  },
  "Eritrea": {
    "FR": "Érythrée"
  },
  "Estonia": {
    "FR": "Estonie"
  },
  "Eswatini (fmr. Swaziland)": {
    "FR": "Eswatini (anciennement Swaziland)"
  },
  "Ethiopia": {
    "FR": "Éthiopie"
  },
  "Fiji": {
    "FR": "Fidji"
  },
  "Finland": {
    "FR": "Finlande"
  },
  "France": {
    "FR": "France"
  },
  "Gabon": {
    "FR": "Gabon"
  },
  "Gambia": {
    "FR": "Gambie"
  },
  "Georgia": {
    "FR": "Géorgie"
  },
  "Germany": {
    "FR": "Allemagne"
  },
  "Ghana": {
    "FR": "Ghana"
  },
  "Greece": {
    "FR": "Grèce"
  },
  "Grenada": {
    "FR": "Grenade"
  },
  "Guatemala": {
    "FR": "Guatemala"
  },
  "Guinea": {
    "FR": "Guinée"
  },
  "Guinea-Bissau": {
    "FR": "Guinée-Bissau"
  },
  "Guyana": {
    "FR": "Guyana"
  },
  "Haiti": {
    "FR": "Haïti"
  },
  "Honduras": {
    "FR": "Honduras"
  },
  "Hungary": {
    "FR": "Hongrie"
  },
  "Iceland": {
    "FR": "Islande"
  },
  "India": {
    "FR": "Inde"
  },
  "Indonesia": {
    "FR": "Indonésie"
  },
  "Iran": {
    "FR": "Iran"
  },
  "Iraq": {
    "FR": "Irak"
  },
  "Ireland": {
    "FR": "Irlande"
  },
  "Israel": {
    "FR": "Israël"
  },
  "Italy": {
    "FR": "Italie"
  },
  "Jamaica": {
    "FR": "Jamaïque"
  },
  "Japan": {
    "FR": "Japon"
  },
  "Jordan": {
    "FR": "Jordanie"
  },
  "Kazakhstan": {
    "FR": "Kazakhstan"
  },
  "Kenya": {
    "FR": "Kenya"
  },
  "Kiribati": {
    "FR": "Kiribati"
  },
  "Korea, Democratic People's Republic of (North Korea)": {
    "FR": "Corée, République populaire démocratique de (Corée du Nord)"
  },
  "Korea, Republic of (South Korea)": {
    "FR": "Corée, République de (Corée du Sud)"
  },
  "Kuwait": {
    "FR": "Koweït"
  },
  "Kyrgyzstan": {
    "FR": "Kirghizistan"
  },
  "Laos": {
    "FR": "Laos"
  },
  "Latvia": {
    "FR": "Lettonie"
  },
  "Lebanon": {
    "FR": "Liban"
  },
  "Lesotho": {
    "FR": "Lesotho"
  },
  "Liberia": {
    "FR": "Libéria"
  },
  "Libya": {
    "FR": "Libye"
  },
  "Liechtenstein": {
    "FR": "Liechtenstein"
  },
  "Lithuania": {
    "FR": "Lituanie"
  },
  "Luxembourg": {
    "FR": "Luxembourg"
  },
  "Madagascar": {
    "FR": "Madagascar"
  },
  "Malawi": {
    "FR": "Malawi"
  },
  "Malaysia": {
    "FR": "Malaisie"
  },
  "Maldives": {
    "FR": "Maldives"
  },
  "Mali": {
    "FR": "Mali"
  },
  "Malta": {
    "FR": "Malte"
  },
  "Marshall Islands": {
    "FR": "Îles Marshall"
  },
  "Mauritania": {
    "FR": "Mauritanie"
  },
  "Mauritius": {
    "FR": "Maurice"
  },
  "Mexico": {
    "FR": "Mexique"
  },
  "Micronesia": {
    "FR": "Micronésie"
  },
  "Moldova": {
    "FR": "Moldavie"
  },
  "Monaco": {
    "FR": "Monaco"
  },
  "Mongolia": {
    "FR": "Mongolie"
  },
  "Montenegro": {
    "FR": "Monténégro"
  },
  "Morocco": {
    "FR": "Maroc"
  },
  "Mozambique": {
    "FR": "Mozambique"
  },
  "Myanmar (formerly Burma)": {
    "FR": "Myanmar (anciennement Birmanie)"
  },
  "Namibia": {
    "FR": "Namibie"
  },
  "Nauru": {
    "FR": "Nauru"
  },
  "Nepal": {
    "FR": "Népal"
  },
  "Netherlands": {
    "FR": "Pays-Bas"
  },
  "New Zealand": {
    "FR": "Nouvelle-Zélande"
  },
  "Nicaragua": {
    "FR": "Nicaragua"
  },
  "Niger": {
    "FR": "Niger"
  },
  "Nigeria": {
    "FR": "Nigéria"
  },
  "North Macedonia": {
    "FR": "Macédoine du Nord"
  },
  "Norway": {
    "FR": "Norvège"
  },
  "Oman": {
    "FR": "Oman"
  },
  "Pakistan": {
    "FR": "Pakistan"
  },
  "Palau": {
    "FR": "Palaos"
  },
  "Palestine State": {
    "FR": "État de Palestine"
  },
  "Panama": {
    "FR": "Panama"
  },
  "Papua New Guinea": {
    "FR": "Papouasie-Nouvelle-Guinée"
  },
  "Paraguay": {
    "FR": "Paraguay"
  },
  "Peru": {
    "FR": "Pérou"
  },
  "Philippines": {
    "FR": "Philippines"
  },
  "Poland": {
    "FR": "Pologne"
  },
  "Portugal": {
    "FR": "Portugal"
  },
  "Qatar": {
    "FR": "Qatar"
  },
  "Romania": {
    "FR": "Roumanie"
  },
  "Russia": {
    "FR": "Russie"
  },
  "Rwanda": {
    "FR": "Rwanda"
  },
  "Saint Kitts and Nevis": {
    "FR": "Saint-Christophe-et-Niévès"
  },
  "Saint Lucia": {
    "FR": "Sainte-Lucie"
  },
  "Saint Vincent and the Grenadines": {
    "FR": "Saint-Vincent-et-les Grenadines"
  },
  "Samoa": {
    "FR": "Samoa"
  },
  "San Marino": {
    "FR": "Saint-Marin"
  },
  "Sao Tome and Principe": {
    "FR": "Sao Tomé-et-Principe"
  },
  "Saudi Arabia": {
    "FR": "Arabie saoudite"
  },
  "Senegal": {
    "FR": "Sénégal"
  },
  "Serbia": {
    "FR": "Serbie"
  },
  "Seychelles": {
    "FR": "Seychelles"
  },
  "Sierra Leone": {
    "FR": "Sierra Leone"
  },
  "Singapore": {
    "FR": "Singapour"
  },
  "Slovakia": {
    "FR": "Slovaquie"
  },
  "Slovenia": {
    "FR": "Slovénie"
  },
  "Solomon Islands": {
    "FR": "Îles Salomon"
  },
  "Somalia": {
    "FR": "Somalie"
  },
  "South Africa": {
    "FR": "Afrique du Sud"
  },
  "South Sudan": {
    "FR": "Soudan du Sud"
  },
  "Spain": {
    "FR": "Espagne"
  },
  "Sri Lanka": {
    "FR": "Sri Lanka"
  },
  "Sudan": {
    "FR": "Soudan"
  },
  "Suriname": {
    "FR": "Suriname"
  },
  "Sweden": {
    "FR": "Suède"
  },
  "Switzerland": {
    "FR": "Suisse"
  },
  "Syria": {
    "FR": "Syrie"
  },
  "Tajikistan": {
    "FR": "Tadjikistan"
  },
  "Tanzania": {
    "FR": "Tanzanie"
  },
  "Thailand": {
    "FR": "Thaïlande"
  },
  "Timor-Leste": {
    "FR": "Timor-Leste"
  },
  "Togo": {
    "FR": "Togo"
  },
  "Tonga": {
    "FR": "Tonga"
  },
  "Trinidad and Tobago": {
    "FR": "Trinité-et-Tobago"
  },
  "Tunisia": {
    "FR": "Tunisie"
  },
  "Turkey": {
    "FR": "Turquie"
  },
  "Turkmenistan": {
    "FR": "Turkménistan"
  },
  "Tuvalu": {
    "FR": "Tuvalu"
  },
  "Uganda": {
    "FR": "Ouganda"
  },
  "Ukraine": {
    "FR": "Ukraine"
  },
  "United Arab Emirates": {
    "FR": "Émirats arabes unis"
  },
  "United Kingdom": {
    "FR": "Royaume-Uni"
  },
  "United States of America": {
    "FR": "États-Unis d'Amérique"
  },
  "Uruguay": {
    "FR": "Uruguay"
  },
  "Uzbekistan": {
    "FR": "Ouzbékistan"
  },
  "Vanuatu": {
    "FR": "Vanuatu"
  },
  "Vatican City (Holy See)": {
    "FR": "Cité du Vatican"
  },
  "Venezuela": {
    "FR": "Venezuela"
  },
  "Vietnam": {
    "FR": "Vietnam"
  },
  "Yemen": {
    "FR": "Yémen"
  },
  "Zambia": {
    "FR": "Zambie"
  },
  "Zimbabwe": {
    "FR": "Zimbabwe"
  }
}

country_de_to_en1: Final[dict] = {
  "Afghanistan": {
    "DE": "Afghanistan"
  },
  "Albania": {
    "DE": "Albanien"
  },
  "Algeria": {
    "DE": "Algerien"
  },
  "Andorra": {
    "DE": "Andorra"
  },
  "Angola": {
    "DE": "Angola"
  },
  "Antigua and Barbuda": {
    "DE": "Antigua und Barbuda"
  },
  "Argentina": {
    "DE": "Argentinien"
  },
  "Armenia": {
    "DE": "Armenien"
  },
  "Australia": {
    "DE": "Australien"
  },
  "Austria": {
    "DE": "Österreich"
  },
  "Azerbaijan": {
    "DE": "Aserbaidschan"
  },
  "Bahamas": {
    "DE": "Bahamas"
  },
  "Bahrain": {
    "DE": "Bahrain"
  },
  "Bangladesh": {
    "DE": "Bangladesch"
  },
  "Barbados": {
    "DE": "Barbados"
  },
  "Belarus": {
    "DE": "Weißrussland"
  },
  "Belgium": {
    "DE": "Belgien"
  },
  "Belize": {
    "DE": "Belize"
  },
  "Benin": {
    "DE": "Benin"
  },
  "Bhutan": {
    "DE": "Bhutan"
  },
  "Bolivia": {
    "DE": "Bolivien"
  },
  "Bosnia and Herzegovina": {
    "DE": "Bosnien und Herzegowina"
  },
  "Botswana": {
    "DE": "Botswana"
  },
  "Brazil": {
    "DE": "Brasilien"
  },
  "Brunei": {
    "DE": "Brunei"
  },
  "Bulgaria": {
    "DE": "Bulgarien"
  },
  "Burkina Faso": {
    "DE": "Burkina Faso"
  },
  "Burundi": {
    "DE": "Burundi"
  },
  "Cabo Verde": {
    "DE": "Cabo Verde"
  },
  "Cambodia": {
    "DE": "Kambodscha"
  },
  "Cameroon": {
    "DE": "Kamerun"
  },
  "Canada": {
    "DE": "Kanada"
  },
  "Central African Republic": {
    "DE": "Zentralafrikanische Republik"
  },
  "Chad": {
    "DE": "Tschad"
  },
  "Chile": {
    "DE": "Chile"
  },
  "China": {
    "DE": "China"
  },
  "Colombia": {
    "DE": "Kolumbien"
  },
  "Comoros": {
    "DE": "Komoren"
  },
  "Congo (Congo-Brazzaville)": {
    "DE": "Kongo (Republik Kongo)"
  },
  "Costa Rica": {
    "DE": "Costa Rica"
  },
  "Croatia": {
    "DE": "Kroatien"
  },
  "Cuba": {
    "DE": "Kuba"
  },
  "Cyprus": {
    "DE": "Zypern"
  },
  "Czechia (Czech Republic)": {
    "DE": "Tschechien"
  },
  "Denmark": {
    "DE": "Dänemark"
  },
  "Djibouti": {
    "DE": "Dschibuti"
  },
  "Dominica": {
    "DE": "Dominica"
  },
  "Dominican Republic": {
    "DE": "Dominikanische Republik"
  },
  "Ecuador": {
    "DE": "Ecuador"
  },
  "Egypt": {
    "DE": "Ägypten"
  },
  "El Salvador": {
    "DE": "El Salvador"
  },
  "Equatorial Guinea": {
    "DE": "Äquatorialguinea"
  },
  "Eritrea": {
    "DE": "Eritrea"
  },
  "Estonia": {
    "DE": "Estland"
  },
  "Eswatini (fmr. Swaziland)": {
    "DE": "Eswatini (ehemals Swasiland)"
  },
  "Ethiopia": {
    "DE": "Äthiopien"
  },
  "Fiji": {
    "DE": "Fidschi"
  },
  "Finland": {
    "DE": "Finnland"
  },
  "France": {
    "DE": "Frankreich"
  },
  "Gabon": {
    "DE": "Gabun"
  },
  "Gambia": {
    "DE": "Gambia"
  },
  "Georgia": {
    "DE": "Georgien"
  },
  "Germany": {
    "DE": "Deutschland"
  },
  "Ghana": {
    "DE": "Ghana"
  },
  "Greece": {
    "DE": "Griechenland"
  },
  "Grenada": {
    "DE": "Grenada"
  },
  "Guatemala": {
    "DE": "Guatemala"
  },
  "Guinea": {
    "DE": "Guinea"
  },
  "Guinea-Bissau": {
    "DE": "Guinea-Bissau"
  },
  "Guyana": {
    "DE": "Guyana"
  },
  "Haiti": {
    "DE": "Haiti"
  },
  "Honduras": {
    "DE": "Honduras"
  },
  "Hungary": {
    "DE": "Ungarn"
  },
  "Iceland": {
    "DE": "Island"
  },
  "India": {
    "DE": "Indien"
  },
  "Indonesia": {
    "DE": "Indonesien"
  },
  "Iran": {
    "DE": "Iran"
  },
  "Iraq": {
    "DE": "Irak"
  },
  "Ireland": {
    "DE": "Irland"
  },
  "Israel": {
    "DE": "Israel"
  },
  "Italy": {
    "DE": "Italien"
  },
  "Jamaica": {
    "DE": "Jamaika"
  },
  "Japan": {
    "DE": "Japan"
  },
  "Jordan": {
    "DE": "Jordanien"
  },
  "Kazakhstan": {
    "DE": "Kasachstan"
  },
  "Kenya": {
    "DE": "Kenia"
  },
  "Kiribati": {
    "DE": "Kiribati"
  },
  "Korea, Democratic People's Republic of (North Korea)": {
    "DE": "Korea, Demokratische Volksrepublik (Nordkorea)"
  },
  "Korea, Republic of (South Korea)": {
    "DE": "Korea, Republik (Südkorea)"
  },
  "Kuwait": {
    "DE": "Kuwait"
  },
  "Kyrgyzstan": {
    "DE": "Kirgisistan"
  },
  "Laos": {
    "DE": "Laos"
  },
  "Latvia": {
    "DE": "Lettland"
  },
  "Lebanon": {
    "DE": "Libanon"
  },
  "Lesotho": {
    "DE": "Lesotho"
  },
  "Liberia": {
    "DE": "Liberia"
  },
  "Libya": {
    "DE": "Libyen"
  },
  "Liechtenstein": {
    "DE": "Liechtenstein"
  },
  "Lithuania": {
    "DE": "Litauen"
  },
  "Luxembourg": {
    "DE": "Luxemburg"
  },
  "Madagascar": {
    "DE": "Madagaskar"
  },
  "Malawi": {
    "DE": "Malawi"
  },
  "Malaysia": {
    "DE": "Malaysia"
  },
  "Maldives": {
    "DE": "Malediven"
  },
  "Mali": {
    "DE": "Mali"
  },
  "Malta": {
    "DE": "Malta"
  },
  "Marshall Islands": {
    "DE": "Marshallinseln"
  },
  "Mauritania": {
    "DE": "Mauretanien"
  },
  "Mauritius": {
    "DE": "Mauritius"
  },
  "Mexico": {
    "DE": "Mexiko"
  },
  "Micronesia": {
    "DE": "Mikronesien"
  },
  "Moldova": {
    "DE": "Moldawien"
  },
  "Monaco": {
    "DE": "Monaco"
  },
  "Mongolia": {
    "DE": "Mongolei"
  },
  "Montenegro": {
    "DE": "Montenegro"
  },
  "Morocco": {
    "DE": "Marokko"
  },
  "Mozambique": {
    "DE": "Mosambik"
  },
  "Myanmar (formerly Burma)": {
    "DE": "Myanmar (ehemals Burma)"
  },
  "Namibia": {
    "DE": "Namibia"
  },
  "Nauru": {
    "DE": "Nauru"
  },
  "Nepal": {
    "DE": "Nepal"
  },
  "Netherlands": {
    "DE": "Niederlande"
  },
  "New Zealand": {
    "DE": "Neuseeland"
  },
  "Nicaragua": {
    "DE": "Nicaragua"
  },
  "Niger": {
    "DE": "Niger"
  },
  "Nigeria": {
    "DE": "Nigeria"
  },
  "North Macedonia": {
    "DE": "Nordmazedonien"
  },
  "Norway": {
    "DE": "Norwegen"
  },
  "Oman": {
    "DE": "Oman"
  },
  "Pakistan": {
    "DE": "Pakistan"
  },
  "Palau": {
    "DE": "Palau"
  },
  "Palestine State": {
    "DE": "Staat Palästina"
  },
  "Panama": {
    "DE": "Panama"
  },
  "Papua New Guinea": {
    "DE": "Papua-Neuguinea"
  },
  "Paraguay": {
    "DE": "Paraguay"
  },
  "Peru": {
    "DE": "Peru"
  },
  "Philippines": {
    "DE": "Philippinen"
  },
  "Poland": {
    "DE": "Polen"
  },
  "Portugal": {
    "DE": "Portugal"
  },
  "Qatar": {
    "DE": "Katar"
  },
  "Romania": {
    "DE": "Rumänien"
  },
  "Russia": {
    "DE": "Russland"
  },
  "Rwanda": {
    "DE": "Ruanda"
  },
  "Saint Kitts and Nevis": {
    "DE": "St. Kitts und Nevis"
  },
  "Saint Lucia": {
    "DE": "St. Lucia"
  },
  "Saint Vincent and the Grenadines": {
    "DE": "St. Vincent und die Grenadinen"
  },
  "Samoa": {
    "DE": "Samoa"
  },
  "San Marino": {
    "DE": "San Marino"
  },
  "Sao Tome and Principe": {
    "DE": "São Tomé und Príncipe"
  },
  "Saudi Arabia": {
    "DE": "Saudi-Arabien"
  },
  "Senegal": {
    "DE": "Senegal"
  },
  "Serbia": {
    "DE": "Serbien"
  },
  "Seychelles": {
    "DE": "Seychellen"
  },
  "Sierra Leone": {
    "DE": "Sierra Leone"
  },
  "Singapore": {
    "DE": "Singapur"
  },
  "Slovakia": {
    "DE": "Slowakei"
  },
  "Slovenia": {
    "DE": "Slowenien"
  },
  "Solomon Islands": {
    "DE": "Salomonen"
  },
  "Somalia": {
    "DE": "Somalia"
  },
  "South Africa": {
    "DE": "Südafrika"
  },
  "South Sudan": {
    "DE": "Südsudan"
  },
  "Spain": {
    "DE": "Spanien"
  },
  "Sri Lanka": {
    "DE": "Sri Lanka"
  },
  "Sudan": {
    "DE": "Sudan"
  },
  "Suriname": {
    "DE": "Suriname"
  },
  "Sweden": {
    "DE": "Schweden"
  },
  "Switzerland": {
    "DE": "Schweiz"
  },
  "Syria": {
    "DE": "Syrien"
  },
  "Tajikistan": {
    "DE": "Tadschikistan"
  },
  "Tanzania": {
    "DE": "Tansania"
  },
  "Thailand": {
    "DE": "Thailand"
  },
  "Timor-Leste": {
    "DE": "Timor-Leste"
  },
  "Togo": {
    "DE": "Togo"
  },
  "Tonga": {
    "DE": "Tonga"
  },
  "Trinidad and Tobago": {
    "DE": "Trinidad und Tobago"
  },
  "Tunisia": {
    "DE": "Tunesien"
  },
  "Turkey": {
    "DE": "Türkei"
  },
  "Turkmenistan": {
    "DE": "Turkmenistan"
  },
  "Tuvalu": {
    "DE": "Tuvalu"
  },
  "Uganda": {
    "DE": "Uganda"
  },
  "Ukraine": {
    "DE": "Ukraine"
  },
  "United Arab Emirates": {
    "DE": "Vereinigte Arabische Emirate"
  },
  "United Kingdom": {
    "DE": "Vereinigtes Königreich"
  },
  "United States of America": {
    "DE": "Vereinigte Staaten von Amerika"
  },
  "Uruguay": {
    "DE": "Uruguay"
  },
  "Uzbekistan": {
    "DE": "Usbekistan"
  },
  "Vanuatu": {
    "DE": "Vanuatu"
  },
  "Vatican City (Holy See)": {
    "DE": "Vatikanstadt"
  },
  "Venezuela": {
    "DE": "Venezuela"
  },
  "Vietnam": {
    "DE": "Vietnam"
  },
  "Yemen": {
    "DE": "Jemen"
  },
  "Zambia": {
    "DE": "Sambia"
  },
  "Zimbabwe": {
    "DE": "Simbabwe"
  }
}

country_es_to_en1: Final[dict] = {
  "Afghanistan": {
    "ES": "Afganistán"
  },
  "Albania": {
    "ES": "Albania"
  },
  "Algeria": {
    "ES": "Argelia"
  },
  "Andorra": {
    "ES": "Andorra"
  },
  "Angola": {
    "ES": "Angola"
  },
  "Antigua and Barbuda": {
    "ES": "Antigua y Barbuda"
  },
  "Argentina": {
    "ES": "Argentina"
  },
  "Armenia": {
    "ES": "Armenia"
  },
  "Australia": {
    "ES": "Australia"
  },
  "Austria": {
    "ES": "Austria"
  },
  "Azerbaijan": {
    "ES": "Azerbaiyán"
  },
  "Bahamas": {
    "ES": "Bahamas"
  },
  "Bahrain": {
    "ES": "Baréin"
  },
  "Bangladesh": {
    "ES": "Bangladés"
  },
  "Barbados": {
    "ES": "Barbados"
  },
  "Belarus": {
    "ES": "Bielorrusia"
  },
  "Belgium": {
    "ES": "Bélgica"
  },
  "Belize": {
    "ES": "Belice"
  },
  "Benin": {
    "ES": "Benín"
  },
  "Bhutan": {
    "ES": "Bután"
  },
  "Bolivia": {
    "ES": "Bolivia"
  },
  "Bosnia and Herzegovina": {
    "ES": "Bosnia y Herzegovina"
  },
  "Botswana": {
    "ES": "Botsuana"
  },
  "Brazil": {
    "ES": "Brasil"
  },
  "Brunei": {
    "ES": "Brunéi"
  },
  "Bulgaria": {
    "ES": "Bulgaria"
  },
  "Burkina Faso": {
    "ES": "Burkina Faso"
  },
  "Burundi": {
    "ES": "Burundi"
  },
  "Cabo Verde": {
    "ES": "Cabo Verde"
  },
  "Cambodia": {
    "ES": "Camboya"
  },
  "Cameroon": {
    "ES": "Camerún"
  },
  "Canada": {
    "ES": "Canadá"
  },
  "Central African Republic": {
    "ES": "República Centroafricana"
  },
  "Chad": {
    "ES": "Chad"
  },
  "Chile": {
    "ES": "Chile"
  },
  "China": {
    "ES": "China"
  },
  "Colombia": {
    "ES": "Colombia"
  },
  "Comoros": {
    "ES": "Comoras"
  },
  "Congo (Congo-Brazzaville)": {
    "ES": "Congo (Brazzaville)"
  },
  "Costa Rica": {
    "ES": "Costa Rica"
  },
  "Croatia": {
    "ES": "Croacia"
  },
  "Cuba": {
    "ES": "Cuba"
  },
  "Cyprus": {
    "ES": "Chipre"
  },
  "Czechia (Czech Republic)": {
    "ES": "Chequia"
  },
  "Denmark": {
    "ES": "Dinamarca"
  },
  "Djibouti": {
    "ES": "Yibuti"
  },
  "Dominica": {
    "ES": "Dominica"
  },
  "Dominican Republic": {
    "ES": "República Dominicana"
  },
  "Ecuador": {
    "ES": "Ecuador"
  },
  "Egypt": {
    "ES": "Egipto"
  },
  "El Salvador": {
    "ES": "El Salvador"
  },
  "Equatorial Guinea": {
    "ES": "Guinea Ecuatorial"
  },
  "Eritrea": {
    "ES": "Eritrea"
  },
  "Estonia": {
    "ES": "Estonia"
  },
  "Eswatini (fmr. Swaziland)": {
    "ES": "Esuatini"
  },
  "Ethiopia": {
    "ES": "Etiopía"
  },
  "Fiji": {
    "ES": "Fiyi"
  },
  "Finland": {
    "ES": "Finlandia"
  },
  "France": {
    "ES": "Francia"
  },
  "Gabon": {
    "ES": "Gabón"
  },
  "Gambia": {
    "ES": "Gambia"
  },
  "Georgia": {
    "ES": "Georgia"
  },
  "Germany": {
    "ES": "Alemania"
  },
  "Ghana": {
    "ES": "Ghana"
  },
  "Greece": {
    "ES": "Grecia"
  },
  "Grenada": {
    "ES": "Granada"
  },
  "Guatemala": {
    "ES": "Guatemala"
  },
  "Guinea": {
    "ES": "Guinea"
  },
  "Guinea-Bissau": {
    "ES": "Guinea-Bisáu"
  },
  "Guyana": {
    "ES": "Guyana"
  },
  "Haiti": {
    "ES": "Haití"
  },
  "Honduras": {
    "ES": "Honduras"
  },
  "Hungary": {
    "ES": "Hungría"
  },
  "Iceland": {
    "ES": "Islandia"
  },
  "India": {
    "ES": "India"
  },
  "Indonesia": {
    "ES": "Indonesia"
  },
  "Iran": {
    "ES": "Irán"
  },
  "Iraq": {
    "ES": "Irak"
  },
  "Ireland": {
    "ES": "Irlanda"
  },
  "Israel": {
    "ES": "Israel"
  },
  "Italy": {
    "ES": "Italia"
  },
  "Jamaica": {
    "ES": "Jamaica"
  },
  "Japan": {
    "ES": "Japón"
  },
  "Jordan": {
    "ES": "Jordania"
  },
  "Kazakhstan": {
    "ES": "Kazajistán"
  },
  "Kenya": {
    "ES": "Kenia"
  },
  "Kiribati": {
    "ES": "Kiribati"
  },
  "Korea, Democratic People's Republic of (North Korea)": {
    "ES": "Corea del Norte"
  },
  "Korea, Republic of (South Korea)": {
    "ES": "Corea del Sur"
  },
  "Kuwait": {
    "ES": "Kuwait"
  },
  "Kyrgyzstan": {
    "ES": "Kirguistán"
  },
  "Laos": {
    "ES": "Laos"
  },
  "Latvia": {
    "ES": "Letonia"
  },
  "Lebanon": {
    "ES": "Líbano"
  },
  "Lesotho": {
    "ES": "Lesoto"
  },
  "Liberia": {
    "ES": "Liberia"
  },
  "Libya": {
    "ES": "Libia"
  },
  "Liechtenstein": {
    "ES": "Liechtenstein"
  },
  "Lithuania": {
    "ES": "Lituania"
  },
  "Luxembourg": {
    "ES": "Luxemburgo"
  },
  "Madagascar": {
    "ES": "Madagascar"
  },
  "Malawi": {
    "ES": "Malaui"
  },
  "Malaysia": {
    "ES": "Malasia"
  },
  "Maldives": {
    "ES": "Maldivas"
  },
  "Mali": {
    "ES": "Malí"
  },
  "Malta": {
    "ES": "Malta"
  },
  "Marshall Islands": {
    "ES": "Islas Marshall"
  },
  "Mauritania": {
    "ES": "Mauritania"
  },
  "Mauritius": {
    "ES": "Mauricio"
  },
  "Mexico": {
    "ES": "México"
  },
  "Micronesia": {
    "ES": "Micronesia"
  },
  "Moldova": {
    "ES": "Moldavia"
  },
  "Monaco": {
    "ES": "Mónaco"
  },
  "Mongolia": {
    "ES": "Mongolia"
  },
  "Montenegro": {
    "ES": "Montenegro"
  },
  "Morocco": {
    "ES": "Marruecos"
  },
  "Mozambique": {
    "ES": "Mozambique"
  },
  "Myanmar (formerly Burma)": {
    "ES": "Myanmar"
  },
  "Namibia": {
    "ES": "Namibia"
  },
  "Nauru": {
    "ES": "Nauru"
  },
  "Nepal": {
    "ES": "Nepal"
  },
  "Netherlands": {
    "ES": "Países Bajos"
  },
  "New Zealand": {
    "ES": "Nueva Zelanda"
  },
  "Nicaragua": {
    "ES": "Nicaragua"
  },
  "Niger": {
    "ES": "Níger"
  },
  "Nigeria": {
    "ES": "Nigeria"
  },
  "North Macedonia": {
    "ES": "Macedonia del Norte"
  },
  "Norway": {
    "ES": "Noruega"
  },
  "Oman": {
    "ES": "Omán"
  },
  "Pakistan": {
    "ES": "Pakistán"
  },
  "Palau": {
    "ES": "Palaos"
  },
  "Palestine State": {
    "ES": "Estado de Palestina"
  },
  "Panama": {
    "ES": "Panamá"
  },
  "Papua New Guinea": {
    "ES": "Papúa Nueva Guinea"
  },
  "Paraguay": {
    "ES": "Paraguay"
  },
  "Peru": {
    "ES": "Perú"
  },
  "Philippines": {
    "ES": "Filipinas"
  },
  "Poland": {
    "ES": "Polonia"
  },
  "Portugal": {
    "ES": "Portugal"
  },
  "Qatar": {
    "ES": "Catar"
  },
  "Romania": {
    "ES": "Rumania"
  },
  "Russia": {
    "ES": "Rusia"
  },
  "Rwanda": {
    "ES": "Ruanda"
  },
  "Saint Kitts and Nevis": {
    "ES": "San Cristóbal y Nieves"
  },
  "Saint Lucia": {
    "ES": "Santa Lucía"
  },
  "Saint Vincent and the Grenadines": {
    "ES": "San Vicente y las Granadinas"
  },
  "Samoa": {
    "ES": "Samoa"
  },
  "San Marino": {
    "ES": "San Marino"
  },
  "Sao Tome and Principe": {
    "ES": "Santo Tomé y Príncipe"
  },
  "Saudi Arabia": {
    "ES": "Arabia Saudí"
  },
  "Senegal": {
    "ES": "Senegal"
  },
  "Serbia": {
    "ES": "Serbia"
  },
  "Seychelles": {
    "ES": "Seychelles"
  },
  "Sierra Leone": {
    "ES": "Sierra Leona"
  },
  "Singapore": {
    "ES": "Singapur"
  },
  "Slovakia": {
    "ES": "Eslovaquia"
  },
  "Slovenia": {
    "ES": "Eslovenia"
  },
  "Solomon Islands": {
    "ES": "Islas Salomón"
  },
  "Somalia": {
    "ES": "Somalia"
  },
  "South Africa": {
    "ES": "Sudáfrica"
  },
  "South Sudan": {
    "ES": "Sudán del Sur"
  },
  "Spain": {
    "ES": "España"
  },
  "Sri Lanka": {
    "ES": "Sri Lanka"
  },
  "Sudan": {
    "ES": "Sudán"
  },
  "Suriname": {
    "ES": "Surinam"
  },
  "Sweden": {
    "ES": "Suecia"
  },
  "Switzerland": {
    "ES": "Suiza"
  },
  "Syria": {
    "ES": "Siria"
  },
  "Tajikistan": {
    "ES": "Tayikistán"
  },
  "Tanzania": {
    "ES": "Tanzania"
  },
  "Thailand": {
    "ES": "Tailandia"
  },
  "Timor-Leste": {
    "ES": "Timor Oriental"
  },
  "Togo": {
    "ES": "Togo"
  },
  "Tonga": {
    "ES": "Tonga"
  },
  "Trinidad and Tobago": {
    "ES": "Trinidad y Tobago"
  },
  "Tunisia": {
    "ES": "Túnez"
  },
  "Turkey": {
    "ES": "Turquía"
  },
  "Turkmenistan": {
    "ES": "Turkmenistán"
  },
  "Tuvalu": {
    "ES": "Tuvalu"
  },
  "Uganda": {
    "ES": "Uganda"
  },
  "Ukraine": {
    "ES": "Ucrania"
  },
  "United Arab Emirates": {
    "ES": "Emiratos Árabes Unidos"
  },
  "United Kingdom": {
    "ES": "Reino Unido"
  },
  "United States of America": {
    "ES": "Estados Unidos"
  },
  "Uruguay": {
    "ES": "Uruguay"
  },
  "Uzbekistan": {
    "ES": "Uzbekistán"
  },
  "Vanuatu": {
    "ES": "Vanuatu"
  },
  "Vatican City (Holy See)": {
    "ES": "Ciudad del Vaticano"
  },
  "Venezuela": {
    "ES": "Venezuela"
  },
  "Vietnam": {
    "ES": "Vietnam"
  },
  "Yemen": {
    "ES": "Yemen"
  },
  "Zambia": {
    "ES": "Zambia"
  },
  "Zimbabwe": {
    "ES": "Zimbabue"
  }
}

country_it_to_en1: Final[dict] = {
  "Afghanistan": {
    "IT": "Afghanistan"
  },
  "Albania": {
    "IT": "Albania"
  },
  "Algeria": {
    "IT": "Algeria"
  },
  "Andorra": {
    "IT": "Andorra"
  },
  "Angola": {
    "IT": "Angola"
  },
  "Antigua and Barbuda": {
    "IT": "Antigua e Barbuda"
  },
  "Argentina": {
    "IT": "Argentina"
  },
  "Armenia": {
    "IT": "Armenia"
  },
  "Australia": {
    "IT": "Australia"
  },
  "Austria": {
    "IT": "Austria"
  },
  "Azerbaijan": {
    "IT": "Azerbaigian"
  },
  "Bahamas": {
    "IT": "Bahamas"
  },
  "Bahrain": {
    "IT": "Bahrein"
  },
  "Bangladesh": {
    "IT": "Bangladesh"
  },
  "Barbados": {
    "IT": "Barbados"
  },
  "Belarus": {
    "IT": "Bielorussia"
  },
  "Belgium": {
    "IT": "Belgio"
  },
  "Belize": {
    "IT": "Belize"
  },
  "Benin": {
    "IT": "Benin"
  },
  "Bhutan": {
    "IT": "Bhutan"
  },
  "Bolivia": {
    "IT": "Bolivia"
  },
  "Bosnia and Herzegovina": {
    "IT": "Bosnia ed Erzegovina"
  },
  "Botswana": {
    "IT": "Botswana"
  },
  "Brazil": {
    "IT": "Brasile"
  },
  "Brunei": {
    "IT": "Brunei"
  },
  "Bulgaria": {
    "IT": "Bulgaria"
  },
  "Burkina Faso": {
    "IT": "Burkina Faso"
  },
  "Burundi": {
    "IT": "Burundi"
  },
  "Cabo Verde": {
    "IT": "Capo Verde"
  },
  "Cambodia": {
    "IT": "Cambogia"
  },
  "Cameroon": {
    "IT": "Camerun"
  },
  "Canada": {
    "IT": "Canada"
  },
  "Central African Republic": {
    "IT": "Repubblica Centrafricana"
  },
  "Chad": {
    "IT": "Ciad"
  },
  "Chile": {
    "IT": "Cile"
  },
  "China": {
    "IT": "Cina"
  },
  "Colombia": {
    "IT": "Colombia"
  },
  "Comoros": {
    "IT": "Comore"
  },
  "Congo (Congo-Brazzaville)": {
    "IT": "Congo (Brazzaville)"
  },
  "Costa Rica": {
    "IT": "Costa Rica"
  },
  "Croatia": {
    "IT": "Croazia"
  },
  "Cuba": {
    "IT": "Cuba"
  },
  "Cyprus": {
    "IT": "Cipro"
  },
  "Czechia (Czech Republic)": {
    "IT": "Repubblica Ceca"
  },
  "Denmark": {
    "IT": "Danimarca"
  },
  "Djibouti": {
    "IT": "Gibuti"
  },
  "Dominica": {
    "IT": "Dominica"
  },
  "Dominican Republic": {
    "IT": "Repubblica Dominicana"
  },
  "Ecuador": {
    "IT": "Ecuador"
  },
  "Egypt": {
    "IT": "Egitto"
  },
  "El Salvador": {
    "IT": "El Salvador"
  },
  "Equatorial Guinea": {
    "IT": "Guinea Equatoriale"
  },
  "Eritrea": {
    "IT": "Eritrea"
  },
  "Estonia": {
    "IT": "Estonia"
  },
  "Eswatini (fmr. Swaziland)": {
    "IT": "Eswatini (ex Swaziland)"
  },
  "Ethiopia": {
    "IT": "Etiopia"
  },
  "Fiji": {
    "IT": "Figi"
  },
  "Finland": {
    "IT": "Finlandia"
  },
  "France": {
    "IT": "Francia"
  },
  "Gabon": {
    "IT": "Gabon"
  },
  "Gambia": {
    "IT": "Gambia"
  },
  "Georgia": {
    "IT": "Georgia"
  },
  "Germany": {
    "IT": "Germania"
  },
  "Ghana": {
    "IT": "Ghana"
  },
  "Greece": {
    "IT": "Grecia"
  },
  "Grenada": {
    "IT": "Grenada"
  },
  "Guatemala": {
    "IT": "Guatemala"
  },
  "Guinea": {
    "IT": "Guinea"
  },
  "Guinea-Bissau": {
    "IT": "Guinea-Bissau"
  },
  "Guyana": {
    "IT": "Guyana"
  },
  "Haiti": {
    "IT": "Haiti"
  },
  "Honduras": {
    "IT": "Honduras"
  },
  "Hungary": {
    "IT": "Ungheria"
  },
  "Iceland": {
    "IT": "Islanda"
  },
  "India": {
    "IT": "India"
  },
  "Indonesia": {
    "IT": "Indonesia"
  },
  "Iran": {
    "IT": "Iran"
  },
  "Iraq": {
    "IT": "Iraq"
  },
  "Ireland": {
    "IT": "Irlanda"
  },
  "Israel": {
    "IT": "Israele"
  },
  "Italy": {
    "IT": "Italia"
  },
  "Jamaica": {
    "IT": "Giamaica"
  },
  "Japan": {
    "IT": "Giappone"
  },
  "Jordan": {
    "IT": "Giordania"
  },
  "Kazakhstan": {
    "IT": "Kazakistan"
  },
  "Kenya": {
    "IT": "Kenya"
  },
  "Kiribati": {
    "IT": "Kiribati"
  },
  "Korea, Democratic People's Republic of (North Korea)": {
    "IT": "Corea del Nord"
  },
  "Korea, Republic of (South Korea)": {
    "IT": "Corea del Sud"
  },
  "Kuwait": {
    "IT": "Kuwait"
  },
  "Kyrgyzstan": {
    "IT": "Kirghizistan"
  },
  "Laos": {
    "IT": "Laos"
  },
  "Latvia": {
    "IT": "Lettonia"
  },
  "Lebanon": {
    "IT": "Libano"
  },
  "Lesotho": {
    "IT": "Lesotho"
  },
  "Liberia": {
    "IT": "Liberia"
  },
  "Libya": {
    "IT": "Libia"
  },
  "Liechtenstein": {
    "IT": "Liechtenstein"
  },
  "Lithuania": {
    "IT": "Lituania"
  },
  "Luxembourg": {
    "IT": "Lussemburgo"
  },
  "Madagascar": {
    "IT": "Madagascar"
  },
  "Malawi": {
    "IT": "Malawi"
  },
  "Malaysia": {
    "IT": "Malaysia"
  },
  "Maldives": {
    "IT": "Maldive"
  },
  "Mali": {
    "IT": "Mali"
  },
  "Malta": {
    "IT": "Malta"
  },
  "Marshall Islands": {
    "IT": "Isole Marshall"
  },
  "Mauritania": {
    "IT": "Mauritania"
  },
  "Mauritius": {
    "IT": "Mauritius"
  },
  "Mexico": {
    "IT": "Messico"
  },
  "Micronesia": {
    "IT": "Micronesia"
  },
  "Moldova": {
    "IT": "Moldavia"
  },
  "Monaco": {
    "IT": "Monaco"
  },
  "Mongolia": {
    "IT": "Mongolia"
  },
  "Montenegro": {
    "IT": "Montenegro"
  },
  "Morocco": {
    "IT": "Marocco"
  },
  "Mozambique": {
    "IT": "Mozambico"
  },
  "Myanmar (formerly Burma)": {
    "IT": "Myanmar (Birmania)"
  },
  "Namibia": {
    "IT": "Namibia"
  },
  "Nauru": {
    "IT": "Nauru"
  },
  "Nepal": {
    "IT": "Nepal"
  },
  "Netherlands": {
    "IT": "Paesi Bassi"
  },
  "New Zealand": {
    "IT": "Nuova Zelanda"
  },
  "Nicaragua": {
    "IT": "Nicaragua"
  },
  "Niger": {
    "IT": "Niger"
  },
  "Nigeria": {
    "IT": "Nigeria"
  },
  "North Macedonia": {
    "IT": "Macedonia del Nord"
  },
  "Norway": {
    "IT": "Norvegia"
  },
  "Oman": {
    "IT": "Oman"
  },
  "Pakistan": {
    "IT": "Pakistan"
  },
  "Palau": {
    "IT": "Palau"
  },
  "Palestine State": {
    "IT": "Stato di Palestina"
  },
  "Panama": {
    "IT": "Panama"
  },
  "Papua New Guinea": {
    "IT": "Papua Nuova Guinea"
  },
  "Paraguay": {
    "IT": "Paraguay"
  },
  "Peru": {
    "IT": "Perù"
  },
  "Philippines": {
    "IT": "Filippine"
  },
  "Poland": {
    "IT": "Polonia"
  },
  "Portugal": {
    "IT": "Portogallo"
  },
  "Qatar": {
    "IT": "Qatar"
  },
  "Romania": {
    "IT": "Romania"
  },
  "Russia": {
    "IT": "Russia"
  },
  "Rwanda": {
    "IT": "Ruanda"
  },
  "Saint Kitts and Nevis": {
    "IT": "Saint Kitts e Nevis"
  },
  "Saint Lucia": {
    "IT": "Santa Lucia"
  },
  "Saint Vincent and the Grenadines": {
    "IT": "Saint Vincent e Grenadine"
  },
  "Samoa": {
    "IT": "Samoa"
  },
  "San Marino": {
    "IT": "San Marino"
  },
  "Sao Tome and Principe": {
    "IT": "São Tomé e Príncipe"
  },
  "Saudi Arabia": {
    "IT": "Arabia Saudita"
  },
  "Senegal": {
    "IT": "Senegal"
  },
  "Serbia": {
    "IT": "Serbia"
  },
  "Seychelles": {
    "IT": "Seychelles"
  },
  "Sierra Leone": {
    "IT": "Sierra Leone"
  },
  "Singapore": {
    "IT": "Singapore"
  },
  "Slovakia": {
    "IT": "Slovacchia"
  },
  "Slovenia": {
    "IT": "Slovenia"
  },
  "Solomon Islands": {
    "IT": "Isole Salomone"
  },
  "Somalia": {
    "IT": "Somalia"
  },
  "South Africa": {
    "IT": "Sud Africa"
  },
  "South Sudan": {
    "IT": "Sud Sudan"
  },
  "Spain": {
    "IT": "Spagna"
  },
  "Sri Lanka": {
    "IT": "Sri Lanka"
  },
  "Sudan": {
    "IT": "Sudan"
  },
  "Suriname": {
    "IT": "Suriname"
  },
  "Sweden": {
    "IT": "Svezia"
  },
  "Switzerland": {
    "IT": "Svizzera"
  },
  "Syria": {
    "IT": "Siria"
  },
  "Tajikistan": {
    "IT": "Tagikistan"
  },
  "Tanzania": {
    "IT": "Tanzania"
  },
  "Thailand": {
    "IT": "Thailandia"
  },
  "Timor-Leste": {
    "IT": "Timor Est"
  },
  "Togo": {
    "IT": "Togo"
  },
  "Tonga": {
    "IT": "Tonga"
  },
  "Trinidad and Tobago": {
    "IT": "Trinidad e Tobago"
  },
  "Tunisia": {
    "IT": "Tunisia"
  },
  "Turkey": {
    "IT": "Turchia"
  },
  "Turkmenistan": {
    "IT": "Turkmenistan"
  },
  "Tuvalu": {
    "IT": "Tuvalu"
  },
  "Uganda": {
    "IT": "Uganda"
  },
  "Ukraine": {
    "IT": "Ucraina"
  },
  "United Arab Emirates": {
    "IT": "Emirati Arabi Uniti"
  },
  "United Kingdom": {
    "IT": "Regno Unito"
  },
  "United States of America": {
    "IT": "Stati Uniti d'America"
  },
  "Uruguay": {
    "IT": "Uruguay"
  },
  "Uzbekistan": {
    "IT": "Uzbekistan"
  },
  "Vanuatu": {
    "IT": "Vanuatu"
  },
  "Vatican City (Holy See)": {
    "IT": "Città del Vaticano"
  },
  "Venezuela": {
    "IT": "Venezuela"
  },
  "Vietnam": {
    "IT": "Vietnam"
  },
  "Yemen": {
    "IT": "Yemen"
  },
  "Zambia": {
    "IT": "Zambia"
  },
  "Zimbabwe": {
    "IT": "Zimbabwe"
  }
}

countries_with_codes1 = {
    "Afghanistan": { "code": "AF" },
    "Albania": { "code": "AL" },
    "Algeria": { "code": "DZ" },
    "Andorra": { "code": "AD" },
    "Angola": { "code": "AO" },
    "Antigua and Barbuda": { "code": "AG" },
    "Argentina": { "code": "AR" },
    "Armenia": { "code": "AM" },
    "Australia": { "code": "AU" },
    "Austria": { "code": "AT" },
    "Azerbaijan": { "code": "AZ" },
    "Bahamas": { "code": "BS" },
    "Bahrain": { "code": "BH" },
    "Bangladesh": { "code": "BD" },
    "Barbados": { "code": "BB" },
    "Belarus": { "code": "BY" },
    "Belgium": { "code": "BE" },
    "Belize": { "code": "BZ" },
    "Benin": { "code": "BJ" },
    "Bhutan": { "code": "BT" },
    "Bolivia": { "code": "BO" },
    "Bosnia and Herzegovina": { "code": "BA" },
    "Botswana": { "code": "BW" },
    "Brazil": { "code": "BR" },
    "Brunei": { "code": "BN" },
    "Bulgaria": { "code": "BG" },
    "Burkina Faso": { "code": "BF" },
    "Burundi": { "code": "BI" },
    "Cabo Verde": { "code": "CV" },
    "Cambodia": { "code": "KH" },
    "Cameroon": { "code": "CM" },
    "Canada": { "code": "CA" },
    "Central African Republic": { "code": "CF" },
    "Chad": { "code": "TD" },
    "Chile": { "code": "CL" },
    "China": { "code": "CN" },
    "Colombia": { "code": "CO" },
    "Comoros": { "code": "KM" },
    "Congo (Congo-Brazzaville)": { "code": "CG" },
    "Costa Rica": { "code": "CR" },
    "Croatia": { "code": "HR" },
    "Cuba": { "code": "CU" },
    "Cyprus": { "code": "CY" },
    "Czechia (Czech Republic)": { "code": "CZ" },
    "Denmark": { "code": "DK" },
    "Djibouti": { "code": "DJ" },
    "Dominica": { "code": "DM" },
    "Dominican Republic": { "code": "DO" },
    "Ecuador": { "code": "EC" },
    "Egypt": { "code": "EG" },
    "El Salvador": { "code": "SV" },
    "Equatorial Guinea": { "code": "GQ" },
    "Eritrea": { "code": "ER" },
    "Estonia": { "code": "EE" },
    "Eswatini (fmr. Swaziland)": { "code": "SZ" },
    "Ethiopia": { "code": "ET" },
    "Fiji": { "code": "FJ" },
    "Finland": { "code": "FI" },
    "France": { "code": "FR" },
    "Gabon": { "code": "GA" },
    "Gambia": { "code": "GM" },
    "Georgia": { "code": "GE" },
    "Germany": { "code": "DE" },
    "Ghana": { "code": "GH" },
    "Greece": { "code": "GR" },
    "Grenada": { "code": "GD" },
    "Guatemala": { "code": "GT" },
    "Guinea": { "code": "GN" },
    "Guinea-Bissau": { "code": "GW" },
    "Guyana": { "code": "GY" },
    "Haiti": { "code": "HT" },
    "Honduras": { "code": "HN" },
    "Hungary": { "code": "HU" },
    "Iceland": { "code": "IS" },
    "India": { "code": "IN" },
    "Indonesia": { "code": "ID" },
    "Iran": { "code": "IR" },
    "Iraq": { "code": "IQ" },
    "Ireland": { "code": "IE" },
    "Israel": { "code": "IL" },
    "Italy": { "code": "IT" },
    "Jamaica": { "code": "JM" },
    "Japan": { "code": "JP" },
    "Jordan": { "code": "JO" },
    "Kazakhstan": { "code": "KZ" },
    "Kenya": { "code": "KE" },
    "Kiribati": { "code": "KI" },
    "Korea, Democratic People's Republic of (North Korea)": { "code": "KP" },
    "Korea, Republic of (South Korea)": { "code": "KR" },
    "Kuwait": { "code": "KW" },
    "Kyrgyzstan": { "code": "KG" },
    "Laos": { "code": "LA" },
    "Latvia": { "code": "LV" },
    "Lebanon": { "code": "LB" },
    "Lesotho": { "code": "LS" },
    "Liberia": { "code": "LR" },
    "Libya": { "code": "LY" },
    "Liechtenstein": { "code": "LI" },
    "Lithuania": { "code": "LT" },
    "Luxembourg": { "code": "LU" },
    "Madagascar": { "code": "MG" },
    "Malawi": { "code": "MW" },
    "Malaysia": { "code": "MY" },
    "Maldives": { "code": "MV" },
    "Mali": { "code": "ML" },
    "Malta": { "code": "MT" },
    "Marshall Islands": { "code": "MH" },
    "Mauritania": { "code": "MR" },
    "Mauritius": { "code": "MU" },
    "Mexico": { "code": "MX" },
    "Micronesia": { "code": "FM" },
    "Moldova": { "code": "MD" },
    "Monaco": { "code": "MC" },
    "Mongolia": { "code": "MN" },
    "Montenegro": { "code": "ME" },
    "Morocco": { "code": "MA" },
    "Mozambique": { "code": "MZ" },
    "Myanmar (formerly Burma)": { "code": "MM" },
    "Namibia": { "code": "NA" },
    "Nauru": { "code": "NR" },
    "Nepal": { "code": "NP" },
    "Netherlands": { "code": "NL" },
    "New Zealand": { "code": "NZ" },
    "Nicaragua": { "code": "NI" },
    "Niger": { "code": "NE" },
    "Nigeria": { "code": "NG" },
    "North Macedonia": { "code": "MK" },
    "Norway": { "code": "NO" },
    "Oman": { "code": "OM" },
    "Pakistan": { "code": "PK" },
    "Palau": { "code": "PW" },
    "Palestine State": { "code": "PS" },
    "Panama": { "code": "PA" },
    "Papua New Guinea": { "code": "PG" },
    "Paraguay": { "code": "PY" },
    "Peru": { "code": "PE" },
    "Philippines": { "code": "PH" },
    "Poland": { "code": "PL" },
    "Portugal": { "code": "PT" },
    "Qatar": { "code": "QA" },
    "Romania": { "code": "RO" },
    "Russia": { "code": "RU" },
    "Rwanda": { "code": "RW" },
    "Saint Kitts and Nevis": { "code": "KN" },
    "Saint Lucia": { "code": "LC" },
    "Saint Vincent and the Grenadines": { "code": "VC" },
    "Samoa": { "code": "WS" },
    "San Marino": { "code": "SM" },
    "Sao Tome and Principe": { "code": "ST" },
    "Saudi Arabia": { "code": "SA" },
    "Senegal": { "code": "SN" },
    "Serbia": { "code": "RS" },
    "Seychelles": { "code": "SC" },
    "Sierra Leone": { "code": "SL" },
    "Singapore": { "code": "SG" },
    "Slovakia": { "code": "SK" },
    "Slovenia": { "code": "SI" },
    "Solomon Islands": { "code": "SB" },
    "Somalia": { "code": "SO" },
    "South Africa": { "code": "ZA" },
    "South Sudan": { "code": "SS" },
    "Spain": { "code": "ES" },
    "Sri Lanka": { "code": "LK" },
    "Sudan": { "code": "SD" },
    "Suriname": { "code": "SR" },
    "Sweden": { "code": "SE" },
    "Switzerland": { "code": "CH" },
    "Syria": { "code": "SY" },
    "Tajikistan": { "code": "TJ" },
    "Tanzania": { "code": "TZ" },
    "Thailand": { "code": "TH" },
    "Timor-Leste": { "code": "TL" },
    "Togo": { "code": "TG" },
    "Tonga": { "code": "TO" },
    "Trinidad and Tobago": { "code": "TT" },
    "Tunisia": { "code": "TN" },
    "Turkey": { "code": "TR" },
    "Turkmenistan": { "code": "TM" },
    "Tuvalu": { "code": "TV" },
    "Uganda": { "code": "UG" },
    "Ukraine": { "code": "UA" },
    "United Arab Emirates": { "code": "AE" },
    "United Kingdom": { "code": "GB" },
    "United States of America": { "code": "US" },
    "Uruguay": { "code": "UY" },
    "Uzbekistan": { "code": "UZ" },
    "Vanuatu": { "code": "VU" },
    "Vatican City (Holy See)": { "code": "VA" },
    "Venezuela": { "code": "VE" },
    "Vietnam": { "code": "VN" },
    "Yemen": { "code": "YE" },
    "Zambia": { "code": "ZM" },
    "Zimbabwe": { "code": "ZW" }
}

# Sample data of countries and their flag URLs
countries_with_flags = {
    "Afghanistan": {
        "FR": "https://flagcdn.com/w320/af.png"
    },
    "Albania": {
        "FR": "https://flagcdn.com/w320/al.png"
    },
    "Algeria": {
        "FR": "https://flagcdn.com/w320/dz.png"
    },
    "Andorra": {
        "FR": "https://flagcdn.com/w320/ad.png"
    },
    "Angola": {
        "FR": "https://flagcdn.com/w320/ao.png"
    },
    "Antigua and Barbuda": {
        "FR": "https://flagcdn.com/w320/ag.png"
    },
    "Argentina": {
        "FR": "https://flagcdn.com/w320/ar.png"
    },
    "Armenia": {
        "FR": "https://flagcdn.com/w320/am.png"
    },
    "Australia": {
        "FR": "https://flagcdn.com/w320/au.png"
    },
    "Austria": {
        "FR": "https://flagcdn.com/w320/at.png"
    },
    "Azerbaijan": {
        "FR": "https://flagcdn.com/w320/az.png"
    },
    "Bahamas": {
        "FR": "https://flagcdn.com/w320/bs.png"
    },
    "Bahrain": {
        "FR": "https://flagcdn.com/w320/bh.png"
    },
    "Bangladesh": {
        "FR": "https://flagcdn.com/w320/bd.png"
    },
    "Barbados": {
        "FR": "https://flagcdn.com/w320/bb.png"
    },
    "Belarus": {
        "FR": "https://flagcdn.com/w320/by.png"
    },
    "Belgium": {
        "FR": "https://flagcdn.com/w320/be.png"
    },
    "Belize": {
        "FR": "https://flagcdn.com/w320/bz.png"
    },
    "Benin": {
        "FR": "https://flagcdn.com/w320/bj.png"
    },
    "Bhutan": {
        "FR": "https://flagcdn.com/w320/bt.png"
    },
    "Bolivia": {
        "FR": "https://flagcdn.com/w320/bo.png"
    },
    "Bosnia and Herzegovina": {
        "FR": "https://flagcdn.com/w320/ba.png"
    },
    "Botswana": {
        "FR": "https://flagcdn.com/w320/bw.png"
    },
    "Brazil": {
        "FR": "https://flagcdn.com/w320/br.png"
    },
    "Brunei": {
        "FR": "https://flagcdn.com/w320/bn.png"
    },
    "Bulgaria": {
        "FR": "https://flagcdn.com/w320/bg.png"
    },
    "Burkina Faso": {
        "FR": "https://flagcdn.com/w320/bf.png"
    },
    "Burundi": {
        "FR": "https://flagcdn.com/w320/bi.png"
    },
    "Cabo Verde": {
        "FR": "https://flagcdn.com/w320/cv.png"
    },
    "Cambodia": {
        "FR": "https://flagcdn.com/w320/kh.png"
    },
    "Cameroon": {
        "FR": "https://flagcdn.com/w320/cm.png"
    },
    "Canada": {
        "FR": "https://flagcdn.com/w320/ca.png"
    },
    "Central African Republic": {
        "FR": "https://flagcdn.com/w320/cf.png"
    },
    "Chad": {
        "FR": "https://flagcdn.com/w320/td.png"
    },
    "Chile": {
        "FR": "https://flagcdn.com/w320/cl.png"
    },
    "China": {
        "FR": "https://flagcdn.com/w320/cn.png"
    },
    "Colombia": {
        "FR": "https://flagcdn.com/w320/co.png"
    },
    "Comoros": {
        "FR": "https://flagcdn.com/w320/km.png"
    },
    "Congo (Congo-Brazzaville)": {
        "FR": "https://flagcdn.com/w320/cg.png"
    },
    "Costa Rica": {
        "FR": "https://flagcdn.com/w320/cr.png"
    },
    "Croatia": {
        "FR": "https://flagcdn.com/w320/hr.png"
    },
    "Cuba": {
        "FR": "https://flagcdn.com/w320/cu.png"
    },
    "Cyprus": {
        "FR": "https://flagcdn.com/w320/cy.png"
    },
    "Czechia (Czech Republic)": {
        "FR": "https://flagcdn.com/w320/cz.png"
    },
    "Denmark": {
        "FR": "https://flagcdn.com/w320/dk.png"
    },
    "Djibouti": {
        "FR": "https://flagcdn.com/w320/dj.png"
    },
    "Dominica": {
        "FR": "https://flagcdn.com/w320/dm.png"
    },
    "Dominican Republic": {
        "FR": "https://flagcdn.com/w320/do.png"
    },
    "Ecuador": {
        "FR": "https://flagcdn.com/w320/ec.png"
    },
    "Egypt": {
        "FR": "https://flagcdn.com/w320/eg.png"
    },
    "El Salvador": {
        "FR": "https://flagcdn.com/w320/sv.png"
    },
    "Equatorial Guinea": {
        "FR": "https://flagcdn.com/w320/gq.png"
    },
    "Eritrea": {
        "FR": "https://flagcdn.com/w320/er.png"
    },
    "Estonia": {
        "FR": "https://flagcdn.com/w320/ee.png"
    },
    "Eswatini (fmr. Swaziland)": {
        "FR": "https://flagcdn.com/w320/sz.png"
    },
    "Ethiopia": {
        "FR": "https://flagcdn.com/w320/et.png"
    },
    "Fiji": {
        "FR": "https://flagcdn.com/w320/fj.png"
    },
    "Finland": {
        "FR": "https://flagcdn.com/w320/fi.png"
    },
    "France": {
        "FR": "https://flagcdn.com/w320/fr.png"
    },
    "Gabon": {
        "FR": "https://flagcdn.com/w320/ga.png"
    },
    "Gambia": {
        "FR": "https://flagcdn.com/w320/gm.png"
    },
    "Georgia": {
        "FR": "https://flagcdn.com/w320/ge.png"
    },
    "Germany": {
        "FR": "https://flagcdn.com/w320/de.png"
    },
    "Ghana": {
        "FR": "https://flagcdn.com/w320/gh.png"
    },
    "Greece": {
        "FR": "https://flagcdn.com/w320/gr.png"
    },
    "Grenada": {
        "FR": "https://flagcdn.com/w320/gd.png"
    },
    "Guatemala": {
        "FR": "https://flagcdn.com/w320/gt.png"
    },
    "Guinea": {
        "FR": "https://flagcdn.com/w320/gn.png"
    },
    "Guinea-Bissau": {
        "FR": "https://flagcdn.com/w320/gw.png"
    },
    "Guyana": {
        "FR": "https://flagcdn.com/w320/gy.png"
    },
    "Haiti": {
        "FR": "https://flagcdn.com/w320/ht.png"
    },
    "Honduras": {
        "FR": "https://flagcdn.com/w320/hn.png"
    },
    "Hungary": {
        "FR": "https://flagcdn.com/w320/hu.png"
    },
    "Iceland": {
        "FR": "https://flagcdn.com/w320/is.png"
    },
    "India": {
        "FR": "https://flagcdn.com/w320/in.png"
    },
    "Indonesia": {
        "FR": "https://flagcdn.com/w320/id.png"
    },
    "Iran": {
        "FR": "https://flagcdn.com/w320/ir.png"
    },
    "Iraq": {
        "FR": "https://flagcdn.com/w320/iq.png"
    },
    "Ireland": {
        "FR": "https://flagcdn.com/w320/ie.png"
    },
    "Israel": {
        "FR": "https://flagcdn.com/w320/il.png"
    },
    "Italy": {
        "FR": "https://flagcdn.com/w320/it.png"
    },
    "Jamaica": {
        "FR": "https://flagcdn.com/w320/jm.png"
    },
    "Japan": {
        "FR": "https://flagcdn.com/w320/jp.png"
    },
    "Jordan": {
        "FR": "https://flagcdn.com/w320/jo.png"
    },
    "Kazakhstan": {
        "FR": "https://flagcdn.com/w320/kz.png"
    },
    "Kenya": {
        "FR": "https://flagcdn.com/w320/ke.png"
    },
    "Kiribati": {
        "FR": "https://flagcdn.com/w320/ki.png"
    },
    "Korea, Democratic People's Republic of (North Korea)": {
        "FR": "https://flagcdn.com/w320/kp.png"
    },
    "Korea, Republic of (South Korea)": {
        "FR": "https://flagcdn.com/w320/kr.png"
    },
    "Kuwait": {
        "FR": "https://flagcdn.com/w320/kw.png"
    },
    "Kyrgyzstan": {
        "FR": "https://flagcdn.com/w320/kg.png"
    },
    "Laos": {
        "FR": "https://flagcdn.com/w320/la.png"
    },
    "Latvia": {
        "FR": "https://flagcdn.com/w320/lv.png"
    },
    "Lebanon": {
        "FR": "https://flagcdn.com/w320/lb.png"
    },
    "Lesotho": {
        "FR": "https://flagcdn.com/w320/ls.png"
    },
    "Liberia": {
        "FR": "https://flagcdn.com/w320/lr.png"
    },
    "Libya": {
        "FR": "https://flagcdn.com/w320/ly.png"
    },
    "Liechtenstein": {
        "FR": "https://flagcdn.com/w320/li.png"
    },
    "Lithuania": {
        "FR": "https://flagcdn.com/w320/lt.png"
    },
    "Luxembourg": {
        "FR": "https://flagcdn.com/w320/lu.png"
    },
    "Madagascar": {
        "FR": "https://flagcdn.com/w320/mg.png"
    },
    "Malawi": {
        "FR": "https://flagcdn.com/w320/mw.png"
    },
    "Malaysia": {
        "FR": "https://flagcdn.com/w320/my.png"
    },
    "Maldives": {
        "FR": "https://flagcdn.com/w320/mv.png"
    },
    "Mali": {
        "FR": "https://flagcdn.com/w320/ml.png"
    },
    "Malta": {
        "FR": "https://flagcdn.com/w320/mt.png"
    },
    "Marshall Islands": {
        "FR": "https://flagcdn.com/w320/mh.png"
    },
    "Mauritania": {
        "FR": "https://flagcdn.com/w320/mr.png"
    },
    "Mauritius": {
        "FR": "https://flagcdn.com/w320/mu.png"
    },
    "Mexico": {
        "FR": "https://flagcdn.com/w320/mx.png"
    },
    "Micronesia": {
        "FR": "https://flagcdn.com/w320/fm.png"
    },
    "Moldova": {
        "FR": "https://flagcdn.com/w320/md.png"
    },
    "Monaco": {
        "FR": "https://flagcdn.com/w320/mc.png"
    },
    "Mongolia": {
        "FR": "https://flagcdn.com/w320/mn.png"
    },
    "Montenegro": {
        "FR": "https://flagcdn.com/w320/me.png"
    },
    "Morocco": {
        "FR": "https://flagcdn.com/w320/ma.png"
    },
    "Mozambique": {
        "FR": "https://flagcdn.com/w320/mz.png"
    },
    "Myanmar (formerly Burma)": {
        "FR": "https://flagcdn.com/w320/mm.png"
    },
    "Namibia": {
        "FR": "https://flagcdn.com/w320/na.png"
    },
    "Nauru": {
        "FR": "https://flagcdn.com/w320/nr.png"
    },
    "Nepal": {
        "FR": "https://flagcdn.com/w320/np.png"
    },
    "Netherlands": {
        "FR": "https://flagcdn.com/w320/nl.png"
    },
    "New Zealand": {
        "FR": "https://flagcdn.com/w320/nz.png"
    },
    "Nicaragua": {
        "FR": "https://flagcdn.com/w320/ni.png"
    },
    "Niger": {
        "FR": "https://flagcdn.com/w320/ne.png"
    },
    "Nigeria": {
        "FR": "https://flagcdn.com/w320/ng.png"
    },
    "North Macedonia": {
        "FR": "https://flagcdn.com/w320/mk.png"
    },
    "Norway": {
        "FR": "https://flagcdn.com/w320/no.png"
    },
    "Oman": {
        "FR": "https://flagcdn.com/w320/om.png"
    },
    "Pakistan": {
        "FR": "https://flagcdn.com/w320/pk.png"
    },
    "Palau": {
        "FR": "https://flagcdn.com/w320/pw.png"
    },
    "Palestine State": {
        "FR": "https://flagcdn.com/w320/ps.png"
    },
    "Panama": {
        "FR": "https://flagcdn.com/w320/pa.png"
    },
    "Papua New Guinea": {
        "FR": "https://flagcdn.com/w320/pg.png"
    },
    "Paraguay": {
        "FR": "https://flagcdn.com/w320/py.png"
    },
    "Peru": {
        "FR": "https://flagcdn.com/w320/pe.png"
    },
    "Philippines": {
        "FR": "https://flagcdn.com/w320/ph.png"
    },
    "Poland": {
        "FR": "https://flagcdn.com/w320/pl.png"
    },
    "Portugal": {
        "FR": "https://flagcdn.com/w320/pt.png"
    },
    "Qatar": {
        "FR": "https://flagcdn.com/w320/qa.png"
    },
    "Romania": {
        "FR": "https://flagcdn.com/w320/ro.png"
    },
    "Russia": {
        "FR": "https://flagcdn.com/w320/ru.png"
    },
    "Rwanda": {
        "FR": "https://flagcdn.com/w320/rw.png"
    },
    "Saint Kitts and Nevis": {
        "FR": "https://flagcdn.com/w320/kn.png"
    },
    "Saint Lucia": {
        "FR": "https://flagcdn.com/w320/lc.png"
    },
    "Saint Vincent and the Grenadines": {
        "FR": "https://flagcdn.com/w320/vc.png"
    },
    "Samoa": {
        "FR": "https://flagcdn.com/w320/ws.png"
    },
    "San Marino": {
        "FR": "https://flagcdn.com/w320/sm.png"
    },
    "Sao Tome and Principe": {
        "FR": "https://flagcdn.com/w320/st.png"
    },
    "Saudi Arabia": {
        "FR": "https://flagcdn.com/w320/sa.png"
    },
    "Senegal": {
        "FR": "https://flagcdn.com/w320/sn.png"
    },
    "Serbia": {
        "FR": "https://flagcdn.com/w320/rs.png"
    },
    "Seychelles": {
        "FR": "https://flagcdn.com/w320/sc.png"
    },
    "Sierra Leone": {
        "FR": "https://flagcdn.com/w320/sl.png"
    },
    "Singapore": {
        "FR": "https://flagcdn.com/w320/sg.png"
    },
    "Slovakia": {
        "FR": "https://flagcdn.com/w320/sk.png"
    },
    "Slovenia": {
        "FR": "https://flagcdn.com/w320/si.png"
    },
    "Solomon Islands": {
        "FR": "https://flagcdn.com/w320/sb.png"
    },
    "Somalia": {
        "FR": "https://flagcdn.com/w320/so.png"
    },
    "South Africa": {
        "FR": "https://flagcdn.com/w320/za.png"
    },
    "South Sudan": {
        "FR": "https://flagcdn.com/w320/ss.png"
    },
    "Spain": {
        "FR": "https://flagcdn.com/w320/es.png"
    },
    "Sri Lanka": {
        "FR": "https://flagcdn.com/w320/lk.png"
    },
    "Sudan": {
        "FR": "https://flagcdn.com/w320/sd.png"
    },
    "Suriname": {
        "FR": "https://flagcdn.com/w320/sr.png"
    },
    "Sweden": {
        "FR": "https://flagcdn.com/w320/se.png"
    },
    "Switzerland": {
        "FR": "https://flagcdn.com/w320/ch.png"
    },
    "Syria": {
        "FR": "https://flagcdn.com/w320/sy.png"
    },
    "Tajikistan": {
        "FR": "https://flagcdn.com/w320/tj.png"
    },
    "Tanzania": {
        "FR": "https://flagcdn.com/w320/tz.png"
    },
    "Thailand": {
        "FR": "https://flagcdn.com/w320/th.png"
    },
    "Timor-Leste": {
        "FR": "https://flagcdn.com/w320/tl.png"
    },
    "Togo": {
        "FR": "https://flagcdn.com/w320/tg.png"
    },
    "Tonga": {
        "FR": "https://flagcdn.com/w320/to.png"
    },
    "Trinidad and Tobago": {
        "FR": "https://flagcdn.com/w320/tt.png"
    },
    "Tunisia": {
        "FR": "https://flagcdn.com/w320/tn.png"
    },
    "Turkey": {
        "FR": "https://flagcdn.com/w320/tr.png"
    },
    "Turkmenistan": {
        "FR": "https://flagcdn.com/w320/tm.png"
    },
    "Tuvalu": {
        "FR": "https://flagcdn.com/w320/tv.png"
    },
    "Uganda": {
        "FR": "https://flagcdn.com/w320/ug.png"
    },
    "Ukraine": {
        "FR": "https://flagcdn.com/w320/ua.png"
    },
    "United Arab Emirates": {
        "FR": "https://flagcdn.com/w320/ae.png"
    },
    "United Kingdom": {
        "FR": "https://flagcdn.com/w320/gb.png"
    },
    "United States of America": {
        "FR": "https://flagcdn.com/w320/us.png"
    },
    "Uruguay": {
        "FR": "https://flagcdn.com/w320/uy.png"
    },
    "Uzbekistan": {
        "FR": "https://flagcdn.com/w320/uz.png"
    },
    "Vanuatu": {
        "FR": "https://flagcdn.com/w320/vu.png"
    },
    "Vatican City (Holy See)": {
        "FR": "https://flagcdn.com/w320/va.png"
    },
    "Venezuela": {
        "FR": "https://flagcdn.com/w320/ve.png"
    },
    "Vietnam": {
        "FR": "https://flagcdn.com/w320/vn.png"
    },
    "Yemen": {
        "FR": "https://flagcdn.com/w320/ye.png"
    },
    "Zambia": {
        "FR": "https://flagcdn.com/w320/zm.png"
    },
    "Zimbabwe": {
        "FR": "https://flagcdn.com/w320/zw.png"
    }
}

# Define a function to merge the two dictionaries into one list
def merge_translation_dicts(dict1, dict2):
    merged_list = []
    for country in dict1:
        if country in dict2:
            merged_dict = { country: { "ES": dict1[country]["ES"], "IT": dict2[country]["IT"] } }
            merged_list.append(merged_dict)
    return merged_list

if __name__ == "__main__":
    # Convert dictionaries to lists
    merged_list = merge_translation_dicts(country_es_to_en1, country_it_to_en1)
    # Print the merged list
    json_obj = json.dumps(merged_list, indent=2, ensure_ascii=False)
    file_path = "src/utils/countries_es+it_2024_08_26_12_19.json"
    print(json_obj)
    write_output_to_file(data=json_obj, file_name=file_path, path_includes_in_file_name=True, include_seconds_in_date=False, extension='.json')
