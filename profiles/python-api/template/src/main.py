from fastapi import FastAPI


app = FastAPI(title="{{PROJECT_NAME}}")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
