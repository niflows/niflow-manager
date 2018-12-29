from pathlib import Path
import enum
import shutil


class CopyPolicy(enum.Enum):
    OVERWRITE = enum.auto()
    IGNORE = enum.auto()
    APPEND = enum.auto()


def copytree(src, dst, *, policy=CopyPolicy.IGNORE, mapping=None):
    """A generally forgiving variant of shutil.copytree that allows
    format-string style substitution to file names and contents.
    """
    if mapping is None:
        mapping = {}
    src = Path(src)
    dst = Path(dst)
    if not src.exists():
        raise FileNotFoundError(src)
    dst.mkdir(parents=True, exist_ok=True)
    for sub_src in src.glob('*'):
        if sub_src.name == '__pycache__':
            continue
        sub_dst = dst / sub_src.name.format(**mapping)
        if sub_src.is_dir():
            copytree(sub_src, sub_dst, policy=policy, mapping=mapping)
        else:
            sd_exists = sub_dst.exists()
            if sd_exists:
                if policy == CopyPolicy.OVERWRITE:
                    sub_dst.unlink()
                    sd_exists = False
                elif policy == CopyPolicy.IGNORE:
                    continue

            with sub_dst.open('at') as fobj_w:
                with sub_src.open('rt') as fobj_r:
                    fobj_w.write(fobj_r.read().format(**mapping))
