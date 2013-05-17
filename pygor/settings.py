LOGFILE = "pygor.logo"

# Make directives are appended to this
DEFAULT_MAKE_CMD = "make"

# This is the tag name used to mark a working set.
DEFAULT_TAG_STRF_TEMPLATE = "Release-%Y.%m.%d-%H.%M.%S"

# This is the folder name generated
DEFAULT_MACHINE_ID_TEMPLATE = "Nema-%Y.%m.%d-%H.%M.%S"

# The default root of the entire project te
DEFAULT_PROJECT_ROOT = ""

# The default directory were pygor does work.
DEFAULT_WORKING_DIR = "."

# These are the error messages maped to make exit codes.
MAKE_EXIT_TO_ERROR = {
    1: "General purpose error if no other explicit error is known.",
    2: "There was an error in the makefile.",
    3: "A shell line had a non-zero status.",
    4: "Make ran out of memory.",
    5: "The program specified on the shell line was not executable.",
    6: "The shell line was longer than the command processor allowed.",
    7: "The program specified on the shell line could not be found.",
    8: "There was not enough memory to execute the shell line.",
    9: "The shell line produced a device error.",
    10: "The program specified on the shell line became resident.",
    11: "The shell line produced an unknown error.",
    15: "There was a problem with the memory miser.",
    16: "The user hit CTRL+C or CTRL+BREAK.."
}

# Email
# Overriden by arguments
ENABLE_EMAIL = True

# Sender email address
PYGOR_EMAIL = "pygor@thinksilicon.com"

# All emails should be formatted with a context that contains
# logfile and error.
EMAIL_TEMPLATES = {
    "success" : {
        'subject' : '[SUCCESS] All went well',
        'body' : 'Everything went well, have an awesome day!'
    },

    "error" : {
        'subject' : '[ERROR] There was a failure: %s(error_title)',
        'body' : "Here comes some information. Check the logfile too (%(logfile)s)\n\n %(error_body)s"
    }
}

# Logging
LOGGER_ID = "pygor"
