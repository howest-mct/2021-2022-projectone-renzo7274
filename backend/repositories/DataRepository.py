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
        sql = "SELECT waarde FROM database_final.historiek where DeviceID = 1 order by Actiedatum DESC limit 1"
        return Database.get_one_row(sql)

    @staticmethod
    def insert_temp(temp):
        sql = "insert into database_final.historiek( actiedatum,waarde,commentaar,deviceid,actieid) values( now(),%s,'graden celcius',1,1)"
        params=[temp]
        return Database.execute_sql(sql,params)

    @staticmethod
    def read_latest_sound_data():
        sql = "SELECT waarde FROM database_final.historiek where DeviceID = 2 order by Actiedatum DESC limit 1"
        return Database.get_one_row(sql)
    
    @staticmethod
    def insert_sound(sound):
        sql = "insert into database_final.historiek( actiedatum,waarde,commentaar,deviceid,actieid) values( now(),%s,'decibel',2,2)"
        params=[sound]
        return Database.execute_sql(sql,params)

    @staticmethod
    def read_latest_fans_data():
        sql = "SELECT waarde FROM database_final.historiek where DeviceID = 4 order by Actiedatum DESC limit 1"
        return Database.get_one_row(sql)

    @staticmethod
    def insert_fanspeed(fanspeed):
        sql = "insert into database_final.historiek( actiedatum,waarde,commentaar,deviceid,actieid) values( now(),%s,'fan snelheid',4,4)"
        params=[fanspeed]
        return Database.execute_sql(sql,params)
