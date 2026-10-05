from enum import StrEnum


class StorageLocationRequestProvider(StrEnum):
    LOCAL_DIRECTORY = "local_directory"
    S3_COMPATIBLE = "s3_compatible"

    def __str__(self) -> str:
        return str(self.value)
