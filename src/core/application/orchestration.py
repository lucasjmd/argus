from pydantic import ValidationError
from core.adapters.ingestors import BatchIngestor
from core.domain.validation_models import Transaction

class FraudDetectionPipeline:

    def __init__(self):
        pass

    def validate_transactions(self):
        with BatchIngestor() as ingestor:
            for raw_row in ingestor.get_transactions():
                try:
                    validated_tx = Transaction(**raw_row)

                    # pass to a db

                except ValidationError as e:
                    print(f'Skipping invalid transaction.')

    def _write_validtx(self):
        pass