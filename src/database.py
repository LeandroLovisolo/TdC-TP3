# coding: utf-8

import sqlite3


class DB:

    SIZE = 'SIZE'
    DELAY_AND_LOSS_PROBABILITY = 'DELAY_AND_LOSS_PROBABILITY'

    EXPERIMENTS = [SIZE,
                   DELAY_AND_LOSS_PROBABILITY]

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

    def get_experiment_id(self, experiment):
        with self as c:
            c.execute('SELECT id FROM experiments WHERE name = ?', (experiment,))
            experiment_id = c.fetchone()[0]
        return experiment_id

    def register(self, experiment, time, retx, size, delay=0.0, loss=0.0):
        with self as c:
            experiment_id = self.get_experiment_id(experiment)
            c.execute('''INSERT INTO records (experiment_id, time, retx, size, delay, loss)
                         VALUES (?, ?, ?, ?, ?, ?)''',
                      (experiment_id, time, retx, size, delay, loss))

    def get_statistics_by_size(self):
        with self as c:
            experiment_id = self.get_experiment_id(DB.SIZE)

            sizes = []
            for row in c.execute('''SELECT DISTINCT(size) FROM records
                                    WHERE experiment_id = ?''', (experiment_id,)):
                sizes.append(row[0])

            statistics = {}
            for size in sizes:
                c.execute('''SELECT avg(time), avg(retx) FROM records WHERE
                             experiment_id = ? AND size = ?''', (experiment_id, size))
                row = c.fetchone()
                time = row[0]
                retransmissions = row[1]
                statistics[size] = (time, retransmissions)

        return statistics

    def get_loss_probabilities(self):
        with self as c:
            experiment_id = self.get_experiment_id(DB.DELAY_AND_LOSS_PROBABILITY)

            loss_probabilities = []
            for row in c.execute('''SELECT DISTINCT(CAST((loss * 1000) AS INTEGER)) FROM records
                                    WHERE experiment_id = ?''', (experiment_id,)):
                loss_probabilities.append(row[0] / 1000.0)

        return loss_probabilities

    def get_statistics_by_delay_and_loss_probability(self, loss_probability):
        with self as c:
            experiment_id = self.get_experiment_id(DB.DELAY_AND_LOSS_PROBABILITY)
            
            delays = []
            for row in c.execute('''SELECT DISTINCT(CAST((delay * 1000) AS INTEGER)) FROM records
                                    WHERE experiment_id = ?''', (experiment_id,)):
                delays.append(row[0] / 1000.0)

            time_vs_delay = {}
            for delay in delays:
                c.execute('''SELECT avg(time), avg(retx) FROM records WHERE
                             experiment_id = ? AND
                             CAST(delay * 1000 AS INT) = CAST(? * 1000 AS INT) AND
                             CAST(loss * 1000 AS INT)  = CAST(? * 1000 AS INT)''',
                          (experiment_id, delay, loss_probability))
                row = c.fetchone()
                time = row[0]
                retransmissions = row[1]
                time_vs_delay[delay] = (time, retransmissions)

        return time_vs_delay

    def __enter__(self):
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None and exc_value is None and traceback is None:
            self.conn.commit()

    def __del__(self):
        self.conn.close()