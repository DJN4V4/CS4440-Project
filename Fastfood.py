# imports
import threading
import time
import random
from queue import Queue

# Lock tasks for synchronization
meat = threading.Lock()
bread = threading.Lock()
fries = threading.Lock()
burger = threading.Lock()
beverages = threading.Lock()
utensils = threading.Lock()
bagging = threading.Lock()
serve = threading.Lock()

# Events (flag raising)
meat_done = threading.Event()
bread_done = threading.Event()
fries_done = threading.Event()
burger_done = threading.Event()
beverage_done = threading.Event()
utensils_done = threading.Event()
bagging_done = threading.Event()

class Cook:

    def __init__(self, cook):
        self.cook = cook

    def grill_Meat(self, order):
        with meat:
            print(f"  [Cook {self.cook} - Order #{order}] - Grilling meat...")
            time.sleep(random.uniform(1, 2))    # Simulate grilling time
            print(f"  [Cook {self.cook} - Order #{order}] - Meat ready")
            meat_done.set()     # Raise ready flag for meat

    def toast_Bread(self, order):
        with bread:
            print(f"  [Cook {self.cook} - Order #{order}] - Toasting bread buns...")
            time.sleep(random.uniform(1, 2))    # Simulate time to cook bread
            print(f"  [Cook {self.cook} - Order #{order}] - Bread ready")
            bread_done.set()    # Raise ready flag for bread

    def fry_Fries(self, order):
        with fries:
            print(f"  [Cook {self.cook} - Order #{order}] - Frying fries...")
            time.sleep(random.uniform(1, 2))    # Simulate frying time
            print(f"  [Cook {self.cook} - Order #{order}] - Fries ready")
            fries_done.set()    # Raise ready flag for fries

    def make_Burger(self, order):
        meat_done.wait()    # Wait for ingrdients to be ready
        bread_done.wait()
        with burger:
            print(f"  [Cook {self.cook} - Order #{order}] - Making burger...")
            time.sleep(random.uniform(1, 2))    # Simulate burger building time
            print(f"  [Cook {self.cook} - Order #{order}] - Burger ready")
            burger_done.set()   # Raise ready flag for burger 

class Server:
    
    def __init__(self, server):
        self.server = server
    
    def Beverages(self, order):
        with beverages:
            print(f"  [Server {self.server} - Order #{order}] - Preparing drinks...")
            time.sleep(random.uniform(1, 2))    # Simulate drink prep time
            print(f"  [Server {self.server} - Order #{order}] - Drinks ready")
            beverage_done.set()     # Raise ready flag for beverages

    def Utensils(self, order):
        with utensils:
            print(f"  [Server {self.server} - Order #{order}] - Gathering utensils...")
            time.sleep(random.uniform(0.5, 1))  # Simulate time to gather utensils
            #print(f"  [Server {self.server} - Order #{order}] - Utensils gathered")
            utensils_done.set()     # Raise ready flag for utensils

    def Bagging(self, order):
        beverage_done.wait()    # Wait for items to be ready
        utensils_done.wait()
        fries_done.wait()
        burger_done.wait()
        with bagging:
            print(f"  [Server {self.server} - Order #{order}] - Packaging the order...")
            time.sleep(1)   # Simulate packaging time
            #print(f"  [Server {self.server} - Order #{order}] - Order packaged")
            bagging_done.set()      # Raise ready flag to serve

    def serve_Order(self, order):
        bagging_done.wait()     # Wait for bagging
        time.sleep(3)
        with serve:
            print(f"  [Server {self.server} - Order #{order}] - Serving the order...")
            #time.sleep(0.5)     # Simulate serving time
            print(f"  Order #{order} served.")

class Order:

    def __init__(self, order, cook, server):
        self.order = order
        self.cook = cook
        self.server = server

    def worker_Task(self):      # Order thread (simulates what task workers are on)
        
        print(f"- - - New ticket: Order #{self.order} - - -")

        # Start all the cook tasks
        cook_threads = [
            threading.Thread(target=self.cook.grill_Meat, args=(self.order,)),
            threading.Thread(target=self.cook.toast_Bread, args=(self.order,)),
            threading.Thread(target=self.cook.fry_Fries, args=(self.order,)),
            threading.Thread(target=self.cook.make_Burger, args=(self.order,))
        ]

        for cook in cook_threads:
            cook.start()
        
        # Start all the server tasks
        server_threads = [
            threading.Thread(target=self.server.Beverages, args=(self.order,)),
            threading.Thread(target=self.server.Utensils, args=(self.order,)),
            threading.Thread(target=self.server.Bagging, args=(self.order,)),
            threading.Thread(target=self.server.serve_Order, args=(self.order,))
        ]

        for server in server_threads:
            server.start()
        
        # Wait for all cook and server threads to finish
        for thread in cook_threads + server_threads:
            thread.join()

def next_Order(Queue):      # Get the next order (customer) from queue
    while not Queue.empty():
        order = Queue.get()
        order.worker_Task()     # Process the order
        Queue.task_done()

def main():

    print("\n----- Welcome to In-N-Out -----\n")

    # Create restaurant cooks and servers
    cook1 = Cook(cook='Mark')
    cook2 = Cook(cook='Jose')
    cook3 = Cook(cook="Ellie")
    server1 = Server(server="Jenny")

    # Queue of customer orders
    orders = Queue()

    # Create customers & place new orders in the queue
    customers = 5

    for order in range(1, customers + 1):
        
        # Assign random cook and start order
        order_Object = Order(order=order, cook=random.choice([cook1, cook2, cook3]), server=server1)
        orders.put(order_Object)
        #time.sleep(2)       # Time between customers
    
    # Worker threads (cooks)
    cook_Threads = []

    # Create 'cook' thread, append, and start
    cook = threading.Thread(target=next_Order, args=(orders,))
    cook_Threads.append(cook)
    cook.start()

    # Join 'cook' thread after starting
    cook.join()
    
    print("\n----- All orders completed -----\n")

# Run the program
if __name__ == "__main__":
    main()
  
