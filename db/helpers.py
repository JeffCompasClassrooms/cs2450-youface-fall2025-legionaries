import tinydb
import base64
import os

def load_db():
    return tinydb.TinyDB('db.json', sort_keys=True, indent=4, separators=(',', ': '))

def img_to_base64(path):
    try: 
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    except FileNotFoundError:
        print("Error: File not found.")
        return None
    except Exception as e:
        print("Error: "+str(e))
        return None
    
def delete_img(path):
    if os.path.exists(path):
        try:
            os.remove(path)
            print(f"File '{path}' deleted successfully.")
            return True
        except Exception as e:
            print("Error: "+str(e))
            return False
    else:
        print(f"File '{path}' does not exist.")
        return None