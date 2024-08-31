import web
import asyncio
from handle import Handle

urls = (
    '/wx', 'Handle'
)
app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()

