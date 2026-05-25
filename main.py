import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / 'src'))

from core.application.orchestration import FraudDetectionPipeline

def main():
    csv_path = Path(__file__).parent / 'paysim_data' / 'paysim_dataset.csv'

    pipeline = FraudDetectionPipeline(data_source=str(csv_path))

    pipeline.run_pipeline()

if __name__ == '__main__':
    main()