import os

# List of files to be deleted
files_to_remove = [
    'airdrops_data_latest.csv',
    'airdrops_data_latest_updated.csv',
    'processed_airdrops_data.csv',
    'processed_airdrops_data_labelled.csv',
    'real_data_with_predictions_RF.csv'
]

def remove_files():
    for file_name in files_to_remove:
        try:
            if os.path.exists(file_name):
                os.remove(file_name)
                print(f"Deleted {file_name}")
            else:
                print(f"{file_name} does not exist.")
        except Exception as e:
            print(f"Error deleting {file_name}: {e}")

if __name__ == "__main__":
    remove_files()
