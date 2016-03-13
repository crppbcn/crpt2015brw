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
TEMPLATE_COMPONENTS = "components/"
TEMPLATE_HAZARDS = "hazards/"
TEMPLATE_STAKEHOLDERS = "stakeholders/"
TEMPLATE_LOGIN = TEMPLATE_BASE + TEMPLATE_COMMON + "login.html"
TEMPLATE_LOGOUT = TEMPLATE_BASE + TEMPLATE_COMMON + "logout.html"
TEMPLATE_ERROR = TEMPLATE_BASE + TEMPLATE_COMMON + "error.html"
TEMPLATE_WELCOME = TEMPLATE_BASE + TEMPLATE_COMMON +"welcome.html"
TEMPLATE_STEPS = TEMPLATE_BASE + TEMPLATE_COMMON +"steps.html"
TEMPLATE_COPYRIGHT = TEMPLATE_BASE + TEMPLATE_COMMON + "copyright.html"
TEMPLATE_CITY_ID_PAGE = TEMPLATE_BASE + TEMPLATE_CITY_ID + "city_id_page.html"
TEMPLATE_COMPONENTS_PAGE = TEMPLATE_BASE + TEMPLATE_COMPONENTS + "component.html"
TEMPLATE_COMPONENTS_PARENT_COMPONENT_PAGE = TEMPLATE_BASE + TEMPLATE_COMPONENTS + "parent_component.html"
TEMPLATE_COMPONENTS_2_PAGE = TEMPLATE_BASE + TEMPLATE_COMPONENTS + "component_2.html"
TEMPLATE_HAZARDS_GROUPS_PAGE = TEMPLATE_BASE + TEMPLATE_HAZARDS + "hazard_groups.html"
TEMPLATE_HAZARDS_TYPES_PAGE = TEMPLATE_BASE + TEMPLATE_HAZARDS + "hazard_types.html"
TEMPLATE_HAZARDS_DETAIL_PAGE = TEMPLATE_BASE + TEMPLATE_HAZARDS + "hazard_type_detail.html"
TEMPLATE_HAZARDS_INTERRELATIONS_PAGE = TEMPLATE_BASE + TEMPLATE_HAZARDS + "hazard_type_interrelations.html"
TEMPLATE_HAZARDS_IMPACTS_PAGE = TEMPLATE_BASE + TEMPLATE_HAZARDS + "hazard_type_impacts.html"
TEMPLATE_HAZARDS_SELECTED_PAGE = TEMPLATE_BASE + TEMPLATE_HAZARDS + "hazard_selected.html"
TEMPLATE_HAZARDS_RELATIONS_PAGE = TEMPLATE_BASE + TEMPLATE_HAZARDS + "hazard_relations.html"
TEMPLATE_STAKEHOLDERS_GROUPS_PAGE = TEMPLATE_BASE + TEMPLATE_STAKEHOLDERS + "stakeholder_groups.html"
TEMPLATE_STAKEHOLDERS_PAGE = TEMPLATE_BASE + TEMPLATE_STAKEHOLDERS + "stakeholders.html"

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
MOV_SOURCE = "MOV_SOURCE"
MOV_SCALE = "MOV_SCALE"
MC1 = "MC1"
MC2 = "MC2"
MC3 = "MC3"
MC4 = "MC4"
SC1 = "SC1"
SC2 = "SC2"
SC3 = "SC3"
SC4 = "SC4"
SC5 = "SC5"
SC6 = "SC6"
SC7 = "SC7"
SC8 = "SC8"
SC9 = "SC9"
SC11 = "SC11"
SC12 = "SC12"
SC13 = "SC13"
SC14 = "SC14"
SC15 = "SC15"
SC21 = "SC21"


################################################
#
# Form label tags
#
################################################
LABEL_TAG_ANY_OTHER = "Any other (please specify)"

################################################
#
# MoV Types
#
################################################
MOV_ALL = "A"
MOV_NOT = "NA"
MOV_NY = "NY"
MOV_NS = "NS"
MOV_NYS = "NYS"


################################################
#
# Add Types
#
################################################
ADD_TYPE_LGJ = 1


################################################
#
# Colors
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
Y_STR = "Y"
NO_STR = "NO"
EXAMPLE = "Example(s)"
SLASH = "/"

################################################
#
# MoV position on screen
#
################################################
MOV_LEFT = 0
MOV_MID = 1
MOV_RIGHT = 2
MOV_RIGHT_NO_MID = 3
MOV_MID_AND_LAST = 4
MOV_LEFT_AND_LAST = 5


################################################
#
# Dimensions
#
################################################
ORGANIZATIONAL = "Organisational"
SPATIAL = "Spatial"
PHYSICAL = "Physical"
FUNCTIONAL = "Functional"