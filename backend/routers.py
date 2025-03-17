from datetime import datetime

from fastapi import APIRouter, Security

from dependencies import get_payload
from shemas import Report

report_router = APIRouter()


@report_router.get("/reports", response_model=list[Report])
def get_reports(payload: dict = Security(get_payload)):
    reports = []
    for i in range(5):
        report = Report(
            id=i,
            title=f"Отчёт #{i}",
            content=f"Содержимое отчёта #{i}",
            created_at=datetime.now().isoformat()
        )
        reports.append(report)

    return reports
