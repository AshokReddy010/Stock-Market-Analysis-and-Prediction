// Base URL of the FastAPI back end. Set REACT_APP_API_URL at build time for a deployed back end.
export const API = (process.env.REACT_APP_API_URL || "http://localhost:8000").replace(/\/$/, "");
