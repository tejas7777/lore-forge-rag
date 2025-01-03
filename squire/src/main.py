from src.consumer import Consumer

def run_worker():
   consumer = Consumer()
   consumer.start()

if __name__ == "__main__":
   run_worker()