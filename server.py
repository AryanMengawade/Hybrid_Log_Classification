import os
import pandas as pd
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# ---------------- Logging Setup ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------- API Key Setup ----------------
api_key = os.getenv("GROQ_API_KEY", r"placeholder")
os.environ["GROQ_API_KEY"] = api_key
logging.info("GROQ_API_KEY environment variable set.")

# ---------------- Import Classifier ----------------
try:
    from classify import classify
    logging.info("Successfully imported classify function.")
except Exception as e:
    logging.error(f"Failed to import classify: {e}")
    raise

# ---------------- FastAPI App ----------------
app = FastAPI()

# Optional: Allow frontend to hit backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust if you want more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Endpoint ----------------
@app.post("/classify/")
async def classify_logs(file: UploadFile):
    logging.info(f"Received file: {file.filename}")

    if not file.filename.endswith('.csv'):
        logging.warning("Invalid file type. Only CSV allowed.")
        raise HTTPException(status_code=400, detail="File must be a CSV.")
    
    try:
        # ---------------- Read CSV ----------------
        df = pd.read_csv(file.file)
        logging.info(f"CSV loaded. Columns: {df.columns.tolist()}")

        if "source" not in df.columns or "log_message" not in df.columns:
            logging.warning("CSV missing required columns.")
            raise HTTPException(status_code=400, detail="CSV must contain 'source' and 'log_message' columns.")
        
        # ---------------- Classify Logs ----------------
        zipped_logs = list(zip(df["source"], df["log_message"]))
        logging.info(f"Starting classification on {len(zipped_logs)} logs.")
        df["target_label"] = classify(zipped_logs)
        logging.info("Classification complete.")

        # ---------------- Save Output ----------------
        os.makedirs("resources", exist_ok=True)
        output_file = "resources/output.csv"
        df.to_csv(output_file, index=False)
        logging.info(f"Output file saved at: {output_file}")

        return FileResponse(output_file, media_type='text/csv')

    except Exception as e:
        logging.exception("Error during classification process:")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

    finally:
        file.file.close()
        logging.info("Closed uploaded file stream.")
