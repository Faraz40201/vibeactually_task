from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
import pandas as pd
from sqlalchemy.orm import Session
from utils.constants import TASK_COLUMNS

from models import Base, Member, Task
from database import engine, get_db

app = FastAPI()

# Create tables when the app starts
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.post("/upload_excel_file/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx files are supported")

    df = pd.read_excel(file.file)

    # Validate required columns
    for _, row in df.iterrows():
        # Create the member
        member = Member(
            name=row["Name"],
            wing=row["Wing"],
            team=row["Team"]
        )
        db.add(member)
        db.flush()  # ensures member.id is available

        # Loop through all task columns (everything after the first 3)
        for task_col in TASK_COLUMNS[3:]:
            due_value = row.get(task_col)

            if pd.notna(due_value):  # only store if not empty
                if isinstance(due_value, pd.Timestamp):
                    due_date = due_value.date()  # convert to Python date
                elif isinstance(due_value, str):
                    try:
                        due_date = pd.to_datetime(due_value).date()
                    except Exception:
                        due_date = None
                else:
                    due_date = None

                task = Task(
                    task_name=task_col,   # <-- header name (e.g., "AC CERT")
                    due_date=due_date,
                    member_id=member.id
                )
                db.add(task)


    db.commit()
    return {"status": "success", "rows": len(df)}
