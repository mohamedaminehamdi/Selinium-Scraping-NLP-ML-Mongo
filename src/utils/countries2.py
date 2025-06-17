import json
from enum import Enum
from typing import Final, Optional

# countries and their codes (ISO 3166-1 alpha-2 codes)
countries_en_fr_de_es_it: Final[dict] = {
    "Afghanistan": {
        "FR": "Afghanistan",
        "DE": "Afghanistan",
        "ES": "Afganistán",
        "IT": "Afghanistan",
        "code": "AF",
        "flag": "https://flagcdn.com/w320/af.png"
    },
    "Albania": {
        "FR": "Albanie",
        "DE": "Albanien",
        "ES": "Albania",
        "IT": "Albania",
        "code": "AL",
        "flag": "https://flagcdn.com/w320/al.png"
    },
    "Algeria": {
        "FR": "Algérie",
        "DE": "Algerien",
        "ES": "Argelia",
        "IT": "Algeria",
        "code": "DZ",
        "flag": "https://flagcdn.com/w320/dz.png"
    },
    "Andorra": {
        "FR": "Andorre",
        "DE": "Andorra",
        "ES": "Andorra",
        "IT": "Andorra",
        "code": "AD",
        "flag": "https://flagcdn.com/w320/ad.png"
    },
    "Angola": {
        "FR": "Angola",
        "DE": "Angola",
        "ES": "Angola",
        "IT": "Angola",
        "code": "AO",
        "flag": "https://flagcdn.com/w320/ao.png"
    },
    "Antigua and Barbuda": {
        "FR": "Antigua-et-Barbuda",
        "DE": "Antigua und Barbuda",
        "ES": "Antigua y Barbuda",
        "IT": "Antigua e Barbuda",
        "code": "AG",
        "flag": "https://flagcdn.com/w320/ag.png"
    },
    "Argentina": {
        "FR": "Argentine",
        "DE": "Argentinien",
        "ES": "Argentina",
        "IT": "Argentina",
        "code": "AR",
        "flag": "https://flagcdn.com/w320/ar.png"
    },
    "Armenia": {
        "FR": "Arménie",
        "DE": "Armenien",
        "ES": "Armenia",
        "IT": "Armenia",
        "code": "AM",
        "flag": "https://flagcdn.com/w320/am.png"
    },
    "Australia": {
        "FR": "Australie",
        "DE": "Australien",
        "ES": "Australia",
        "IT": "Australia",
        "code": "AU",
        "flag": "https://flagcdn.com/w320/au.png"
    },
    "Austria": {
        "FR": "Autriche",
        "DE": "Österreich",
        "ES": "Austria",
        "IT": "Austria",
        "code": "AT",
        "flag": "https://flagcdn.com/w320/at.png"
    },
    "Azerbaijan": {
        "FR": "Azerbaïdjan",
        "DE": "Aserbaidschan",
        "ES": "Azerbaiyán",
        "IT": "Azerbaigian",
        "code": "AZ",
        "flag": "https://flagcdn.com/w320/az.png"
    },
    "Bahamas": {
        "FR": "Bahamas",
        "DE": "Bahamas",
        "ES": "Bahamas",
        "IT": "Bahamas",
        "code": "BS",
        "flag": "https://flagcdn.com/w320/bs.png"
    },
    "Bahrain": {
        "FR": "Bahreïn",
        "DE": "Bahrain",
        "ES": "Baréin",
        "IT": "Bahrein",
        "code": "BH",
        "flag": "https://flagcdn.com/w320/bh.png"
    },
    "Bangladesh": {
        "FR": "Bangladesh",
        "DE": "Bangladesch",
        "ES": "Bangladés",
        "IT": "Bangladesh",
        "code": "BD",
        "flag": "https://flagcdn.com/w320/bd.png"
    },
    "Barbados": {
        "FR": "Barbade",
        "DE": "Barbados",
        "ES": "Barbados",
        "IT": "Barbados",
        "code": "BB",
        "flag": "https://flagcdn.com/w320/bb.png"
    },
    "Belarus": {
        "FR": "Biélorussie",
        "DE": "Weißrussland",
        "ES": "Bielorrusia",
        "IT": "Bielorussia",
        "code": "BY",
        "flag": "https://flagcdn.com/w320/by.png"
    },
    "Belgium": {
        "FR": "Belgique",
        "DE": "Belgien",
        "ES": "Bélgica",
        "IT": "Belgio",
        "code": "BE",
        "flag": "https://flagcdn.com/w320/be.png"
    },
    "Belize": {
        "FR": "Belize",
        "DE": "Belize",
        "ES": "Belice",
        "IT": "Belize",
        "code": "BZ",
        "flag": "https://flagcdn.com/w320/bz.png"
    },
    "Benin": {
        "FR": "Bénin",
        "DE": "Benin",
        "ES": "Benín",
        "IT": "Benin",
        "code": "BJ",
        "flag": "https://flagcdn.com/w320/bj.png"
    },
    "Bhutan": {
        "FR": "Bhoutan",
        "DE": "Bhutan",
        "ES": "Bután",
        "IT": "Bhutan",
        "code": "BT",
        "flag": "https://flagcdn.com/w320/bt.png"
    },
    "Bolivia": {
        "FR": "Bolivie",
        "DE": "Bolivien",
        "ES": "Bolivia",
        "IT": "Bolivia",
        "code": "BO",
        "flag": "https://flagcdn.com/w320/bo.png"
    },
    "Bosnia and Herzegovina": {
        "FR": "Bosnie-Herzégovine",
        "DE": "Bosnien und Herzegowina",
        "ES": "Bosnia y Herzegovina",
        "IT": "Bosnia ed Erzegovina",
        "code": "BA",
        "flag": "https://flagcdn.com/w320/ba.png"
    },
    "Botswana": {
        "FR": "Botswana",
        "DE": "Botswana",
        "ES": "Botsuana",
        "IT": "Botswana",
        "code": "BW",
        "flag": "https://flagcdn.com/w320/bw.png"
    },
    "Brazil": {
        "FR": "Brésil",
        "DE": "Brasilien",
        "ES": "Brasil",
        "IT": "Brasile",
        "code": "BR",
        "flag": "https://flagcdn.com/w320/br.png"
    },
    "Brunei": {
        "FR": "Brunéi Darussalam",
        "DE": "Brunei",
        "ES": "Brunéi",
        "IT": "Brunei",
        "code": "BN",
        "flag": "https://flagcdn.com/w320/bn.png"
    },
    "Bulgaria": {
        "FR": "Bulgarie",
        "DE": "Bulgarien",
        "ES": "Bulgaria",
        "IT": "Bulgaria",
        "code": "BG",
        "flag": "https://flagcdn.com/w320/bg.png"
    },
    "Burkina Faso": {
        "FR": "Burkina Faso",
        "DE": "Burkina Faso",
        "ES": "Burkina Faso",
        "IT": "Burkina Faso",
        "code": "BF",
        "flag": "https://flagcdn.com/w320/bf.png"
    },
    "Burundi": {
        "FR": "Burundi",
        "DE": "Burundi",
        "ES": "Burundi",
        "IT": "Burundi",
        "code": "BI",
        "flag": "https://flagcdn.com/w320/bi.png"
    },
    "Cabo Verde": {
        "FR": "Cap-Vert",
        "DE": "Cabo Verde",
        "ES": "Cabo Verde",
        "IT": "Capo Verde",
        "code": "CV",
        "flag": "https://flagcdn.com/w320/cv.png"
    },
    "Cambodia": {
        "FR": "Cambodge",
        "DE": "Kambodscha",
        "ES": "Camboya",
        "IT": "Cambogia",
        "code": "KH",
        "flag": "https://flagcdn.com/w320/kh.png"
    },
    "Cameroon": {
        "FR": "Cameroun",
        "DE": "Kamerun",
        "ES": "Camerún",
        "IT": "Camerun",
        "code": "CM",
        "flag": "https://flagcdn.com/w320/cm.png"
    },
    "Canada": {
        "FR": "Canada",
        "DE": "Kanada",
        "ES": "Canadá",
        "IT": "Canada",
        "code": "CA",
        "flag": "https://flagcdn.com/w320/ca.png"
    },
    "Central African Republic": {
        "FR": "République centrafricaine",
        "DE": "Zentralafrikanische Republik",
        "ES": "República Centroafricana",
        "IT": "Repubblica Centrafricana",
        "code": "CF",
        "flag": "https://flagcdn.com/w320/cf.png"
    },
    "Chad": {
        "FR": "Tchad",
        "DE": "Tschad",
        "ES": "Chad",
        "IT": "Ciad",
        "code": "TD",
        "flag": "https://flagcdn.com/w320/td.png"
    },
    "Chile": {
        "FR": "Chili",
        "DE": "Chile",
        "ES": "Chile",
        "IT": "Cile",
        "code": "CL",
        "flag": "https://flagcdn.com/w320/cl.png"
    },
    "China": {
        "FR": "Chine",
        "DE": "China",
        "ES": "China",
        "IT": "Cina",
        "code": "CN",
        "flag": "https://flagcdn.com/w320/cn.png"
    },
    "Colombia": {
        "FR": "Colombie",
        "DE": "Kolumbien",
        "ES": "Colombia",
        "IT": "Colombia",
        "code": "CO",
        "flag": "https://flagcdn.com/w320/co.png"
    },
    "Comoros": {
        "FR": "Comores",
        "DE": "Komoren",
        "ES": "Comoras",
        "IT": "Comore",
        "code": "KM",
        "flag": "https://flagcdn.com/w320/km.png"
    },
    "Congo (Congo-Brazzaville)": {
        "FR": "Congo (République du Congo)",
        "DE": "Kongo (Republik Kongo)",
        "ES": "Congo (Brazzaville)",
        "IT": "Congo (Brazzaville)",
        "code": "CG",
        "flag": "https://flagcdn.com/w320/cg.png"
    },
    "Costa Rica": {
        "FR": "Costa Rica",
        "DE": "Costa Rica",
        "ES": "Costa Rica",
        "IT": "Costa Rica",
        "code": "CR",
        "flag": "https://flagcdn.com/w320/cr.png"
    },
    "Croatia": {
        "FR": "Croatie",
        "DE": "Kroatien",
        "ES": "Croacia",
        "IT": "Croazia",
        "code": "HR",
        "flag": "https://flagcdn.com/w320/hr.png"
    },
    "Cuba": {
        "FR": "Cuba",
        "DE": "Kuba",
        "ES": "Cuba",
        "IT": "Cuba",
        "code": "CU",
        "flag": "https://flagcdn.com/w320/cu.png"
    },
    "Cyprus": {
        "FR": "Chypre",
        "DE": "Zypern",
        "ES": "Chipre",
        "IT": "Cipro",
        "code": "CY",
        "flag": "https://flagcdn.com/w320/cy.png"
    },
    "Czechia (Czech Republic)": {
        "FR": "Tchéquie (République tchèque)",
        "DE": "Tschechien",
        "ES": "Chequia",
        "IT": "Repubblica Ceca",
        "code": "CZ",
        "flag": "https://flagcdn.com/w320/cz.png"
    },
    "Denmark": {
        "FR": "Danemark",
        "DE": "Dänemark",
        "ES": "Dinamarca",
        "IT": "Danimarca",
        "code": "DK",
        "flag": "https://flagcdn.com/w320/dk.png"
    },
    "Djibouti": {
        "FR": "Djibouti",
        "DE": "Dschibuti",
        "ES": "Yibuti",
        "IT": "Gibuti",
        "code": "DJ",
        "flag": "https://flagcdn.com/w320/dj.png"
    },
    "Dominica": {
        "FR": "Dominique",
        "DE": "Dominica",
        "ES": "Dominica",
        "IT": "Dominica",
        "code": "DM",
        "flag": "https://flagcdn.com/w320/dm.png"
    },
    "Dominican Republic": {
        "FR": "République dominicaine",
        "DE": "Dominikanische Republik",
        "ES": "República Dominicana",
        "IT": "Repubblica Dominicana",
        "code": "DO",
        "flag": "https://flagcdn.com/w320/do.png"
    },
    "Ecuador": {
        "FR": "Équateur",
        "DE": "Ecuador",
        "ES": "Ecuador",
        "IT": "Ecuador",
        "code": "EC",
        "flag": "https://flagcdn.com/w320/ec.png"
    },
    "Egypt": {
        "FR": "Égypte",
        "DE": "Ägypten",
        "ES": "Egipto",
        "IT": "Egitto",
        "code": "EG",
        "flag": "https://flagcdn.com/w320/eg.png"
    },
    "El Salvador": {
        "FR": "Salvador",
        "DE": "El Salvador",
        "ES": "El Salvador",
        "IT": "El Salvador",
        "code": "SV",
        "flag": "https://flagcdn.com/w320/sv.png"
    },
    "Equatorial Guinea": {
        "FR": "Guinée équatoriale",
        "DE": "Äquatorialguinea",
        "ES": "Guinea Ecuatorial",
        "IT": "Guinea Equatoriale",
        "code": "GQ",
        "flag": "https://flagcdn.com/w320/gq.png"
    },
    "Eritrea": {
        "FR": "Érythrée",
        "DE": "Eritrea",
        "ES": "Eritrea",
        "IT": "Eritrea",
        "code": "ER",
        "flag": "https://flagcdn.com/w320/er.png"
    },
    "Estonia": {
        "FR": "Estonie",
        "DE": "Estland",
        "ES": "Estonia",
        "IT": "Estonia",
        "code": "EE",
        "flag": "https://flagcdn.com/w320/ee.png"
    },
    "Eswatini (fmr. Swaziland)": {
        "FR": "Eswatini (anciennement Swaziland)",
        "DE": "Eswatini (ehemals Swasiland)",
        "ES": "Esuatini",
        "IT": "Eswatini (ex Swaziland)",
        "code": "SZ",
        "flag": "https://flagcdn.com/w320/sz.png"
    },
    "Ethiopia": {
        "FR": "Éthiopie",
        "DE": "Äthiopien",
        "ES": "Etiopía",
        "IT": "Etiopia",
        "code": "ET",
        "flag": "https://flagcdn.com/w320/et.png"
    },
    "Fiji": {
        "FR": "Fidji",
        "DE": "Fidschi",
        "ES": "Fiyi",
        "IT": "Figi",
        "code": "FJ",
        "flag": "https://flagcdn.com/w320/fj.png"
    },
    "Finland": {
        "FR": "Finlande",
        "DE": "Finnland",
        "ES": "Finlandia",
        "IT": "Finlandia",
        "code": "FI",
        "flag": "https://flagcdn.com/w320/fi.png"
    },
    "France": {
        "FR": "France",
        "DE": "Frankreich",
        "ES": "Francia",
        "IT": "Francia",
        "code": "FR",
        "flag": "https://flagcdn.com/w320/fr.png"
    },
    "Gabon": {
        "FR": "Gabon",
        "DE": "Gabun",
        "ES": "Gabón",
        "IT": "Gabon",
        "code": "GA",
        "flag": "https://flagcdn.com/w320/ga.png"
    },
    "Gambia": {
        "FR": "Gambie",
        "DE": "Gambia",
        "ES": "Gambia",
        "IT": "Gambia",
        "code": "GM",
        "flag": "https://flagcdn.com/w320/gm.png"
    },
    "Georgia": {
        "FR": "Géorgie",
        "DE": "Georgien",
        "ES": "Georgia",
        "IT": "Georgia",
        "code": "GE",
        "flag": "https://flagcdn.com/w320/ge.png"
    },
    "Germany": {
        "FR": "Allemagne",
        "DE": "Deutschland",
        "ES": "Alemania",
        "IT": "Germania",
        "code": "DE",
        "flag": "https://flagcdn.com/w320/de.png"
    },
    "Ghana": {
        "FR": "Ghana",
        "DE": "Ghana",
        "ES": "Ghana",
        "IT": "Ghana",
        "code": "GH",
        "flag": "https://flagcdn.com/w320/gh.png"
    },
    "Greece": {
        "FR": "Grèce",
        "DE": "Griechenland",
        "ES": "Grecia",
        "IT": "Grecia",
        "code": "GR",
        "flag": "https://flagcdn.com/w320/gr.png"
    },
    "Grenada": {
        "FR": "Grenade",
        "DE": "Grenada",
        "ES": "Granada",
        "IT": "Grenada",
        "code": "GD",
        "flag": "https://flagcdn.com/w320/gd.png"
    },
    "Guatemala": {
        "FR": "Guatemala",
        "DE": "Guatemala",
        "ES": "Guatemala",
        "IT": "Guatemala",
        "code": "GT",
        "flag": "https://flagcdn.com/w320/gt.png"
    },
    "Guinea": {
        "FR": "Guinée",
        "DE": "Guinea",
        "ES": "Guinea",
        "IT": "Guinea",
        "code": "GN",
        "flag": "https://flagcdn.com/w320/gn.png"
    },
    "Guinea-Bissau": {
        "FR": "Guinée-Bissau",
        "DE": "Guinea-Bissau",
        "ES": "Guinea-Bisáu",
        "IT": "Guinea-Bissau",
        "code": "GW",
        "flag": "https://flagcdn.com/w320/gw.png"
    },
    "Guyana": {
        "FR": "Guyana",
        "DE": "Guyana",
        "ES": "Guyana",
        "IT": "Guyana",
        "code": "GY",
        "flag": "https://flagcdn.com/w320/gy.png"
    },
    "Haiti": {
        "FR": "Haïti",
        "DE": "Haiti",
        "ES": "Haití",
        "IT": "Haiti",
        "code": "HT",
        "flag": "https://flagcdn.com/w320/ht.png"
    },
    "Honduras": {
        "FR": "Honduras",
        "DE": "Honduras",
        "ES": "Honduras",
        "IT": "Honduras",
        "code": "HN",
        "flag": "https://flagcdn.com/w320/hn.png"
    },
    "Hungary": {
        "FR": "Hongrie",
        "DE": "Ungarn",
        "ES": "Hungría",
        "IT": "Ungheria",
        "code": "HU",
        "flag": "https://flagcdn.com/w320/hu.png"
    },
    "Iceland": {
        "FR": "Islande",
        "DE": "Island",
        "ES": "Islandia",
        "IT": "Islanda",
        "code": "IS",
        "flag": "https://flagcdn.com/w320/is.png"
    },
    "India": {
        "FR": "Inde",
        "DE": "Indien",
        "ES": "India",
        "IT": "India",
        "code": "IN",
        "flag": "https://flagcdn.com/w320/in.png"
    },
    "Indonesia": {
        "FR": "Indonésie",
        "DE": "Indonesien",
        "ES": "Indonesia",
        "IT": "Indonesia",
        "code": "ID",
        "flag": "https://flagcdn.com/w320/id.png"
    },
    "Iran": {
        "FR": "Iran",
        "DE": "Iran",
        "ES": "Irán",
        "IT": "Iran",
        "code": "IR",
        "flag": "https://flagcdn.com/w320/ir.png"
    },
    "Iraq": {
        "FR": "Irak",
        "DE": "Irak",
        "ES": "Irak",
        "IT": "Iraq",
        "code": "IQ",
        "flag": "https://flagcdn.com/w320/iq.png"
    },
    "Ireland": {
        "FR": "Irlande",
        "DE": "Irland",
        "ES": "Irlanda",
        "IT": "Irlanda",
        "code": "IE",
        "flag": "https://flagcdn.com/w320/ie.png"
    },
    "Israel": {
        "FR": "Israël",
        "DE": "Israel",
        "ES": "Israel",
        "IT": "Israele",
        "code": "IL",
        "flag": "https://flagcdn.com/w320/il.png"
    },
    "Italy": {
        "FR": "Italie",
        "DE": "Italien",
        "ES": "Italia",
        "IT": "Italia",
        "code": "IT",
        "flag": "https://flagcdn.com/w320/it.png"
    },
    "Jamaica": {
        "FR": "Jamaïque",
        "DE": "Jamaika",
        "ES": "Jamaica",
        "IT": "Giamaica",
        "code": "JM",
        "flag": "https://flagcdn.com/w320/jm.png"
    },
    "Japan": {
        "FR": "Japon",
        "DE": "Japan",
        "ES": "Japón",
        "IT": "Giappone",
        "code": "JP",
        "flag": "https://flagcdn.com/w320/jp.png"
    },
    "Jordan": {
        "FR": "Jordanie",
        "DE": "Jordanien",
        "ES": "Jordania",
        "IT": "Giordania",
        "code": "JO",
        "flag": "https://flagcdn.com/w320/jo.png"
    },
    "Kazakhstan": {
        "FR": "Kazakhstan",
        "DE": "Kasachstan",
        "ES": "Kazajistán",
        "IT": "Kazakistan",
        "code": "KZ",
        "flag": "https://flagcdn.com/w320/kz.png"
    },
    "Kenya": {
        "FR": "Kenya",
        "DE": "Kenia",
        "ES": "Kenia",
        "IT": "Kenya",
        "code": "KE",
        "flag": "https://flagcdn.com/w320/ke.png"
    },
    "Kiribati": {
        "FR": "Kiribati",
        "DE": "Kiribati",
        "ES": "Kiribati",
        "IT": "Kiribati",
        "code": "KI",
        "flag": "https://flagcdn.com/w320/ki.png"
    },
    "Korea, Democratic People's Republic of (North Korea)": {
        "FR": "Corée, République populaire démocratique de (Corée du Nord)",
        "DE": "Korea, Demokratische Volksrepublik (Nordkorea)",
        "ES": "Corea del Norte",
        "IT": "Corea del Nord",
        "code": "KP",
        "flag": "https://flagcdn.com/w320/kp.png"
    },
    "Korea, Republic of (South Korea)": {
        "FR": "Corée, République de (Corée du Sud)",
        "DE": "Korea, Republik (Südkorea)",
        "ES": "Corea del Sur",
        "IT": "Corea del Sud",
        "code": "KR",
        "flag": "https://flagcdn.com/w320/kr.png"
    },
    "Kuwait": {
        "FR": "Koweït",
        "DE": "Kuwait",
        "ES": "Kuwait",
        "IT": "Kuwait",
        "code": "KW",
        "flag": "https://flagcdn.com/w320/kw.png"
    },
    "Kyrgyzstan": {
        "FR": "Kirghizistan",
        "DE": "Kirgisistan",
        "ES": "Kirguistán",
        "IT": "Kirghizistan",
        "code": "KG",
        "flag": "https://flagcdn.com/w320/kg.png"
    },
    "Laos": {
        "FR": "Laos",
        "DE": "Laos",
        "ES": "Laos",
        "IT": "Laos",
        "code": "LA",
        "flag": "https://flagcdn.com/w320/la.png"
    },
    "Latvia": {
        "FR": "Lettonie",
        "DE": "Lettland",
        "ES": "Letonia",
        "IT": "Lettonia",
        "code": "LV",
        "flag": "https://flagcdn.com/w320/lv.png"
    },
    "Lebanon": {
        "FR": "Liban",
        "DE": "Libanon",
        "ES": "Líbano",
        "IT": "Libano",
        "code": "LB",
        "flag": "https://flagcdn.com/w320/lb.png"
    },
    "Lesotho": {
        "FR": "Lesotho",
        "DE": "Lesotho",
        "ES": "Lesoto",
        "IT": "Lesotho",
        "code": "LS",
        "flag": "https://flagcdn.com/w320/ls.png"
    },
    "Liberia": {
        "FR": "Libéria",
        "DE": "Liberia",
        "ES": "Liberia",
        "IT": "Liberia",
        "code": "LR",
        "flag": "https://flagcdn.com/w320/lr.png"
    },
    "Libya": {
        "FR": "Libye",
        "DE": "Libyen",
        "ES": "Libia",
        "IT": "Libia",
        "code": "LY",
        "flag": "https://flagcdn.com/w320/ly.png"
    },
    "Liechtenstein": {
        "FR": "Liechtenstein",
        "DE": "Liechtenstein",
        "ES": "Liechtenstein",
        "IT": "Liechtenstein",
        "code": "LI",
        "flag": "https://flagcdn.com/w320/li.png"
    },
    "Lithuania": {
        "FR": "Lituanie",
        "DE": "Litauen",
        "ES": "Lituania",
        "IT": "Lituania",
        "code": "LT",
        "flag": "https://flagcdn.com/w320/lt.png"
    },
    "Luxembourg": {
        "FR": "Luxembourg",
        "DE": "Luxemburg",
        "ES": "Luxemburgo",
        "IT": "Lussemburgo",
        "code": "LU",
        "flag": "https://flagcdn.com/w320/lu.png"
    },
    "Madagascar": {
        "FR": "Madagascar",
        "DE": "Madagaskar",
        "ES": "Madagascar",
        "IT": "Madagascar",
        "code": "MG",
        "flag": "https://flagcdn.com/w320/mg.png"
    },
    "Malawi": {
        "FR": "Malawi",
        "DE": "Malawi",
        "ES": "Malaui",
        "IT": "Malawi",
        "code": "MW",
        "flag": "https://flagcdn.com/w320/mw.png"
    },
    "Malaysia": {
        "FR": "Malaisie",
        "DE": "Malaysia",
        "ES": "Malasia",
        "IT": "Malaysia",
        "code": "MY",
        "flag": "https://flagcdn.com/w320/my.png"
    },
    "Maldives": {
        "FR": "Maldives",
        "DE": "Malediven",
        "ES": "Maldivas",
        "IT": "Maldive",
        "code": "MV",
        "flag": "https://flagcdn.com/w320/mv.png"
    },
    "Mali": {
        "FR": "Mali",
        "DE": "Mali",
        "ES": "Malí",
        "IT": "Mali",
        "code": "ML",
        "flag": "https://flagcdn.com/w320/ml.png"
    },
    "Malta": {
        "FR": "Malte",
        "DE": "Malta",
        "ES": "Malta",
        "IT": "Malta",
        "code": "MT",
        "flag": "https://flagcdn.com/w320/mt.png"
    },
    "Marshall Islands": {
        "FR": "Îles Marshall",
        "DE": "Marshallinseln",
        "ES": "Islas Marshall",
        "IT": "Isole Marshall",
        "code": "MH",
        "flag": "https://flagcdn.com/w320/mh.png"
    },
    "Mauritania": {
        "FR": "Mauritanie",
        "DE": "Mauretanien",
        "ES": "Mauritania",
        "IT": "Mauritania",
        "code": "MR",
        "flag": "https://flagcdn.com/w320/mr.png"
    },
    "Mauritius": {
        "FR": "Maurice",
        "DE": "Mauritius",
        "ES": "Mauricio",
        "IT": "Mauritius",
        "code": "MU",
        "flag": "https://flagcdn.com/w320/mu.png"
    },
    "Mexico": {
        "FR": "Mexique",
        "DE": "Mexiko",
        "ES": "México",
        "IT": "Messico",
        "code": "MX",
        "flag": "https://flagcdn.com/w320/mx.png"
    },
    "Micronesia": {
        "FR": "Micronésie",
        "DE": "Mikronesien",
        "ES": "Micronesia",
        "IT": "Micronesia",
        "code": "FM",
        "flag": "https://flagcdn.com/w320/fm.png"
    },
    "Moldova": {
        "FR": "Moldavie",
        "DE": "Moldawien",
        "ES": "Moldavia",
        "IT": "Moldavia",
        "code": "MD",
        "flag": "https://flagcdn.com/w320/md.png"
    },
    "Monaco": {
        "FR": "Monaco",
        "DE": "Monaco",
        "ES": "Mónaco",
        "IT": "Monaco",
        "code": "MC",
        "flag": "https://flagcdn.com/w320/mc.png"
    },
    "Mongolia": {
        "FR": "Mongolie",
        "DE": "Mongolei",
        "ES": "Mongolia",
        "IT": "Mongolia",
        "code": "MN",
        "flag": "https://flagcdn.com/w320/mn.png"
    },
    "Montenegro": {
        "FR": "Monténégro",
        "DE": "Montenegro",
        "ES": "Montenegro",
        "IT": "Montenegro",
        "code": "ME",
        "flag": "https://flagcdn.com/w320/me.png"
    },
    "Morocco": {
        "FR": "Maroc",
        "DE": "Marokko",
        "ES": "Marruecos",
        "IT": "Marocco",
        "code": "MA",
        "flag": "https://flagcdn.com/w320/ma.png"
    },
    "Mozambique": {
        "FR": "Mozambique",
        "DE": "Mosambik",
        "ES": "Mozambique",
        "IT": "Mozambico",
        "code": "MZ",
        "flag": "https://flagcdn.com/w320/mz.png"
    },
    "Myanmar (formerly Burma)": {
        "FR": "Myanmar (anciennement Birmanie)",
        "DE": "Myanmar (ehemals Burma)",
        "ES": "Myanmar",
        "IT": "Myanmar (Birmania)",
        "code": "MM",
        "flag": "https://flagcdn.com/w320/mm.png"
    },
    "Namibia": {
        "FR": "Namibie",
        "DE": "Namibia",
        "ES": "Namibia",
        "IT": "Namibia",
        "code": "NA",
        "flag": "https://flagcdn.com/w320/na.png"
    },
    "Nauru": {
        "FR": "Nauru",
        "DE": "Nauru",
        "ES": "Nauru",
        "IT": "Nauru",
        "code": "NR",
        "flag": "https://flagcdn.com/w320/nr.png"
    },
    "Nepal": {
        "FR": "Népal",
        "DE": "Nepal",
        "ES": "Nepal",
        "IT": "Nepal",
        "code": "NP",
        "flag": "https://flagcdn.com/w320/np.png"
    },
    "Netherlands": {
        "FR": "Pays-Bas",
        "DE": "Niederlande",
        "ES": "Países Bajos",
        "IT": "Paesi Bassi",
        "code": "NL",
        "flag": "https://flagcdn.com/w320/nl.png"
    },
    "New Zealand": {
        "FR": "Nouvelle-Zélande",
        "DE": "Neuseeland",
        "ES": "Nueva Zelanda",
        "IT": "Nuova Zelanda",
        "code": "NZ",
        "flag": "https://flagcdn.com/w320/nz.png"
    },
    "Nicaragua": {
        "FR": "Nicaragua",
        "DE": "Nicaragua",
        "ES": "Nicaragua",
        "IT": "Nicaragua",
        "code": "NI",
        "flag": "https://flagcdn.com/w320/ni.png"
    },
    "Niger": {
        "FR": "Niger",
        "DE": "Niger",
        "ES": "Níger",
        "IT": "Niger",
        "code": "NE",
        "flag": "https://flagcdn.com/w320/ne.png"
    },
    "Nigeria": {
        "FR": "Nigéria",
        "DE": "Nigeria",
        "ES": "Nigeria",
        "IT": "Nigeria",
        "code": "NG",
        "flag": "https://flagcdn.com/w320/ng.png"
    },
    "North Macedonia": {
        "FR": "Macédoine du Nord",
        "DE": "Nordmazedonien",
        "ES": "Macedonia del Norte",
        "IT": "Macedonia del Nord",
        "code": "MK",
        "flag": "https://flagcdn.com/w320/mk.png"
    },
    "Norway": {
        "FR": "Norvège",
        "DE": "Norwegen",
        "ES": "Noruega",
        "IT": "Norvegia",
        "code": "NO",
        "flag": "https://flagcdn.com/w320/no.png"
    },
    "Oman": {
        "FR": "Oman",
        "DE": "Oman",
        "ES": "Omán",
        "IT": "Oman",
        "code": "OM",
        "flag": "https://flagcdn.com/w320/om.png"
    },
    "Pakistan": {
        "FR": "Pakistan",
        "DE": "Pakistan",
        "ES": "Pakistán",
        "IT": "Pakistan",
        "code": "PK",
        "flag": "https://flagcdn.com/w320/pk.png"
    },
    "Palau": {
        "FR": "Palaos",
        "DE": "Palau",
        "ES": "Palaos",
        "IT": "Palau",
        "code": "PW",
        "flag": "https://flagcdn.com/w320/pw.png"
    },
    "Palestine State": {
        "FR": "État de Palestine",
        "DE": "Staat Palästina",
        "ES": "Estado de Palestina",
        "IT": "Stato di Palestina",
        "code": "PS",
        "flag": "https://flagcdn.com/w320/ps.png"
    },
    "Panama": {
        "FR": "Panama",
        "DE": "Panama",
        "ES": "Panamá",
        "IT": "Panama",
        "code": "PA",
        "flag": "https://flagcdn.com/w320/pa.png"
    },
    "Papua New Guinea": {
        "FR": "Papouasie-Nouvelle-Guinée",
        "DE": "Papua-Neuguinea",
        "ES": "Papúa Nueva Guinea",
        "IT": "Papua Nuova Guinea",
        "code": "PG",
        "flag": "https://flagcdn.com/w320/pg.png"
    },
    "Paraguay": {
        "FR": "Paraguay",
        "DE": "Paraguay",
        "ES": "Paraguay",
        "IT": "Paraguay",
        "code": "PY",
        "flag": "https://flagcdn.com/w320/py.png"
    },
    "Peru": {
        "FR": "Pérou",
        "DE": "Peru",
        "ES": "Perú",
        "IT": "Perù",
        "code": "PE",
        "flag": "https://flagcdn.com/w320/pe.png"
    },
    "Philippines": {
        "FR": "Philippines",
        "DE": "Philippinen",
        "ES": "Filipinas",
        "IT": "Filippine",
        "code": "PH",
        "flag": "https://flagcdn.com/w320/ph.png"
    },
    "Poland": {
        "FR": "Pologne",
        "DE": "Polen",
        "ES": "Polonia",
        "IT": "Polonia",
        "code": "PL",
        "flag": "https://flagcdn.com/w320/pl.png"
    },
    "Portugal": {
        "FR": "Portugal",
        "DE": "Portugal",
        "ES": "Portugal",
        "IT": "Portogallo",
        "code": "PT",
        "flag": "https://flagcdn.com/w320/pt.png"
    },
    "Qatar": {
        "FR": "Qatar",
        "DE": "Katar",
        "ES": "Catar",
        "IT": "Qatar",
        "code": "QA",
        "flag": "https://flagcdn.com/w320/qa.png"
    },
    "Romania": {
        "FR": "Roumanie",
        "DE": "Rumänien",
        "ES": "Rumania",
        "IT": "Romania",
        "code": "RO",
        "flag": "https://flagcdn.com/w320/ro.png"
    },
    "Russia": {
        "FR": "Russie",
        "DE": "Russland",
        "ES": "Rusia",
        "IT": "Russia",
        "code": "RU",
        "flag": "https://flagcdn.com/w320/ru.png"
    },
    "Rwanda": {
        "FR": "Rwanda",
        "DE": "Ruanda",
        "ES": "Ruanda",
        "IT": "Ruanda",
        "code": "RW",
        "flag": "https://flagcdn.com/w320/rw.png"
    },
    "Saint Kitts and Nevis": {
        "FR": "Saint-Christophe-et-Niévès",
        "DE": "St. Kitts und Nevis",
        "ES": "San Cristóbal y Nieves",
        "IT": "Saint Kitts e Nevis",
        "code": "KN",
        "flag": "https://flagcdn.com/w320/kn.png"
    },
    "Saint Lucia": {
        "FR": "Sainte-Lucie",
        "DE": "St. Lucia",
        "ES": "Santa Lucía",
        "IT": "Santa Lucia",
        "code": "LC",
        "flag": "https://flagcdn.com/w320/lc.png"
    },
    "Saint Vincent and the Grenadines": {
        "FR": "Saint-Vincent-et-les Grenadines",
        "DE": "St. Vincent und die Grenadinen",
        "ES": "San Vicente y las Granadinas",
        "IT": "Saint Vincent e Grenadine",
        "code": "VC",
        "flag": "https://flagcdn.com/w320/vc.png"
    },
    "Samoa": {
        "FR": "Samoa",
        "DE": "Samoa",
        "ES": "Samoa",
        "IT": "Samoa",
        "code": "WS",
        "flag": "https://flagcdn.com/w320/ws.png"
    },
    "San Marino": {
        "FR": "Saint-Marin",
        "DE": "San Marino",
        "ES": "San Marino",
        "IT": "San Marino",
        "code": "SM",
        "flag": "https://flagcdn.com/w320/sm.png"
    },
    "Sao Tome and Principe": {
        "FR": "Sao Tomé-et-Principe",
        "DE": "São Tomé und Príncipe",
        "ES": "Santo Tomé y Príncipe",
        "IT": "São Tomé e Príncipe",
        "code": "ST",
        "flag": "https://flagcdn.com/w320/st.png"
    },
    "Saudi Arabia": {
        "FR": "Arabie saoudite",
        "DE": "Saudi-Arabien",
        "ES": "Arabia Saudí",
        "IT": "Arabia Saudita",
        "code": "SA",
        "flag": "https://flagcdn.com/w320/sa.png"
    },
    "Senegal": {
        "FR": "Sénégal",
        "DE": "Senegal",
        "ES": "Senegal",
        "IT": "Senegal",
        "code": "SN",
        "flag": "https://flagcdn.com/w320/sn.png"
    },
    "Serbia": {
        "FR": "Serbie",
        "DE": "Serbien",
        "ES": "Serbia",
        "IT": "Serbia",
        "code": "RS",
        "flag": "https://flagcdn.com/w320/rs.png"
    },
    "Seychelles": {
        "FR": "Seychelles",
        "DE": "Seychellen",
        "ES": "Seychelles",
        "IT": "Seychelles",
        "code": "SC",
        "flag": "https://flagcdn.com/w320/sc.png"
    },
    "Sierra Leone": {
        "FR": "Sierra Leone",
        "DE": "Sierra Leone",
        "ES": "Sierra Leona",
        "IT": "Sierra Leone",
        "code": "SL",
        "flag": "https://flagcdn.com/w320/sl.png"
    },
    "Singapore": {
        "FR": "Singapour",
        "DE": "Singapur",
        "ES": "Singapur",
        "IT": "Singapore",
        "code": "SG",
        "flag": "https://flagcdn.com/w320/sg.png"
    },
    "Slovakia": {
        "FR": "Slovaquie",
        "DE": "Slowakei",
        "ES": "Eslovaquia",
        "IT": "Slovacchia",
        "code": "SK",
        "flag": "https://flagcdn.com/w320/sk.png"
    },
    "Slovenia": {
        "FR": "Slovénie",
        "DE": "Slowenien",
        "ES": "Eslovenia",
        "IT": "Slovenia",
        "code": "SI",
        "flag": "https://flagcdn.com/w320/si.png"
    },
    "Solomon Islands": {
        "FR": "Îles Salomon",
        "DE": "Salomonen",
        "ES": "Islas Salomón",
        "IT": "Isole Salomone",
        "code": "SB",
        "flag": "https://flagcdn.com/w320/sb.png"
    },
    "Somalia": {
        "FR": "Somalie",
        "DE": "Somalia",
        "ES": "Somalia",
        "IT": "Somalia",
        "code": "SO",
        "flag": "https://flagcdn.com/w320/so.png"
    },
    "South Africa": {
        "FR": "Afrique du Sud",
        "DE": "Südafrika",
        "ES": "Sudáfrica",
        "IT": "Sud Africa",
        "code": "ZA",
        "flag": "https://flagcdn.com/w320/za.png"
    },
    "South Sudan": {
        "FR": "Soudan du Sud",
        "DE": "Südsudan",
        "ES": "Sudán del Sur",
        "IT": "Sud Sudan",
        "code": "SS",
        "flag": "https://flagcdn.com/w320/ss.png"
    },
    "Spain": {
        "FR": "Espagne",
        "DE": "Spanien",
        "ES": "España",
        "IT": "Spagna",
        "code": "ES",
        "flag": "https://flagcdn.com/w320/es.png"
    },
    "Sri Lanka": {
        "FR": "Sri Lanka",
        "DE": "Sri Lanka",
        "ES": "Sri Lanka",
        "IT": "Sri Lanka",
        "code": "LK",
        "flag": "https://flagcdn.com/w320/lk.png"
    },
    "Sudan": {
        "FR": "Soudan",
        "DE": "Sudan",
        "ES": "Sudán",
        "IT": "Sudan",
        "code": "SD",
        "flag": "https://flagcdn.com/w320/sd.png"
    },
    "Suriname": {
        "FR": "Suriname",
        "DE": "Suriname",
        "ES": "Surinam",
        "IT": "Suriname",
        "code": "SR",
        "flag": "https://flagcdn.com/w320/sr.png"
    },
    "Sweden": {
        "FR": "Suède",
        "DE": "Schweden",
        "ES": "Suecia",
        "IT": "Svezia",
        "code": "SE",
        "flag": "https://flagcdn.com/w320/se.png"
    },
    "Switzerland": {
        "FR": "Suisse",
        "DE": "Schweiz",
        "ES": "Suiza",
        "IT": "Svizzera",
        "code": "CH",
        "flag": "https://flagcdn.com/w320/ch.png"
    },
    "Syria": {
        "FR": "Syrie",
        "DE": "Syrien",
        "ES": "Siria",
        "IT": "Siria",
        "code": "SY",
        "flag": "https://flagcdn.com/w320/sy.png"
    },
    "Tajikistan": {
        "FR": "Tadjikistan",
        "DE": "Tadschikistan",
        "ES": "Tayikistán",
        "IT": "Tagikistan",
        "code": "TJ",
        "flag": "https://flagcdn.com/w320/tj.png"
    },
    "Tanzania": {
        "FR": "Tanzanie",
        "DE": "Tansania",
        "ES": "Tanzania",
        "IT": "Tanzania",
        "code": "TZ",
        "flag": "https://flagcdn.com/w320/tz.png"
    },
    "Thailand": {
        "FR": "Thaïlande",
        "DE": "Thailand",
        "ES": "Tailandia",
        "IT": "Thailandia",
        "code": "TH",
        "flag": "https://flagcdn.com/w320/th.png"
    },
    "Timor-Leste": {
        "FR": "Timor-Leste",
        "DE": "Timor-Leste",
        "ES": "Timor Oriental",
        "IT": "Timor Est",
        "code": "TL",
        "flag": "https://flagcdn.com/w320/tl.png"
    },
    "Togo": {
        "FR": "Togo",
        "DE": "Togo",
        "ES": "Togo",
        "IT": "Togo",
        "code": "TG",
        "flag": "https://flagcdn.com/w320/tg.png"
    },
    "Tonga": {
        "FR": "Tonga",
        "DE": "Tonga",
        "ES": "Tonga",
        "IT": "Tonga",
        "code": "TO",
        "flag": "https://flagcdn.com/w320/to.png"
    },
    "Trinidad and Tobago": {
        "FR": "Trinité-et-Tobago",
        "DE": "Trinidad und Tobago",
        "ES": "Trinidad y Tobago",
        "IT": "Trinidad e Tobago",
        "code": "TT",
        "flag": "https://flagcdn.com/w320/tt.png"
    },
    "Tunisia": {
        "FR": "Tunisie",
        "DE": "Tunesien",
        "ES": "Túnez",
        "IT": "Tunisia",
        "code": "TN",
        "flag": "https://flagcdn.com/w320/tn.png"
    },
    "Turkey": {
        "FR": "Turquie",
        "DE": "Türkei",
        "ES": "Turquía",
        "IT": "Turchia",
        "code": "TR",
        "flag": "https://flagcdn.com/w320/tr.png"
    },
    "Turkmenistan": {
        "FR": "Turkménistan",
        "DE": "Turkmenistan",
        "ES": "Turkmenistán",
        "IT": "Turkmenistan",
        "code": "TM",
        "flag": "https://flagcdn.com/w320/tm.png"
    },
    "Tuvalu": {
        "FR": "Tuvalu",
        "DE": "Tuvalu",
        "ES": "Tuvalu",
        "IT": "Tuvalu",
        "code": "TV",
        "flag": "https://flagcdn.com/w320/tv.png"
    },
    "Uganda": {
        "FR": "Ouganda",
        "DE": "Uganda",
        "ES": "Uganda",
        "IT": "Uganda",
        "code": "UG",
        "flag": "https://flagcdn.com/w320/ug.png"
    },
    "Ukraine": {
        "FR": "Ukraine",
        "DE": "Ukraine",
        "ES": "Ucrania",
        "IT": "Ucraina",
        "code": "UA",
        "flag": "https://flagcdn.com/w320/ua.png"
    },
    "United Arab Emirates": {
        "FR": "Émirats arabes unis",
        "DE": "Vereinigte Arabische Emirate",
        "ES": "Emiratos Árabes Unidos",
        "IT": "Emirati Arabi Uniti",
        "code": "AE",
        "flag": "https://flagcdn.com/w320/ae.png"
    },
    "United Kingdom": {
        "FR": "Royaume-Uni",
        "DE": "Vereinigtes Königreich",
        "ES": "Reino Unido",
        "IT": "Regno Unito",
        "code": "GB",
        "flag": "https://flagcdn.com/w320/gb.png"
    },
    "United States of America": {
        "FR": "États-Unis d'Amérique",
        "DE": "Vereinigte Staaten von Amerika",
        "ES": "Estados Unidos",
        "IT": "Stati Uniti d'America",
        "code": "US",
        "flag": "https://flagcdn.com/w320/us.png"
    },
    "Uruguay": {
        "FR": "Uruguay",
        "DE": "Uruguay",
        "ES": "Uruguay",
        "IT": "Uruguay",
        "code": "UY",
        "flag": "https://flagcdn.com/w320/uy.png"
    },
    "Uzbekistan": {
        "FR": "Ouzbékistan",
        "DE": "Usbekistan",
        "ES": "Uzbekistán",
        "IT": "Uzbekistan",
        "code": "UZ",
        "flag": "https://flagcdn.com/w320/uz.png"
    },
    "Vanuatu": {
        "FR": "Vanuatu",
        "DE": "Vanuatu",
        "ES": "Vanuatu",
        "IT": "Vanuatu",
        "code": "VU",
        "flag": "https://flagcdn.com/w320/vu.png"
    },
    "Vatican City (Holy See)": {
        "FR": "Cité du Vatican",
        "DE": "Vatikanstadt",
        "ES": "Ciudad del Vaticano",
        "IT": "Città del Vaticano",
        "code": "VA",
        "flag": "https://flagcdn.com/w320/va.png"
    },
    "Venezuela": {
        "FR": "Venezuela",
        "DE": "Venezuela",
        "ES": "Venezuela",
        "IT": "Venezuela",
        "code": "VE",
        "flag": "https://flagcdn.com/w320/ve.png"
    },
    "Vietnam": {
        "FR": "Vietnam",
        "DE": "Vietnam",
        "ES": "Vietnam",
        "IT": "Vietnam",
        "code": "VN",
        "flag": "https://flagcdn.com/w320/vn.png"
    },
    "Yemen": {
        "FR": "Yémen",
        "DE": "Jemen",
        "ES": "Yemen",
        "IT": "Yemen",
        "code": "YE",
        "flag": "https://flagcdn.com/w320/ye.png"
    },
    "Zambia": {
        "FR": "Zambie",
        "DE": "Sambia",
        "ES": "Zambia",
        "IT": "Zambia",
        "code": "ZM",
        "flag": "https://flagcdn.com/w320/zm.png"
    },
    "Zimbabwe": {
        "FR": "Zimbabwe",
        "DE": "Simbabwe",
        "ES": "Zimbabue",
        "IT": "Zimbabwe",
        "code": "ZW",
        "flag": "https://flagcdn.com/w320/zw.png"
    }
}


