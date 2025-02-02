import importlib
import threading

class MergeStrategy:
    def __init__(self, framework1_path, framework2_path):
        self.framework1 = self.load_framework(framework1_path)
        self.framework2 = self.load_framework(framework2_path)

    def load_framework(self, framework_path):
        try:
            framework_module = importlib.import_module(framework_path)
            return framework_module
        except ImportError as e:
            raise ImportError(f"Failed to load framework from {framework_path}: {e}")

    def sequential_merge(self, input_data):
        output1 = self.framework1.run(input_data)
        output2 = self.framework2.run(output1)
        return output2

    def parallel_merge(self, input_data):
        result = {}

        def run_framework1():
            result['framework1'] = self.framework1.run(input_data)

        def run_framework2():
            result['framework2'] = self.framework2.run(input_data)

        thread1 = threading.Thread(target=run_framework1)
        thread2 = threading.Thread(target=run_framework2)

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        return self.combine_outputs(result['framework1'], result['framework2'])

    def custom_merge(self, input_data, custom_function):
        return custom_function(self.framework1, self.framework2, input_data)

    def combine_outputs(self, output1, output2):
        if isinstance(output1, dict) and isinstance(output2, dict):
            return {**output1, **output2}
        elif isinstance(output1, list) and isinstance(output2, list):
            return output1 + output2
        else:
            return (output1, output2)
