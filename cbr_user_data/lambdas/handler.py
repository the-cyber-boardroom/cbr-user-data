from mangum                                         import Mangum
from cbr_user_data.fast_api.Fast_API__User_Data     import Fast_API__User_Data

fast_api_user_data = Fast_API__User_Data().setup()
app                = fast_api_user_data.app()
run                = Mangum(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)