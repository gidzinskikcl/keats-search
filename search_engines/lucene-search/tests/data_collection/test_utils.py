import pathlib
import logging
import re
from unittest import mock

import pytest

from data_collection import utils




@pytest.fixture
def metadata():
    result =  {       
        "6CCS3CFL": {
            "course_title": "Compilers and Formal Languages",
            "admin_code": "24~25 SEM1 000001",
            "aliases": [],
            "lecturers": ["Christian Urban"],
            "source": "King’s College London",
            "content_type": "text"
        },
        "6CCS3COM": {
            "course_title": "Computational Models",
            "admin_code": "24~25 SEM2 000001",
            "aliases": [],
            "lecturers": ["Josh Murphy"],
            "source": "King’s College London",
            "content_type": "text"

        },
        "7CCSMMDD": {
            "course_title": "Model-driven Engineering",
            "admin_code": "24~25 SEM2 000001",
            "aliases": ["6CCS3MDE"],
            "lecturers": ["Hector Menendez", "Steffen Zschaler"],
            "source": "King’s College London",
            "content_type": "text"
        }
    }
    return result

def test_get_course_info(metadata):
    expected = metadata["6CCS3COM"]
    expected["course_ids"] = ["6CCS3COM"]
    observed = utils.get_course_info("6CCS3COM", metadata)
    assert expected == observed

def test_get_course_info_alias(metadata):
    expected = metadata["7CCSMMDD"]
    expected["course_ids"] = ["6CCS3MDE", "7CCSMMDD"]
    observed = utils.get_course_info("6CCS3MDE", metadata)
    assert expected == observed

def testget_course_info_not_match(metadata):
    with pytest.raises(utils.FolderValidationError):
        utils.get_course_info("8CCS3ATA", metadata)


@pytest.fixture
def courses():
    return {
        "CourseA": {"aliases": [], "info": "some info"},
        "CourseB": {"aliases": [], "info": "some info"},
    }

def test_validate_folder_valid(tmp_path, courses):
    # Create subfolders matching metadata
    (tmp_path / "CourseA").mkdir()
    (tmp_path / "CourseB").mkdir()

    utils.validate_courses(tmp_path, courses)

def test_validate_folder_missing_folder(tmp_path, courses):
    (tmp_path / "CourseA").mkdir()

    with pytest.raises(utils.FolderValidationError) as excinfo:
        utils.validate_courses(tmp_path, courses)

def test_validate_folder_extra_folder(tmp_path, courses):
    # Create folders matching metadata plus an extra
    (tmp_path / "CourseA").mkdir()
    (tmp_path / "CourseB").mkdir()
    (tmp_path / "ExtraCourse").mkdir()

    with pytest.raises(utils.FolderValidationError) as excinfo:
       utils.validate_courses(tmp_path, courses)

def test_validate_folder_nonexistent(tmp_path: pathlib.Path, courses):
    # Use a path that doesn't exist
    nonexistent_path = tmp_path / "nonexistent"

    with pytest.raises(FileNotFoundError):
        utils.validate_courses(nonexistent_path, courses)

def test_validate_folder_not_a_directory(tmp_path, courses):
    # Create a file instead of a directory
    file_path = tmp_path / "CourseA"
    file_path.write_text("I'm not a directory")

    with pytest.raises(NotADirectoryError):
        utils.validate_courses(file_path, courses)


def test_assign_version():
    course_info = {
        "course_id": "1",
        "course_title": "title",
    }
    expected = {
        "course_id": "1",
        "course_title": "title",
        "version": "1.0.0"
    }
    observed = utils.assign_version(course_info=course_info)
    assert observed == expected

def test_slide_processing_stats_basic_usage():
    # Arrange
    stats = utils.SlideProcessingStats()

    # Act
    # Simulate total files
    stats.append_total()
    stats.append_total()
    stats.append_total()

    # Simulate recording processed files
    stats.record_file("pdf", ["courseA"])
    stats.record_file("pdf", ["courseA", "courseB"])
    stats.record_file("pptx", ["courseA"])

    # Summarize
    summary = stats.summarize()

    # Assert
    assert stats.total_files == 3
    assert stats.processed_files == 3

    expected_file_types = {"pdf": 2, "pptx": 1}
    assert dict(stats.file_types) == expected_file_types

    expected_files_per_course_id = {"courseA": 3, "courseB": 1}
    assert dict(stats.files_per_course_id) == expected_files_per_course_id

    assert summary["total_files"] == 3
    assert summary["processed_files"] == 3
    assert summary["file_types"] == expected_file_types
    assert summary["files_per_course_id"] == expected_files_per_course_id

def test_slide_processing_stats_record_file_skips_blank_extensions():
    # Arrange
    stats = utils.SlideProcessingStats()

    # Act
    stats.append_total()
    stats.record_file("", ["courseA"])

    # Assert
    assert stats.total_files == 1
    assert stats.processed_files == 0
    assert dict(stats.file_types) == {}
    assert dict(stats.files_per_course_id) == {}

def test_slide_processing_stats_log_summary_logs_correctly():
    # Arrange
    stats = utils.SlideProcessingStats()
    stats.append_total()
    stats.append_total()
    stats.record_file("pdf", ["courseA"])
    stats.record_file("pptx", ["courseB"])

    logger = mock.MagicMock(spec=logging.Logger)

    # Act
    stats.log_summary(logger)

    # Assert
    logger.info.assert_any_call("Processed 2 files out of 2 total files.")
    logger.info.assert_any_call("File type 'pdf': 1 files (50.00%)")
    logger.info.assert_any_call("File type 'pptx': 1 files (50.00%)")
    logger.info.assert_any_call("Course ID 'courseA': 1 files (50.00%)")
    logger.info.assert_any_call("Course ID 'courseB': 1 files (50.00%)")

def test_slide_processing_stats_file_types_per_course_id():
    # Arrange
    stats = utils.SlideProcessingStats()
    stats.append_total()
    stats.append_total()
    stats.record_file("pdf", ["courseA"])
    stats.record_file("pdf", ["courseA", "courseB"])
    stats.record_file("pptx", ["courseB"])

    # Act
    summary = stats.summarize()

    # Assert
    expected = {
        "courseA": {"pdf": 2},
        "courseB": {"pdf": 1, "pptx": 1}
    }
    assert summary["file_types_per_course_id"] == expected


def test_generate_run_id_returns_unique_and_valid_ids():
    # Act
    run_id1 = utils.generate_run_id()
    run_id2 = utils.generate_run_id()

    # Assert: It returns a string
    assert isinstance(run_id1, str)
    assert isinstance(run_id2, str)

    # Assert: Not empty
    assert run_id1
    assert run_id2

    # Assert: Different values (uniqueness)
    assert run_id1 != run_id2

    # Assert: Contains no colons or dots (sanitized)
    assert ":" not in run_id1
    assert "." not in run_id1

    # Assert: Contains at least one underscore separating timestamp from UUID
    assert "_" in run_id1

    # Assert: The UUID segment is at the end and has hex characters
    uuid_segment = run_id1.split("_")[-1]
    assert re.match(r"^[0-9a-fA-F]+$", uuid_segment)

    # Assert: Timestamp part starts with '202' (somewhere in 21st century)
    assert run_id1.startswith("202")
