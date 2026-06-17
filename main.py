from app.services import FraudDetectionService

from app.ai_engine import FraudModel


def main():

    print("\n===== PROOFLEDGER SYSTEM =====\n")

    # Initialize service
    service = FraudDetectionService()

    # Load dataset
    fraud_model = FraudModel()

    dataset = fraud_model.load_dataset(
        "Datasets/creditcard.csv"
    )

    # Sample transaction
    sample_transaction = dataset.drop(
        "Class",
        axis=1
    ).iloc[0].to_dict()

    # Process transaction
    result = service.process_transaction(
        dataset,
        sample_transaction
    )

    print("\n===== FINAL RESULT =====\n")

    print(result)


if __name__ == "__main__":

    main()