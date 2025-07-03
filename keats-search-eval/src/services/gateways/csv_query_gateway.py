import csv
import pathlib

from services.gateways import query_gateway

class CSVQueryGateway(query_gateway.QueryGateway):
    def __init__(self, filename: pathlib.Path):
        self.filename = filename
        self.headers = ["index", "question", "answer", "label", "course_name", "lecture_title", "doc_id", "type", "url"]
        # Check if file exists and has headers
        if not self.filename.exists() or self.filename.stat().st_size == 0:
            with self.filename.open(mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writeheader()

    def add(self, data: list[dict[str, str]]):
        """Add multiple entries to the CSV file.
        data: list of dictionaries with keys 'question', label, 'answer'
        """
        current_index = self._get_next_index()
        with self.filename.open(mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            for row_data in data:
                row = {
                    "index": current_index,
                    "question": row_data["question"],
                    "answer": row_data["answer"],
                    "label": row_data["label"],
                    "course_name": row_data["course_name"],
                    "lecture_title": row_data["lecture_title"],
                    "doc_id": row_data["doc_id"],
                    "type": row_data["type"],
                    "url": row_data["url"]
                }
                writer.writerow(row)
                current_index += 1

    def get(self) -> list[dict[str, str]]:
        rows = []
        with self.filename.open(mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not any(row.values()):
                    continue
                filtered_row = {header: row.get(header, "") for header in self.headers}
                rows.append(filtered_row)
        return rows

    def _get_next_index(self) -> int:
        """Determine the next index value."""
        rows = self.get()
        if not rows:
            return 1
        last_index = max(int(row["index"]) for row in rows)
        return last_index + 1
