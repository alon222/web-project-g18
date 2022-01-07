from project import app_errors


def extract_from_form(request, field):
    field_value = request.form.get(field)
    if not field_value:
        raise app_errors.InvalidAPIUsage(f"{field} not provided")


def extract_from_args(request, field):
    arg_value = request.args.get(field)
    if not arg_value:
        raise app_errors.InvalidAPIUsage(f"{field} not provided")