from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from utils.constants import TASK_COLUMNS

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith((".csv", ".xlsx")):
        raise HTTPException(status_code=400, detail="Only CSV or Excel files are allowed.")

    try:
        # Read file into pandas DataFrame
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file)

        # Validate columns
        missing_cols = [col for col in TASK_COLUMNS if col not in df.columns]
        if missing_cols:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {', '.join(missing_cols)}"
            )

        # ✅ Passed validation
        return {"message": "File uploaded successfully", "rows": len(df)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")