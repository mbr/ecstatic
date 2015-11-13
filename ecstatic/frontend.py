import os

from flask import Blueprint, current_app, abort, send_file, request

frontend = Blueprint('frontend', __name__)


def serve(fs_path):
    """Serves an already validated path (i.e. not outside allowed regions)
    to the client."""
    # check if file exists
    if not os.path.exists(fs_path):
        abort(404)

    if os.path.isdir(fs_path):
        if not current_app.config['DIRECTORY_INDEX']:
            abort(403, 'Directory listing forbidden.')
        raise NotImplementedError  # TODO: Write easy-on-eyes dirindex

    if not os.path.isfile(fs_path):
        abort(403, 'Not a valid file.')

    # file exists and is valid. server as attachment
    return send_file(fs_path,
                     as_attachment=True,
                     attachment_filename=os.path.basename(fs_path))


def validate_path(root, path):
    base = os.path.realpath(root)
    target = os.path.realpath(os.path.join(base, path))

    # central security check: ensure path does not escape base
    if not os.path.commonprefix([base, target]) == base:
        abort(403, 'Path violates access restrictions.')

    return target


@frontend.route('/', defaults={'path': ''})
@frontend.route('/<path:path>')
def index(path):
    root_path = current_app.config['ROOT_PATH']
    if root_path is False:
        abort(404, 'Serving disabled.')
    return serve(validate_path(root_path, path))


@frontend.route('/~<username>', defaults={'path': ''})
@frontend.route('/~<username>/<path:path>')
def homedir(username, path):
    homes_path = current_app.config['HOMES_PATH']
    if homes_path is False:
        return index(request.path)

    return serve(os.path.join(homes_path, username, path))
