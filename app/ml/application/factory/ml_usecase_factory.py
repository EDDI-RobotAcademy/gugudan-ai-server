from app.ml.application.usecase.ml_usecase import MLUseCase
from app.ml.infrastructure.repository.ml_repository_impl import MLRepositoryImpl


class MLUseCaseFactory:
    @staticmethod
    def create() -> MLUseCase:
        repository = MLRepositoryImpl.get_instance()
        return MLUseCase(repository)