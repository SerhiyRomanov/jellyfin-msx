# jellyfin-msx
The API application implements [MediaStationX](https://msx.benzac.de/info/) portal which provide ability to use [Jellyfin](https://jellyfin.org/)

The backend application is written on Python 3.12 using FastAPI, Pydantic and others.

# Status
It is a proof of concept with minimal features: login, explore user views and folder/content and play video streams.
Any pull requests, suggestions, and other type of collaboration are highly welcome 

# Development
 - Install Python 3.12
 - Create virtual environment
 - Install dependencies from [src/requirements.txt](src%2Frequirements.txt)
 - run via `python -m uvicorn app.app:app --host 0.0.0.0 --reload`

## Structure of project
 - `src/app` - the FastAPI application with endpoints and session implementation
 - `src/msx_models` - Pydantic-based models for MSX Object. _Potentially can be as separate package in the future
    therefore please consider to adding only necessary dependencies_
 - `src/jellyfin-api` - Asynchronous API Client for https://api.jellyfin.org/. _Potentially can be as separate package in the future
    therefore please consider to adding only necessary dependencies_

# Run with Docker
See [docker-compose-example.yml](docker-compose-example.yml)

# Roadmap for near future
 - i18n
 - Support for all Jellyfin media types
 - Add basic Jellyfin features
   - details about content (posters, description, metainfo about streams)
   - playback sessions
   - sorting
   - search
 - Sessions
   - Redis session implementation
   - Explore how to use cookies with MSX (implement CookieSessionStorage)
 - more...