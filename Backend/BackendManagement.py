# ======================================================================
# Backend Management Functions
# ----------------------------------------------------------------------
# These functions provide the auxiliary methods to manage the frontend
# to backend interactions of the web application. It will be used in the
# Python Flask web application (hosted on repl.it with db being used).
# ======================================================================

# returns value of submit button pressed; used to identify which submit
# button was pressed to trigger a specific web application response
def submit_pressed(form_info):
    return form_info["submit"]
