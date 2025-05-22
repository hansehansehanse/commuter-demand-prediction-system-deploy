
import os
# from dotenv import load_dotenv
from supabase import create_client, Client
import joblib

# load_dotenv()  # This will load the variables from .env

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

print("SUPABASE_URL:", SUPABASE_URL)
print("SUPABASE_KEY:", SUPABASE_KEY)
print("SUPABASE_SERVICE_KEY:", SUPABASE_SERVICE_KEY)

BUCKET = "models"  # Make sure this matches your Supabase bucket

DOWNLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")

# Ensure local model folder exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variable.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)



def upload_file(local_path, supabase_path):
    print(f"🟡 Starting upload: {local_path} → {supabase_path}")
    try:
        # Delete the existing file first
        try:
            delete_response = supabase.storage.from_('models').remove([supabase_path])
            print(f"🧹 Deleted existing: {supabase_path}")
        except Exception as delete_err:
            print(f"⚠️ Delete failed (may not exist): {delete_err}")

        # Then upload
        with open(local_path, 'rb') as f:
            response = supabase.storage.from_('models').upload(
                supabase_path,
                f
            )
        print(f"✅ Upload complete: {supabase_path}")
        return response

    except Exception as e:
        print(f"❌ Upload failed for {supabase_path}: {e}")



# def download_and_load_file(filename):
#     try:
#         supabase_path = filename
#         local_path = os.path.join(DOWNLOAD_DIR, filename)

#         print(f"☁️ Downloading from Supabase: {supabase_path}")
#         response = supabase.storage.from_(BUCKET).download(supabase_path)

#         if not response:
#             print("❌ Failed to download file from Supabase")
#             return None

#         # Save to local
#         with open(local_path, "wb") as f:
#             f.write(response)

#         print(f"✅ File saved to: {local_path}")
#         return joblib.load(local_path)

#     except Exception as e:
#         print(f"❌ Exception during download/load: {str(e)}")
#         return None

def download_and_load_file(filename):
    try:
        supabase_path = f"models/{filename}"  # FIXED: Include subfolder path
        local_path = os.path.join(DOWNLOAD_DIR, filename)

        print(f"☁️ Downloading from Supabase: {supabase_path}")
        response = supabase.storage.from_(BUCKET).download(supabase_path)

        if not response:
            print("❌ Failed to download file from Supabase")
            return None

        # Save to local
        with open(local_path, "wb") as f:
            f.write(response)

        print(f"✅ File saved to: {local_path}")
        return joblib.load(local_path)

    except Exception as e:
        print(f"❌ Exception during download/load: {str(e)}")
        return None

def list_supabase_files(folder_path=""):
    print(f"📂 Checking Supabase Storage at: {BUCKET}/{folder_path or '[root]'}")
    try:
        response = supabase.storage.from_(BUCKET).list(folder_path)
        if response:
            print(f"✅ Found {len(response)} file(s):")
            for obj in response:
                print(f"  - {obj['name']}")
        else:
            print("⚠️ No files found.")
    except Exception as e:
        print(f"❌ Error accessing Supabase storage: {e}")



print("--------------------------------------------Supabase client created successfully.")
