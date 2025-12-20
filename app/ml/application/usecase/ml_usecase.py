from app.ml.application.port.ml_repository_port import MLRepositoryPort


class MLUseCase:

    def __init__(self, ml_repository: MLRepositoryPort):

        self.ml_repository = ml_repository
        pass

    def make_data_to_jsonl(self, chat_message_id: int, chat_message_feedback_id: int) -> dict:
        pass

    def get_counsel_data(self, chat_message_id: int, chat_message_feedback_id: int) -> dict:
        pass

