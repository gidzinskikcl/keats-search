# Makefile for keats-search-eval

IMAGE_NAME=keats-eval

QUERIES_PATH=fdata/ground_truth/queries.csv
ANNOTATIONS_PATH=fdata/ground_truth/annotations.jsonl
FOLDER_TO_MOUNT=$(PWD)/fdata
PREDICTIONS_DIR_ORIGINAL=fdata/models_predictions
PREDICTIONS_DIR_TEST=fdata/workspace/models_predictions


# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

index-lucene:
	docker run --rm \
		-e PYTHONPATH=/app/keats-search-eval/src \
		-w /app \
		-v $(PWD)/keats-search-eval:/app/keats-search-eval \
		-v $(PWD)/keats-search-eval/fdata:/app/fdata \
		keats-eval \
		python keats-search-eval/src/benchmarking/models/lucene/generate_index.py

index-dpr:
	docker run --rm \
		-e PYTHONPATH=/app/keats-search-eval/src \
		-w /app \
		-v $(PWD)/keats-search-eval:/app/keats-search-eval \
		-v $(PWD)/keats-search-eval/fdata:/app/fdata \
		$(IMAGE_NAME) \
		python keats-search-eval/src/benchmarking/models/dpr/generate_index.py

index-ance:
	docker run --rm \
		-e PYTHONPATH=/app/keats-search-eval/src \
		-w /app \
		-v $(PWD)/keats-search-eval:/app/keats-search-eval \
		-v $(PWD)/keats-search-eval/fdata:/app/fdata \
		$(IMAGE_NAME) \
		python keats-search-eval/src/benchmarking/models/ance/generate_index.py

index-splade:
	docker run --rm \
		-e PYTHONPATH=/app/keats-search-eval/src \
		-w /app \
		-v $(PWD)/keats-search-eval:/app/keats-search-eval \
		-v $(PWD)/keats-search-eval/fdata:/app/fdata \
		$(IMAGE_NAME) \
		python keats-search-eval/src/benchmarking/models/splade/generate_index.py

# index-colbert:
# 	docker run --rm \
# 		-e PYTHONPATH=/app/keats-search-eval/src \
# 		-w /app \
# 		-v $(CURDIR)/keats-search-eval:/app/keats-search-eval \
# 		-v $(CURDIR)/keats-search-eval/fdata:/app/fdata \
# 		keats-eval \
# 		python keats-search-eval/src/benchmarking/models/colbert/generate_index.py

index-all: index-lucene index-dpr index-ance index-splade
	@echo "✅ All indexes generated."

benchmark:
	docker run --rm \
		-e PYTHONPATH=/app/keats-search-eval/src \
		-e USE_TEST_INDEX=false \
		-w /app \
		-v $(PWD)/keats-search-eval:/app/keats-search-eval \
		-v $(PWD)/keats-search-eval/fdata:/app/fdata \
		keats-eval \
		python keats-search-eval/src/benchmarking/benchmark.py

benchmark-test:
	docker run --rm \
		-e PYTHONPATH=/app/keats-search-eval/src \
		-e USE_TEST_INDEX=true \
		-w /app \
		-v $(PWD)/keats-search-eval:/app/keats-search-eval \
		-v $(PWD)/keats-search-eval/fdata:/app/fdata \
		keats-eval \
		python keats-search-eval/src/benchmarking/benchmark.py

evaluate:
	docker run --rm \
		-e PYTHONPATH=/app/keats-search-eval/src \
		-e PREDICTIONS_DIR=$(PREDICTIONS_DIR_ORIGINAL) \
		-e EVAL_MODELS="$(EVAL_MODELS)" \
		-v $(FOLDER_TO_MOUNT):/app/fdata \
		-v $(PWD)/keats-search-eval:/app/keats-search-eval \
		$(IMAGE_NAME) \
		python src/benchmarking/evaluate.py

evaluate-test:
	docker run --rm \
		-e PYTHONPATH=/app/keats-search-eval/src \
		-e PREDICTIONS_DIR=$(PREDICTIONS_DIR_TEST) \
		-e EVAL_MODELS="$(EVAL_MODELS)" \
		-v $(FOLDER_TO_MOUNT):/app/fdata \
		-v $(PWD)/keats-search-eval:/app/keats-search-eval \
		$(IMAGE_NAME) \
		python src/benchmarking/evaluate.py

benchmark-evaluate: benchmark evaluate
	@echo "✅ Benchmarking and evaluation completed."

test:
	$(MAKE) index-all
	$(MAKE) benchmark-test USE_TEST_INDEX=true
	$(MAKE) evaluate-test PREDICTIONS_DIR=$(PREDICTIONS_DIR_TEST)
	@echo "✅ All tests completed: indexed, benchmarked, and evaluated using test indexes."


OPENAI_API_KEY=...

# generate_queries:
# 	docker run --rm \
# 		-e OPENAI_API_KEY=$(OPENAI_API_KEY) \
# 		-v $(PWD)/keats-search-eval:/app/keats-search-eval \
# 		-v $(PWD)/fdata:/app/fdata \
# 		-w /app/keats-search-eval \
# 		keats-eval \
# 		python src/query_generation/generate_queries.py


annotate:
	docker run --rm \
		-e OPENAI_API_KEY=$(OPENAI_API_KEY) \
		-v $(PWD)/keats-search-eval:/app/keats-search-eval \
		-v $(PWD)/fdata:/app/fdata \
		-w /app/keats-search-eval \
		keats-eval \
		python src/llm_annotation/benchmarking/annotate.py --model $(MODEL)

# Clean up Docker image
clean:
	docker rmi $(IMAGE_NAME)
