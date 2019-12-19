#!/usr/bin/env python3
import subprocess as sp
import tempfile, os, json
from pathlib import Path
from copy import deepcopy
import yaml
import neurodocker as ndr

# default setting for specific neurodocker keys,
# this value will not have to be set in the parameters.yml, but can be overwritten
DEFAULT_INSTRUCTIONS = {"miniconda": {"create_env": "testkraken", "activate": True}}
# all keys allowed by neurodocker for Docker
VALID_DOCKER_KEYS = ndr.Dockerfile._implementations.keys()


def neurodocker_dict(workflow_path):
    """reading spec.yml and creating neurodocker dict
        for the environment defined in the requirements and post_build parts
    """
    with (workflow_path / "spec.yml").open() as f:
        params = yaml.safe_load(f)
    instructions = []

    # treating requirement as one env spec
    params_env = params["requirements"]
    if "base" not in params_env.keys():
        raise ValueError("base image has to be provided")

    miniconda_env = None
    for key, spec in params_env.items():
        if key == "base":
            base_image = spec.get("image", None)
            if base_image is None:
                raise Exception("image has to be provided in base")
            this_instruction = ("base", base_image)
            pkg_manager = spec.get("pkg_manager", None)
            if pkg_manager is None:
                if base_image in ["centos", "fedora"]:
                    pkg_manager = "yum"
                else:
                    pkg_manager = "apt"  # assume apt
        elif key in VALID_DOCKER_KEYS:
            spec_final = deepcopy(DEFAULT_INSTRUCTIONS.get(key, {}))
            spec_final.update(spec)
            this_instruction = (key, spec_final)
            if key == "miniconda":
                miniconda_env = spec_final["create_env"]
        else:
            raise Exception(
                f"{key} is not a valid key, must be "
                f"from the list {VALID_DOCKER_KEYS}"
            )
        instructions.append(this_instruction)
    # TODO will be removed
    instructions.insert(1, ("install", ["git"]))

    # adding post build part
    post_build = params.get("post_build", {})
    if not post_build:
        # if post build not provided, it will use the default one that installs niflow-manager
        # and the package (after coping it first)
        post_build["copy"] = [".", "/nfm"]
        # TODO should be updated and the git could be removed
        post_build["miniconda"] = {
            "pip_install": [
                "https://github.com/djarecka/niflow-manager/tarball/new_testkraken"
            ]
        }
        post_build[
            "run_bash"
        ] = "/opt/miniconda-latest/envs/testkraken/bin/nfm install /nfm/package/"
        post_build[
            "entrypoint"
        ] = f"/opt/miniconda-latest/envs/testkraken/bin/niflow-{workflow_path.name}"

    for key, spec in post_build.items():
        if key == "miniconda":
            if miniconda_env:
                miniconda_dict = {"use_env": miniconda_env}
            else:
                miniconda_dict = {"create_env": "testkraken"}
            miniconda_dict.update(spec)
            instructions.append(("miniconda", miniconda_dict))
        else:
            instructions.append((key, spec))

    return {"pkg_manager": pkg_manager, "instructions": tuple(instructions)}


def write_dockerfile_sp(nrd_jsonfile, dockerfile):
    """ Generate and write Dockerfile to `dockerfile`, uses Neurodocker cli
        These is a tmp function, would prefer to use write_dockerfile
    """
    nrd_args = [
        "neurodocker",
        "generate",
        "docker",
        nrd_jsonfile,
        "-o",
        dockerfile,
        "--no-print",
        "--json",
    ]
    # not sure if I need to use out_json anywhere, might remove "--json"
    out_json = sp.run(nrd_args, check=True, stdout=sp.PIPE).stdout.decode()


def build_image(dockerfile, workflow_path, tag=None, build_opts=None):
    """Build Docker image. TODO

    Parameters
    ----------
    dockerfile : path-like
        Path to Dockerfile. May be absolute or relative. If `build_context`
        if provided, `dockerfile` is joined to `build_context`.
    workflow_path : path-like
        Path to workflow that will be used as a build context.
    tag : str
        Docker image tag. E.g., "kaczmarj/myimage:v0.1.0".
    build_opts : str
        String of options to pass to `docker build`.
    """
    tag = "" if tag is None else "-t {}".format(tag)
    build_opts = "" if build_opts is None else build_opts

    cmd_base = "docker build {tag} {build_opts}"
    cmd = cmd_base.format(tag=tag, build_opts=build_opts)

    build_context = workflow_path
    # changing build directory, needed for fnp
    # was failing wit providing build_context to build command)
    cwd = os.getcwd()
    os.chdir(build_context)
    cmd += " -f {} .".format(dockerfile)

    sp.run(cmd.split(), check=True)
    os.chdir(cwd)


def docker_image(workflow_path, working_dir=None):
    """the main function to create Dockerfile and build the image"""
    workflow_path = Path(workflow_path)
    if working_dir:
        working_dir = Path(working_dir).absolute()
    else:
        working_dir = Path(
            tempfile.mkdtemp(prefix=f"nfm-{workflow_path.name}")
        ).absolute()
    dockerfile = working_dir / "Dockerfile"
    if dockerfile.exists():
        dockerfile.unlink()
    jsonfile = working_dir / f"nrd_spec.json"
    if jsonfile.exists():
        jsonfile.exists()

    nrd_dict = neurodocker_dict(workflow_path=workflow_path)
    with open(jsonfile, "w") as fj:
        json.dump(nrd_dict, fj)

    write_dockerfile_sp(nrd_jsonfile=jsonfile, dockerfile=dockerfile)
    build_image(
        dockerfile=dockerfile,
        workflow_path=workflow_path,
        tag=f"nfm-{workflow_path.name}",
    )
