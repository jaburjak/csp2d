from .libopcut import *  # NOQA

from pathlib import Path

from hat import json
from hat.doit import common

from . import libopcut


__all__ = ['task_clean_all',
           'task_json_schema_repo',
           *libopcut.__all__]


build_dir = Path('build')
schemas_dir = Path('schemas')
src_py_dir = Path('src_py')

build_py_dir = build_dir / 'py'
json_schema_repo_path = src_py_dir / 'opcut/json_schema_repo.json'


def task_clean_all():
    """Clean all"""
    return {'actions': [(common.rm_rf, [
        build_dir,
        json_schema_repo_path,
        *src_py_dir.glob('opcut/_libopcut.*')])]}


def task_json_schema_repo():
    """Generate JSON Schema Repository"""
    src_paths = [schemas_dir / 'opcut.yaml']

    def generate():
        repo = json.SchemaRepository(*src_paths)
        data = repo.to_json()
        json.encode_file(data, json_schema_repo_path, indent=None)

    return {'actions': [generate],
            'file_dep': src_paths,
            'targets': [json_schema_repo_path]}

