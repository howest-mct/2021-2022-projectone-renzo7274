from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_latest_temp_data():
        sql = "SELECT waarde FROM database_test.historiek where DeviceID = 2 order by Actiedatum DESC limit 1"
        return Database.get_one_row(sql)

    @staticmethod
    def insert_temp(temp):
        sql = "insert into historiek( actiedatum,waarde,commentaar,deviceid,actieid) values( now(),%s,'graden celcius',2,1)"
        params=[temp]
        return Database.execute_sql(sql,params)

    

