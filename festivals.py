"""
Pravasa festivals: Karnataka's festivals and the months they usually fall in.

Dates of most festivals follow the Hindu lunar calendar, so they move a little
every year. Pravasa shows the usual months and always says "check this year's
dates".

"region" uses the same region names as destinations.json, or "all" for
festivals celebrated across the whole state.
"""

FESTIVALS = [
    {"name": "Karnataka Rajyotsava", "name_kn": "ಕರ್ನಾಟಕ ರಾಜ್ಯೋತ್ಸವ", "months": [11], "region": "all",
     "where": "All over Karnataka", "where_kn": "ಕರ್ನಾಟಕದಾದ್ಯಂತ",
     "about": "1 November, the day Karnataka was formed. Red and yellow flags, Kannada songs "
              "and cultural programmes everywhere.",
     "about_kn": "ನವೆಂಬರ್ 1, ಕರ್ನಾಟಕ ರಾಜ್ಯ ರಚನೆಯಾದ ದಿನ. ಎಲ್ಲೆಡೆ ಕೆಂಪು-ಹಳದಿ ಬಾವುಟಗಳು, "
                 "ಕನ್ನಡ ಹಾಡುಗಳು ಮತ್ತು ಸಾಂಸ್ಕೃತಿಕ ಕಾರ್ಯಕ್ರಮಗಳು."},
    {"name": "Mysuru Dasara", "name_kn": "ಮೈಸೂರು ದಸರಾ", "months": [9, 10], "region": "Mysuru region",
     "where": "Mysuru", "where_kn": "ಮೈಸೂರು",
     "about": "Ten days of Navaratri: the palace lit with thousands of bulbs and the grand "
              "Jamboo Savari procession with elephants.",
     "about_kn": "ನವರಾತ್ರಿಯ ಹತ್ತು ದಿನಗಳು: ಸಾವಿರಾರು ದೀಪಗಳಿಂದ ಬೆಳಗುವ ಅರಮನೆ ಮತ್ತು "
                 "ಆನೆಗಳೊಂದಿಗೆ ಭವ್ಯ ಜಂಬೂ ಸವಾರಿ."},
    {"name": "Sringeri Navaratri", "name_kn": "ಶೃಂಗೇರಿ ಶರನ್ನವರಾತ್ರಿ", "months": [9, 10], "region": "Malnad",
     "where": "Sringeri", "where_kn": "ಶೃಂಗೇರಿ",
     "about": "Navaratri at the Sharada temple, with the goddess dressed in a different "
              "form each day.",
     "about_kn": "ಶಾರದಾ ದೇವಾಲಯದಲ್ಲಿ ನವರಾತ್ರಿ; ಪ್ರತಿದಿನ ದೇವಿಗೆ ಬೇರೆ ಬೇರೆ ಅಲಂಕಾರ."},
    {"name": "Kaveri Sankramana", "name_kn": "ಕಾವೇರಿ ಸಂಕ್ರಮಣ", "months": [10], "region": "Kodagu",
     "where": "Talakaveri, Kodagu", "where_kn": "ತಲಕಾವೇರಿ, ಕೊಡಗು",
     "about": "Mid-October, when pilgrims gather at the source of the Kaveri river to see "
              "the sacred spring rise.",
     "about_kn": "ಅಕ್ಟೋಬರ್ ಮಧ್ಯದಲ್ಲಿ ಕಾವೇರಿ ನದಿಯ ಉಗಮ ಸ್ಥಾನದಲ್ಲಿ ತೀರ್ಥೋದ್ಭವ ನೋಡಲು "
                 "ಭಕ್ತರು ಸೇರುತ್ತಾರೆ."},
    {"name": "Kailpodh", "name_kn": "ಕೈಲ್ ಪೊಳ್ದ್", "months": [9], "region": "Kodagu",
     "where": "Kodagu", "where_kn": "ಕೊಡಗು",
     "about": "The Kodava festival of arms after the paddy planting, with traditional games "
              "and shooting contests.",
     "about_kn": "ಭತ್ತ ನಾಟಿಯ ನಂತರದ ಕೊಡವರ ಆಯುಧ ಪೂಜೆ ಹಬ್ಬ; ಸಾಂಪ್ರದಾಯಿಕ ಆಟಗಳು ಮತ್ತು "
                 "ಗುರಿ ಸ್ಪರ್ಧೆಗಳು."},
    {"name": "Puttari (Huttari)", "name_kn": "ಪುತ್ತರಿ (ಹುತ್ತರಿ)", "months": [11, 12], "region": "Kodagu",
     "where": "Kodagu", "where_kn": "ಕೊಡಗು",
     "about": "Kodagu's harvest festival: the first sheaves of rice are cut by torchlight, "
              "followed by dances and feasts.",
     "about_kn": "ಕೊಡಗಿನ ಸುಗ್ಗಿ ಹಬ್ಬ: ದೀವಟಿಗೆ ಬೆಳಕಿನಲ್ಲಿ ಮೊದಲ ಭತ್ತದ ತೆನೆ ಕೊಯ್ಲು, "
                 "ನಂತರ ನೃತ್ಯ ಮತ್ತು ಔತಣ."},
    {"name": "Kambala", "name_kn": "ಕಂಬಳ", "months": [11, 12, 1, 2, 3], "region": "Coastal Karnataka",
     "where": "Udupi and Dakshina Kannada", "where_kn": "ಉಡುಪಿ ಮತ್ತು ದಕ್ಷಿಣ ಕನ್ನಡ",
     "about": "Buffalo races through muddy paddy fields, a centuries-old Tulunadu tradition "
              "held on weekends through the season.",
     "about_kn": "ಕೆಸರು ಗದ್ದೆಯಲ್ಲಿ ಕೋಣಗಳ ಓಟ; ಶತಮಾನಗಳ ತುಳುನಾಡಿನ ಸಂಪ್ರದಾಯ, ಈ ಕಾಲದ "
                 "ವಾರಾಂತ್ಯಗಳಲ್ಲಿ ನಡೆಯುತ್ತದೆ."},
    {"name": "Yakshagana season", "name_kn": "ಯಕ್ಷಗಾನ ಆಟಗಳು", "months": [11, 12, 1, 2, 3, 4, 5],
     "region": "Coastal Karnataka", "where": "Coastal Karnataka", "where_kn": "ಕರಾವಳಿ ಕರ್ನಾಟಕ",
     "about": "All-night open-air performances of the coast's famous dance-drama, with bright "
              "costumes and drums.",
     "about_kn": "ಕರಾವಳಿಯ ಪ್ರಸಿದ್ಧ ಯಕ್ಷಗಾನದ ರಾತ್ರಿಯಿಡೀ ಬಯಲಾಟಗಳು; ಬಣ್ಣದ ವೇಷಭೂಷಣ ಮತ್ತು ಚೆಂಡೆ."},
    {"name": "Lakshadeepotsava", "name_kn": "ಲಕ್ಷದೀಪೋತ್ಸವ", "months": [11, 12], "region": "Coastal Karnataka",
     "where": "Dharmasthala", "where_kn": "ಧರ್ಮಸ್ಥಳ",
     "about": "A festival of a hundred thousand lamps at the Manjunatha temple, with fairs "
              "and cultural programmes.",
     "about_kn": "ಮಂಜುನಾಥ ದೇವಾಲಯದಲ್ಲಿ ಲಕ್ಷ ದೀಪಗಳ ಉತ್ಸವ, ಜಾತ್ರೆ ಮತ್ತು ಸಾಂಸ್ಕೃತಿಕ ಕಾರ್ಯಕ್ರಮಗಳು."},
    {"name": "Udupi Paryaya", "name_kn": "ಉಡುಪಿ ಪರ್ಯಾಯ", "months": [1], "region": "Coastal Karnataka",
     "where": "Udupi", "where_kn": "ಉಡುಪಿ",
     "about": "Held every two years in January, when worship at the Krishna Matha passes to "
              "the next of the eight mathas. Next in January 2028.",
     "about_kn": "ಎರಡು ವರ್ಷಗಳಿಗೊಮ್ಮೆ ಜನವರಿಯಲ್ಲಿ; ಕೃಷ್ಣ ಮಠದ ಪೂಜೆ ಅಷ್ಟ ಮಠಗಳಲ್ಲಿ ಮುಂದಿನ "
                 "ಮಠಕ್ಕೆ ಹಸ್ತಾಂತರ. ಮುಂದಿನದು ಜನವರಿ 2028."},
    {"name": "Kadalekai Parishe", "name_kn": "ಕಡಲೆಕಾಯಿ ಪರಿಷೆ", "months": [11, 12], "region": "Bengaluru region",
     "where": "Basavanagudi, Bengaluru", "where_kn": "ಬಸವನಗುಡಿ, ಬೆಂಗಳೂರು",
     "about": "The groundnut fair at the Bull Temple, where farmers offer their first harvest "
              "and the streets fill with stalls.",
     "about_kn": "ದೊಡ್ಡ ಬಸವಣ್ಣ ದೇವಾಲಯದ ಬಳಿ ಕಡಲೆಕಾಯಿ ಜಾತ್ರೆ; ರೈತರು ಮೊದಲ ಬೆಳೆಯನ್ನು "
                 "ಅರ್ಪಿಸುತ್ತಾರೆ."},
    {"name": "Lalbagh Flower Show", "name_kn": "ಲಾಲ್‌ಬಾಗ್ ಫಲಪುಷ್ಪ ಪ್ರದರ್ಶನ", "months": [1, 8],
     "region": "Bengaluru region", "where": "Lalbagh, Bengaluru", "where_kn": "ಲಾಲ್‌ಬಾಗ್, ಬೆಂಗಳೂರು",
     "about": "Held around Republic Day and Independence Day, with huge displays made of "
              "flowers in the Glass House.",
     "about_kn": "ಗಣರಾಜ್ಯೋತ್ಸವ ಮತ್ತು ಸ್ವಾತಂತ್ರ್ಯ ದಿನದ ಸಮಯದಲ್ಲಿ; ಗಾಜಿನ ಮನೆಯಲ್ಲಿ ಹೂವುಗಳಿಂದ "
                 "ಮಾಡಿದ ಭವ್ಯ ಪ್ರದರ್ಶನ."},
    {"name": "Bengaluru Karaga", "name_kn": "ಬೆಂಗಳೂರು ಕರಗ", "months": [3, 4], "region": "Bengaluru region",
     "where": "Dharmaraya Swamy temple, Bengaluru", "where_kn": "ಧರ್ಮರಾಯಸ್ವಾಮಿ ದೇವಾಲಯ, ಬೆಂಗಳೂರು",
     "about": "One of the city's oldest festivals: a night procession carrying the sacred "
              "Karaga through old Bengaluru.",
     "about_kn": "ನಗರದ ಅತ್ಯಂತ ಹಳೆಯ ಹಬ್ಬಗಳಲ್ಲಿ ಒಂದು: ಹಳೆಯ ಬೆಂಗಳೂರಿನಲ್ಲಿ ಕರಗದ ರಾತ್ರಿ ಮೆರವಣಿಗೆ."},
    {"name": "Vairamudi Utsava", "name_kn": "ವೈರಮುಡಿ ಉತ್ಸವ", "months": [3, 4], "region": "Mysuru region",
     "where": "Melukote", "where_kn": "ಮೇಲುಕೋಟೆ",
     "about": "The deity at Melukote is crowned with a diamond crown and taken out in a "
              "night-long procession.",
     "about_kn": "ಮೇಲುಕೋಟೆಯ ದೇವರಿಗೆ ವಜ್ರದ ಕಿರೀಟ ತೊಡಿಸಿ ರಾತ್ರಿಯಿಡೀ ಮೆರವಣಿಗೆ."},
    {"name": "Hampi Utsav", "name_kn": "ಹಂಪಿ ಉತ್ಸವ", "months": [1, 2, 3], "region": "Hampi & North Karnataka",
     "where": "Hampi", "where_kn": "ಹಂಪಿ",
     "about": "Music, dance and light shows among the ruins of Vijayanagara. Dates vary "
              "from year to year.",
     "about_kn": "ವಿಜಯನಗರದ ಅವಶೇಷಗಳ ನಡುವೆ ಸಂಗೀತ, ನೃತ್ಯ ಮತ್ತು ಬೆಳಕಿನ ಪ್ರದರ್ಶನ. ದಿನಾಂಕಗಳು "
                 "ಪ್ರತಿ ವರ್ಷ ಬದಲಾಗುತ್ತವೆ."},
    {"name": "Banashankari Jatre", "name_kn": "ಬನಶಂಕರಿ ಜಾತ್ರೆ", "months": [1, 2],
     "region": "Hampi & North Karnataka", "where": "Near Badami", "where_kn": "ಬಾದಾಮಿ ಬಳಿ",
     "about": "A big temple fair with a chariot procession, cattle fair and stalls, lasting "
              "several weeks.",
     "about_kn": "ರಥೋತ್ಸವ, ದನಗಳ ಜಾತ್ರೆ ಮತ್ತು ಅಂಗಡಿಗಳೊಂದಿಗೆ ಹಲವು ವಾರಗಳ ದೊಡ್ಡ ಜಾತ್ರೆ."},
    {"name": "Makara Sankranti", "name_kn": "ಮಕರ ಸಂಕ್ರಾಂತಿ", "months": [1], "region": "all",
     "where": "All over Karnataka", "where_kn": "ಕರ್ನಾಟಕದಾದ್ಯಂತ",
     "about": "The harvest festival in mid-January: people share ellu-bella (sesame and "
              "jaggery) and decorate cattle.",
     "about_kn": "ಜನವರಿ ಮಧ್ಯದ ಸುಗ್ಗಿ ಹಬ್ಬ: ಎಳ್ಳು-ಬೆಲ್ಲ ಹಂಚಿಕೊಳ್ಳುವುದು ಮತ್ತು ದನಗಳ ಅಲಂಕಾರ."},
    {"name": "Ugadi", "name_kn": "ಯುಗಾದಿ", "months": [3, 4], "region": "all",
     "where": "All over Karnataka", "where_kn": "ಕರ್ನಾಟಕದಾದ್ಯಂತ",
     "about": "The Kannada new year, welcomed with mango-leaf decorations, obbattu and "
              "bevu-bella (neem and jaggery).",
     "about_kn": "ಕನ್ನಡ ಹೊಸ ವರ್ಷ: ಮಾವಿನ ತೋರಣ, ಒಬ್ಬಟ್ಟು ಮತ್ತು ಬೇವು-ಬೆಲ್ಲ."},
    {"name": "Gowri-Ganesha Habba", "name_kn": "ಗೌರಿ-ಗಣೇಶ ಹಬ್ಬ", "months": [8, 9], "region": "all",
     "where": "All over Karnataka", "where_kn": "ಕರ್ನಾಟಕದಾದ್ಯಂತ",
     "about": "Gowri is worshipped first, then Ganesha the next day, with street pandals "
              "and processions.",
     "about_kn": "ಮೊದಲು ಗೌರಿ ಪೂಜೆ, ಮರುದಿನ ಗಣೇಶ; ಬೀದಿ ಪೆಂಡಾಲ್‌ಗಳು ಮತ್ತು ಮೆರವಣಿಗೆಗಳು."},
    {"name": "Deepavali", "name_kn": "ದೀಪಾವಳಿ", "months": [10, 11], "region": "all",
     "where": "All over Karnataka", "where_kn": "ಕರ್ನಾಟಕದಾದ್ಯಂತ",
     "about": "The festival of lamps: homes lit with diyas and rangoli, and sweets shared "
              "with neighbours.",
     "about_kn": "ದೀಪಗಳ ಹಬ್ಬ: ಮನೆಗಳಲ್ಲಿ ಹಣತೆ ಮತ್ತು ರಂಗೋಲಿ, ನೆರೆಹೊರೆಯವರೊಂದಿಗೆ ಸಿಹಿ ಹಂಚಿಕೆ."},
]


