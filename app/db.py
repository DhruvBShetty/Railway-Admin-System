import sqlite3

conn = sqlite3.connect('railwaydb1') 
c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS User
          ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [username] TEXT UNIQUE, [email] TEXT UNIQUE, [password_hash] TEXT)
          ''')
          
c.execute('''
          CREATE TABLE IF NOT EXISTS Station
          ([code] CHARACTER PRIMARY KEY, [name] TEXT, [zone] CHARACTER, [address] TEXT, [state] TEXT,[coordinates] CHARACTER)
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS Train
          ([number] CHARACTER PRIMARY KEY UNIQUE, [name] TEXT, [type] CHARACTER, [initial_station_code] CHARACTER, [final_station_code] CHARACTER, [initial_departure_time] 
          DATETIME, [final_arriving_time] DATETIME, [duration] TIME, [distance] INTEGER, [first_class] BOOLEAN, [chair_car] BOOLEAN, [first_ac] BOOLEAN, 
          [second_ac] BOOLEAN,[third_ac] BOOLEAN, [sleeper] BOOLEAN,FOREIGN KEY (initial_station_code) REFERENCES Station(code),FOREIGN KEY (final_station_code) 
          REFERENCES Station(code) ON DELETE CASCADE ON UPDATE CASCADE)
          ''')
c.execute('''
          CREATE TABLE IF NOT EXISTS Schedule
          ([sc_id] INTEGER PRIMARY KEY AUTOINCREMENT, [train_number] CHARACTER, [station_code] CHARACTER,[departure_time] DATETIME, [arrival_time] DATETIME, 
          [day_of_travel] INTEGER,FOREIGN KEY (train_number) REFERENCES Train(number),FOREIGN KEY (station_code) REFERENCES Station(code) ON DELETE CASCADE ON 
          UPDATE CASCADE)
          ''')


                     
conn.commit()