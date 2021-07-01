# отправка сообщений в Телеграм с помощью обыкновенных запросов POST

TOKEN = "1818338603:AAEv3AOttf2NqRSSphapItXr-ADv3sbL0tM"
BASE_URL = 'https://api.telegram.org'
CHAT_ID = 362857450

# Телеграм говорит нам, что мы можем собрать URL по некоторому правилу и отправка сообщения
# произойдет просто по переходу по нему

sender_url = "https://api.telegram.org/bot1818338603:AAEv3AOttf2NqRSSphapItXr-ADv3sbL0tM/sendMessage?chat_id=362857450" \
             "text=ТЕСТОВОЕ СОООБЩЕНИЕ"

f"{BASE_URL}/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={notification.message}"













# Deque, Queue, Stack
# классические коллекции.

# Stack - стек, первым вошёл - последним обслужен
l = []
l.append(1)
l.append(2)
l.append(3)

# классическое название - pop
l.pop()
l.pop()
l.pop()

# Queue - очередь, первым вошёл - первым обслужен
l = []
l.append(1)
l.append(2)
l.append(3)

# классическое название - push
l.pop(0)
l.pop(0)
l.pop(0)

# Deque - двусторонняя очередь - по сути совмещает в себе поведение Stack и Queue
# подробнее можно прочитать в книге Грокаем алгоритмы)
l = []
l.append(1)
l.append(2)
l.append(3)

# классическое название - pop
l.pop()
l.pop()
l.pop()

# классическое название - push
l.pop(0)
l.pop(0)
l.pop(0)
