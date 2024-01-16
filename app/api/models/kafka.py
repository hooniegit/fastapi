from confluent_kafka import Consumer, KafkaException, KafkaError
from threading import Thread
import gc

consumer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'example',
    'auto.offset.reset': 'earliest',
}

class KafkaConsumerModel:
    def __init__(self, conf:dict):
        self.conf = conf
        self.consumer = Consumer(self.conf)

class KafkaExampleModel(KafkaConsumerModel):
    def __init__(self, consumer, topics:list):
        super().__init__(consumer)
        self.consumer.subscribe(self.topics)
    
    def poll_message(self, period:int=1):
        try:
            message = self.consumer.poll(period)
            if message is not None:
                return message.value().decode('utf-8')
            
        except KafkaException as E:
            print(f"KafkaException: {E}")
            
        except KafkaError as E:
            print(f"KafkaError: {E}")
            
        return None
    
    def poll_messages(self, period:int=1):
        try:
            while True:
                gc.collect()
                message = self.consumer.poll(period)
                if message is None:
                    continue
                self.tasks(message)
        
        except KeyboardInterrupt:
            pass
        
        finally:
            self.consumer.close()
            
    def tasks(self, message):
        topic = message.topic()
        key = message.key().decode('utf-8') if message.key() else None
        value = message.value().decode('utf-8')
        timestamp = message.timestamp()
        # nowdate = datetime.fromtimestamp(message.timestamp()[-1]).strftime('%Y-%m-%d %H:%M:%S')
        
        # run tasks with extra threads
        threads = []
        threads.append(Thread(target = self.message, args = (f"topic: {topic} - key: {key} - value: {value} - timestamp: {timestamp}", )))
        for thread in threads:
            thread.start()
            
    def example(self, message):
        for i in range(10):
            print(f"{i}: {message}")
    