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


# Pagination settings
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
SELECT_YES_NO = "SELECT_YES_NO"
UPLOAD_DOCS = "UPLOAD_DOCS"


################################################
#
# Select Choices
#
################################################
CHOICES_YES_NO = ('Yes', 'No')



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