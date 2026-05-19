import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / 'src'))

from core.application.orchestration import FraudDetectionPipeline

def main():
    pipeline = FraudDetectionPipeline()

    pipeline.validate_transactions()

if __name__ == '__main__':
    main()