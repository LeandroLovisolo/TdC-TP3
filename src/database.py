# coding: utf-8

import sqlite3


class DB:

    TIME_VS_SIZE  = 'TIME_VS_SIZE'
    TIME_VS_DELAY = 'TIME_VS_DELAY'

    EXPERIMENTS = [TIME_VS_SIZE,
                   TIME_VS_DELAY]

    def __init__(self):
        self.conn = sqlite3.connect('experiments.db')
        
        with self as c:
            c.execute('''CREATE TABLE IF NOT EXISTS experiments (
                             id INTEGER PRIMARY KEY,
                             name TEXT,
                             UNIQUE(name))''')
            c.execute('''CREATE TABLE IF NOT EXISTS records (
                             id INTEGER PRIMARY KEY,
                             experiment_id INTEGER,
                             time REAL,
                             retx INTEGER,
                             size INTEGER,
                             delay REAL,
                             loss REAL,
                             FOREIGN KEY(experiment_id) REFERENCES experiments(id))''')
            for e in DB.EXPERIMENTS:
                c.execute('INSERT OR IGNORE INTO experiments (name) VALUES (?)', (e,))

    def register(self, experiment, time, retx, size, delay=0.0, loss=0.0):
        with self as c:
            c.execute('SELECT id FROM experiments WHERE name = ?', (experiment,))
            experiment_id = c.fetchone()[0]

            c.execute('''INSERT INTO records (experiment_id, time, retx, size, delay, loss)
                         VALUES (?, ?, ?, ?, ?, ?)''',
                      (experiment_id, time, retx, size, delay, loss))

    def __enter__(self):
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None and exc_value is None and traceback is None:
            self.conn.commit()

    def __del__(self):
        self.conn.close()