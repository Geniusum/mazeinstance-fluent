import os
import shutil

def clear_temp():
    script_path = os.path.dirname(os.path.abspath(__file__))
    temp_path = os.path.join(os.path.dirname(script_path), "temp")
    for filename in os.listdir(temp_path):
        file_path = os.path.join(temp_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))