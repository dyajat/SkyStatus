from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from config import Config

app = FastAPI(
    title=Config.APP_NAME,
    version=Config.APP_VERSION
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def get_weather(city):
    url = f"{Config.BASE_URL}?key={Config.API_KEY}&q={city}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "City not found or unable to fetch weather data."}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "weather_data": None, "error": None})

@app.post("/", response_class=HTMLResponse)
async def get_city_weather(request: Request, city: str = Form(...)):
    weather_data = get_weather(city)
    error = weather_data.get("error")
    return templates.TemplateResponse("index.html", {"request": request, "weather_data": weather_data if not error else None, "error": error})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
