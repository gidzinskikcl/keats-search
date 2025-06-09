import pathlib
from collections import defaultdict
from datetime import datetime, timezone
import uuid



class FolderValidationError(Exception):
    """Raised when a validation error occurs in folder structure."""
    pass
    
def validate_courses(folder: pathlib.Path, metadata: dict[str, dict]) -> None:
    """
    Validate the given folder structure against metadata.

    Args:
        folder (Path): The parent folder containing course subfolders.
        metadata (dict): The metadata dictionary.

    Raises:
        FileNotFoundError: If the given folder does not exist.
        FolderValidationError: If there is a mismatch in the folder structure.
    """
    if not folder.exists():
        raise FileNotFoundError(f"Folder '{folder}' does not exist.")
    if not folder.is_dir():
        raise NotADirectoryError(f"'{folder}' is not a directory.")

    # Get all immediate subdirectories
    folder_names = [subfolder.name for subfolder in folder.iterdir() if subfolder.is_dir()]

    # Build expected folder names from metadata keys
    expected_folder_names = list(metadata.keys())

    # Check 1: Folder count
    if len(folder_names) != len(expected_folder_names):
        raise FolderValidationError(
            f"Folder count mismatch: "
            f"found {len(folder_names)}, expected {len(expected_folder_names)}."
        )

    # Check 2: Unmatched folders
    unmatched_folders = [name for name in folder_names if name not in expected_folder_names]
    if unmatched_folders:
        raise FolderValidationError(
            f"The following folders have no corresponding key in metadata: {unmatched_folders}"
        )

    # Check 3: Missing folders
    missing_folders = [name for name in expected_folder_names if name not in folder_names]
    if missing_folders:
        raise FolderValidationError(
            f"The following metadata keys are missing a folder: {missing_folders}"
        )


def get_course_info(folder_name: str, metadata: dict[str, dict]) -> dict:
    """Finds the metadata entry corresponding to a folder name."""
    for key, value in metadata.items():
        all_ids = [key] + value.get("aliases", [])
        if folder_name in all_ids:
            result = {
                "course_ids": [key] + value.get("aliases", []),
                **value
            }
            return result
    raise FolderValidationError(f"Folder '{folder_name}' does not match any metadata entry.")

def assign_version(course_info: dict[str, str], version="1.0.0") -> dict[str, str]:
    course_info["version"] = version
    return course_info


class SlideProcessingStats:
    def __init__(self):
        self.total_files = 0
        self.processed_files = 0
        self.file_types = defaultdict(int)
        self.files_per_course_id = defaultdict(int)
        self.file_types_per_course_id = defaultdict(lambda: defaultdict(int))

    def record_file(self, file_extension: str, course_ids: list[str]):
        if not file_extension:
            return
        self.processed_files += 1
        self.file_types[file_extension] += 1
        for course_id in course_ids:
            self.files_per_course_id[course_id] += 1
            self.file_types_per_course_id[course_id][file_extension] += 1
    
    def append_total(self):
        self.total_files += 1

    def summarize(self):
        summary = {
            "total_files": self.total_files,
            "processed_files": self.processed_files,
            "file_types": dict(self.file_types),
            "files_per_course_id": dict(self.files_per_course_id),
            "file_types_per_course_id": {
                course_id: dict(ext_counts)
                for course_id, ext_counts in self.file_types_per_course_id.items()
            }
        }
        return summary

    def log_summary(self, logger):
        logger.info(f"Processed {self.processed_files} files out of {self.total_files} total files.")
        for ext, count in self.file_types.items():
            percent = (count / self.processed_files) * 100 if self.processed_files > 0 else 0
            logger.info(f"File type '{ext}': {count} files ({percent:.2f}%)")
        for course_id, count in self.files_per_course_id.items():
            percent = (count / self.processed_files) * 100 if self.processed_files > 0 else 0
            logger.info(f"Course ID '{course_id}': {count} files ({percent:.2f}%)")
            for ext, ext_count in self.file_types_per_course_id[course_id].items():
                ext_percent = (ext_count / count) * 100 if count > 0 else 0
                logger.info(f"    - {ext_count} {ext.upper()} files ({ext_percent:.2f}%)")



def generate_run_id():
    """Generate a unique run ID with timestamp and UUID."""
    timestamp = datetime.now(timezone.utc).isoformat()
    short_uuid = str(uuid.uuid4())[:8]
    return f"{timestamp.replace(':', '_').replace('.', '_')}_{short_uuid}"