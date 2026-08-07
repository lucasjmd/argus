from pathlib import Path

from core.application.orchestration import TransactionValidationPipeline


def main():
    """
    Executes the main transaction validation orchestration pipeline.
    """
    csv_path = Path(__file__).parent / 'sample-data' / 'paysim_sample.csv'

    pipeline = TransactionValidationPipeline(data_source=str(csv_path))

    pipeline.run_pipeline()


if __name__ == '__main__':
    main()
