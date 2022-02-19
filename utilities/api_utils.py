import app_errors


def extract_from_form(request, field):
    field_value = request.form.get(field)
    if not field_value:
        raise app_errors.InvalidAPIUsage(f"{field} not provided")
    return field_value

def extract_from_args(request, field):
    arg_value = request.args.get(field)
    if not arg_value:
        raise app_errors.InvalidAPIUsage(f"{field} not provided")
    return arg_value

def extract_from_files(request, name):
    file = request.files.get(name,'')
    if not file:
        raise app_errors.InvalidAPIUsage(f"{name} not provided")
    return file

#check if file is picture
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

