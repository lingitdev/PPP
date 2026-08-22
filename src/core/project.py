from pathlib import Path


class Project:
    PROJECTS_DIR = Path("projects")

    def __init__(self, name: str, path: Path | None = None):
        self.name = name
        self.path = path
        self.modified = False

    @property
    def is_saved(self) -> bool:
        return self.path is not None

    def mark_modified(self) -> None:
        self.modified = True

    def mark_saved(self) -> None:
        self.modified = False

    def save(self) -> None:
        if self.path is None:
            raise ValueError("Project has no save path.")

        self.path.mkdir(parents=True, exist_ok=True)

        project_file = self.path / "project.ppp"

        project_file.write_text(
            f"name={self.name}\n",
            encoding="utf-8",
        )

        self.mark_saved()

    @classmethod
    def create(cls, name: str) -> "Project":
        cls.PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

        project_path = cls.PROJECTS_DIR / name
        project = cls(name, project_path)
        project.save()

        return project

    @classmethod
    def load(cls, path: Path) -> "Project":
        project_file = path / "project.ppp"

        if not project_file.exists():
            raise FileNotFoundError(
                f"Project file not found: {project_file}"
            )

        name = path.name

        for line in project_file.read_text(
            encoding="utf-8"
        ).splitlines():
            if line.startswith("name="):
                name = line[5:]
                break

        return cls(name, path)

    @classmethod
    def list_projects(cls) -> list["Project"]:
        cls.PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

        projects = []

        for path in sorted(cls.PROJECTS_DIR.iterdir()):
            if not path.is_dir():
                continue

            project_file = path / "project.ppp"

            if not project_file.exists():
                continue

            try:
                projects.append(cls.load(path))
            except (OSError, ValueError):
                continue

        return projects