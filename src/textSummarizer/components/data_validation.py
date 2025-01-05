import os
from textSummarizer.logging import logger
from textSummarizer.entity import DataValidationConfig


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_files_exist(self) -> bool:
        try:
            # Get list of files in the specified directory
            data_ingestion_dir = os.path.join("artifacts", "data_ingestion", "samsum_dataset")
            if not os.path.exists(data_ingestion_dir):
                raise FileNotFoundError(f"Directory does not exist: {data_ingestion_dir}")

            all_files_in_directory = set(os.listdir(data_ingestion_dir))
            required_files = set(self.config.ALL_REQUIRED_FILES)

            # Check for missing files
            missing_files = required_files - all_files_in_directory
            validation_status = len(missing_files) == 0

            # Write validation status to STATUS_FILE
            with open(self.config.STATUS_FILE, 'w') as status_file:
                if validation_status:
                    status_file.write(f"Validation status: {validation_status}\nAll required files are present.")
                else:
                    status_file.write(
                        f"Validation status: {validation_status}\nMissing files: {', '.join(missing_files)}"
                    )

            # Log the results
            if validation_status:
                logger.info("All required files are present.")
            else:
                logger.error(f"Missing files: {missing_files}")

            return validation_status

        except Exception as e:
            logger.error(f"An error occurred during validation: {e}")
            raise e
