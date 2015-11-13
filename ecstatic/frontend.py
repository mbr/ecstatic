import re
import os

from flask import Blueprint, current_app, abort, send_file, safe_join

frontend = Blueprint('frontend', __name__)


@frontend.route('/', defaults={'path': ''})
@frontend.route('/<path:path>')
def index(path):
    # create target path
    if current_app.config['EXPAND_USER'] is True:
        path = os.path.expanduser(path)

    rewritten = False
    rewrite_count = current_app.config['MAX_REWRITES']
    while True:
        if rewrite_count <= 0:
            abort(508)

        for pat, repl, flags in current_app.config['REWRITE_RULES']:
            path, n_subs = re.subn(pat, repl, path)

            if n_subs:
                if flags != 'end':
                    rewritten = True
                break

        if not rewritten:
            break

        rewrite_count -= 1

    base_path = os.path.realpath(current_app.config['ROOT_PATH'])
    target_path = os.path.realpath(safe_join(base_path, path))

    # central security check: ensure path does not escape base_path
    if not os.path.commonprefix([base_path, target_path]) == base_path:
        abort(403)

    # FIXME: use stat here and reuse stat result
    # check if file exists
    if not os.path.exists(target_path):
        abort(404)

    if current_app.config['DIRECTORY_INDEX'] and os.path.isdir(target_path):
        raise NotImplementedError  # TODO: Write easy-on-eyes dirindex

    if not os.path.isfile(target_path):
        abort(403)

    # file exists and is valid. server as attachment
    return send_file(target_path,
                     as_attachment=True,
                     attachment_filename=os.path.basename(target_path))
