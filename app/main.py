from config.settings import settings
import uvicorn


def main():
    uvicorn.run(
        'config:app',
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.AUTO_RELOAD,
        timeout_keep_alive=300,
    )


if __name__ == '__main__':
    main()
