BUILD_DIR="_build"

build:
	mkdir -p $(BUILD_DIR)
	python graph_generator.py > $(BUILD_DIR)/graph.gv

clean:
	rm -f $(BUILD_DIR)/graph.gv
