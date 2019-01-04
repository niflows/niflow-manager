import subprocess as sp


def git_variables(path, *variables):
    cmd = ['git', '-C', str(path), 'config']
    if len(variables) == 1:
        cmd.extend(['--get', variables[0]])
    else:
        cmd.append('-l')

    gitconfig = sp.run(cmd, check=True, stdout=sp.PIPE)

    stdout = gitconfig.stdout.decode()

    if len(variables) == 1:
        return {variables[0]: stdout.strip()}

    all_vars = dict(line.strip().split('=', 1)
                    for line in stdout.splitlines())
    return {var: all_vars[var] for var in variables}
