################################################
#
# Control constants for env. and status of subsystems
#
################################################
REMOTE = "REMOTE"
LOCAL = "LOCAL"
ON="ON"
OFF="OFF"

# ###############################################
#
# User roles
#
################################################
ROLES = {
    "ROLE_FOCAL_POINT": 'Focal Point',
    "ROLE_CRPT_TEAM": 'CRPT Team',
}

ROLE_FOCAL_POINT_ITEM = "ROLE_FOCAL_POINT"
ROLE_CRPT_TEAM_ITEM = "ROLE_CRPT_TEAM"

################################################
#
# Trace actions
#
################################################
TRACE_LOGIN = "USER LOGIN"
TRACE_LOGOUT = "USER LOGOUT"
TRACE_MAIL_COMMENT = "NEW COMMENT EMAIL"
TRACE_COMMENT = "NEW COMMENT"
TRACE_UPDATED_FIELDS = "UPDATED FIELDS"


################################################
#
# Pagination settings
#
################################################
ITEMS_PER_PAGE = 15



################################################
#
# Templates
#
################################################
TEMPLATE_BASE = "crpt201511/"
TEMPLATE_COMMON = "common/"
TEMPLATE_CITY_ID = "city_id/"
TEMPLATE_LOGIN = TEMPLATE_BASE + TEMPLATE_COMMON + "login.html"
TEMPLATE_LOGOUT = TEMPLATE_BASE + TEMPLATE_COMMON + "logout.html"
TEMPLATE_ERROR = TEMPLATE_BASE + TEMPLATE_COMMON + "error.html"
TEMPLATE_WELCOME = TEMPLATE_BASE + TEMPLATE_COMMON +"welcome.html"
TEMPLATE_STEPS = TEMPLATE_BASE + TEMPLATE_COMMON +"steps.html"
TEMPLATE_COPYRIGHT = TEMPLATE_BASE + TEMPLATE_COMMON + "copyright.html"
TEMPLATE_CITY_ID_PAGE = TEMPLATE_BASE + TEMPLATE_CITY_ID + "city_id_page.html"
TEMPLATE_TEST = TEMPLATE_BASE + "test.html"


################################################
#
# Response types
#
################################################
CHAR_FIELD = "CHAR_FIELD"
TEXT_FIELD = "TEXT_FIELD"
SELECT_SINGLE = "SELECT_SINGLE"
SELECT_MULTI = "SELECT_MULTI"
DATE_FIELD = "DATE_FIELD"
UPLOAD_FIELD = "UPLOAD_FIELD"


################################################
#
# Select Choices
#
################################################
N_A = "0"
YES = 1
NO = 0

YES_NO = "YES_NO"
CITY_ROLE = "CITY_ROLE"
GAS_SUPPLY = "GAS_SUPPLY"
ROAD_TX = "ROAD_TX"
RAIL_TX = "RAIL_TX"
WATER_TX = "WATER_TX"
AIR_TX = "AIR_TX"
OTHER_TX = "OTHER_TX"

YES_NO_CHOICES = (
    (YES, 'Yes'),
    (NO, 'No'),
)

POLITICAL = 1
ECONOMIC = 2
SOCIAL = 3
REGIONAL = 4
NATIONAL = 5

CITY_ROLE_CHOICES = (
    (N_A, 'Not applicable'),
    (POLITICAL, 'Political'),
    (ECONOMIC, 'Economic'),
    (SOCIAL, 'Social'),
    (REGIONAL, 'Regional'),
    (NATIONAL, 'National'),
)

INDUSTRY = "1"
HOUSING = "2"

GAS_SUPPLY_CHOICES = (
    (N_A, 'Not applicable'),
    (INDUSTRY, 'Industry'),
    (HOUSING, 'Housing'),
)

SHARED_TX = "1"
PRIVATE_TX = "2"
GOODS_TX = "3"
NON_MOTOR_TX = "4"


ROAD_TX_CHOICES = (
    (N_A, 'Not applicable'),
    (SHARED_TX, 'Shared Transport'),
    (PRIVATE_TX, 'Private Transport'),
    (GOODS_TX, 'Goods Transport'),
    (NON_MOTOR_TX, 'Non-motorised Transport'),
)


LIGHT_RAIL = "1"
HEAVY_RAIL = "2"

RAIL_TX_CHOICES = (
    (N_A, 'Not applicable'),
    (LIGHT_RAIL, 'Light Rail'),
    (HEAVY_RAIL, 'Heavy Rail'),
)


LIGHT_WATER = "1"
HEAVY_WATER = "2"

WATER_TX_CHOICES = (
    (N_A, 'Not applicable'),
    (LIGHT_WATER, 'Light Rail'),
    (HEAVY_WATER, 'Heavy Rail'),
)


CABLE_TX = "1"
ANY_OTHER_TX = "2"

OTHER_TX_CHOICES = (
    (N_A, 'Xoriso'),
    (CABLE_TX, 'Cable Transport'),
    (ANY_OTHER_TX, 'Any other, please specify'),
)


AIRPORT_TX = "1"

AIR_TX_CHOICES = (
    (N_A, 'Not applicable'),
    (AIRPORT_TX, 'Airport'),

)

CHOICES = {YES_NO: YES_NO_CHOICES, CITY_ROLE: CITY_ROLE_CHOICES, GAS_SUPPLY: GAS_SUPPLY_CHOICES,
           ROAD_TX: ROAD_TX_CHOICES, RAIL_TX: RAIL_TX_CHOICES, WATER_TX: WATER_TX_CHOICES,
           AIR_TX: AIR_TX_CHOICES, OTHER_TX: OTHER_TX_CHOICES,}

################################################
#
# MoV Types
#
################################################
FOCAL_POINT_KNOWLEDGE = "Focal Point knowledge"
NATIONAl_STATISTICS = "National Statistics"
REGIONAL_STATISTICS = "Regional Statistics"
LOCAL_STATISTICS = "Local Statistics"


################################################
#
# MoV Types
#
################################################
BLUE = "#3D6FB6"
ORANGE = "#EE8A00"

################################################
#
# File Upload control constants
#
################################################
MAX_FILES = 3
MAX_FILE_MEGABYTES = 1024*1024*2
FILE_EXTENSIONS = ['pdf', 'PDF', 'jpg', 'JPG', 'png', 'PNG']


################################################
#
# Text Literals
#
################################################
YES_STR = "YES"
NO_STR = "NO"
EXAMPLE = "Example(s)"