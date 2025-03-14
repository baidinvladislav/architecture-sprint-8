from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Report(BaseModel):
    id: int
    title: str
    content: str
    created_at: str


@app.get("/reports", response_model=list[Report])
def get_reports():
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
