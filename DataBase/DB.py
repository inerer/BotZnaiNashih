import psycopg2


class DB:

    def __init__(self):
        try:
            self.connection=psycopg2.connect(
                user="postgres",password="160324",database="ZnaiNashih"
            )
            self.cursor=self.connection.cursor()
            self.connection.autocommit=True
        except:
            print("Ошибка")

    # def add_info_event(self):
    #      with self.connection:
    #          self.cursor.execute("insert into event values (1,'1','24.08.2004','1')")
    def get_info_from_event(self):
        with self.connection:
            self.cursor.execute("Select * from event")
            return self.cursor.fetchall()

    def get_id_from_event(self, name):
        with self.connection:
            self.cursor.execute("Select id from event where name=?", name)
            return self.cursor.fetchone()

    def get_event_by_id(self, id):
        with self.connection:
            self.cursor.execute("Select * from event where id=?", id)
            return self.cursor.fetchone()

    def get_all_heroes_from_id(self, event_id):
        with self.connection:
            self.cursor.execute(f"Select heroes_id from event_heroes where event_id={event_id}")
            return self.cursor.fetchall()

    def get_hero_by_id(self, id):
        with self.connection:
            self.cursor.execute(f"Select * from heroes where id={id}")
            return self.cursor.fetchone()

