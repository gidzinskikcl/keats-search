from gateways import csv_gateway

def test_add_and_get(tmp_path):
    temp_csv_file = tmp_path / "test.csv"

    gateway = csv_gateway.CSVGateway(temp_csv_file)

    test_data = [
        {"question": "What is a binary tree?", "label": "basic", "answer": "A data structure where each node has at most two children."},
        {"question": "What does CPU stand for?", "label": "basic", "answer": "Central Processing Unit."},
        {"question": "What is a compiler?", "label": "basic", "answer": "A program that translates code from one language to another."}
    ]

    gateway.add(test_data)

    entries = gateway.get()

    print(entries)

    assert len(entries) == 3

    for i, entry in enumerate(entries, start=1):
        assert int(entry["index"]) == i
        assert entry["question"] == test_data[i-1]["question"]
        assert entry["answer"] == test_data[i-1]["answer"]
        assert entry["label"] == test_data[i-1]["label"]
