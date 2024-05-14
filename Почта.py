class Server:
    def __init__(self, name, max_sms):
        """при создании сервера вводим его название и максимальное количество хранимых сообщений, также в словаре sms
        ключ - получатель, значение - список:
        1й элемент - словарь -> ключ - отправитель, значение - список текстов писем
        2й элемент - количество сообщений получателю"""
        self.name = name
        self.max_sms = max_sms
        self.sms = {}
        self.sms_quantity = 0

    def receive_mail(self, recipient):
        if recipient.name in self.sms.keys():
            for i in self.sms[recipient.name][0].keys():
                print(f'Сообщения от {i}:')
                for j in range(len(self.sms[recipient.name][0][i])):
                    print(f'{j + 1}. ' + self.sms[recipient.name][0][i][j])
            self.sms_quantity -= self.sms[recipient.name][1]
            del self.sms[recipient.name]

        else:
            print('Нет новых писем')

    def send_mail(self, recipient, message, sender):
        if self.sms_quantity < self.max_sms:
            print('Отправка ...')
            if recipient not in self.sms.keys():
                self.sms[recipient] = [{sender: [message]}, 0]
            elif sender not in self.sms[recipient][0].keys():
                self.sms[recipient][0][sender] = [message]
            else:
                self.sms[recipient][0][sender].append(message)
            self.sms[recipient][1] += 1
            self.sms_quantity += 1
            print('Успешно отправлено!')
        else:
            print(f'{sender}, простите, но мы не сможем отправить письмо, т.к. сервер перегружен, попробуйте на '
                  'другом сервере или повторите попытку в другой раз.')


# ключ - пользователь, значение - сервер, к которому подключена его учётная запись
servers = {}


class MailClient:
    def __init__(self, server, user):
        self.server = server
        self.name = user
        servers[self] = server

    def receive_mail(self):
        return self.server.receive_mail(self)

    def send_mail(self, server, user, message):
        if server not in servers.values():
            print('Такого сервера нет!')
        elif server != servers[user]:
            print('Учётная запись этого аккаунта не на этом сервере')
        else:
            server.send_mail(user.name, message, self.name)


server1 = Server('сервер Вася', 2)
server2 = Server('сервер Петя', 1)
client1 = MailClient(server1, 'Петя')
client2 = MailClient(server2, 'Вася')
client1.send_mail(server2, client2, 'Привет')
client1.send_mail(server2, client2, 'Как дела?')
client2.send_mail(server1, client1, 'Привет')
client2.send_mail(server1, client1, 'Как дела?')
client2.receive_mail()
client1.receive_mail()
