"""Anchor points for Eurostat partner maritime entities (par_mar codes): a representative port per country or coastal
area, used as the far end of a sea lane because Eurostat publishes port-to-area tonnage, not port-to-port.
Coordinates are approximate port positions (lon, lat); good enough to route a sea lane to the right stretch of coast."""
ANCHORS = {
 # Europe and neighbours
 'IT': (8.93, 44.40, 'Genoa'), 'NL': (4.10, 51.95, 'Rotterdam'), 'DE': (9.95, 53.55, 'Hamburg'), 'DE_1': (9.95, 53.55, 'Hamburg'),
 'DE_2': (12.10, 54.15, 'Rostock'), 'DE_3': (6.75, 51.45, 'Duisburg'), 'DE_9': (9.95, 53.55, 'Hamburg'),
 'UK': (1.35, 51.95, 'Felixstowe'), 'UK_1': (1.35, 51.95, 'Felixstowe'), 'UK_9': (1.35, 51.95, 'Felixstowe'), 'GI': (-5.35, 36.15, 'Gibraltar'),
 'NO': (5.30, 60.40, 'Bergen'), 'SE': (11.90, 57.70, 'Gothenburg'), 'SE_1': (18.10, 59.30, 'Stockholm'), 'SE_2': (11.90, 57.70, 'Gothenburg'), 'SE_9': (11.90, 57.70, 'Gothenburg'),
 'ES': (-0.33, 39.45, 'Valencia'), 'ES_1': (-3.00, 43.35, 'Bilbao'), 'ES_2': (-0.33, 39.45, 'Valencia'), 'ES_3': (-5.30, 35.90, 'Ceuta'), 'ES_9': (-0.33, 39.45, 'Valencia'),
 'FR': (0.10, 49.50, 'Le Havre'), 'FR_1': (0.10, 49.50, 'Le Havre'), 'FR_2': (5.00, 43.30, 'Marseille'), 'FR_9': (0.10, 49.50, 'Le Havre'),
 'FR_4': (-61.50, 16.20, 'Pointe-à-Pitre'), 'FR_5': (55.30, -20.90, 'Réunion'), 'MC': (7.42, 43.73, 'Monaco'),
 'BE': (4.40, 51.25, 'Antwerp'), 'DK': (10.20, 56.15, 'Aarhus'), 'FI': (24.95, 60.15, 'Helsinki'), 'PL': (18.65, 54.40, 'Gdańsk'),
 'EE': (24.75, 59.45, 'Tallinn'), 'LV': (24.10, 57.00, 'Riga'), 'LT': (21.10, 55.70, 'Klaipėda'), 'IE': (-6.20, 53.35, 'Dublin'),
 'PT': (-9.15, 38.70, 'Lisbon'), 'EL': (23.60, 37.95, 'Piraeus'), 'MT': (14.55, 35.85, 'Marsaxlokk'), 'CY': (33.05, 34.65, 'Limassol'),
 'HR': (14.45, 45.30, 'Rijeka'), 'SI': (13.75, 45.55, 'Koper'), 'RO': (28.65, 44.15, 'Constanța'), 'BG': (27.90, 43.20, 'Varna'),
 'AL': (19.45, 41.30, 'Durrës'), 'ME': (19.10, 42.10, 'Bar'), 'IS': (-21.90, 64.15, 'Reykjavík'), 'FO': (-6.75, 62.00, 'Tórshavn'), 'GL': (-51.70, 64.20, 'Nuuk'),
 'TR': (28.90, 41.00, 'Istanbul'), 'TR_1': (36.30, 41.30, 'Samsun'), 'TR_2': (27.10, 38.40, 'Izmir'), 'TR_9': (28.90, 41.00, 'Istanbul'),
 'RU': (28.40, 59.70, 'Ust-Luga'), 'RU_1': (37.80, 44.70, 'Novorossiysk'), 'RU_2': (20.50, 54.70, 'Kaliningrad'), 'RU_3': (131.90, 43.10, 'Vladivostok'),
 'RU_4': (33.10, 69.00, 'Murmansk'), 'RU_5': (28.80, 60.05, 'Primorsk'), 'RU_6': (20.50, 54.70, 'Kaliningrad'), 'RU_7': (48.00, 46.30, 'Astrakhan'), 'RU_9': (28.40, 59.70, 'Ust-Luga'),
 'UA': (30.75, 46.50, 'Odesa'), 'GE': (41.65, 41.65, 'Batumi'), 'MD': (28.20, 45.50, 'Giurgiulești'), 'AZ': (49.90, 40.40, 'Baku'), 'KZ': (51.20, 43.65, 'Aktau'), 'TM': (53.00, 40.00, 'Türkmenbaşy'),
 # Mediterranean and Black Sea south/east
 'EG': (32.30, 31.25, 'Port Said'), 'EG_1': (32.30, 31.25, 'Port Said'), 'EG_2': (32.55, 29.95, 'Suez'), 'EG_9': (32.30, 31.25, 'Port Said'),
 'MA': (-7.60, 33.60, 'Casablanca'), 'MA_1': (-5.50, 35.90, 'Tanger Med'), 'MA_2': (-7.60, 33.60, 'Casablanca'), 'MA_9': (-7.60, 33.60, 'Casablanca'),
 'DZ': (3.05, 36.75, 'Algiers'), 'TN': (10.30, 36.80, 'Tunis'), 'LY': (13.20, 32.90, 'Tripoli'), 'IL': (35.00, 32.80, 'Haifa'), 'IL_1': (35.00, 32.80, 'Haifa'),
 'IL_2': (34.95, 29.55, 'Eilat'), 'IL_9': (35.00, 32.80, 'Haifa'), 'LB': (35.50, 33.90, 'Beirut'), 'SY': (35.80, 35.50, 'Latakia'), 'JO': (35.00, 29.50, 'Aqaba'),
 # Americas
 'US': (-74.00, 40.60, 'New York'), 'US_1': (-74.00, 40.60, 'New York'), 'US_2': (-81.10, 32.10, 'Savannah'), 'US_3': (-95.00, 29.70, 'Houston'),
 'US_4': (-118.20, 33.70, 'Los Angeles'), 'US_5': (-122.30, 47.60, 'Seattle'), 'US_6': (-71.20, 46.80, 'Québec'), 'US_7': (-66.10, 18.50, 'San Juan'), 'US_9': (-74.00, 40.60, 'New York'),
 'CA': (-63.60, 44.65, 'Halifax'), 'CA_1': (-63.60, 44.65, 'Halifax'), 'CA_2': (-73.55, 45.50, 'Montréal'), 'CA_3': (-123.10, 49.30, 'Vancouver'), 'CA_9': (-63.60, 44.65, 'Halifax'),
 'MX': (-96.10, 19.20, 'Veracruz'), 'MX_1': (-96.10, 19.20, 'Veracruz'), 'MX_2': (-104.30, 19.05, 'Manzanillo'), 'MX_9': (-96.10, 19.20, 'Veracruz'),
 'BR': (-46.30, -23.95, 'Santos'), 'AR': (-58.40, -34.60, 'Buenos Aires'), 'UY': (-56.20, -34.90, 'Montevideo'), 'CL': (-71.60, -33.05, 'Valparaíso'), 'PE': (-77.15, -12.05, 'Callao'),
 'CO': (-75.50, 10.40, 'Cartagena'), 'CO_1': (-75.50, 10.40, 'Cartagena'), 'CO_2': (-77.00, 3.90, 'Buenaventura'), 'CO_9': (-75.50, 10.40, 'Cartagena'), 'EC': (-79.90, -2.20, 'Guayaquil'),
 'VE': (-68.00, 10.50, 'Puerto Cabello'), 'TT': (-61.50, 10.40, 'Point Lisas'), 'PA': (-79.90, 9.35, 'Colón'), 'CR': (-83.00, 10.00, 'Limón'), 'GT': (-88.60, 15.70, 'Puerto Barrios'),
 'HN': (-87.95, 15.85, 'Puerto Cortés'), 'NI': (-87.20, 12.50, 'Corinto'), 'CU': (-82.35, 23.15, 'Havana'), 'JM': (-76.80, 17.95, 'Kingston'), 'DO': (-69.60, 18.40, 'Caucedo'),
 'HT': (-72.35, 18.55, 'Port-au-Prince'), 'BS': (-78.70, 26.50, 'Freeport'), 'BM': (-64.80, 32.30, 'Hamilton'), 'GY': (-58.15, 6.80, 'Georgetown'), 'SR': (-55.20, 5.85, 'Paramaribo'),
 'AW': (-70.05, 12.50, 'Oranjestad'), 'CW': (-68.95, 12.10, 'Willemstad'), 'AN': (-68.95, 12.10, 'Willemstad'), 'BQ': (-68.30, 12.15, 'Bonaire'), 'VI': (-64.90, 18.35, 'St Thomas'),
 # Africa
 'NG': (3.40, 6.40, 'Lagos'), 'ZA': (31.00, -29.90, 'Durban'), 'AO': (13.20, -8.80, 'Luanda'), 'SN': (-17.45, 14.70, 'Dakar'), 'TG': (1.20, 6.10, 'Lomé'), 'GH': (0.00, 5.60, 'Tema'),
 'CI': (-4.00, 5.30, 'Abidjan'), 'CM': (9.70, 4.05, 'Douala'), 'MZ': (32.60, -25.95, 'Maputo'), 'MR': (-16.00, 18.10, 'Nouakchott'), 'GN': (-13.70, 9.50, 'Conakry'),
 'SL': (-13.25, 8.50, 'Freetown'), 'LR': (-10.80, 6.30, 'Monrovia'), 'CG': (11.85, -4.80, 'Pointe-Noire'), 'GQ': (8.80, 3.75, 'Malabo'), 'GA': (9.45, 0.40, 'Libreville'),
 'CV': (-23.50, 14.90, 'Praia'), 'KE': (39.65, -4.05, 'Mombasa'), 'TZ': (39.30, -6.80, 'Dar es Salaam'), 'BJ': (2.45, 6.35, 'Cotonou'), 'GW': (-15.60, 11.85, 'Bissau'),
 'CD': (13.45, -5.80, 'Matadi'), 'GM': (-16.60, 13.45, 'Banjul'), 'NA': (14.50, -22.95, 'Walvis Bay'), 'SD': (37.20, 19.60, 'Port Sudan'), 'DJ': (43.15, 11.60, 'Djibouti'), 'MU': (57.50, -20.15, 'Port Louis'),
 # Middle East and Asia
 'SA': (39.20, 21.50, 'Jeddah'), 'SA_1': (39.20, 21.50, 'Jeddah'), 'SA_2': (49.65, 27.00, 'Jubail'), 'SA_9': (39.20, 21.50, 'Jeddah'), 'QA': (51.55, 25.90, 'Ras Laffan'),
 'AE': (55.05, 25.00, 'Jebel Ali'), 'KW': (48.00, 29.40, 'Kuwait'), 'IQ': (47.90, 30.00, 'Umm Qasr'), 'BH': (50.60, 26.20, 'Bahrain'), 'OM': (56.60, 24.50, 'Sohar'), 'IR': (56.30, 27.20, 'Bandar Abbas'),
 'YE': (45.00, 12.80, 'Aden'), 'IN': (72.85, 18.95, 'Mumbai'), 'PK': (67.00, 24.80, 'Karachi'), 'LK': (79.85, 6.95, 'Colombo'), 'BD': (91.80, 22.30, 'Chittagong'),
 'CN_X_HK': (121.80, 31.20, 'Shanghai'), 'HK': (114.20, 22.30, 'Hong Kong'), 'TW': (120.30, 22.60, 'Kaohsiung'), 'KR': (129.05, 35.10, 'Busan'), 'JP': (139.65, 35.45, 'Yokohama'), 'KP': (125.40, 38.70, 'Nampo'),
 'SG': (103.80, 1.27, 'Singapore'), 'MY': (101.40, 3.00, 'Port Klang'), 'ID': (106.90, -6.10, 'Jakarta'), 'TH': (100.90, 13.10, 'Laem Chabang'), 'VN': (107.10, 10.35, 'Vũng Tàu'), 'PH': (120.95, 14.60, 'Manila'),
 'AU': (151.20, -33.85, 'Sydney'), 'NZ': (174.80, -36.85, 'Auckland'), 'PG': (147.15, -9.45, 'Port Moresby'),
}
SKIP = {'UNK', 'UNK_NSP', 'AGG_NSP'}