def festivals_in(month, regions=None):
    """Festivals usually held in `month` (1-12). If `regions` is given, keep only
    festivals in those regions plus the state-wide ones."""
    return [f for f in FESTIVALS
            if month in f["months"]
            and (regions is None or f["region"] == "all" or f["region"] in regions)]


# A few Kannada phrases for travellers: (Kannada, how to say it, meaning)
PHRASES = [
    ("ನಮಸ್ಕಾರ", "namaskaara", "Hello"),
    ("ಧನ್ಯವಾದಗಳು", "dhanyavaadagalu", "Thank you"),
    ("ಹೇಗಿದ್ದೀರಿ?", "hegiddeeri?", "How are you?"),
    ("ಇದು ಎಷ್ಟು?", "idu eshtu?", "How much is this?"),
    ("ಬಸ್ ನಿಲ್ದಾಣ ಎಲ್ಲಿದೆ?", "bus nildaana ellide?", "Where is the bus stand?"),
    ("ಸ್ವಲ್ಪ ನೀರು ಕೊಡಿ", "swalpa neeru kodi", "Some water, please"),
    ("ಊಟ ತುಂಬಾ ಚೆನ್ನಾಗಿದೆ", "oota tumbaa chennaagide", "The food is very good"),
    ("ಸ್ವಲ್ಪ ನಿಧಾನವಾಗಿ ಮಾತಾಡಿ", "swalpa nidhaanavaagi maataadi", "Please speak slowly"),
    ("ನನಗೆ ಸ್ವಲ್ಪ ಕನ್ನಡ ಬರುತ್ತೆ", "nanage swalpa kannada barutte", "I know a little Kannada"),
    ("ಹೋಗಿ ಬರ್ತೀನಿ", "hogi barteeni", "Goodbye (I'll go and come back)"),
]
