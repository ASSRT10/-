import threading
import time
import logging
import uuid


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tasks.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class PeriodicTask:
  
    def __init__(self, name, interval, base, exponent):
        self.id = str(uuid.uuid4())[:8] 
        self.name = name
        self.interval = interval
        self.base = base
        self.exponent = exponent
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)
       
        self.is_started = False 

    def _run(self):
        logging.info(f"Задача '{self.name}' (ID: {self.id}) запущена. Интервал: {self.interval}с")
        while not self.stop_event.is_set():
           
            for _ in range(int(self.interval * 10)):
                if self.stop_event.is_set(): return
                time.sleep(0.1)
            
            
            try:
                if self.base > 1000 and self.exponent > 10:
                     logging.warning(f"ВЫПОЛНЕНИЕ: {self.name} (ID: {self.id}) - Основание и степень слишком велики, пропускаем вычисление.")
                     continue
                
                result = self.base ** self.exponent
                logging.info(f"ВЫПОЛНЕНИЕ: {self.name} (ID: {self.id}) - Результат {self.base}^{self.exponent} = {result}")
            except OverflowError:
                logging.error(f"ВЫПОЛНЕНИЕ: {self.name} (ID: {self.id}) - Результат слишком большой для представления.")
            except Exception as e:
                logging.error(f"ВЫПОЛНЕНИЕ: {self.name} (ID: {self.id}) - Ошибка при вычислении: {e}")
            

    def start(self):
        if not self.is_started: 
            self.thread.start()
            self.is_started = True
        else:
            logging.warning(f"Попытка запустить уже запущенную задачу '{self.name}' (ID: {self.id}).")

    def stop(self):
        if self.is_started:
            self.stop_event.set()
            
            self.thread.join(timeout=self.interval + 1) 
            self.is_started = False
            logging.info(f"Задача '{self.name}' (ID: {self.id}) остановлена.")
        else:
            logging.warning(f"Попытка остановить незапущенную задачу '{self.name}' (ID: {self.id}).")


class Scheduler:
    
    def __init__(self):
        self.tasks = {}

    
    def add_task(self, name, interval, base, exponent, start_immediately=True):
        task = PeriodicTask(name, interval, base, exponent)
        self.tasks[task.id] = task
        if start_immediately:
            task.start()
            print(f"Успешно добавлено (активна): {name} [ID: {task.id}]")
        else:
            print(f"Успешно добавлено (неактивна): {name} [ID: {task.id}]")

    def remove_task(self, task_id):
        if task_id in self.tasks:
            if self.tasks[task_id].is_started:
                self.tasks[task_id].stop()
            del self.tasks[task_id]
            print(f"Задача {task_id} удалена.")
        else:
            print("Ошибка: ID не найден.")

    def list_tasks(self):
        if not self.tasks:
            print("Список задач пуст.")
        for tid, t in self.tasks.items():
            status = "Активна" if t.is_started else "Неактивна"
            print(f"ID: {tid} | Имя: {t.name} | Интервал: {t.interval} сек. | Действие: {t.base}^{t.exponent} | Статус: {status}")

def main():
    sched = Scheduler()

    print("Добавляем предварительно настроенные задачи (неактивные)...")
   
    sched.add_task("Квадрат числа 5", 5, 5, 2, start_immediately=False)
    sched.add_task("Куб числа 2", 10, 2, 3, start_immediately=False)
    sched.add_task("10 в 4й степени", 15, 10, 4, start_immediately=False)
    print("Предварительные задачи добавлены.\n")

    while True:
        print("\n--- Меню планировщика ---")
        print("1. Добавить новую задачу\n2. Удалить задачу\n3. Список активных задач\n4. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            name = input("Введите название задачи: ")
            try:
                interval_sec = float(input("Введите интервал выполнения (сек): "))
                base_num = float(input("Введите число (основание): "))
                exponent_num = float(input("Введите степень: "))
                
                
                sched.add_task(name, interval_sec, base_num, exponent_num, start_immediately=True)
            except ValueError:
                print("Ошибка: Введите числовые значения для интервала, основания и степени.")
        elif choice == '2':
            tid = input("Введите ID задачи для удаления: ")
            sched.remove_task(tid)
        elif choice == '3':
            sched.list_tasks()
        elif choice == '4':
            print("Завершение работы...")
            
            for task_id in list(sched.tasks.keys()):
                if sched.tasks[task_id].is_started: 
                    sched.remove_task(task_id) 
            break
        else:
            print("Неверный ввод.")


main()