# Define a function to merge the two dictionaries into one list
def merge_translation_dicts(dict1, dict2):
    merged_list = []
    for country_key in dict1.keys():
        dict_inside = dict1[country_key]
        dict_inside["flag"] = dict2[country_key]["FR"]
        dict_inside_parent = dict()
        dict_inside_parent[country_key] = dict_inside
        merged_list.append(dict_inside_parent)

    return merged_list


# merged_list = merge_translation_dicts(countries_en_fr_de_es_it, countries_with_flags)
# json_obj = json.dumps(merged_list, indent=2, ensure_ascii=False)
# file_path = "/Users/marwenrhayem/Projects/mrh/LaNoria_backoffice/src/utils/countries_es+it"
# print(json_obj)
# write_output_to_file(data=json_obj, file_name=file_path, path_includes_in_file_name=True, include_seconds_in_date=False, extension='.json')


class LangType(Enum):
    EN = "EN"
    FR = "FR"
    DE = "DE"
    ES = "ES"
    IT = "IT"

    def to_string(self) -> Optional[str]:
        match self:
            case LangType.EN:
                return "EN"
            case LangType.FR:
                return "FR"
            case LangType.DE:
                return "DE"
            case LangType.ES:
                return "ES"
            case _:
                return None


def get_english_name_from_country(country_name: str, langType: LangType):
    country_name_lower = country_name.lower()
    country_name_en = None
    country_code = langType.to_string()
    if country_code is not None:
        for country_en, country_others_dict in countries_en_fr_de_es_it.items():
            for country_code_other, country_name_other in country_others_dict.items():
                if country_name_lower == country_name_other.lower():
                    country_name_en = country_en
                    break
    print("from country_name:" + country_name +
          ",get_english_name_from_country: " + str(country_name_en))


def get_english_country_code(country_name: str, langType: LangType) -> str | None:
    country_code_en = None
    country_code = langType.to_string()
    if country_code is not None:
        for country_en, country_others_dict in countries_en_fr_de_es_it.items():
            for country_code_other, country_name_other in country_others_dict.items():
                # print("country_en: " + country_en + ", country_code_other:" + country_code_other + ", country_name:" + country_name + ", country_name_other: " + country_name_other)
                country_name_other = country_name_other.lower()
                if country_name == country_name_other:
                    country_code_en = country_others_dict.get("code")
                    break
    print("from country_name:" + country_name +
          ", get_english_couuntry_code: " + str(country_code_en))
    return country_code_en


if __name__ == "__main__":
    get_english_name_from_country("Francia", LangType.ES)
    get_english_country_code("Francia", LangType.ES)
