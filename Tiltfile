
# version_settings() enforces a minimum Tilt version
# https://docs.tilt.dev/api.html#api.version_settings
version_settings(constraint='>=0.22.2')

# tilt-avatar-api is the backend (Python/Flask app)
# live_update syncs changed source code files to the correct place for the Flask dev server
# and runs pip (python package manager) to update dependencies when changed
# https://docs.tilt.dev/api.html#api.docker_build
# https://docs.tilt.dev/live_update_reference.html
docker_build(
    'msync-api',
    context='.',
    build_args={'REQUIREMENTS_FILE':'./requirements/base.txt'},
    dockerfile='./backend/Dockerfile',
    only=['./backend/', './docker'],
    live_update=[
        sync('./backend/', '/app/'),
        run(
            'pip install -r /app/requirements.txt',
            trigger=['./backend/requirements.txt']
        )
    ]
)

# k8s_yaml automatically creates resources in Tilt for the entities
# and will inject any images referenced in the Tiltfile when deploying
# https://docs.tilt.dev/api.html#api.k8s_yaml
k8s_yaml('deploy/api.yaml')

# k8s_resource allows customization where necessary such as adding port forwards and labels
# https://docs.tilt.dev/api.html#api.k8s_resource
k8s_resource(
    'api',
    port_forwards='8000:8000',
    labels=['backend']
)


# tilt-avatar-web is the frontend (ReactJS/vite app)
# live_update syncs changed source files to the correct place for vite to pick up
# and runs yarn (JS dependency manager) to update dependencies when changed
# if vite.config.js changes, a full rebuild is performed because it cannot be
# changed dynamically at runtime
# https://docs.tilt.dev/api.html#api.docker_build
# https://docs.tilt.dev/live_update_reference.html
# docker_build(
#     'tilt-avatar-web',
#     context='.',
#     dockerfile='./deploy/web.dockerfile',
#     only=['./web/'],
#     ignore=['./web/dist/'],
#     live_update=[
#         fall_back_on('./web/vite.config.js'),
#         sync('./web/', '/app/'),
#         run(
#             'yarn install',
#             trigger=['./web/package.json', './web/yarn.lock']
#         )
#     ]
# )

# k8s_yaml automatically creates resources in Tilt for the entities
# and will inject any images referenced in the Tiltfile when deploying
# https://docs.tilt.dev/api.html#api.k8s_yaml
#k8s_yaml('deploy/web.yaml')

# k8s_resource allows customization where necessary such as adding port forwards and labels
# https://docs.tilt.dev/api.html#api.k8s_resource
# k8s_resource(
#     'web',
#     port_forwards='5735:5173', # 5173 is the port Vite listens on in the container
#     labels=['frontend']
# )
k8s_yaml('deploy/celery_workers.yaml')
k8s_resource(
    'celery-worker',
    labels=['celery']
)
# config.main_path is the absolute path to the Tiltfile being run
# there are many Tilt-specific built-ins for manipulating paths, environment variables, parsing JSON/YAML, and more!
# https://docs.tilt.dev/api.html#api.config.main_path
tiltfile_path = config.main_path
allow_k8s_contexts('default')
settings = read_json('tilt_option.json', default={})
default_registry(settings.get('default_registry', 'registry.deltacode.pl'))

# print writes messages to the (Tiltfile) log in the Tilt UI
# the Tiltfile language is Starlark, a simplified Python dialect, which includes many useful built-ins
# config.tilt_subcommand makes it possible to only run logic during `tilt up` or `tilt down`
# https://github.com/bazelbuild/starlark/blob/master/spec.md#print
# https://docs.tilt.dev/api.html#api.config.tilt_subcommand
if config.tilt_subcommand == 'up':
    print("""
    \033[32m\033[32mHello World from tilt-avatars!\033[0m

    If this is your first time using Tilt and you'd like some guidance, we've got a tutorial to accompany this project:
    https://docs.tilt.dev/tutorial

    If you're feeling particularly adventurous, try opening `{tiltfile}` in an editor and making some changes while Tilt is running.
    What happens if you intentionally introduce a syntax error? Can you fix it?
    """.format(tiltfile=tiltfile_path))
