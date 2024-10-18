from cbr_user_data.fast_api.Fast_API__User_Data import Fast_API__User_Data

user_data_fast_api = Fast_API__User_Data().setup()
app          = user_data_fast_api.app()

