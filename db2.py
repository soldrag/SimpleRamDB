from copy import copy


class RedisSon:

    def __init__(self,):
        self.db = {}
        self.journal = []
        self.cursor = self.db
        self.command = ''
        self.key = None
        self.value = None

    def set_arguments(self, raw_input):
        inputs = {
            'command': '',
            'key': None,
            'value': None
        }
        for inputs_key, raw_item in zip(inputs, raw_input):
            inputs[inputs_key] = raw_item.upper() if inputs_key == 'command' else raw_item
        self.command, self.key, self.value = inputs.values()

    def get_obj(self):
        if self.key:
            print(self.cursor.get(self.key) if self.key in self.cursor else 'NULL')

    def set_obj(self):
        if self.value:
            self.cursor[self.key] = self.value

    def unset_obj(self):
        self.cursor.pop(self.key, None)

    def counts_obj(self):
        if self.key:
            print(list(self.cursor.values()).count(self.key))

    def begin_transaction(self):
        self.journal.append(copy(self.cursor))
        self.cursor = self.journal[-1]

    def rollback_transaction(self):
        if self.journal:
            self.journal.pop()
            self.cursor = self.journal[-1] if self.journal else self.db

    def commit_transaction(self):
        if self.journal:
            self.db = self.journal[-1]
            self.journal.clear()
            self.cursor = self.db


def run():
    database = RedisSon()
    commands = {
        'GET': database.get_obj,
        'SET': database.set_obj,
        'UNSET': database.unset_obj,
        'COUNTS': database.counts_obj,
        'BEGIN': database.begin_transaction,
        'ROLLBACK': database.rollback_transaction,
        'COMMIT': database.commit_transaction,
    }
    while True:
        database.set_arguments(input().split())
        if database.command in commands:
            commands.get(database.command)()
        elif database.command == 'END' or database.command == '':
            break
        else:
            print('Unknown command')


if __name__ == '__main__':
    run()
