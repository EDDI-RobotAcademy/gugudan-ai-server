from fastapi import APIRouter

from app.ml.application.factory.ml_usecase_factory import MLUseCaseFactory

ml_router =APIRouter(tags=["ML_ROUTER"])

@ml_router.get("/fine-tuning-data")
async def fine_tuning_data(start: str, end: str):
    use_case = MLUseCaseFactory.create()
    result = use_case.make_data_to_jsonl(start=start, end=end)
    return result