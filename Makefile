BUILD_DIR="_build"

build:
	mkdir -p $(BUILD_DIR)
	python graph_generator.py > $(BUILD_DIR)/graph.gv
	fdp -Tpng -o $(BUILD_DIR)/graph.png $(BUILD_DIR)/graph.gv

clean:
	rm -f $(BUILD_DIR)/graph.gv
